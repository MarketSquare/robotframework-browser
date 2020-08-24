import os
import re
from concurrent.futures._base import Future
from typing import List, Set

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
from .utils import AutoClosingLevel, logger
from .version import VERSION


class Browser(DynamicCore):
    """Browser library is a browser automation library for Robot Framework.

    This is the keyword documentation for Browser library. For information
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

    = Browser, Context and Page =

    Browser library works with three different layers that build on each other:
    *Browser*, *Context* and *Page*.


    == Browsers ==

    A *browser* can be started with one of the three
    different engines Chromium, Firefox or Webkit.

    === Supported Browsers ===

    |   Browser     | Browser with this engine                          |
    | ``chromium``  | Google Chrome, Microsoft Edge (since 2020), Opera |
    | ``firefox``   | Mozilla Firefox                                   |
    | ``webkit``    | Apple Safari, Mail, AppStore on MacOS and iOS     |

    Since [https://github.com/microsoft/playwright|Playwright] comes with a pack of builtin
    binaries for all browsers, no additional drivers e.g. geckodriver are needed.

    All these browsers that cover more than 85% of the world wide used browsers,
    can be tested on Windows, Linux and MacOS.
    Theres is not need for dedicated machines anymore.

    A browser process is started ``headless`` (without a GUI) by default.
    Run `New Browser` with specified arguments if a browser with a GUI is requested
    or if a proxy has to be configured.
    A browser process can contain several contexts.


    == Contexts ==

    A *context* corresponds to several independent incognito browsers in Chrome
    that do not share cookies, sessions or profile settings.
    Compared to Selenium, these do *not* require their own browser process!
    Therefore, to get a clean environment the tests shall just close the current
    context and open a new context.
    Due to this new independent browser sessions can be opened with
    Robot Framework Browser about 10 times faster than with Selenium by
    just opening a `New Context` within the opened browser.

    The context layer is useful e.g. for testing different users sessions on the
    same webpage without opening a whole new browser context.
    Contexts can also have detailed configurations, such as geo-location, language settings,
    the viewport size or color scheme.
    Contexts do also support http credentials to be set, so that basic authentication
    can also be tested. To be able to download files within the test,
    the ``acceptDownloads`` argument must be set to ``True`` in `New Context` keyword.
    A context can contain different pages.


    == Pages ==

    A *page* does contain the content of the loaded web site.
    Pages and browser tabs are the same.

    Typical usage could be:
    | *** Test Cases ***
    | Starting a browser with a page
    |     New Browser    chromium    headless=false
    |     New Context    viewport={'width': 1920, 'height': 1080}
    |     New Page       https://marketsquare.github.io/robotframework-browser/Browser.html
    |     Get Title      ==    Browser

    There are shortcuts to open new pages together with new browsers but the offer less control.

    The `Open Browser` keyword opens a new browser, a new context and a new page.
    This keyword is usefull for quick experiments or debugging sessions.

    When a `New Page` is called without an open browser, `New Browser`
    and `New Context` are executed with default values first.

    If there is no browser opened in Suite Setup and `New Page` is executed in
    Test Setup, the corresponding pages and context is closed automatically at the end of
    the test. The browser process remains open and will be closed at the end of
    execution.

    Each Browser, Context and Page has a unique ID with which they can be adressed.
    A full catalog of what is open can be recieved by `Get Browser Catalog` as dictionary.



    = Finding elements =

    All keywords in the library that need to interact with an element
    on a web page take an argument typically named ``selector`` that specifies
    how to find the element.

    Selector strategies that are supported by default are listed in the table
    below.

    | = Strategy = |     = Match based on =     |         = Example =                |
    | ``css``      | CSS selector.              | ``css=.class > #login_btn``        |
    | ``xpath``    | XPath expression.          | ``xpath=//input[@id="login_btn"]`` |
    | ``text``     | Browser text engine.       | ``text=Login``                     |
    | ``id``       | Element ID Attribute.      | ``id=login_btn``                   |


    == Explicit Selector Strategy ==

    The explicit selector strategy is specified with a prefix using syntax
    ``strategy=value``. Spaces around the separator are ignored, so
    ``css=foo``, ``css= foo`` and ``css = foo`` are all equivalent.


    == Implicit Selector Strategy ==

    *The default selector strategy is `css`.*

    If selector does not contain one of the know explicit selector strategies, it is
    assumed to contain css selector.

    Selectors that are starting with ``//`` or ``..`` are considered as xpath selectors.

    Selectors that are in quotes are considered as text selectors.

    Examples:

    | # CSS selectors are default.
    | `Click`  span > button.some_class         # This is equivalent
    | `Click`  css=span > button.some_class     # to this.
    |
    | # // or .. leads to xpath selector strategy
    | `Click`  //span/button[@class="some_class"]
    | `Click`  xpath=//span/button[@class="some_class"]
    |
    | # "text" in quotes leads to exact text selector strategy
    | `Click`  "Login"
    | `Click`  text="Login"


    == CSS ==

    As written before, the default selector strategy is `css`. See
    [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors | css selector]
    for more information.

    Any malformed selector not starting with ``//`` or ``..`` nor starting and ending
    with a quote is assumed to be a css selector.

    Example:
    | `Click`  span > button.some_class


    == XPath ==

    XPath engine is equivalent to [https://developer.mozilla.org/en/docs/Web/API/Document/evaluate|Document.evaluate].
    Example: ``xpath=//html/body//span[text()="Hello World"]``.

    Malformed selector starting with ``//`` or ``..`` is assumed to be an xpath selector.
    For example, ``//html/body`` is converted to ``xpath=//html/body``. More
    examples are displayed in `Examples`.

    Note that xpath does not pierce [https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM|shadow_roots].


    == Text ==

    Text engine finds an element that contains a text node with the passed text.
    For example, ``Click    text=Login`` clicks on a login button, and
    ``Wait For Elements State   text="lazy loaded text"`` waits for the "lazy loaded text"
    to appear in the page.

    Malformed selector starting and ending with a quote (either ``"`` or ``'``) is assumed
    to be a text selector. For example, ``Click    "Login"`` is converted to ``Click    text="Login"``.
    Be aware that these leads to exact matches only!
    More examples are displayed in `Examples`.


    === Insensitive match ===

    By default, the match is case-insensitive, ignores leading/trailing whitespace and
    searches for a substring. This means ``text= Login`` matches
    ``<button>Button loGIN (click me)</button>``.

    === Exact match ===

    Text body can be escaped with single or double quotes for precise matching,
    insisting on exact match, including specified whitespace and case.
    This means ``text="Login "`` will only match ``<button>Login </button>`` with exactly
    one space after "Login". Quoted text follows the usual escaping rules, e.g.
    use ``\\"`` to escape double quote in a double-quoted string: ``text="foo\\"bar"``.

    === RegEx ===

    Text body can also be a JavaScript-like regex wrapped in / symbols.
    This means ``text=/^hello .*!$/i`` or ``text=/^Hello .*!$/`` will match ``<span>Hello Peter Parker!</span>``
    with any name after ``Hello``, ending with ``!``.
    The first one flagged with ``i`` for case-insensitive.
    See [https://regex101.com/|https://regex101.com] for more information about RegEx.

    === Button and Submit Values ===

    Input elements of the type button and submit are rendered with their value as text,
    and text engine finds them. For example, ``text=Login`` matches
    ``<input type=button value="Login">``.

    == Cascaded selector syntax ==

    Browser library supports the same selector strategies as the underlying
    Playwright node module: xpath, css, id and text. The strategy can either
    be explicitly specified with a prefix or the strategy can be implicit.

    A major advantage of Browser is, that multiple selector engines can be used
    within one selector. It is possible to mix XPath, CSS and Text selectors while
    selecting a single element.

    Selectors are strings that consists of one or more clauses separated by
    ``>>`` token, e.g. ``clause1 >> clause2 >> clause3``. When multiple clauses
    are present, next one is queried relative to the previous one's result.
    Browser library supports concatination of different selectors seperated by ``>>``.

    For example:
    | `Highlight Elements`    "Hello" >> ../.. >> .select_button
    | `Highlight Elements`    text=Hello >> xpath=../.. >> css=.select_button

    Each clause contains a selector engine name and selector body, e.g.
    ``engine=body``. Here ``engine`` is one of the supported engines (e.g. css or
    a custom one). Selector ``body`` follows the format of the particular engine,
    e.g. for css engine it should be a [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors | css selector].
    Body format is assumed to ignore leading and trailing white spaces,
    so that extra whitespace can be added for readability. If selector
    engine needs to include ``>>`` in the body, it should be escaped
    inside a string to not be confused with clause separator,
    e.g. ``text="some >> text"``.

    Selector engine name can be prefixed with ``*`` to capture element that
    matches the particular clause instead of the last one. For example,
    ``css=article >> text=Hello`` captures the element with the text ``Hello``,
    and ``*css=article >> text=Hello`` (note the *) captures the article element
    that contains some element with the text Hello.

    For convenience, selectors in the wrong format are heuristically converted
    to the right format. See `Implicit Selector Strategy`

    == Examples ==
    | # queries 'div' css selector
    | Get Element    css=div
    |
    | # queries '//html/body/div' xpath selector
    | Get Element    //html/body/div
    |
    | # queries '"foo"' text selector
    | Get Element    text=foo
    |
    | # queries 'span' css selector inside the result of '//html/body/div' xpath selector
    | Get Element    xpath=//html/body/div >> css=span
    |
    | # converted to 'css=div'
    | Get Element    div
    |
    | # converted to 'xpath=//html/body/div'
    | Get Element    //html/body/div
    |
    | # converted to 'text="foo"'
    | Get Element    "foo"
    |
    | # queries the div element of every 2nd span element inside an element with the id foo
    | Get Element    \\#foo >> css=span:nth-child(2n+1) >> div
    | Get Element    id=foo >> css=span:nth-child(2n+1) >> div

    Be aware that using ``#`` as a starting character in Robot Framework would be interpreted as comment.
    Due to that fact a ``#id`` must be escaped as ``\\#id``.

    == Frames ==

    By default, selector chains do not cross frame boundaries. It means that a
    simple CSS selector is not able to select and element located inside an iframe
    or a frameset. For this usecase, there is a special selector ``>>>`` which can
    be used to combine a selector for the frame and a selector for an element
    inside a frame.

    Given this simple pseudo html snippet:
    | <iframe id="iframe" src="src.html">
    |   #document
    |     <!DOCTYPE html>
    |     <html>
    |       <head></head>
    |       <body>
    |         <button id="btn">Click Me</button>
    |       </body>
    |     </html>
    | </iframe>

    Here's a keyword call that clicks the button inside the frame.

    | Click   id=iframe >>> id=btn

    The selectors on the left and right side of ``>>>`` can be any valid selectors.
    The selector clause directly before the frame opener ``>>>`` must select the frame element.

    == WebComponents and Shadow DOM ==

    Playwright and so also Browser are able to do automatic piercing of Shadow DOMs
    and therefore are the best automation technology when working with WebComponents.

    Also other technologies claim that they can handle
    [https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM|Shadow DOM and Web Components].
    However, non of them do pierce shadow roots automatically,
    which may be inconvenient when working with Shadow DOM and Web Components.

    For that reason, css engine pierces shadow roots. More specifically, every
    [https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator|Descendant combinator]
    pierces an arbitrary number of open shadow roots, including the implicit descendant combinator
    at the start of the selector.

    That means, it is not nessesary to select each shadow host, open its shadow root and
    select the next shadow host until you reach the element that should be controlled.

    === CSS:light ===

    ``css:light`` engine is equivalent to [https://developer.mozilla.org/en/docs/Web/API/Document/querySelector | Document.querySelector]
    and behaves according to the CSS spec.
    However, it does not pierce shadow roots.

    ``css`` engine first searches for elements in the light dom in the iteration order,
    and then recursively inside open shadow roots in the iteration order. It does not
    search inside closed shadow roots or iframes.

    Examples:

    | <article>
    |   <div>In the light dom</div>
    |   <div slot='myslot'>In the light dom, but goes into the shadow slot</div>
    |   <open mode shadow root>
    |       <div class='in-the-shadow'>
    |           <span class='content'>
    |               In the shadow dom
    |               <open mode shadow root>
    |                   <li id='target'>Deep in the shadow</li>
    |               </open mode shadow root>
    |           </span>
    |       </div>
    |       <slot name='myslot'></slot>
    |   </open mode shadow root>
    | </article>

    Note that ``<open mode shadow root>`` is not an html element, but rather a shadow root
    created with ``element.attachShadow({mode: 'open'})``.

    - Both ``"css=article div"`` and ``"css:light=article div"`` match the first ``<div>In the light dom</div>``.
    - Both ``"css=article > div"`` and ``"css:light=article > div"`` match two ``div`` elements that are direct children of the ``article``.
    - ``"css=article .in-the-shadow"`` matches the ``<div class='in-the-shadow'>``, piercing the shadow root, while ``"css:light=article .in-the-shadow"`` does not match anything.
    - ``"css:light=article div > span"`` does not match anything, because both light-dom ``div`` elements do not contain a ``span``.
    - ``"css=article div > span"`` matches the ``<span class='content'>``, piercing the shadow root.
    - ``"css=article > .in-the-shadow"`` does not match anything, because ``<div class='in-the-shadow'>`` is not a direct child of ``article``
    - ``"css:light=article > .in-the-shadow"`` does not match anything.
    - ``"css=article li#target"`` matches the ``<li id='target'>Deep in the shadow</li>``, piercing two shadow roots.

    === text:light ===

    ``text`` engine open pierces shadow roots similarly to ``css``, while ``text:light`` does not.
    Text engine first searches for elements in the light dom in the iteration order, and then
    recursively inside open shadow roots in the iteration order. It does not search inside
    closed shadow roots or iframes.

    === id, data-testid, data-test-id, data-test and their :light counterparts ===

    Attribute engines are selecting based on the corresponding attribute value.
    For example: ``data-test-id=foo`` is equivalent to ``css=[data-test-id="foo"]``,
    and ``id:light=foo`` is equivalent to ``css:light=[id="foo"]``.

    == Element reference syntax ==

    It is possible to get a reference to an element by using `Get Element` keyword. This
    reference can be used as a *first* part of a selector by using a special selector
    syntax `element=` like this:

    | ${ref}=    Get Element    .some_class
    |            Click          element=${ref} >> .some_child

    The `.some_child` selector in the example is relative to the element referenced by ${ref}.

    = Assertions =

    Keywords that accept arguments ``assertion_operator`` and ``assertion_expected``
    can optionally assert.
    Currently supported assertion operators are:

    |      = Operator =   |   = Alternative Operators =       |              = Description =                                         | = Validate Equivalent =              |
    | ``==``              | ``equal``, ``should be``          | Checks if returned value is equal to expected value.                 | ``value == expected``                |
    | ``!=``              | ``inequal``, ``should not be``    | Checks if returned value is not equal to expected value.             | ``value != expected``                |
    | ``>``               | ``greater than``                  | Checks if returned value is greater than expected value.             | ``value > expected``                 |
    | ``>=``              |                                   | Checks if returned value is greater than or equal to expected value. | ``value >= expected``                |
    | ``<``               | ``less than``                     | Checks if returned value is less than expected value.                | ``value < expected``                 |
    | ``<=``              |                                   | Checks if returned value is less than or equal to expected value.    | ``value <= expected``                |
    | ``*=``              | ``contains``                      | Checks if returned value contains expected value as substring.       | ``expected in value``                |
    | ``^=``              | ``should start with``, ``starts`` | Checks if returned value starts with expected value.                 | ``re.search(f"^{expected}", value)`` |
    | ``$=``              | ``should end with``, ``ends``     | Checks if returned value ends with expected value.                   | ``re.search(f"{expected}$", value)`` |
    | ``matches``         |                                   | Checks if given RegEx matches minimum once in returned value.        | ``re.search(expected, value)``       |
    | ``validate``        |                                   | Checks if given Python expression evaluates to ``True``.             |                                      |
    | ``evaluate``        |  ``then``                         | When using this operator, the keyword does return the evaluated Python expression. |                        |


    The keywords will provide an error message if the assertion fails.
    Assertions will retry until ``timeout`` has expired if they do not pass.

    Be aware that some keywords return strings others return numbers.
    `Get Text` for example always returns a strings and has to be compared with a string.

    Other Keywords have other specific types they return.
    `Get Element Count` always returns an integer.
    `Get Bounding Box` and `Get Viewport Size` can be filtered.
    They return a dictionary without filter and a number when filtered.
    These Keywords do autoconvert the expected value if a number is returned.

    * < less or greater > With Strings*
    Compairisons of strings with ``greater than`` or ``less than`` compares each character,
    starting from 0 reagarding where it stands in the code page.
    Example: ``A < Z``, ``Z < a``, ``ac < dc`
    It does never compare the length of elements. Neither lists nor strings.
    The comparison stops at the first character that is different.
    Examples: ``'abcde' < 'abd'``, ``'100.000' < '2'``
    In Python 3 and therefore also in Browser it is not possible to compare numbers
    with strings with a greater or less operator.
    On keywords that return numbers, the given expected value is automatically
    converted to a number before comparison.


    The getters `Get Page State` and `Get Browser Catalog` return a dictionary. Values of the dictionary can directly asserted.
    Pay attention of possible types because they are evaluated in Python. For example:

    | Get Page State    validate    2020 >= value['year']                     # Compairsion of numbers
    | Get Page State    validate    "IMPORTANT MESSAGE!" == value['message']  # Compairsion of strings

    == The 'then' or 'evaluate' closure ==

    Keywords that accept arguments ``assertion_operator`` and ``assertion_expected``
    can optionally also use ``then`` or ``evaluate`` closure to modify the returned value with
    BuiltIn Evaluate. Actual value can be accessed with ``value``.

    For example ``Get Title  then  'TITLE: '+value``.
    See
    [https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Evaluating%20expressions|
    Builtin Evaluating expressions]
    for more info on the syntax.

    == Examples ==

    | # *Keyword*    *Selector*                    *Key*        *Assertion Operator*    *Assertion Expected*
    | Get Title                                           equal                 Page Title
    | Get Title                                           ^=                    Page
    | Get Style    //*[@id="div-element"]      width      >                     100
    | Get Title                                           matches               \\\\w+\\\\s\\\\w+
    | Get Title                                           validate              value == "Login Page"
    | Get Title                                           evaluate              value if value == "some value" else "something else"

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
        retry_assertions_for="1s",
    ):
        """Browser library can be taken into use with optional arguments:

        - ``timeout`` <str>
          Timeout for keywords that operate on elements. The keywords will wait
          for this time for the element to appear into the page. Defaults to "10s" => 10 seconds.
        - ``enable_playwright_debug`` <bool>
          Enable low level debug information from the playwright tool. Mainly
          Useful for the library developers and for debugging purposes.
        - ``auto_closing_level`` < ``SUITE`` | ``TEST`` | ``MANUAL`` >
          Configure context and page automatic closing. Default is after each test.
          Other options are SUITE for closing after each suite and MANUAL
          for no automatic closing.
        - ``retry_assertions_for`` <str>
          Timeout for retrying assertions on keywords before failing the keywords.
          This timeout starts counting from the first failure.
          Global ``timeout`` will still be in effect.
          This allows stopping execution faster to assertion failure when element is found fast.
        """
        self.timeout = timeout
        self.retry_assertions_for = retry_assertions_for
        self.ROBOT_LIBRARY_LISTENER = self
        self._execution_stack: List[object] = []
        self._unresolved_promises: Set[Future] = set()
        self._playwright_state = PlaywrightState(self)
        libraries = [
            Control(self),
            Cookie(self),
            Devices(self),
            Evaluation(self),
            Interaction(self),
            Getters(self),
            self._playwright_state,
            Network(self),
            Promises(self),
            Waiter(self),
            WebAppState(self),
        ]
        self.playwright = Playwright(self, enable_playwright_debug)
        self._auto_closing_level = auto_closing_level
        DynamicCore.__init__(self, libraries)

    @property
    def outputdir(self):
        return BuiltIn().get_variable_value("${OUTPUTDIR}")

    def _close(self):
        self.playwright.close()

    def _start_suite(self, name, attrs):
        if self._auto_closing_level != AutoClosingLevel.MANUAL:
            self._execution_stack.append(self.get_browser_catalog())

    def _start_test(self, name, attrs):
        if self._auto_closing_level == AutoClosingLevel.TEST:
            self._execution_stack.append(self.get_browser_catalog())

    def _end_test(self, name, attrs):
        if len(self._unresolved_promises) > 0:
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
        catalog_after = self.get_browser_catalog()
        ctx_before_ids = [c["id"] for b in catalog_before for c in b["contexts"]]
        ctx_after_ids = [c["id"] for b in catalog_after for c in b["contexts"]]
        new_ctx_ids = [c for c in ctx_after_ids if c not in ctx_before_ids]
        for ctx_id in new_ctx_ids:
            self._playwright_state.switch_context(ctx_id)
            self._playwright_state.close_context()
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
            self._playwright_state.switch_context(ctx_id)
            self._playwright_state.switch_page(page_id)
            self._playwright_state.close_page()
        # try to set active page and context back to right place.
        for browser in catalog_after:
            if browser["activeBrowser"]:
                activeContext = browser.get("activeContext", None)
                activePage = browser.get("activePage", None)
                if not new_ctx_ids and activeContext is not None:
                    self._playwright_state.switch_context(activeContext)
                    if not (activePage, activeContext) in new_page_ids:
                        self._playwright_state.switch_page(activePage)

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
            self.take_screenshot(path)
        except Exception as err:
            logger.info(f"Was unable to take page screenshot after failure:\n{err}")

    def failure_screenshot_path(self, test_name):
        return os.path.join(
            BuiltIn().get_variable_value("${OUTPUTDIR}"),
            test_name.replace(" ", "_") + "_FAILURE_SCREENSHOT_{index}",
        ).replace("\\", "\\\\")
