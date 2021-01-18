# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import re
import string
import sys
from concurrent.futures._base import Future
from datetime import timedelta
from typing import Dict, List, Optional, Set, Union

from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn  # type: ignore
from robot.utils import secs_to_timestr, timestr_to_secs  # type: ignore
from robotlibcore import DynamicCore  # type: ignore

from .base import ContextCache, LibraryComponent
from .generated.playwright_pb2 import Request
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
    RunOnFailureKeywords,
    Waiter,
    WebAppState,
)
from .playwright import Playwright
from .utils import AutoClosingLevel, is_falsy, is_same_keyword, keyword, logger

# Importing this directly from .utils break the stub type checks
from .utils.data_types import SupportedBrowsers
from .version import __version__ as VERSION


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

    A *context* corresponds to set of independent incognito pages in a browser
    that share cookies, sessions or profile settings. Pages in two separate
    contexts do not share cookies, sessions or profile settings.
    Compared to Selenium, these do *not* require their own browser process.
    To get a clean environment a test can just open a new context.
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

    A *page* does contain the content of the loaded web site and has a browsing history.
    Pages and browser tabs are the same.

    Typical usage could be:
    | *** Test Cases ***
    | Starting a browser with a page
    |     New Browser    chromium    headless=false
    |     New Context    viewport={'width': 1920, 'height': 1080}
    |     New Page       https://marketsquare.github.io/robotframework-browser/Browser.html
    |     Get Title      ==    Browser

    The `Open Browser` keyword opens a new browser, a new context and a new page.
    This keyword is useful for quick experiments or debugging sessions.

    When a `New Page` is called without an open browser, `New Browser`
    and `New Context` are executed with default values first.

    If there is no browser opened in Suite Setup and `New Page` is executed in
    Test Setup, the corresponding pages and context is closed automatically at the end of
    the test. The browser process remains open and will be closed at the end of
    execution.

    Each Browser, Context and Page has a unique ID with which they can be addressed.
    A full catalog of what is open can be received by `Get Browser Catalog` as dictionary.



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

    Keywords that accept arguments ``assertion_operator`` <`AssertionOperator`> and ``assertion_expected``
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


    Bu default the keywords will provide an error message if the assertion fails,
    but default error message can be overwritten with a ``message`` argument. The
    ``message`` argument accepts `{value}`, `{value_type}`, `{expected}` and
    `{expected_type}` [https://docs.python.org/3/library/stdtypes.html#str.format|format]
    options. The `{value}` is the value returned by the keyword and the `{expected}`
    is the expected value defined by the user, usually value in the
    ``assertion_expected`` argument. The `{value_type}` and
    `{expected_type}` are the type definitions from `{value}` and `{expected}`
    arguments. In similar fashion as Python
    [https://docs.python.org/3/library/functions.html#type|type] returns type definition.
    Assertions will retry until ``timeout`` has expired if they do not pass.

    The assertion ``assertion_expected`` value is not converted by the library and
    is used as is. Therefore when assertion is made, the ``assertion_expected``
    argument value and value returned the keyword must have same type. If types
    are not same, assertion will fail. Example `Get Text` always returns a string
    and has to be compared with a string, even the returnd value might look like
    a number.

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

    = Extending Browser library with a JavaScript module =

    Browser library can be extended with JavaScript. Module must be in CommonJS format that Node.js uses.
    You can translate your ES6 module to Node.js CommonJS style with Babel. Many other languages
    can be also translated to modules that can be used from Node.js. For example TypeScript, PureScript and
    ClojureScript just to mention few.

    | async function myGoToKeyword(page, args, logger, playwright) {
    |   logger(args.toString())
    |   playwright.coolNewFeature()
    |   return await page.goto(args[0]);
    | }

    ``page``: [https://playwright.dev/docs/api/class-page|the playwright Page object].

    ``args``: list of strings from Robot Framework keyword call.

    !! A BIT UNSTABLE AND SUBJECT TO API CHANGES !!
    ``logger``: callback function that takes strings as arguments and writes them to robot log. Can be called multiple times.

    ``playwright``: playwright module (* from 'playwright'). Useful for integrating with Playwright features that Browser library doesn't support with it's own keywords. [https://playwright.dev/docs/api/class-playwright| API docs]



    == Example module.js ==

    | async function myGoToKeyword(page, args) {
    |   await page.goto(args[0]);
    |   return await page.title();
    | }
    | exports.__esModule = true;
    | exports.myGoToKeyword = myGoToKeyword;

    == Example Robot Framework side ==

    | *** Settings ***
    | Library   Browser  jsextension=${CURDIR}/module.js
    |
    | *** Test Cases ***
    | Hello
    |   New Page
    |   ${title}=  myGoToKeyword  https://playwright.dev
    |   Should be equal  ${title}  Playwright
    """

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_LISTENER: "Browser"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    SUPPORTED_BROWSERS = ["chromium", "firefox", "webkit"]
    _auto_closing_level: AutoClosingLevel
    _pause_on_failure: Set["Browser"] = set()
    _context_cache = ContextCache()

    def __init__(
        self,
        timeout: timedelta = timedelta(seconds=10),
        enable_playwright_debug: bool = False,
        auto_closing_level: AutoClosingLevel = AutoClosingLevel.TEST,
        retry_assertions_for: timedelta = timedelta(seconds=1),
        run_on_failure: str = "Take Screenshot",
        external_browser_executable: Optional[Dict[SupportedBrowsers, str]] = None,
        jsextension: Optional[str] = None,
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
        - ``run_on_failure`` <str>
          Sets the keyword to execute in case of a failing Browser keyword.
          It can be the name of any keyword that does not have any mandatory argument.
          If no extra action should be done after a failure, set it to ``None`` or any other robot falsy value.
        - ``external_browser_executable`` <Dict <SupportedBrowsers, Path>>
          Dict mapping name of browser to path of executable of a browser.
          Will make opening new browsers of the given type use the set executablePath.
        - ``jsextension`` <str>
          Path to Javascript module exposed as extra keywords. Module must be in CommonJS.
        """
        self.timeout = self.convert_timeout(timeout)
        self.retry_assertions_for = self.convert_timeout(retry_assertions_for)
        self.ROBOT_LIBRARY_LISTENER = self
        self._execution_stack: List[object] = []
        self._running_on_failure_keyword = False
        self._pause_on_failure = set()
        self.run_on_failure_keyword = (
            None if is_falsy(run_on_failure) else run_on_failure
        )
        self.external_browser_executable: Dict[SupportedBrowsers, str] = (
            external_browser_executable or {}
        )
        self._unresolved_promises: Set[Future] = set()
        self._playwright_state = PlaywrightState(self)
        libraries = [
            self._playwright_state,
            Control(self),
            Cookie(self),
            Devices(self),
            Evaluation(self),
            Interaction(self),
            Getters(self),
            Network(self),
            RunOnFailureKeywords(self),
            Promises(self),
            Waiter(self),
            WebAppState(self),
        ]
        self.playwright = Playwright(self, enable_playwright_debug)
        self._auto_closing_level = auto_closing_level
        self.current_arguments = ()
        if jsextension is not None:
            libraries.append(self._initialize_jsextension(jsextension))
        DynamicCore.__init__(self, libraries)

    def _initialize_jsextension(self, jsextension: str) -> LibraryComponent:
        component = LibraryComponent(self)
        with self.playwright.grpc_channel() as stub:
            response = stub.InitializeExtension(
                Request().FilePath(path=os.path.abspath(jsextension))
            )
            for name in response.keywords:
                setattr(component, name, self._jskeyword_call(name))
        return component

    def _jskeyword_call(self, name: str):
        @keyword
        def func(*args):
            with self.playwright.grpc_channel() as stub:
                responses = stub.CallExtensionKeyword(
                    Request().KeywordCall(name=name, arguments=args)
                )
                for response in responses:
                    logger.info(response.log)
                if response.json == "":
                    return
                return json.loads(response.json)

        return func

    @property
    def outputdir(self) -> str:
        if EXECUTION_CONTEXTS.current:
            return BuiltIn().get_variable_value("${OUTPUTDIR}")
        else:
            return "."

    def _close(self):
        try:
            self.playwright.close()
        except ConnectionError as e:
            logger.trace(f"Browser library closing problem: {e}")

    def _start_suite(self, name, attrs):
        if self._auto_closing_level != AutoClosingLevel.MANUAL:
            try:
                self._execution_stack.append(self.get_browser_catalog())
            except ConnectionError as e:
                logger.debug(f"Browser._start_suite connection problem: {e}")

    def _start_test(self, name, attrs):
        if self._auto_closing_level == AutoClosingLevel.TEST:
            try:
                self._execution_stack.append(self.get_browser_catalog())
            except ConnectionError as e:
                logger.debug(f"Browser._start_test connection problem: {e}")

    def _end_test(self, name, attrs):
        if len(self._unresolved_promises) > 0:
            logger.warn(f"Waiting unresolved promises at the end of test '{name}'")
            self.wait_for_all_promises()
        if self._auto_closing_level == AutoClosingLevel.TEST:
            if len(self._execution_stack) == 0:
                logger.debug("Browser._end_test empty execution stack")
                return
            try:
                catalog_before_test = self._execution_stack.pop()
                self._prune_execution_stack(catalog_before_test)
            except AssertionError as e:
                logger.debug(f"Test Case: {name}, End Test: {e}")
            except ConnectionError as e:
                logger.debug(f"Browser._end_test connection problem: {e}")

    def _end_suite(self, name, attrs):
        if self._auto_closing_level != AutoClosingLevel.MANUAL:
            if len(self._execution_stack) == 0:
                logger.debug("Browser._end_suite empty execution stack")
                return
            try:
                catalog_before_suite = self._execution_stack.pop()
                self._prune_execution_stack(catalog_before_suite)
            except AssertionError as e:
                logger.debug(f"Test Suite: {name}, End Suite: {e}")
            except ConnectionError as e:
                logger.debug(f"Browser._end_suite connection problem: {e}")

    def _prune_execution_stack(self, catalog_before: dict) -> None:
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
            self._playwright_state.close_page(page_id, ctx_id)
        # try to set active page and context back to right place.
        # Not needed now that active page and context are just stack heads
        """ for browser in catalog_after:
            if browser["activeBrowser"]:
                activeContext = browser.get("activeContext", None)
                activePage = browser.get("activePage", None)
                if not new_ctx_ids and activeContext is not None:
                    self._playwright_state.switch_context(activeContext)
                    if not (activePage, activeContext) in new_page_ids:
                        self._playwright_state.switch_page(activePage)
        """

    def run_keyword(self, name, args, kwargs=None):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except AssertionError as e:
            self.keyword_error()
            if self._pause_on_failure:
                sys.__stdout__.write(f"\n[ FAIL ] {e}")
                sys.__stdout__.write(
                    "\n[Paused on failure] Press Enter to continue..\n"
                )
                sys.__stdout__.flush()
                input()
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
        self.current_arguments = tuple(attrs["args"])
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
        if self._running_on_failure_keyword or not self.run_on_failure_keyword:
            return
        try:
            self._running_on_failure_keyword = True
            if is_same_keyword(self.run_on_failure_keyword, "Take Screenshot"):
                self.take_screenshot(self._failure_screenshot_path())
            else:
                BuiltIn().run_keyword(self.run_on_failure_keyword)
        except Exception as err:
            logger.warn(
                f"Keyword '{self.run_on_failure_keyword}' could not be run on failure:\n{err}"
            )
        finally:
            self._running_on_failure_keyword = False

    def _failure_screenshot_path(self):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        return os.path.join(
            self.outputdir,
            "".join(c for c in test_name if c in valid_chars).replace(" ", "_")
            + "_FAILURE_SCREENSHOT_{index}",
        )

    def get_timeout(self, timeout: Union[timedelta, None]) -> float:
        if timeout is None:
            return self.timeout
        return self.convert_timeout(timeout)

    def convert_timeout(self, timeout: Union[timedelta, float]) -> float:
        if isinstance(timeout, timedelta):
            return timeout.total_seconds() * 1000
        return timestr_to_secs(timeout) * 1000

    def millisecs_to_timestr(self, timeout: float) -> str:
        return secs_to_timestr(timeout / 1000)
