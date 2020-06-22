__version__ = "0.1.1"

import os
from subprocess import Popen, STDOUT
import contextlib
from functools import cached_property
import time
from typing import Optional

import grpc  # type: ignore

from robot.api import logger  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import DynamicCore  # type: ignore

from Browser.generated.playwright_pb2 import Empty
import Browser.generated.playwright_pb2_grpc as playwright_pb2_grpc

from .keywords import Validation, Control, Input
from .util import find_free_port


class Browser(DynamicCore):
    """Browser library is a web testing library for Robot Framework.

    This documents explains how to use keywords provided by the Browser
    library. For information about installation, support, and more, please
    visit the
    [https://github.com/MarketSquare/robotframework-playwright|project pages].
    For more information about Robot Framework, see http://robotframework.org.

    Browser library uses
    [https://github.com/microsoft/playwright|Playwright Node module]
    to automate [https://www.chromium.org/Home|Chromium],
    [https://www.mozilla.org/en-US/firefox/new/|Firefox]
    and [https://webkit.org/|WebKit] with a single library.

    == Table of contents ==

    %TOC%

    = Locating elements =

    All keywords in Browser library that need to interact with an element
    on a web page take an argument typically named ``selector`` that specifies
    how to find the element.

    == Locator syntax ==

    Browser library supports same selector strategies as the underlying
    Playwright node module: xpath, css, id and text. The strategy can either
    be explicitly specified with a prefix or the strategy can be implicit.

    === Implicit selector strategy ===
    == !!! THIS ISN'T IMPLEMENTED YET !!! ==

    The default selector strategy is `css`. If selector does not contain
    one of the know selector strategies, `css`, `xpath`, `id` or `text` it is
    assumed to contain css selector. Also `selectors` starting with `//`
    considered as xpath selectors.

    Examples:

    | `Click` | span > button | # Use css selector strategy the element.   |
    | `Click` | //span/button | # Use xpath selector strategy the element. |

    === Explicit selector strategy ===

    The explicit selector strategy is specified with a prefix using syntax
    ``strategy=value``. Spaces around the separator are ignored, so
    ``css=foo``, ``css= foo`` and ``css = foo`` are all equivalent.


    Selector strategies that are supported by default are listed in the table
    below.

    | = Strategy = |     = Match based on =     |         = Example =            |
    | css          | CSS selector.              | ``css=div#example``            |
    | xpath        | XPath expression.          | ``xpath=//div[@id="example"]`` |
    | text         | Browser text engine.    | ``text=Login``                 |
    """

    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_LISTENER: "Browser"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    port: Optional[str] = None
    _SUPPORTED_BROWSERS = ["chrome", "firefox", "webkit"]

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        libraries = [
            Validation(self._insecure_stub),
            Control(self._insecure_stub, self._SUPPORTED_BROWSERS),
            Input(self._insecure_stub),
        ]
        DynamicCore.__init__(self, libraries)

    @cached_property
    def _playwright_process(self) -> Popen:
        cwd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrapper")
        path_to_script = os.path.join(cwd_dir, "index.js")
        logger.info(f"Starting Browser process {path_to_script}")
        logfile = open(
            os.path.join(
                BuiltIn().get_variable_value("${OUTPUTDIR}"), "playwright-log.txt"
            ),
            "w",
        )
        self.port = str(find_free_port())
        popen = Popen(
            ["node", path_to_script],
            shell=False,
            cwd=cwd_dir,
            env={"PORT": self.port, "PATH": os.environ["PATH"]},
            stdout=logfile,
            stderr=STDOUT,
        )
        for i in range(50):
            with grpc.insecure_channel(f"localhost:{self.port}") as channel:
                try:
                    stub = playwright_pb2_grpc.PlaywrightStub(channel)
                    response = stub.Health(Empty())
                    logger.info(
                        f"Connected to the playwright process at port ${self.port}: ${response}"
                    )
                    return popen
                except grpc.RpcError:
                    time.sleep(0.1)
        raise RuntimeError(
            f"Could not connect to the playwright process at port ${self.port}"
        )

    def _close(self):
        logger.debug("Closing Playwright process")
        self._playwright_process.kill()
        logger.debug("Playwright process killed")

        # Yields a PlayWrightstub on a newly initialized channel and

    # closes channel after control returns
    @contextlib.contextmanager
    def _insecure_stub(self):
        returncode = self._playwright_process.poll()
        if returncode is not None:
            raise ConnectionError(
                "Playwright process has been terminated with code {}".format(returncode)
            )
        channel = grpc.insecure_channel(f"localhost:{self.port}")
        yield playwright_pb2_grpc.PlaywrightStub(channel)
        channel.close()

    def run_keyword(self, name, args, kwargs):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self._test_error()
            raise

    """ Sends screenshot message through the stub and then raises an AssertionError with message
        Only works during testing since this uses robot's outputdir for output
    """

    def _test_error(self):
        path = os.path.join(
            BuiltIn().get_variable_value("${OUTPUTDIR}"),
            BuiltIn().get_variable_value("${TEST NAME}") + "_FAILURE_SCREENSHOT",
        )
        BuiltIn.run_keyword("Take Page Screenshot", path)
