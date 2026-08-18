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
from collections.abc import Iterator
from concurrent.futures._base import Future
from copy import copy
from datetime import timedelta
from pathlib import Path
from typing import Any, Literal

from assertionengine import AssertionOperator
from overrides import overrides
from robot.api.deco import library
from robot.errors import DataError
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn
from robot.running.arguments import PythonArgumentParser
from robot.utils import secs_to_timestr, timestr_to_secs
from robot.utils.robottypes import is_falsy
from robotlibcore import DynamicCore, PluginParser  # type: ignore

from .base import ContextCache, LibraryComponent
from .generated.playwright_pb2 import Request, Response
from .keywords import (
    Clock,
    Control,
    Cookie,
    Coverage,
    Credential,
    Devices,
    Evaluation,
    Formatter,
    Getters,
    Interaction,
    KeywordCallObserver,
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
from .python_arguments import add_argument_conversion
from .utils import (
    AutoClosingLevel,
    PlaywrightLogTypes,
    Scope,
    SettingsStack,
    get_normalized_keyword,
    keyword,
    logger,
    suppress_logging,
)

# Importing this directly from .utils break the stub type checks
from .utils.data_types import (
    DelayedKeyword,
    HighLightElement,
    KeywordCallStackEntry,
    LambdaFunction,
    RegExp,
    RobotTypeConverter,
    SelectionType,
    SupportedBrowsers,
    TracingGroupMode,
)
from .version import __version__ as VERSION


class _RFContextTracker:
    def __init__(self) -> None:
        self._suite_stack: list[tuple[str, str]] = []
        self._test_id: str = ""
        self._test_name: str = ""

    def start_suite(self, suite_id: str, suite_name: str) -> None:
        self._suite_stack.append((suite_id, suite_name))

    def end_suite(self) -> None:
        if self._suite_stack:
            self._suite_stack.pop()

    def start_test(self, test_id: str, test_name: str) -> None:
        self._test_id = test_id
        self._test_name = test_name

    def end_test(self) -> None:
        self._test_id = ""
        self._test_name = ""

    def context(self) -> dict:
        if self._suite_stack:
            suite_id, suite_name = self._suite_stack[-1]
        else:
            suite_id, suite_name = "", ""
        return {
            "suite_id": suite_id,
            "suite_name": suite_name,
            "test_id": self._test_id,
            "test_name": self._test_name,
        }


@library(
    converters={RegExp: RegExp.from_string, LambdaFunction: LambdaFunction.from_string}
)
class Browser(DynamicCore):
    """Browser library is a browser automation library for Robot Framework.

    This is the keyword documentation for Browser library. For installation,
    guides and everything else, see
    [https://robotframework-browser.org|robotframework-browser.org].
    For more information about Robot Framework itself, see [https://robotframework.org|robotframework.org].

    Browser library uses
    [https://github.com/microsoft/playwright|Playwright Node module]
    to automate [https://www.chromium.org/Home|Chromium],
    [https://www.mozilla.org/en-US/firefox/new/|Firefox]
    and [https://webkit.org/|WebKit] with a single library.


    == Table of contents ==

    %TOC%

    = Browser, Context and Page =

    Browser library works in three layers that build on each other.

    | = Layer =     | = Is =                                                        | = Opened with =  |
    | *Browser*     | A browser process: ``chromium``, ``firefox`` or ``webkit``.    | `New Browser`    |
    | *Context*     | An isolated session in that process: its own cookies, storage and permissions. Contexts share nothing with each other. | `New Context` |
    | *Page*        | A tab, with its own content and history. Selectors resolve here. | `New Page`      |

    Playwright brings its own browser binaries, so no separate driver is needed.
    A browser starts ``headless`` unless `New Browser`'s ``headless`` argument is set to ``False``.

    | = Engine =    | = Ships in =                                       |
    | ``chromium``  | Google Chrome, Microsoft Edge, Opera               |
    | ``firefox``   | Mozilla Firefox                                    |
    | ``webkit``    | Safari on macOS and iOS                            |

    The layers fill themselves in downwards: `New Page` with nothing open starts a
    browser and a context first, using defaults. `Open Browser` opens all three at
    once and is meant for experiments and debugging rather than for suites.

    A context is the cheap unit of isolation — opening one is roughly a thousand
    times cheaper than starting a browser, so a clean session per test does not
    mean a new process. Context-level settings include ``viewport``,
    ``geolocation``, ``locale``, ``colorScheme`` and ``httpCredentials``;
    downloads are accepted unless ``acceptDownloads=False`` is given.

    Each browser, context and page has an id. `Get Browser Catalog` returns
    everything currently open.

    Which layer to open for which job, and the cost of each:
    https://robotframework-browser.org/docs/concepts/browser-context-page

    = Automatic page and context closing =

    %AUTO_CLOSING_LEVEL%

    = Finding elements =

    Keywords that act on an element take a ``selector`` argument. A selector is
    one or more clauses, each naming a strategy, chained with ``>>``.

    Under strict mode a selector matching more than one element fails the keyword.
    It is on by default, changeable in the library `importing` or with
    `Set Strict Mode`, and each keyword's documentation states whether it applies.

    == Strategies ==

    | = Strategy =     | = Matches on =                               | = Example =                        |
    | ``role``         | ARIA role, with optional accessible name.    | ``role=button[name="Login"]``      |
    | ``data-testid``  | ``data-testid`` attribute.                   | ``data-testid=login``              |
    | ``text``         | Text content. See `Text matching`.           | ``text=Login``                     |
    | ``id``           | Element ID attribute.                        | ``id=login_btn``                   |
    | ``css``          | CSS selector.                                | ``css=.class > \\#login_btn``      |
    | ``xpath``        | XPath expression.                            | ``xpath=//input[@id="login_btn"]`` |
    | ``data-test-id`` | ``data-test-id`` attribute.                  | ``data-test-id=login``             |
    | ``data-test``    | ``data-test`` attribute.                     | ``data-test=login``                |
    | ``css:light``    | As ``css``, but does not pierce shadow DOM.  | ``css:light=.class``               |

    An attribute engine is equivalent to the matching css attribute selector:
    ``data-test-id=foo`` is ``css=[data-test-id="foo"]``.

    ``css:light`` is the only non-piercing engine still supported.
    All other locator, except ``xpath``, pierce shadow DOM automatically.

    Two filters narrow what a clause already matched. Filter order changes the
    result.

    | = Filter =  | = Selects =                                           | = Example =                    |
    | ``nth``     | The nth match, zero based. ``0`` first, ``-1`` last.  | ``css=button >> nth=1``        |
    | ``visible`` | Only visible, or only hidden, matches.                | ``css=button >> visible=true`` |

    Playwright's CSS pseudo-classes (``:has()``, ``:has-text()``,
    ``:nth-match()``) and its layout selectors (``:right-of()``, ``:below()``)
    are available inside a ``css`` clause. Which strategy to prefer, and the full
    list with examples:
    https://robotframework-browser.org/docs/concepts/selectors

    == Explicit and implicit strategy ==

    A strategy is named with a ``strategy=value`` prefix. Spaces around the
    separator are ignored, so ``css=foo``, ``css= foo`` and ``css = foo`` are the
    same.

    Without a prefix the strategy is inferred:

    | = Selector starts with = | = Read as = | = Example =                             |
    | ``//`` or ``..``         | ``xpath``   | ``//span/button`` is ``xpath=//span/button`` |
    | ``"`` or ``'``           | ``text``, exact | ``"Login"`` is ``text="Login"``     |
    | anything else            | ``css``     | ``span > button`` is ``css=span > button``   |

    Because ``#`` starts a comment in Robot Framework data, an id selector must be
    escaped as ``\\#id``.

    ``css`` follows the
    [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors|CSS selector]
    specification and ``xpath`` the
    [https://developer.mozilla.org/en-US/docs/Web/XPath|XPath] specification;
    neither is re-documented here.

    == Text matching ==

    The ``text`` engine matches a text node, and the value of ``button`` and
    ``submit`` inputs. In keywords that insert text it also matches a field by its
    label.

    | = Form =             | = Matches =                                                              |
    | ``text=Login``       | Substring, case-insensitive, leading and trailing whitespace ignored.    |
    | ``text="Login "``    | Exact: case, whitespace and all. Escape a quote as ``\\"``.              |
    | ``text=/^Hi .*!$/i`` | JavaScript-style [https://regex101.com/|regular expression] with flags: e.g. ``i`` for case-insensitive. |

    == Chaining ==

    Clauses are separated by ``>>`` and each searches inside the result of the
    previous one. The chain returns what the last clause matched; prefix a clause
    with ``*`` to return that one instead. A value containing ``>>`` must be
    quoted, as in ``text="some >> text"``.

    | Click    css=.checkout >> text=Confirm
    | Get Element    *css=article >> text=Hello    # returns the article

    == iFrames ==

    A chain does not cross a frame boundary. ``>>>`` combines a selector for the
    frame element with a selector inside it; the clause immediately before ``>>>``
    must select the frame itself.

    | Click    id=iframe >>> id=btn

    For several keywords inside one frame, set a prefix with `Set Selector Prefix`.

    == Shadow DOM ==

    All engines, except ``css:light`` and ``xpath``, pierce open shadow roots automatically:
    every descendant combinator, including the implicit one at the start of a
    selector, crosses any number of them. Light DOM is searched first, then open
    shadow roots, in document order. Closed shadow roots and iframes are never
    entered.

    Use ``css:light`` to stop at the shadow boundary. Worked examples of what
    each matches:
    https://robotframework-browser.org/docs/concepts/selectors

    == Element references ==

    `Get Element` returns a *selector string* for what it matched, and
    `Get Elements` returns a list of them. They are ordinary selectors, so they go
    in the *first* clause of another selector, chained with ``>>``:

    | ${ref}=    Get Element    .some_class
    |            Click          ${ref} >> .some_child
    |            Click          ${ref} >> .other_child

    Clauses after the reference are relative to it. Because the value is a
    selector rather than a captured DOM node, it is resolved from the page again
    on every use. A reference works like any other first clause, ``>>>`` included:
    if it points at an iframe, ``${ref} >>> h1`` crosses into it.

    = Assertions =

    Keywords taking ``assertion_operator`` <`AssertionOperator`> and
    ``assertion_expected`` can assert on the value they return, and still return
    it. An assertion retries until it passes or ``retry_assertions_for`` expires;
    see `Importing` for that setting, which defaults to 1 second.

    %ASSERTION_TABLE%

    Expected values are generally used as given, so they must already have the type
    returned by the keyword. Keywords returning numbers are an exception and convert the expected value.

    Examples:
    - `Get Text` returns a string even when it looks like a number
    - `Get Element Count` returns an integer.
    - `Get BoundingBox` and `Get Viewport Size` return a dictionary unfiltered and a number when a key is selected.

    Comparing strings with ``<`` or ``>`` compares code points character by
    character and stops at the first difference; length is never considered.
    Example: ``A < Z``, ``Z < a``, ``ac < dc``, ``'abcde' < 'abd'``.

    ``validate`` takes a Python expression over ``value``. ``then`` and
    ``evaluate`` do not assert: they return the result of an expression over
    ``value``.

    | Get Text             h1      validate    value.startswith("Welcome")
    | ${id}=    Get Property    a#link    href    then    value.split("/")[-1]

    A failing assertion has a default message, replaceable with ``message``. It
    accepts the
    [https://docs.python.org/3/library/stdtypes.html#str.format|format] fields
    ``{value}``, ``{expected}``, ``{value_type}`` and ``{expected_type}``.

    What each operator is for, why a type mismatch is the usual failure, and the
    formatters that normalise a value before comparison:
    https://robotframework-browser.org/docs/concepts/assertions

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

    The Node.js side can be started as a standalone process and shared by every
    Browser library running on the same machine, instead of each one starting its
    own. This can speed up parallel runs. Start it from the directory where the
    Browser package is installed with
    ```
    PLAYWRIGHT_BROWSERS_PATH=0 node Browser/wrapper/index.js HOST PORT
    ```
    , for example ``... index.js 127.0.0.1 12345``. Both arguments are required: the
    script reads the host first and exits with ``No port defined`` if only one is
    given. Point runs at it
    with the ``playwright_process_port`` import parameter or the
    ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT`` environment variable, for example
    ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT=PORT pabot ..``.

    What this costs, how to run it under Pabot, and how to pass Node flags such as
    ``--inspect``:
    https://robotframework-browser.org/docs/operations/node-process

    = Scope Setting =

    Some keywords which manipulates library settings have a scope argument.
    With that scope argument one can set the "live time" of that setting.
    Available Scopes are: ``Global``, ``Suite`` and ``Test``/`Task`
    See `Scope`.
    Is a scope finished, this scoped setting, like timeout, will no longer be used.

    Live Times:
    - A ``Global`` scope will live forever until it is overwritten by another ``Global`` scope. Or locally temporarily overridden by a more narrow scope.
    - A ``Suite`` scope will locally override the ``Global`` scope and live until the end of the Suite within it is set, or if it is overwritten by a later setting with ``Global`` or same scope. Children suite does inherit the setting from the parent suite but also may have its own local ``Suite`` setting that then will be inherited to its children suites.
    - A ``Test`` or `Task` scope will be inherited from its parent suite but when set, lives until the end of that particular test or task.

    A new set higher order scope will always remove the lower order scope which may be in charge.
    So the setting of a ``Suite`` scope from a test, will set that scope to the robot file suite where that test is and removes the ``Test`` scope that may have been in place.

    = Language =

    Keyword names and their documentation can be translated. Install a Python
    package whose name starts with ``robotframework_browser_translation`` and set
    the ``language`` import parameter to the language that the package declares;
    Browser discovers it on the module search path through the Python plugin API.

    A template for a new translation, containing every keyword in the correct
    format, is produced by ``rfbrowser translation /path/to/translation.json``.
    Keywords coming from library plugins and JavaScript extensions can be included
    with the ``--plugings`` and ``--jsextension`` arguments.

    Writing and packaging a translation:
    https://robotframework-browser.org/docs/extending/translations

    = ENVIRONMENT VARIABLES =

    These environment variables modify the behaviour of the library. Two of them are
    development features and must not be set in production; they are listed here so
    that nobody uses them by accident.

    | =Environment variable=                         | =Description= |
    | ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT``          | Port number for connecting to an existing node process. This is an alternative to ``playwright_process_port`` import argument. |
    | ``ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE``      | If set to ``1``, will collect code coverage for the node process. This must not be used in production environments and is not supported on Windows. |
    | ``ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS`` | Debug options for the node process. This is a comma-separated list of arguments, for example ``--inspect``. This must not be used in production environments. |

    Which of these to prefer over an import parameter, and how they behave with
    BrowserBatteries:
    https://robotframework-browser.org/docs/operations/environment-variables
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
        enable_playwright_debug: PlaywrightLogTypes | bool = PlaywrightLogTypes.library,
        enable_presenter_mode: HighLightElement | bool = False,
        external_browser_executable: dict[SupportedBrowsers, str] | None = None,
        highlight_on_failure: bool = False,
        jsextension: list[str] | str | None = None,
        language: str | None = None,
        playwright_process_host: str | None = None,
        playwright_process_port: int | None = None,
        plugins: list[str] | str | None = None,
        retry_assertions_for: timedelta = timedelta(seconds=1),
        run_on_failure: str = "Take Screenshot  fail-screenshot-{index}",
        selector_prefix: str | None = None,
        show_keyword_call_banner: bool | None = None,
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
        | ``highlight_on_failure``          | If set to ``True``, will highlight the element in the screenshot when a keyword fails, by highlighting the selector used in the failed keyword. If set to ``False``, will not highlight the element. |
        | ``jsextension``                   | Path to JavaScript modules exposed as extra keywords. The modules must be in CommonJS format; exported functions become keywords and an ``fn.rfdoc`` string becomes a keyword's documentation. The argument names ``page``, ``context``, ``browser``, ``logger`` and ``playwright`` are filled in by the library rather than taken from the keyword call. Can be a single path, a comma-separated list of paths or a real list of strings. See https://robotframework-browser.org/docs/extending/javascript-extensions |
        | ``language``                      | Defines language which is used to translate keyword names and documentation. |
        | ``playwright_process_host``       | Hostname / Host address which should be used when spawning the Playwright process. Defaults to 127.0.0.1. |
        | ``playwright_process_port``       | Experimental reusing of playwright process. ``playwright_process_port`` is preferred over environment variable ``ROBOT_FRAMEWORK_BROWSER_NODE_PORT``. See `Experimental: Re-using same node process` for more details. |
        | ``plugins``                       | Allows extending the Browser library with external Python classes, which can add keywords and modify some internal behaviour without forking the library. Can be a single class/module, a comma-separated list or a real list of strings. See https://robotframework-browser.org/docs/extending/python-plugins |
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
        self.current_test_id: str | None = None
        self._rf_context = _RFContextTracker()
        self._playwright_state: PlaywrightState = PlaywrightState(self)
        self._browser_control = Control(self)
        self._assertion_formatter = Formatter(self)
        self._keyword_call = KeywordCallObserver(self)
        libraries = [
            self._playwright_state,
            self._browser_control,
            Cookie(self),
            Clock(self),
            Credential(self),
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
        self.playwright_process_host = playwright_process_host
        self.playwright_process_port = playwright_process_port
        if self.enable_playwright_debug is True:
            self.enable_playwright_debug = PlaywrightLogTypes.playwright
        elif self.enable_playwright_debug is False:
            self.enable_playwright_debug = PlaywrightLogTypes.library
        if self.enable_playwright_debug == PlaywrightLogTypes.disabled:
            self._playwright_log = None
        else:
            self._playwright_log = self._get_log_file_name()
        self._playwright: Playwright | None = None
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
        self.presenter_mode = enable_presenter_mode
        self.tracing_group_mode = tracing_group_mode
        self._execution_stack: list[dict] = []
        self._running_on_failure_keyword = False
        self.pause_on_failure: set[str] = set()
        self._unresolved_promises: set[Future] = set()
        self._keyword_formatters: dict = {}
        self.is_test_case_running = False
        self.auto_closing_default_run_before_unload: bool = False
        self.keyword_call_stack: list[KeywordCallStackEntry] = []
        self.tracing_contexts: list[str] = []

        translation_file = self._get_translation(language)
        DynamicCore.__init__(self, libraries, translation_file)
        add_argument_conversion(self)

        self.scope_stack["timeout"] = SettingsStack(
            self.convert_timeout(timeout),
            self,
            lambda time_out: self._browser_control.set_playwright_timeout(
                time_out, loglevel="TRACE"
            ),
        )
        self.scope_stack["retry_assertions_for"] = SettingsStack(
            self.convert_timeout(retry_assertions_for), self
        )
        self.scope_stack["strict_mode"] = SettingsStack(strict, self)
        self.scope_stack["selector_prefix"] = SettingsStack(selector_prefix, self)
        self.scope_stack["run_on_failure"] = SettingsStack(
            self._parse_run_on_failure_keyword(run_on_failure), self
        )
        self.scope_stack["highlight_on_failure"] = SettingsStack(
            highlight_on_failure, self
        )
        self.scope_stack["show_keyword_call_banner"] = SettingsStack(
            show_keyword_call_banner, self
        )
        self.scope_stack["keyword_call_banner_add_style"] = SettingsStack("", self)
        self.scope_stack["assertion_formatter"] = SettingsStack({}, self)

    @property
    def presenter_mode(self) -> HighLightElement | bool:
        return copy(self._presenter_mode)

    @presenter_mode.setter
    def presenter_mode(self, value: HighLightElement | bool):
        if not isinstance(value, (bool, dict)):
            raise ValueError(
                f"'Presenter Mode' got value {value!r} ({type(value).__name__}) that cannot be converted to HighLightElement or boolean."
            )
        if isinstance(value, bool):
            if not value:
                self._presenter_mode = False
                return
            value = {}
        duration = value.get("duration", timedelta(seconds=2))
        width = value.get("width", "2px")
        style = value.get("style", "dotted")
        color = value.get("color", "blue")
        self._presenter_mode = RobotTypeConverter.converter_for(
            HighLightElement
        ).convert(
            {"duration": duration, "width": width, "style": style, "color": color},
            name="presenter_mode",
            kind="Field",
        )

    @property
    def playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = Playwright(
                self,
                self.enable_playwright_debug,
                self.playwright_process_host,
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
    def highlight_on_failure(self) -> bool:
        return self.scope_stack["highlight_on_failure"].get()

    @property
    def timeout(self):
        return self.scope_stack["timeout"].get()

    def _parse_run_on_failure_keyword(self, keyword: str | None) -> DelayedKeyword:
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
            strict=False,
        ):
            self._jskeyword_call(component, name, args, doc)
        return component

    def init_js_extension(self, js_extension_path: Path | str) -> Response.Keywords:
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
        body_parts: list[str] = []
        last_json = ""
        for response in responses:
            logger.info(response.log)
            if response.bodyPart:
                body_parts.append(response.bodyPart)
            if response.json:
                last_json = response.json
        if body_parts:
            body = "".join(body_parts)
            return json.loads(body)
        if not last_json:
            return
        return json.loads(last_json)
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
            body_parts: list[str] = []
            last_json = ""
            for response in responses:
                logger.info(response.log)
                if response.bodyPart:
                    body_parts.append(response.bodyPart)
                if response.json:
                    last_json = response.json
            if body_parts:
                body = "".join(body_parts)
                return json.loads(body)
            if not last_json:
                return None
            return json.loads(last_json)

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

    def _start_suite(self, name, attrs):
        self.suite_ids[attrs["id"]] = None
        self._add_to_scope_stack(attrs["id"], Scope.Suite)
        self._rf_context.start_suite(attrs["id"], attrs.get("longname", name))
        self._playwright_state.set_rf_context(**self._rf_context.context())
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
                    logger.trace(f"Removing: {path}")
                    shutil.rmtree(str(path), ignore_errors=True)
        if self._auto_closing_level in [AutoClosingLevel.TEST, AutoClosingLevel.SUITE]:
            try:
                self._execution_stack.append(
                    []  # type: ignore
                    if self._playwright is None
                    else self._playwright_state._get_browser_catalog()
                )
            except ConnectionError as e:
                logger.trace(f"Browser._start_suite connection problem: {e}")

    def _start_test(self, name, attrs):
        self.current_test_id = attrs["id"]
        self._add_to_scope_stack(attrs["id"], Scope.Test)
        self.is_test_case_running = True
        self._rf_context.start_test(attrs["id"], attrs.get("longname", name))
        self._playwright_state.set_rf_context(**self._rf_context.context())
        if self._auto_closing_level == AutoClosingLevel.TEST:
            try:
                self._execution_stack.append(
                    []  # type: ignore
                    if self._playwright is None
                    else self._playwright_state._get_browser_catalog()
                )
            except ConnectionError as e:
                logger.trace(f"Browser._start_test connection problem: {e}")

    def _resolve_path(self, attrs: dict) -> Path | None:
        source = (
            Path(attrs["source"])
            if "source" in attrs and attrs["source"] is not None
            else None
        )
        if source is not None and source.is_dir():
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
            kwname=attrs["kwname"],
        )
        self.keyword_call_stack.append(kw_call_stack_entry)
        if self.tracing_group_mode == TracingGroupMode.Full:
            self._playwright_state.open_trace_group(
                **self._trace_group_arguments(kw_call_stack_entry)
            )
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
        source: str | Path | None,
        lineno: int,
        typ: str,
        *,
        kwname: str = "",
    ) -> KeywordCallStackEntry:
        if typ not in ["SETUP", "KEYWORD", "TEARDOWN"]:
            args = [name] if name else []
            name = typ
            kwname = typ
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
            "kwname": kwname,
            "args": list(args),
        }

    @staticmethod
    def _trace_group_arguments(entry: KeywordCallStackEntry) -> dict[str, Any]:
        return {"name": entry["name"], "file": entry["file"], "line": entry["line"]}

    def run_keyword(self, name, args, kwargs=None):
        is_secret_keyword = self._keyword_call.is_secret_keyword(name)
        try:
            if is_secret_keyword:
                self._keyword_call.suppress_logging()
            self._keyword_call.show(name)
            if (
                self.tracing_group_mode == TracingGroupMode.Browser
                and self.keyword_call_stack
            ):
                self._playwright_state.open_trace_group(
                    **self._trace_group_arguments(self.keyword_call_stack[-1])
                )
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except (AssertionError, AttributeError) as e:
            selector = self._get_selector_value_from_keyword_call(name, args, kwargs)
            self.keyword_error(selector)
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
            if is_secret_keyword:
                self._keyword_call.restore_logging()

    def _get_selector_value_from_keyword_call(self, name, args, kwargs):
        selector = kwargs.get("selector")
        if not selector and args:
            arguments = self.get_keyword_arguments(name)
            for i, arg in enumerate(args):
                if isinstance(arg, str) and arg.startswith("*"):
                    break
                if (
                    isinstance(arguments[i], str)
                    and arguments[i].startswith("selector")
                ) or (
                    isinstance(arguments[i], tuple)
                    and arguments[i][0].startswith("selector")
                ):
                    selector = arg
                    break
        return selector

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

    def _end_test(self, name, attrs):
        self._remove_from_scope_stack(attrs["id"])
        self.current_test_id = None
        self.is_test_case_running = False
        self._rf_context.end_test()
        self._playwright_state.set_rf_context(**self._rf_context.context())
        if len(self._unresolved_promises) > 0:
            logger.warn(f"Waiting unresolved promises at the end of test '{name}'")
            self.wait_for_all_promises()
        if self._auto_closing_level == AutoClosingLevel.TEST:
            if self.presenter_mode:
                logger.trace("Presenter mode: Wait for 5 seconds before pruning pages")
                time.sleep(5.0)
            self.execute_auto_closing(name, attrs, "Test", attrs["status"])

    def _end_suite(self, name, attrs):
        self._remove_from_scope_stack(attrs["id"])
        self.suite_ids.pop(attrs["id"], None)
        self._rf_context.end_suite()
        self._playwright_state.set_rf_context(**self._rf_context.context())
        if self._auto_closing_level in [AutoClosingLevel.TEST, AutoClosingLevel.SUITE]:
            self.execute_auto_closing(name, attrs, "Suite", attrs["status"])

    def _close(self):
        if self.auto_delete_passed_tracing and self.traces_temp.is_dir():
            shutil.rmtree(str(self.traces_temp), ignore_errors=True)

    def execute_auto_closing(
        self, name: str, attrs: dict, typ: Literal["Test", "Suite"], status: str
    ):
        if len(self._execution_stack) == 0:
            logger.trace(f"Browser._end_{typ.lower()} empty execution stack")
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
            logger.trace(f"{typ}: {name}, End {typ}: {e}")
        except ConnectionError as e:
            logger.trace(f"Browser._end_{typ.lower()} connection problem: {e}")

    def _add_to_scope_stack(self, scope_id: str, scope: Scope):
        for stack in self.scope_stack.values():
            stack.start(scope_id, scope)

    def _remove_from_scope_stack(self, scope_id):
        for stack in self.scope_stack.values():
            stack.end(scope_id)

    def _prune_execution_stack(self, catalog_before: dict, status: str) -> None:
        catalog_after = self._playwright_state._get_browser_catalog()
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
        return (clean_message, *args[1:])

    def keyword_error(self, selector):
        """Runs keyword on failure."""
        if self._running_on_failure_keyword or not self.run_on_failure_keyword.name:
            return
        self._running_on_failure_keyword = True
        varargs = self.run_on_failure_keyword.args
        kwargs = self.run_on_failure_keyword.kwargs
        try:
            if selector and self.highlight_on_failure:
                with suppress_logging():
                    BuiltIn()._variables.set_suite(
                        "${ROBOT_FRAMEWORK_BROWSER_FAILING_SELECTOR}",
                        selector,
                        children=False,
                    )
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
            if selector and self.highlight_on_failure:
                with suppress_logging():
                    BuiltIn()._variables.set_suite(
                        "${ROBOT_FRAMEWORK_BROWSER_FAILING_SELECTOR}",
                        None,
                        children=False,
                    )

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

    def get_timeout(self, timeout: timedelta | None) -> float:
        if timeout is None:
            return self.scope_stack["timeout"].get()
        return self.convert_timeout(timeout)

    def convert_timeout(self, timeout: timedelta | float, to_ms: bool = True) -> float:
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
    def _iter_module_names() -> Iterator[str]:
        for importer in pkgutil.iter_importers():
            # A Windows console script such as ``robot.exe`` is a zip archive on sys.path.
            # Which may fail, therefore own wrapper.
            try:
                modules = list(pkgutil.iter_importer_modules(importer))
            except KeyError as error:
                logger.debug(f"Could not list modules of {importer}: {error}")
                continue
            for name, _ in modules:
                yield name

    @staticmethod
    def _get_translation(language: str | None) -> Path | None:
        if not language:
            return None
        discovered_plugins = {
            name: importlib.import_module(name)
            for name in Browser._iter_module_names()
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

    def execute_npx_playwright(
        self,
        command: str,
        *args: str,
    ):
        self._browser_control.execute_npx_playwright(command, *args)
