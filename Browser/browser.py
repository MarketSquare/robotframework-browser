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
import importlib
import json
import pkgutil
import re
import shutil
import string
import sys
import time
import types
from concurrent.futures._base import Future
from datetime import timedelta
from pathlib import Path
from typing import Any, Literal, Optional, Union

from assertionengine import AssertionOperator
from overrides import overrides
from robot.api.deco import library
from robot.errors import DataError
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn
from robot.running.arguments import PythonArgumentParser
from robot.utils import secs_to_timestr, timestr_to_secs
from robotlibcore import DynamicCore, PluginParser  # type: ignore

from .base import ContextCache, LibraryComponent
from .generated.playwright_pb2 import Request, Response
from .keywords import (
    Clock,
    Control,
    Cookie,
    Coverage,
    Devices,
    Evaluation,
    Formatter,
    Getters,
    Interaction,
    LocatorHandler,
    Network,
    Pdf,
    PlaywrightState,
    Promises,
    RunOnFailureKeywords,
    StrictMode,
    Waiter,
    WebAppState,
)
from .keywords.crawling import Crawling
from .playwright import Playwright
from .utils import (
    AutoClosingLevel,
    PlaywrightLogTypes,
    Scope,
    SettingsStack,
    get_normalized_keyword,
    is_falsy,
    keyword,
    logger,
)

# Importing this directly from .utils break the stub type checks
from .utils.data_types import (
    DelayedKeyword,
    HighLightElement,
    KeywordCallStackEntry,
    LambdaFunction,
    RegExp,
    SelectionType,
    SupportedBrowsers,
    TracingGroupMode,
)
from .version import __version__ as VERSION

KW_CALL_CONTENT_TEMPLATE = """body::before {{
    content: '{keyword_call}';
    position: fixed;
    z-index: 9999;
    border: 1px solid lightblue;
    border-radius: 1rem;
    background: #00008b90;
    color: white;
    padding: 2px 10px;
    pointer-events: none;
    font-family: monospace;
    font-size: medium;
    font-weight: normal;
    white-space: pre;
    bottom: 5px;
    left: 5px;
    {additional_styles}
}}"""

KW_CALL_BANNER_FUNCTION = """(content) => {
    const kwCallBanner = document.getElementById('kwCallBanner');
    if (kwCallBanner) {
        kwCallBanner.textContent = content;
    } else {
        const kwCallBanner = document.createElement("style");
        kwCallBanner.setAttribute("id", 'kwCallBanner');
        kwCallBanner.textContent = content;
        document.head.appendChild(kwCallBanner);
    }
}"""


@library(
    converters={RegExp: RegExp.from_string, LambdaFunction: LambdaFunction.from_string}
)
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
    There is no need for dedicated machines anymore.

    A browser process is started ``headless`` (without a GUI) by default.
    Run `New Browser` with specified arguments if a browser with a GUI is requested
    or if a proxy has to be configured.
    A browser process can contain several contexts.


    == Contexts ==

    A *context* corresponds to a set of independent incognito pages in a browser
    that share cookies, sessions or profile settings. Pages in two separate
    contexts do not share cookies, sessions or profile settings.
    Compared to Selenium, these do *not* require their own browser process.
    To get a clean environment a test can just open a new context.
    Due to this new independent browser sessions can be opened with
    Robot Framework Browser about 10 times faster than with Selenium by
    just opening a `New Context` within the opened browser.

    To make pages in the same suite share state, use the same context by opening the
    context with `New Context` on suite setup.

    The context layer is useful e.g. for testing different user sessions on the
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

    Each Browser, Context and Page has a unique ID with which they can be addressed.
    A full catalog of what is open can be received by `Get Browser Catalog` as a dictionary.

    = Automatic page and context closing =

    %AUTO_CLOSING_LEVEL%

    = Finding elements =

    All keywords in the library that need to interact with an element
    on a web page take an argument typically named ``selector`` that specifies
    how to find the element. Keywords can find elements with strict mode. If
    strict mode is true and locator finds multiple elements from the page, keyword
    will fail. If keyword finds one element, keyword does not fail because of
    strict mode. If strict mode is false, keyword does not fail if selector points
    many elements. Strict mode is enabled by default, but can be changed in library
    `importing` or `Set Strict Mode` keyword. Keyword documentation states if keyword
    uses strict mode. If keyword does not state that strict mode is used, then strict
    mode is not applied for the keyword. For more details, see Playwright
    [https://playwright.dev/docs/api/class-page#page-query-selector|strict documentation].

    Selector strategies that are supported by default are listed in the table
    below.

    | = Strategy = |     = Match based on =     |         = Example =                |
    | ``css``      | CSS selector.              | ``css=.class > \\#login_btn``      |
    | ``xpath``    | XPath expression.          | ``xpath=//input[@id="login_btn"]`` |
    | ``text``     | Browser text engine.       | ``text=Login``                     |
    | ``id``       | Element ID Attribute.      | ``id=login_btn``                   |

    CSS Selectors can also be recorded with `Record selector` keyword.

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

    Note that ``#`` is a comment character in [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#ignored-data | Robot Framework syntax] and needs to be
    escaped like ``\\#`` to work as a [https://developer.mozilla.org/en-US/docs/Web/CSS/ID_selectors | css ID selector].

    Examples:
    | `Click`  span > button.some_class
    | `Get Text`  \\#username_field  ==  George


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

    Text engine finds fields based on their labels in text inserting keywords.

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

    A major advantage of Browser is that multiple selector engines can be used
    within one selector. It is possible to mix XPath, CSS and Text selectors while
    selecting a single element.

    Selectors are strings that consists of one or more clauses separated by
    ``>>`` token, e.g. ``clause1 >> clause2 >> clause3``. When multiple clauses
    are present, next one is queried relative to the previous one's result.
    Browser library supports concatenation of different selectors separated by ``>>``.

    For example:
    | `Highlight Elements`    "Hello" >> ../.. >> .select_button
    | `Highlight Elements`    text=Hello >> xpath=../.. >> css=.select_button

    Each clause contains a selector engine name and selector body, e.g.
    ``engine=body``. Here ``engine`` is one of the supported engines (e.g. css or
    a custom one). Selector ``body`` follows the format of the particular engine,
    e.g. for css engine it should be a [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors | css selector].
    Body format is assumed to ignore leading and trailing white spaces,
    so that extra whitespace can be added for readability. If the selector
    engine needs to include ``>>`` in the body, it should be escaped
    inside a string to not be confused with clause separator,
    e.g. ``text="some >> text"``.

    Selector engine name can be prefixed with ``*`` to capture an element that
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

    == iFrames ==

    By default, selector chains do not cross frame boundaries. It means that a
    simple CSS selector is not able to select an element located inside an iframe
    or a frameset. For this use case, there is a special selector ``>>>`` which can
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
    The selector clause directly before the frame opener ``>>>`` must select the frame element itself.
    Frame selection is the only place where Browser Library modifies the selector, as explained in above.
    In all cases, the library does not alter the selector in any way, instead it is passed as is to the
    Playwright side.

    If multiple keyword shall be performed inside a frame,
    it is possible to define a selector prefix with `Set Selector Prefix`.
    If this prefix is set to a frame/iframe it has similar behavior as SeleniumLibrary keyword `Select Frame`.

    == WebComponents and Shadow DOM ==

    Playwright and so also Browser are able to do automatic piercing of Shadow DOMs
    and therefore are the best automation technology when working with WebComponents.

    Also other technologies claim that they can handle
    [https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM|Shadow DOM and Web Components].
    However, none of them do pierce shadow roots automatically,
    which may be inconvenient when working with Shadow DOM and Web Components.

    For that reason, the css engine pierces shadow roots. More specifically, every
    [https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator|Descendant combinator]
    pierces an arbitrary number of open shadow roots, including the implicit descendant combinator
    at the start of the selector.

    That means, it is not necessary to select each shadow host, open its shadow root and
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

    It is possible to get a reference to a Locator by using `Get Element` and `Get Elements` keywords.
    Keywords do not save reference to an element in the HTML document, instead it saves reference to a Playwright
    [https://playwright.dev/docs/api/class-locator|Locator]. In nutshell Locator captures the logic of how to
    retrieve that element from the page. Each time an action is performed, the locator re-searches the elements
    in the page. This reference can be used as a *first* part of a selector by using a special selector
    syntax `element=`. like this:

    | ${ref}=    Get Element    .some_class
    |            Click          ${ref} >> .some_child     # Locator searches an element from the page.
    |            Click          ${ref} >> .other_child    # Locator searches again an element from the page.

    The `.some_child` and `.other_child` selectors in the example are relative to the element referenced
    by ${ref}. Please note that frame piercing is not possible with element reference.

    = Assertions =

    Keywords that accept arguments ``assertion_operator`` <`AssertionOperator`> and ``assertion_expected``
    can optionally assert that a specified condition holds. Keywords will return the value even when the
    assertion is performed by the keyword.

    Assert will retry and fail only after a specified timeout.
    See `Importing` and ``retry_assertions_for`` (default is 1 second) for configuring this timeout.


    %ASSERTION_TABLE%

    By default, keywords will provide an error message if an assertion fails.
    Default error messages can be overwritten with a ``message`` argument.
    The ``message`` argument accepts `{value}`, `{value_type}`, `{expected}` and
    `{expected_type}` [https://docs.python.org/3/library/stdtypes.html#str.format|format]
    options.
    The `{value}` is the value returned by the keyword and the `{expected}`
    is the expected value defined by the user, usually the value in the
    ``assertion_expected`` argument. The `{value_type}` and
    `{expected_type}` are the type definitions from `{value}` and `{expected}`
    arguments. In similar fashion as Python
    [https://docs.python.org/3/library/functions.html#type|type] returns type definition.
    Assertions will retry until ``timeout`` has expired if they do not pass.

    The assertion ``assertion_expected`` value is not converted by the library and
    is used as is. Therefore when assertion is made, the ``assertion_expected``
    argument value and value returned the keyword must have the same type. If types
    are not the same, assertion will fail. Example `Get Text` always returns a string
    and has to be compared with a string, even the returned value might look like
    a number.

    Other Keywords have other specific types they return.
    `Get Element Count` always returns an integer.
    `Get Bounding Box` and `Get Viewport Size` can be filtered.
    They return a dictionary without a filter and a number when filtered.
    These Keywords do automatic conversion for the expected value if a number is returned.

    * < less or greater > With Strings*
    Comparisons of strings with ``greater than`` or ``less than`` compares each character,
    starting from 0 regarding where it stands in the code page.
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

    | Get Page State    validate    2020 >= value['year']                     # Comparison of numbers
    | Get Page State    validate    "IMPORTANT MESSAGE!" == value['message']  # Comparison of strings

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


    = Implicit waiting =

    Browser library and Playwright have many mechanisms to help in waiting for elements.
    Playwright will auto-wait before performing actions on elements.
    Please see [https://playwright.dev/docs/actionability/ | Auto-waiting on Playwright documentation]
    for more information.

    On top of Playwright auto-waiting Browser assertions will wait and retry
    for specified time before failing any `Assertions`.
    Time is specified in Browser library initialization with ``retry_assertions_for``.

    Browser library also includes explicit waiting keywords such as `Wait for Elements State`
    if more control for waiting is needed.

    = Experimental: Re-using same node process =

    Browser library integrated nodejs and python. The NodeJS side can be also executed as a standalone process.
    Browser libraries running on the same machine can talk to that instead of starting new node processes.
    This can speed execution when running tests parallel.
    To start node side run on the directory when the Browser package is
    ``PLAYWRIGHT_BROWSERS_PATH=0 node Browser/wrapper/index.js PORT``.

    ``PORT`` is the port you want to use for the node process.
    To execute tests then with pabot for example do ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT=PORT pabot ..``.

    = Experimental: Provide parameters to node process =

    Browser library is integrated with NodeJSand and Python. Browser library starts a node process, to communicate
    Playwright API in NodeJS side. It is possible to provide parameters for the started node process by defining
    ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS environment variable, before starting the test execution. Example:
    ``ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS=--inspect;robot path/to/tests``.
    There can be multiple arguments defined in the environment variable and arguments must be separated with comma.

    = Scope Setting =

    Some keywords which manipulates library settings have a scope argument.
    With that scope argument one can set the "live time" of that setting.
    Available Scopes are: `Global`, `Suite` and `Test`/`Task`
    See `Scope`.
    Is a scope finished, this scoped setting, like timeout, will no longer be used.

    Live Times:
    - A `Global` scope will live forever until it is overwritten by another `Global` scope. Or locally temporarily overridden by a more narrow scope.
    - A `Suite` scope will locally override the `Global` scope and live until the end of the Suite within it is set, or if it is overwritten by a later setting with `Global` or same scope. Children suite does inherit the setting from the parent suite but also may have its own local `Suite` setting that then will be inherited to its children suites.
    - A `Test` or `Task` scope will be inherited from its parent suite but when set, lives until the end of that particular test or task.

    A new set higher order scope will always remove the lower order scope which may be in charge.
    So the setting of a `Suite` scope from a test, will set that scope to the robot file suite where that test is and removes the `Test` scope that may have been in place.

    = Extending Browser library with a JavaScript module =

    Browser library can be extended with JavaScript. The module must be in CommonJS format that Node.js uses.
    You can translate your ES6 module to Node.js CommonJS style with Babel. Many other languages
    can be also translated to modules that can be used from Node.js. For example TypeScript, PureScript and
    ClojureScript just to mention few.

    | async function myGoToKeyword(url, args, page, logger, playwright) {
    |   logger(args.toString())
    |   playwright.coolNewFeature()
    |   return await page.goto(url);
    | }

    Functions can contain any number of arguments and arguments may have default values.

    There are some reserved arguments that are not accessible from Robot Framework side.
    They are injected to the function if they are in the arguments:

    ``page``: [https://playwright.dev/docs/api/class-page|the playwright Page object].

    ``context``: [https://playwright.dev/docs/api/class-browsercontext|the playwright BrowserContext object].

    ``browser``: [https://playwright.dev/docs/api/class-browser|the playwright Browser object].

    ``args``: the rest of values from Robot Framework keyword call ``*args``.

    ``logger``: callback function that takes strings as arguments and writes them to robot log. Can be called multiple times.

    ``playwright``: playwright module (* from 'playwright'). Useful for integrating with Playwright features that Browser library doesn't support with it's own keywords. [https://playwright.dev/docs/api/class-playwright| API docs]

    also argument name ``self`` can not be used.

    == Example module.js ==

    | async function myGoToKeyword(pageUrl, page) {
    |   await page.goto(pageUrl);
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

    Also selector syntax can be extended with a custom selector using a js module

    == Example module keyword for custom selector registering ==

    | async function registerMySelector(playwright) {
    | playwright.selectors.register("myselector", () => ({
    |    // Returns the first element matching given selector in the root's subtree.
    |    query(root, selector) {
    |       return root.querySelector(`a[data-title="${selector}"]`);
    |     },
    |
    |     // Returns all elements matching given selector in the root's subtree.
    |     queryAll(root, selector) {
    |       return Array.from(root.querySelectorAll(`a[data-title="${selector}"]`));
    |     }
    | }));
    | return 1;
    | }
    | exports.__esModule = true;
    | exports.registerMySelector = registerMySelector;

    = Plugins =

    Browser library offers plugins as a way to modify and add library keywords and modify some of the internal
    functionality without creating a new library or hacking the source code. See plugin API
    [https://github.com/MarketSquare/robotframework-browser/blob/main/docs/plugins/README.md | documentation] for
    further details.

    = Language =

    Browser library offers possibility to translate keyword names and documentation to new language. If language
    is defined, Browser library will search from
    [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path | module search path]
    Python packages starting with `robotframework_browser_translation` by using
    [https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/ | Python pluging API]. Library
    is using naming convention to find Python plugins.

    The package must implement single API call, ``get_language`` without any arguments. Method must return a
    dictionary containing two keys: ``language`` and ``path``. The language key value defines which language
    the package contains. Also value should match (case insentive) the library ``language`` import parameter.
    The path parameter value should be full path to the translation file.

    == Translation file ==

    The file name or extension is not important, but data must be in [https://www.json.org/json-en.html | json]
    format. The keys of json are the methods names, not the keyword names, which implements keywords. Value of
    key is json object which contains two keys: ``name`` and ``doc``. The ``name`` key contains the keyword
    translated name and `doc` contains translated documentation. Providing doc and name are optional, example
    translation json file can only provide translations to keyword names or only to documentatin. But it is
    always recomended to provide translation to both name and doc. Special key ``__intro__`` is for class level
    documentation and ``__init__`` is for init level documentation. These special values ``name`` can not be
    translated, instead ``name`` should be kept the same.

    == Generating template translation file ==

    Template translation file, with English language can be created by running:
    `rfbrowser translation /path/to/translation.json` command. Command does not provide translations to other
    languages, it only provides easy way to create full list keywords and their documentation in correct
    format. It is also possible to add keywords from library plugins and js extensions by providing
    `--plugings` and `--jsextension` arguments to command. Example:
    `rfbrowser translation --plugings myplugin.SomePlugin --jsextension /path/ot/jsplugin.js /path/to/translation.json`

    Example project for translation can be found from
    [https://github.com/MarketSquare/robotframework-browser-translation-fi | robotframework-browser-translation-fi]
    repository.
    """

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_LISTENER: "Browser"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    _context_cache = ContextCache()
    _suite_cleanup_done = False
    _output_dir = "."

    def __init__(  # noqa: PLR0915
        self,
        *_,
        auto_closing_level: AutoClosingLevel = AutoClosingLevel.TEST,
        auto_delete_passed_tracing: bool = False,
        enable_playwright_debug: Union[
            PlaywrightLogTypes, bool
        ] = PlaywrightLogTypes.library,
        enable_presenter_mode: Union[HighLightElement, bool] = False,
        external_browser_executable: Optional[dict[SupportedBrowsers, str]] = None,
        jsextension: Union[list[str], str, None] = None,
        language: Optional[str] = None,
        playwright_process_port: Optional[int] = None,
        plugins: Union[list[str], str, None] = None,
        retry_assertions_for: timedelta = timedelta(seconds=1),
        run_on_failure: str = "Take Screenshot  fail-screenshot-{index}",
        selector_prefix: Optional[str] = None,
        show_keyword_call_banner: Optional[bool] = None,
        strict: bool = True,
        timeout: timedelta = timedelta(seconds=10),
        tracing_group_mode: TracingGroupMode = TracingGroupMode.Full,
    ):
        """Browser library can be taken into use with optional arguments:

        | =Argument=                        | =Description= |
        | ``auto_closing_level``            | Configure context and page automatic closing. Default is ``TEST``, for more details, see `AutoClosingLevel` |
        | ``auto_delete_passed_tracing``    | If ``auto_closing_level`` is set to ``SUITE`` or ``TEST`` and ``tracing`` of `New Context` active, traces of passed tests or suites, depending on the context scope, not be saved. Also temp files will all be deleted after the whole execution ends. |
        | ``enable_playwright_debug``       | Enable low level debug information from the playwright to playwright-log.txt file. For more details, see `PlaywrightLogTypes`. |
        | ``enable_presenter_mode``         | Automatic highlights the interacted components, slowMo and a small pause at the end. Can be enabled by giving True or can be customized by giving a dictionary: `{"duration": "2 seconds", "width": "2px", "style": "dotted", "color": "blue"}` Where `duration` is time format in Robot Framework format, defaults to 2 seconds. `width` is width of the marker in pixels, defaults the `2px`. `style` is the style of border, defaults to `dotted`. `color` is the color of the marker, defaults to `blue`. By default, the call banner keyword is also enabled unless explicitly disabled. |
        | ``external_browser_executable``   | Dict mapping name of browser to path of executable of a browser. Will make opening new browsers of the given type use the set executablePath. Currently only configuring of `chromium` to a separate executable (chrome, chromium and Edge executables all work with recent versions) works. |
        | ``jsextension``                   | Path to Javascript modules exposed as extra keywords. The modules must be in CommonJS. It can either be a single path, a comma-separated lists of path or a real list of strings |
        | ``language``                      | Defines language which is used to translate keyword names and documentation. |
        | ``playwright_process_port``       | Experimental reusing of playwright process. ``playwright_process_port`` is preferred over environment variable ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT``. See `Experimental: Re-using same node process` for more details. |
        | ``plugins``                       | Allows extending the Browser library with external Python classes. Can either be a single class/module, a comma-separated list or a real list of strings |
        | ``retry_assertions_for``          | Timeout for retrying assertions on keywords before failing the keywords. This timeout starts counting from the first failure. Global ``timeout`` will still be in effect. This allows stopping execution faster to assertion failure when element is found fast. |
        | ``run_on_failure``                | Sets the keyword to execute in case of a failing Browser keyword. It can be the name of any keyword. If the keyword has arguments those must be separated with two spaces for example ``My keyword \\ arg1 \\ arg2``. If no extra action should be done after a failure, set it to ``None`` or any other robot falsy value. Run on failure is not applied when library methods are executed directly from Python. |
        | ``selector_prefix``               | Prefix for all selectors. This is useful when you need to use add an iframe selector before each selector. |
        | ``show_keyword_call_banner``      | If set to ``True``, will show a banner with the keyword name and arguments before the keyword is executed at the bottom of the page. If set to ``False``, will not show the banner. If set to None, which is the default, will show the banner only if the presenter mode is enabled. `Get Page Source` and `Take Screenshot` will not show the banner, because that could negatively affect your test cases/tasks. This feature may be super helpful when you are debugging your tests and using tracing from `New Context` or `Video recording` features. |
        | ``strict``                        | If keyword selector points multiple elements and keywords should interact with one element, keyword will fail if ``strict`` mode is true. Strict mode can be changed individually in keywords or by ``Set Strict Mode`` keyword. |
        | ``timeout``                       | Timeout for keywords that operate on elements. The keywords will wait for this time for the element to appear into the page. Defaults to "10s" => 10 seconds. |
        | ``tracing_group_mode``            | Defines how Robot Framework keyword calls are logged in Playwright trace log. Default is `Full`. For more details, see `TracingGroupMode`. |
        """
        if _:
            raise ValueError("Browser library does not accept positional arguments.")
        self.ROBOT_LIBRARY_LISTENER = self
        self.scope_stack: dict = {}
        self.suite_ids: dict[str, None] = {}
        self.current_test_id: Optional[str] = None
        self._playwright_state: PlaywrightState = PlaywrightState(self)
        self._browser_control = Control(self)
        self._assertion_formatter = Formatter(self)
        libraries = [
            self._playwright_state,
            self._browser_control,
            Cookie(self),
            Clock(self),
            Coverage(self),
            Crawling(self),
            Devices(self),
            Evaluation(self),
            self._assertion_formatter,
            Interaction(self),
            Getters(self),
            LocatorHandler(self),
            Network(self),
            Pdf(self),
            RunOnFailureKeywords(self),
            StrictMode(self),
            Promises(self),
            Waiter(self),
            WebAppState(self),
        ]
        self.enable_playwright_debug = enable_playwright_debug
        self.playwright_process_port = playwright_process_port
        if self.enable_playwright_debug is True:
            self.enable_playwright_debug = PlaywrightLogTypes.playwright
        elif self.enable_playwright_debug is False:
            self.enable_playwright_debug = PlaywrightLogTypes.library
        if self.enable_playwright_debug == PlaywrightLogTypes.disabled:
            self._playwright_log = None
        else:
            self._playwright_log = self._get_log_file_name()
        self._playwright: Optional[Playwright] = None
        self._auto_closing_level = auto_closing_level
        self.auto_delete_passed_tracing = auto_delete_passed_tracing
        # Parsing needs keywords to be discovered.
        self.external_browser_executable: dict[SupportedBrowsers, str] = (
            external_browser_executable or {}
        )
        if jsextension:
            jsextensions = (
                jsextension.split(",") if isinstance(jsextension, str) else jsextension
            )
            for js_ext in jsextensions:
                libraries.append(self._create_lib_component_from_jsextension(js_ext))
        if plugins:
            parser = PluginParser(LibraryComponent, [self])
            parsed_plugins = parser.parse_plugins(plugins)
            libraries.extend(parsed_plugins)
            self._plugin_keywords = parser.get_plugin_keywords(parsed_plugins)
        else:
            self._plugin_keywords = []
        self.presenter_mode: Union[HighLightElement, bool] = enable_presenter_mode
        self.tracing_group_mode = tracing_group_mode
        self._execution_stack: list[dict] = []
        self._running_on_failure_keyword = False
        self.pause_on_failure: set[str] = set()
        self._unresolved_promises: set[Future] = set()
        self._keyword_formatters: dict = {}
        self._current_loglevel: Optional[str] = None
        self.is_test_case_running = False
        self.auto_closing_default_run_before_unload: bool = False
        self.keyword_call_stack: list[KeywordCallStackEntry] = []
        self.tracing_contexts: list[str] = []

        translation_file = self._get_translation(language)
        DynamicCore.__init__(self, libraries, translation_file)

        self.scope_stack["timeout"] = SettingsStack(
            self.convert_timeout(timeout),
            self,
            self._browser_control.set_playwright_timeout,
        )
        self.scope_stack["retry_assertions_for"] = SettingsStack(
            self.convert_timeout(retry_assertions_for), self
        )
        self.scope_stack["strict_mode"] = SettingsStack(strict, self)
        self.scope_stack["selector_prefix"] = SettingsStack(selector_prefix, self)
        self.scope_stack["run_on_failure"] = SettingsStack(
            self._parse_run_on_failure_keyword(run_on_failure), self
        )
        self.scope_stack["show_keyword_call_banner"] = SettingsStack(
            show_keyword_call_banner, self
        )
        self.scope_stack["keyword_call_banner_add_style"] = SettingsStack("", self)
        self.scope_stack["assertion_formatter"] = SettingsStack({}, self)

    @property
    def playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = Playwright(
                self,
                self.enable_playwright_debug,
                self.playwright_process_port,
                self._playwright_log,
            )
        return self._playwright

    @property
    def keyword_call_banner_add_style(self):
        return self.scope_stack["keyword_call_banner_add_style"].get()

    @property
    def show_keyword_call_banner(self):
        return self.scope_stack["show_keyword_call_banner"].get()

    @property
    def run_on_failure_keyword(self) -> DelayedKeyword:
        return self.scope_stack["run_on_failure"].get()

    @property
    def timeout(self):
        return self.scope_stack["timeout"].get()

    def _parse_run_on_failure_keyword(
        self, keyword: Union[str, None]
    ) -> DelayedKeyword:
        if keyword is None or is_falsy(keyword):
            return DelayedKeyword(None, None, (), {})
        parts = keyword.split("  ")
        keyword_name = parts[0]
        normalized_keyword_name = get_normalized_keyword(keyword_name)
        args = parts[1:]
        if normalized_keyword_name not in self.keywords:
            return DelayedKeyword(keyword_name, keyword_name, tuple(args), {})
        spec = PythonArgumentParser().parse(
            self.keywords[normalized_keyword_name], keyword_name
        )
        varargs = []
        kwargs = {}
        for arg in spec.resolve(args):
            for item in arg:
                if isinstance(item, tuple):
                    kwargs[item[0]] = item[1]
                else:
                    varargs.append(item)
        return DelayedKeyword(
            normalized_keyword_name, keyword_name, tuple(varargs), kwargs
        )

    def _create_lib_component_from_jsextension(
        self, jsextension: str
    ) -> LibraryComponent:
        component = LibraryComponent(self)
        response = self.init_js_extension(Path(jsextension))
        for name, args, doc in zip(
            response.keywords,
            response.keywordArguments,
            response.keywordDocumentations,
        ):
            self._jskeyword_call(component, name, args, doc)
        return component

    def init_js_extension(
        self, js_extension_path: Union[Path, str]
    ) -> Response.Keywords:
        with self.playwright.grpc_channel() as stub:
            return stub.InitializeExtension(
                Request().FilePath(
                    path=str(Path(js_extension_path).resolve().absolute())
                )
            )

    def _js_value_to_python_value(self, value: str) -> str:
        return {
            "true": "True",
            "false": "False",
            "null": "None",
            "undefined": "None",
            "NaN": "float('nan')",
            "Infinity": "float('inf')",
            "-Infinity": "float('-inf')",
        }.get(value, value)

    def _jskeyword_call(
        self,
        component: LibraryComponent,
        name: str,
        argument_names_and_default_values: str,
        doc: str,
    ):
        argument_names_and_vals = [
            [a.strip() for a in arg.split("=")]
            for arg in (argument_names_and_default_values or "").split(",")
            if arg
        ]
        argument_names_and_default_values_texts = []
        arg_set_texts = []
        for item in argument_names_and_vals:
            arg_name = item[0]
            if arg_name in ["logger", "playwright", "page", "context", "browser"]:
                arg_set_texts.append(f'("{arg_name}", "RESERVED")')
            else:
                arg_set_texts.append(f'("{arg_name}", {arg_name})')
                if arg_name == "args":
                    argument_names_and_default_values_texts.append("*args")
                elif len(item) > 1:
                    argument_names_and_default_values_texts.append(
                        f"{arg_name}={self._js_value_to_python_value(item[1])}"
                    )
                else:
                    argument_names_and_default_values_texts.append(f"{arg_name}")
        text = f"""
@keyword
def {name}(self, {", ".join(argument_names_and_default_values_texts)}):
    \"\"\"{doc}\"\"\"
    _args_browser_internal = dict()
    _args_browser_internal["arguments"] = [{", ".join(arg_set_texts)}]
    with self.playwright.grpc_channel() as stub:
        responses = stub.CallExtensionKeyword(
            Request().KeywordCall(name="{name}", arguments=json.dumps(_args_browser_internal))
        )
        for response in responses:
            logger.info(response.log)
        if response.json == "":
            return
        return json.loads(response.json)
"""
        try:
            exec(
                text,
                {**globals(), "keyword": keyword, "json": json},
                component.__dict__,
            )
            setattr(
                component, name, types.MethodType(component.__dict__[name], component)
            )
        except SyntaxError as e:
            raise DataError(f"{e.msg} in {name}")

    def call_js_keyword(self, keyword_name: str, **args) -> Any:
        reserved = {
            "logger": "RESERVED",
            "playwright": "RESERVED",
            "page": "RESERVED",
            "context": "RESERVED",
            "browser": "RESERVED",
        }
        _args_browser_internal = {
            "arguments": [
                (arg_name, reserved.get(arg_name, value))
                for arg_name, value in args.items()
            ]
        }
        with self.playwright.grpc_channel() as stub:
            responses = stub.CallExtensionKeyword(
                Request().KeywordCall(
                    name=keyword_name, arguments=json.dumps(_args_browser_internal)
                )
            )
            for response in responses:
                logger.info(response.log)
            if response.json == "":
                return None
            return json.loads(response.json)

    @property
    def outputdir(self) -> str:
        if EXECUTION_CONTEXTS.current:
            return BuiltIn().get_variable_value("${OUTPUTDIR}")
        return self._output_dir

    @outputdir.setter
    def outputdir(self, value: str):
        self._output_dir = value

    @property
    def browser_output(self) -> Path:
        return Path(self.outputdir, "browser")

    @property
    def screenshots_output(self) -> Path:
        return self.browser_output / "screenshot"

    @property
    def video_output(self) -> Path:
        return self.browser_output / "video"

    @property
    def traces_output(self) -> Path:
        return self.browser_output / "traces"

    @property
    def traces_temp(self) -> Path:
        return self.traces_output / "temp"

    @property
    def state_file(self):
        return self.browser_output / "state"

    @property
    def coverage_output(self) -> Path:
        return self.browser_output / "coverage"

    def _start_suite(self, _name, attrs):
        self.suite_ids[attrs["id"]] = None
        self._add_to_scope_stack(attrs["id"], Scope.Suite)
        if not Browser._suite_cleanup_done:
            Browser._suite_cleanup_done = True
            for path in [
                self.screenshots_output,
                self.video_output,
                self.traces_output,
                self.state_file,
                self.coverage_output,
            ]:
                if path.is_dir():
                    logger.debug(f"Removing: {path}")
                    shutil.rmtree(str(path), ignore_errors=True)
        if self._auto_closing_level in [AutoClosingLevel.TEST, AutoClosingLevel.SUITE]:
            try:
                self._execution_stack.append(
                    [] if self._playwright is None else self.get_browser_catalog()
                )
            except ConnectionError as e:
                logger.debug(f"Browser._start_suite connection problem: {e}")

    def _start_test(self, _name, attrs):
        self.current_test_id = attrs["id"]
        self._add_to_scope_stack(attrs["id"], Scope.Test)
        self.is_test_case_running = True
        if self._auto_closing_level == AutoClosingLevel.TEST:
            try:
                self._execution_stack.append(
                    [] if self._playwright is None else self.get_browser_catalog()
                )
            except ConnectionError as e:
                logger.debug(f"Browser._start_test connection problem: {e}")

    def _resolve_path(self, attrs: dict) -> Union[Path, None]:
        source = Path(attrs["source"])
        if source.is_dir():
            source = source / "__init__.robot"
            if not source.exists():
                return None
        return source

    def _start_keyword(self, name, attrs):
        source = self._resolve_path(attrs)
        kw_call_stack_entry = self._create_keyword_call_stack_entry(
            name or attrs.get("value", ""),
            attrs["args"],
            source,
            attrs["lineno"],
            attrs["type"],
        )
        self.keyword_call_stack.append(kw_call_stack_entry)
        if self.tracing_group_mode == TracingGroupMode.Full:
            self._playwright_state.open_trace_group(**kw_call_stack_entry)
        if not (
            self.show_keyword_call_banner is False
            or (self.show_keyword_call_banner is None and not self.presenter_mode)
            or attrs["libname"] != "Browser"
            or attrs["status"] == "NOT RUN"
        ):
            self._show_keyword_call(attrs)
        if "secret" in attrs["kwname"].lower() and attrs["libname"] == "Browser":
            self._set_logging(False)

        if attrs["type"] == "Teardown":
            timeout_pattern = "Test timeout .* exceeded."
            test = EXECUTION_CONTEXTS.current.test
            if (
                test is not None
                and test.status == "FAIL"
                and re.match(timeout_pattern, test.message)
            ):
                self.screenshot_on_failure(test.name)

    def _create_keyword_call_stack_entry(
        self,
        name: str,
        args: list,
        source: Union[str, Path, None],
        lineno: int,
        typ: str,
    ) -> KeywordCallStackEntry:
        if typ not in ["SETUP", "KEYWORD", "TEARDOWN"]:
            args = [name] if name else []
            name = typ
        try:
            lineno = int(lineno)
        except (ValueError, TypeError):
            lineno = 0
        return {
            "name": (
                f"{name}    {'    '.join(args)}" if args else name  # noqa: RUF001
            ),
            "file": str(source),
            "line": lineno,
        }

    def run_keyword(self, name, args, kwargs=None):
        try:
            if (
                self.tracing_group_mode == TracingGroupMode.Browser
                and self.keyword_call_stack
            ):
                self._playwright_state.open_trace_group(**(self.keyword_call_stack[-1]))
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except AssertionError as e:
            self.keyword_error()
            e.args = self._alter_keyword_error(name, e.args)
            if self.pause_on_failure and sys.__stdout__ is not None:
                sys.__stdout__.write(f"\n[ FAIL ] {e}")
                sys.__stdout__.write(
                    "\n[Paused on failure] Press Enter to continue..\n"
                )
                sys.__stdout__.flush()
                input()
            raise e
        finally:
            if (
                self.tracing_group_mode == TracingGroupMode.Browser
                and self.keyword_call_stack
            ):
                self._playwright_state.close_trace_group()

    def get_keyword_tags(self, name: str) -> list:
        tags = list(DynamicCore.get_keyword_tags(self, name))
        if name in self._plugin_keywords:
            tags.append("Plugin")
        return tags

    def _end_keyword(self, _name, attrs):
        if self.keyword_call_stack:
            self.keyword_call_stack.pop()
        if self.tracing_group_mode == TracingGroupMode.Full:
            self._playwright_state.close_trace_group()
        if "secret" in attrs["kwname"].lower() and attrs["libname"] == "Browser":
            self._set_logging(True)

    def _end_test(self, name, attrs):
        self._remove_from_scope_stack(attrs["id"])
        self.current_test_id = None
        self.is_test_case_running = False
        if len(self._unresolved_promises) > 0:
            logger.warn(f"Waiting unresolved promises at the end of test '{name}'")
            self.wait_for_all_promises()
        if self._auto_closing_level == AutoClosingLevel.TEST:
            if self.presenter_mode:
                logger.debug("Presenter mode: Wait for 5 seconds before pruning pages")
                time.sleep(5.0)
            self.execute_auto_closing(name, attrs, "Test", attrs["status"])

    def _end_suite(self, name, attrs):
        self._remove_from_scope_stack(attrs["id"])
        self.suite_ids.pop(attrs["id"], None)
        if self._auto_closing_level in [AutoClosingLevel.TEST, AutoClosingLevel.SUITE]:
            self.execute_auto_closing(name, attrs, "Suite", attrs["status"])

    def _close(self):
        if self.auto_delete_passed_tracing and self.traces_temp.is_dir():
            shutil.rmtree(str(self.traces_temp), ignore_errors=True)

    def execute_auto_closing(
        self, name: str, attrs: dict, typ: Literal["Test", "Suite"], status: str
    ):
        if len(self._execution_stack) == 0:
            logger.debug(f"Browser._end_{typ.lower()} empty execution stack")
            return
        try:
            catalog_before = self._execution_stack.pop()
            self._playwright_state.open_trace_group(
                f"Auto Closing    {typ}: {name}",  # noqa: RUF001
                file=attrs.get("source"),
                line=attrs.get("lineno", 0),
            )
            self._prune_execution_stack(catalog_before, status)
            self._playwright_state.close_trace_group()
        except AssertionError as e:
            logger.debug(f"{typ}: {name}, End {typ}: {e}")
        except ConnectionError as e:
            logger.debug(f"Browser._end_{typ.lower()} connection problem: {e}")

    def _add_to_scope_stack(self, scope_id: str, scope: Scope):
        for stack in self.scope_stack.values():
            stack.start(scope_id, scope)

    def _remove_from_scope_stack(self, scope_id):
        for stack in self.scope_stack.values():
            stack.end(scope_id)

    def _prune_execution_stack(self, catalog_before: dict, status: str) -> None:
        catalog_after = self.get_browser_catalog()
        ctx_before_ids: list[str] = [
            c["id"] for b in catalog_before for c in b["contexts"]
        ]
        ctx_after_ids: list[str] = [
            c["id"] for b in catalog_after for c in b["contexts"]
        ]
        new_ctx_ids: list[str] = [c for c in ctx_after_ids if c not in ctx_before_ids]
        for ctx_id in new_ctx_ids:
            self._playwright_state.open_trace_group(
                f"Auto Closing Context    {ctx_id}",  # noqa: RUF001
                None,
            )
            self._playwright_state.close_context(
                ctx_id,
                SelectionType.ALL,
                save_trace=not bool(
                    self.auto_delete_passed_tracing and status == "PASS"
                ),
            )
            self._playwright_state.close_trace_group()
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
            self._playwright_state.open_trace_group(
                f"Auto Closing Page    {page_id}",  # noqa: RUF001
                None,
            )
            self._playwright_state.close_page(
                page_id,
                ctx_id,
                runBeforeUnload=self.auto_closing_default_run_before_unload,
            )
            self._playwright_state.close_trace_group()

    def _alter_keyword_error(self, name: str, args: tuple) -> tuple:
        if not (args and isinstance(args, tuple)):
            return args
        ansi_escape = re.compile(
            r"""
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        """,
            re.VERBOSE,
        )
        clean_message = ansi_escape.sub("", args[0])
        return (clean_message,) + args[1:]

    def _set_logging(self, status: bool):
        try:
            context = BuiltIn()._context.output
        except DataError:
            context = BuiltIn()
        if status:
            if self._current_loglevel:
                context.set_log_level(self._current_loglevel)
                self._current_loglevel = None
        else:
            self._current_loglevel = context.set_log_level("NONE")

    def _show_keyword_call(self, attrs):
        try:
            if attrs["kwname"] in ["Take Screenshot", "Get Page Source"]:
                self.set_keyword_call_banner()
            else:
                args = "    ".join(attrs["args"])
                args = BuiltIn().replace_variables(args)
                content = f"{attrs['kwname']}{'    ' * bool(attrs['args'])}{args}"
                self.set_keyword_call_banner(content)
        except Exception:
            pass

    def set_keyword_call_banner(self, keyword_call=None):
        if keyword_call:
            keyword_call = keyword_call.replace("'", "\\'")
            content = KW_CALL_CONTENT_TEMPLATE.format(
                keyword_call=keyword_call,
                additional_styles=self.keyword_call_banner_add_style,
            )
        else:
            content = "body::before{}"

        with self.playwright.grpc_channel() as stub:
            stub.EvaluateJavascript(
                Request().EvaluateAll(
                    selector="",
                    script=KW_CALL_BANNER_FUNCTION,
                    arg=json.dumps(content),
                    allElements=False,
                    strict=False,
                )
            )

    def keyword_error(self):
        """Runs keyword on failure."""
        if self._running_on_failure_keyword or not self.run_on_failure_keyword.name:
            return
        self._running_on_failure_keyword = True
        varargs = self.run_on_failure_keyword.args
        kwargs = self.run_on_failure_keyword.kwargs
        try:
            if self.run_on_failure_keyword.name in self.keywords:
                if (
                    self.run_on_failure_keyword.name == "take_screenshot"
                    and not varargs
                    and "filename" not in kwargs
                ):
                    varargs = (self._failure_screenshot_path(),)
                self.keywords[self.run_on_failure_keyword.name](*varargs, **kwargs)
            else:
                BuiltIn().run_keyword(
                    self.run_on_failure_keyword.name, *varargs, **kwargs
                )
        except Exception as err:
            if "Tried to take screenshot, but no page was open." in str(
                err
            ) or re.match(r".*\.screenshot: Timeout.*exceeded.*", str(err)):
                level = logger.info
            else:
                level = logger.warn
            level(
                f"Keyword '{self.run_on_failure_keyword}' could not be run on failure:\n{err}"
            )
        finally:
            if self._playwright_log:
                logger.info(
                    f"See also {self._playwright_log.as_uri()} for additional details."
                )
            else:
                logger.info(
                    "playwright-log.txt is not created, consider enabling it for debug reasons."
                )
            self._running_on_failure_keyword = False

    def _failure_screenshot_path(self):
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        test_name = (
            BuiltIn().get_variable_value("${TEST NAME}", "GENERIC")
            if EXECUTION_CONTEXTS.current
            else ""
        )
        return str(
            Path(self.outputdir)
            / Path(
                "".join(c for c in test_name if c in valid_chars).replace(" ", "_")
                + "_FAILURE_SCREENSHOT_{index}"
            )
        )

    def get_timeout(self, timeout: Union[timedelta, None]) -> float:
        if timeout is None:
            return self.scope_stack["timeout"].get()
        return self.convert_timeout(timeout)

    def convert_timeout(
        self, timeout: Union[timedelta, float], to_ms: bool = True
    ) -> float:
        convert = 1000 if to_ms else 1
        if isinstance(timeout, timedelta):
            return timeout.total_seconds() * convert
        return timestr_to_secs(timeout) * convert

    def millisecs_to_timestr(self, timeout: float) -> str:
        return secs_to_timestr(timeout / 1000)

    @overrides
    def get_keyword_documentation(self, name):
        doc = DynamicCore.get_keyword_documentation(self, name)
        if name == "__intro__":
            doc = doc.replace("%ASSERTION_TABLE%", AssertionOperator.__doc__)
            doc = doc.replace("%AUTO_CLOSING_LEVEL%", AutoClosingLevel.__doc__)
        elif name == "set_assertion_formatters":
            doc = doc.replace('"Keyword Name"', '"Get Text"')
            doc = f"{doc}\n    | ${{value}} =    `Get Text`    //div    ==    ${{SPACE}}Expected${{SPACE * 2}}Text"
            doc = f"{doc}\n    | Should Be Equal    ${{value}}    Expected Text\n\n"
            doc = f"{doc}\n[https://forum.robotframework.org/t//4327|Comment >>]"
        return doc

    def _get_assertion_formatter(self, keyword: str) -> list:
        return self._assertion_formatter.get_formatter(keyword)

    def _get_log_file_name(self) -> Path:
        log_file = Path(self.outputdir, "playwright-log.txt")
        if not log_file.is_file():
            return log_file
        if self._unlink(log_file):
            return log_file
        name = log_file.name
        file_name, ext = name.split(".")
        name = f"{file_name}-{time.time_ns()}.{ext}"
        return Path(self.outputdir, name)

    def _unlink(self, file: Path):  # to ease unit testing
        try:
            file.unlink(missing_ok=True)
        except Exception:
            return False
        return True

    @staticmethod
    def _get_translation(language: Union[str, None]) -> Union[Path, None]:
        if not language:
            return None
        discovered_plugins = {
            name: importlib.import_module(name)
            for _, name, _ in pkgutil.iter_modules()
            if name.startswith("robotframework_browser_translation")
        }
        lang = language.lower()
        for plugin in discovered_plugins.values():
            try:
                data = plugin.get_language()
            except AttributeError:
                continue
            if isinstance(data, list):
                for item in data:
                    if item.get("language", "").lower() == lang and item.get("path"):
                        return Path(item.get("path")).absolute()
        return None
