__version__ = "0.1.0"

import os
from subprocess import Popen, PIPE
from functools import cached_property
from typing import Optional

import grpc  # type: ignore

from robot.api import logger  # type: ignore

import Playwright.generated.playwright_pb2 as playwright_pb2
from Playwright.generated.playwright_pb2 import Empty
import Playwright.generated.playwright_pb2_grpc as playwright_pb2_grpc

_SUPPORTED_BROWSERS = ["chrome", "firefox", "webkit"]


class Playwright:
    """Playwright library is a web testing library for Robot Framework.

    This documents explains how to use keywords provided by the Playwright
    library. For information about installation, support, and more, please
    visit the
    [https://github.com/MarketSquare/robotframework-playwright|project pages].
    For more information about Robot Framework, see http://robotframework.org.

    Playwright library uses
    [https://github.com/microsoft/playwright|Playwright Node module]
    to automate [https://www.chromium.org/Home|Chromium],
    [https://www.mozilla.org/en-US/firefox/new/|Firefox]
    and [https://webkit.org/|WebKit] with a single library.

    == Table of contents ==

    %TOC%

    = Locating elements =

    All keywords in Playwright library that need to interact with an element
    on a web page take an argument typically named ``locator`` that specifies
    how to find the element.

    == Locator syntax ==

    Playwright library supports same locator strategies as the underlying
    Playwright None module: xpath, css, id and text. The strategy can either
    be explicitly specified with a prefix or the strategy can be implicit.

    === Implicit locator strategy ===

    The default locator strategy is `css`. If locator does not contain
    one of the know locator strategies, `css`, `xpath`, `id` or `text` it is
    assumed to contain css locator. Also `locators` starting with `//` is
    considered as xpath locators.

    Examples:

    | `Click` | span > button | # Use css locator strategy the element.   |
    | `Click` | //span/button | # Use xpath locator strategy the element. |

    === Explicit locator strategy ===

    The explicit locator strategy is specified with a prefix using syntax
    ``strategy:value``. Spaces around the separator are ignored, so
    ``css:foo``, ``css: foo`` and ``css : foo`` are all equivalent.

    Locator strategies that are supported by default are listed in the table
    below.

    | = Strategy = |     = Match based on =     |         = Example =            |
    | css          | CSS selector.              | ``css:div#example``            |
    | xpath        | XPath expression.          | ``xpath://div[@id="example"]`` |
    | text         | Playwright text engine.    | ``text:Login``                 |
    | id           | Converted to CSS selector. | ``id:example``                 |
    """

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_LISTENER: "Playwright"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    port: Optional[str] = None

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    @cached_property
    def _playwright_process(self) -> Popen:
        cwd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrapper")
        path_to_script = os.path.join(cwd_dir, "index.js")
        logger.info(f"Starting Playwright process {path_to_script}")
        popen = Popen(
            f"node '{path_to_script}'",
            shell=True,
            cwd=cwd_dir,
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout = popen.stdout
        if stdout is None:
            raise RuntimeError("No expected output from Playwright process")
        for line in stdout:
            if line.startswith(b"Listening on "):
                self.port = str(line).strip()[15:-3]
                return popen
        raise RuntimeError("No expected output from Playwright process")

    def _close(self):
        logger.debug("Closing Playwright process")
        self._playwright_process.kill()
        logger.debug("Playwright process killed")

    # Control keywords
    def open_browser(self, browser="Chrome", url=None):
        if url is None:
            url = "about:blank"
        browser_ = browser.lower().strip()
        if browser_ not in _SUPPORTED_BROWSERS:
            raise ValueError(
                f"{browser} is not supported, "
                f'it should be one of: {", ".join(_SUPPORTED_BROWSERS)}'
            )
        if self._playwright_process.poll() is not None:
            raise ConnectionError("Playwright process has been terminated")
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.OpenBrowser(
                playwright_pb2.openBrowserRequest(url=url, browser=browser_)
            )
            logger.info(response.log)

    def close_browser(self):
        if self._playwright_process.poll() is not None:
            raise ConnectionError("Playwright process has been terminated")
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.CloseBrowser(Empty())
            logger.info(response.log)

    def go_to(self, url: str):
        if self._playwright_process.poll() is not None:
            raise ConnectionError("Playwright process has been terminated")
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.GoTo(playwright_pb2.goToRequest(url=url))
            logger.info(response.log)

    # Validation keywords
    def title_should_be(self, title: str):
        if self._playwright_process.poll() is not None:
            raise ConnectionError("Playwright process has been terminated")
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.GetTitle(Empty())
            logger.info(response.log)
            if response.body != title:
                raise AssertionError(
                    "Title should be {} but was {}".format(title, response)
                )
