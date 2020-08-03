import os
import re
from typing import List

from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn  # type: ignore
from robotlibcore import DynamicCore  # type: ignore

from .keywords import (
    Control,
    Cookie,
    Devices,
    Evaluation,
    Getters,
    Interaction,
    Network,
    PlaywrightState,
    Promises,
    Waiter,
    WebAppState,
)
from .playwright import Playwright
from .utils import logger
from .utils.data_types import AutoClosingLevel
from .version import VERSION


class Browser(DynamicCore):
    """Browser library is a browser automation library for Robot Framework.

    This is hte keyword documentation for Browser library. For information
    about installation, support, and more please visit the
    [https://github.com/MarketSquare/robotframework-playwright|project pages].
    For more information about Robot Framework itself, see [https://robotframework.org|robotframework.org].

    Browser library uses
    [https://github.com/microsoft/playwright|Playwright Node module]
    to automate [https://www.chromium.org/Home|Chromium],
    [https://www.mozilla.org/en-US/firefox/new/|Firefox]
    and [https://webkit.org/|WebKit] with a single library.

    == Table of contents ==

    %TOC%

    = Finding elements =

    All keywords in hte library that need to interact with an element
    on a web page take an argument typically named ``selector`` that specifies
    how to find the element.

    == Selector syntax ==

    Browser library supports the same selector strategies as the underlying
    Playwright node module: xpath, css, id and text. The strategy can either
    be explicitly specified with a prefix or the strategy can be implicit.

    === Implicit selector strategy ===

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
    | text         | Browser text engine.       | ``text=Login``                 |

    == Finding elements inside frames ==

    By default, selector chains do not cross frame boundaries. It means that a
    simple CSS selector is not able to select and element located inside an iframe
    or a frameset. For this usecase, there is a special selector ``>>>`` which can
    be used to combine a selector for the frame and a selector for an element
    inside a frame.

    Given this simple pseudo html snippet:
    ``<iframe name="iframe" src="src.html"><button id="btn">Click Me</button></iframe>``,
    here's a keyword call that clicks the button inside the frame.

    | Click  | iframe[name="iframe"] >>> #btn  |

    The selectors on the left and right side of ``>>>`` can be any valid selectors.

    == Element reference syntax ==

    It is possible to get a reference to an element by using `Get Element` keyword. This
    reference can be used as a *first* part of a selector by using a special selector
    syntax `element=` like this:

    | ${ref}=  |  Get Element  |  .some_class  |
    | Click    |  element=${ref} >>  .some_child |

    The `.some_child` selector in the example is relative to the element referenced by ${ref}.

    = Assertions =

    Keywords that accept arguments ``assertion_operator`` and ``assertion_expected``
    can optionally assert.
    Currently supported assertion operators are:

    |      = Operator =               |              = Description =                          |
    | ``==`` or ``should be``         | equal                                                 |
    | ``!=`` or ``should not be``     | not equal                                             |
    | ``>``                           | greater than                                          |
    | ``>=``                          | greater than or equal                                 |
    | ``<``                           | less than                                             |
    | ``<=``                          | less than or equal                                    |
    | ``*=`` or ``contains``          | for checking that a value contains an element         |
    | ``matches``                     | for matching against a regular expression.            |
    | ``^=`` or ``should start with`` | starts with                                           |
    | ``$=`` or ``should end with``   | ends with                                             |
    | ``validate``                    | use BuiltIn Evaluate. Access to actual with ``value`` |

    Assertion value can be any valid robot value, and the keywords will provide an error
    message if the assertion fails.

    = The 'then' closure =

    Keywords that accept arguments ``assertion_operator`` and ``assertion_expected``
    can optionally also use ``then`` closure to modify the returned value with
    BuiltIn Evaluate. Actual value can be accessed with ``value``.

    For example ``Get Title  then  'TITLE: '+value``.
    See
    [https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Evaluating%20expressions|
    Builtin Evaluating expressions]
    for more info on the syntax.

    = Automatic page and context closing =

    Library will close pages and contexts that are created during test execution.
    Pages and contexts created before test in Suite Setup or Suite Teardown will be closed after that suite.
    This will remove the burden of closing these resources in teardowns.

    Browsers will not be automatically closed. A browser is expensive to create and should be reused.

    Automatic closing can be configured or switched off with the ``auto_closing_level`` library parameter.
    """

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_LISTENER: "Browser"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    SUPPORTED_BROWSERS = ["chromium", "firefox", "webkit"]
    _auto_closing_level: AutoClosingLevel

    def __init__(
        self,
        timeout="10s",
        enable_playwright_debug: bool = False,
        auto_closing_level: AutoClosingLevel = AutoClosingLevel.TEST,
    ):
        """Browser library can be taken into use with optional arguments:

        - ``timeout``:
          Timeout for keywords that operate on elements. The keywords will wait
          for this time for the element to appear into the page.
        - ``enable_playwright_debug``:
          Enable low level debug information from the playwright tool. Mainly
          Useful for the library developers and for debugging purposes.
        - ``auto_closing_level``:
          Configure context and page automatic closing. Default is after each test.
          Other options are SUITE for closing after each suite and MANUAL
          for no automatic closing.
        """
        self.ROBOT_LIBRARY_LISTENER = self
        self._execution_stack: List[object] = []
        # This is more explicit than to have all the libraries be referenceable when they don't need it.
        self.browser_control = Control(self)
        self.promises = Promises(self)
        self.getters = Getters(self)
        self.playwright_state = PlaywrightState(self)
        libraries = [
            self.browser_control,
            Cookie(self),
            Devices(self),
            Evaluation(self),
            Interaction(self),
            self.getters,
            self.playwright_state,
            Network(self),
            self.promises,
            Waiter(self),
            WebAppState(self),
        ]
        self.playwright = Playwright(timeout, enable_playwright_debug)
        self._auto_closing_level = auto_closing_level
        DynamicCore.__init__(self, libraries)

    @property
    def outputdir(self):
        return BuiltIn().get_variable_value("${OUTPUTDIR}")

    def _close(self):
        self.playwright.close()

    def _start_suite(self, name, attrs):
        if self._auto_closing_level != AutoClosingLevel.MANUAL:
            self._execution_stack.append(self.getters.get_browser_catalog())

    def _start_test(self, name, attrs):
        if self._auto_closing_level == AutoClosingLevel.TEST:
            self._execution_stack.append(self.getters.get_browser_catalog())

    def _end_test(self, name, attrs):
        if len(self.promises._unresolved_promises) > 0:
            logger.warn(f"Waiting unresolved promises at the end of test '{name}'")
            self.wait_for_all_promises()
        if self._auto_closing_level == AutoClosingLevel.TEST:
            catalog_before_test = self._execution_stack.pop()
            self._prune_execution_stack(catalog_before_test)

    def _end_suite(self, name, attrs):
        if self._auto_closing_level != AutoClosingLevel.MANUAL:
            catalog_before_suite = self._execution_stack.pop()
            self._prune_execution_stack(catalog_before_suite)

    def _prune_execution_stack(self, catalog_before):
        # WIP CODE BEGINS
        catalog_after = self.getters.get_browser_catalog()
        ctx_before_ids = [c["id"] for b in catalog_before for c in b["contexts"]]
        ctx_after_ids = [c["id"] for b in catalog_after for c in b["contexts"]]
        new_ctx_ids = [c for c in ctx_after_ids if c not in ctx_before_ids]
        for ctx_id in new_ctx_ids:
            self.playwright_state.switch_context(ctx_id)
            self.playwright_state.close_context()
        pages_before = [
            (p["id"], c["id"])
            for b in catalog_before
            for c in b["contexts"]
            for p in c["pages"]
        ]
        pages_after = [
            (p["id"], c["id"])
            for b in catalog_after
            for c in b["contexts"]
            for p in c["pages"]
            if c["id"] not in new_ctx_ids
        ]
        new_page_ids = [p for p in pages_after if p not in pages_before]
        for page_id, ctx_id in new_page_ids:
            self.playwright_state.switch_context(ctx_id)
            self.playwright_state.switch_page(page_id)
            self.playwright_state.close_page()
        # try to set active page and context back to right place.
        for browser in catalog_after:
            if browser["activeBrowser"]:
                activeContext = browser.get("activeContext", None)
                activePage = browser.get("activePage", None)
                if not new_ctx_ids and activeContext is not None:
                    self.playwright_state.switch_context(activeContext)
                    if not (activePage, activeContext) in new_page_ids:
                        self.playwright_state.switch_page(activePage)

    def run_keyword(self, name, args, kwargs=None):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except AssertionError as e:
            self.keyword_error()
            raise e

    def start_keyword(self, name, attrs):
        """Take screenshot of tests that have failed due to timeout.

        This method is part of the Listener API implemented by the library.

        This can be done with BuiltIn keyword `Run Keyword If Timeout
        Occurred`, but the problem there is that you have to remember to
        put it into your Suite/Test Teardown. Since taking screenshot is
        the most obvious thing to do on failure, let's do it automatically.

        This cannot be implemented as a `end_test` listener method, since at
        that time, the teardown has already been executed and browser may have
        been closed already. This implementation will take the screenshot
        before the teardown begins to execute.
        """
        if attrs["type"] == "Teardown":
            timeout_pattern = "Test timeout .* exceeded."
            test = EXECUTION_CONTEXTS.current.test
            if (
                test is not None
                and test.status == "FAIL"
                and re.match(timeout_pattern, test.message)
            ):
                self.screenshot_on_failure(test.name)

    def keyword_error(self):
        """Sends screenshot command to Playwright.

        Only works during testing since this uses robot's outputdir for output.
        """
        self.screenshot_on_failure(BuiltIn().get_variable_value("${TEST NAME}"))

    def screenshot_on_failure(self, test_name):
        try:
            path = self.failure_screenshot_path(test_name)
            self.browser_control.take_page_screenshot(path)
        except Exception as err:
            logger.info(f"Was unable to take page screenshot after failure:\n{err}")

    def failure_screenshot_path(self, test_name):
        return os.path.join(
            BuiltIn().get_variable_value("${OUTPUTDIR}"),
            test_name.replace(" ", "_") + "_FAILURE_SCREENSHOT",
        ).replace("\\", "\\\\")
