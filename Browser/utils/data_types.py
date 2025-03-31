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
import re
from datetime import timedelta
from enum import Enum, IntFlag, auto
from typing import Dict, Optional, TypedDict, Union  # noqa: UP035

from robot.running.arguments.typeconverters import TypeConverter


class RobotTypeConverter(TypeConverter):
    @classmethod
    def converter_for(cls, arg_type):
        if arg_type is None:
            return None
        try:
            from robot.api import TypeInfo

            if not isinstance(arg_type, TypeInfo):
                type_hint = TypeInfo.from_type_hint(arg_type)
        except ImportError:
            type_hint = arg_type
        return TypeConverter.converter_for(type_hint)


class TypedDictDummy(TypedDict):
    pass


def convert_typed_dict(function_annotations: dict, params: dict) -> dict:  # noqa: C901
    for arg_name, arg_type in function_annotations.items():
        if arg_name not in params or params[arg_name] is None:
            continue
        arg_value = params[arg_name]
        if getattr(arg_type, "__origin__", None) is Union:
            for union_type in arg_type.__args__:
                if arg_value is None or not isinstance(
                    union_type, type(TypedDictDummy)
                ):
                    continue
                arg_type = union_type  # noqa: PLW2901
                break
        if isinstance(arg_type, type(TypedDictDummy)):
            if not isinstance(arg_value, dict):
                raise TypeError(
                    f"Argument '{arg_name}' expects a dictionary like object but did get '{type(arg_value)} instead.'"
                )
            lower_case_dict = {k.lower(): v for k, v in arg_value.items()}
            struct = arg_type.__annotations__
            typed_dict = arg_type()
            for req_key in arg_type.__required_keys__:
                if req_key.lower() not in lower_case_dict:
                    raise RuntimeError(
                        f"`{lower_case_dict}` cannot be converted to {arg_type.__name__} for argument '{arg_name}'."
                        f"\nThe required key '{req_key}' in not set in given value."
                        f"\nExpected types: {arg_type.__annotations__}"
                    )
                typed_dict[req_key] = struct[req_key](lower_case_dict[req_key.lower()])  # type: ignore
            for opt_key in arg_type.__optional_keys__:
                if opt_key.lower() not in lower_case_dict:
                    continue
                typed_dict[opt_key] = struct[opt_key](lower_case_dict[opt_key.lower()])  # type: ignore
            params[arg_name] = typed_dict
    return params


class Deprecated:
    def __str__(self) -> str:
        return ""


deprecated = Deprecated()


class NotSet(Enum):
    """Defines a value that is not set.

    This is used to differentiate between a value that is set to None and
    a value that is not set at all. Example `ForcedColors` has an options
    active, none and null. If user does not not want to give any of
    the `ForcedColors` options, user can use `not_set` value. Then keyword
    will not define `ForcedColors` option at all when underlying Playwright
    method(s) is called.
    """

    not_set = "not_set"


class KeywordCallStackEntry(TypedDict):
    """Information about the keyword call stack."""

    name: str
    file: str
    line: int


class SelectOptions(TypedDict):
    """Dictionary with the following keys and their values
    "index", "value", "label" and "selected".

    | =Keys= | =Description= |
    | ``index`` | 0 based index of the option. |
    | ``value`` | Value attribute of the option. |
    | ``label`` | Label/Text of the option. |
    | ``selected`` | Boolean if the option is selected. |
    """

    index: int
    value: str
    label: str
    selected: bool


class SelectionStrategy(Enum):
    """SelectionStrategy to be used. Refers to Playwrights ``page.getBy***`` functions. See [https://playwright.dev/docs/locators|Playwright Locators]

    == AltText ==
    All images should have an alt attribute that describes the image. You can locate an image based on the text alternative using page.getByAltText().

    For example, consider the following DOM structure.
    | <img alt="playwright logo" src="/img/playwright-logo.svg" width="100" />

    == Label ==
    Allows locating input elements by the text of the associated ``<label>`` or ``aria-labelledby`` element, or by the ``aria-label`` attribute.

    For example, this method will find inputs by label "Username" and "Password" in the following DOM:

    | <input aria-label="Username">
    | <label for="password-input">Password:</label>
    | <input id="password-input">

    == Placeholder ==
    Allows locating input elements by the placeholder text.

    Example:
    | <input type="email" placeholder="name@example.com" />

    == TestId ==
    Locate element by the test id.

    Currently only the exact attribute ``data-testid`` is supported.

    Example:
    | <button data-testid="directions">Itinéraire</button>

    == Text ==
    Allows locating elements that contain given text.

    Matching by text always normalizes whitespace, even with exact match.
    For example, it turns multiple spaces into one, turns line breaks into spaces and ignores leading and trailing whitespace.
    Input elements of the type button and submit are matched by their value instead of the text content.
    For example, locating by text "Log in" matches <input type=button value="Log in">.

    == Title ==
    Allows locating elements by their title attribute.

    Example:
    | <img alt="playwright logo" src="/img/playwright-logo.svg" title="Playwright" width="100" />
    """

    AltText = "AltText"
    Label = "Label"
    Placeholder = "Placeholder"
    TestID = "TestId"
    Text = "Text"
    Title = "Title"


class RegExp(str):
    @classmethod
    def from_string(cls, string: str) -> "RegExp":
        """Create a (JavaScript) RegExp object from a string.

        The matcher must start with a slash and end with a slash and can be followed by flags.

        Example: ``/hello world/gi``
        Which is equivalent to ``new RegExp("hello world", "gi")`` in JavaScript.

        Following flags are supported:
        | =Flag= | =Description= |
        | g | Global search. |
        | i | Case-insensitive search. |
        | m | Allows ``^`` and ``$`` to match newline characters. |
        | s | Allows ``.`` to match newline characters. |
        | u | "unicode"; treat a pattern as a sequence of unicode code points. |
        | y | Perform a "sticky" search that matches starting at the current position in the target string. |

        See [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp|RegExp Object]
        and [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions|RegExp Guide] for more information.
        """
        match = re.fullmatch(r"\/(?<matcher>.*)\/(?<flags>[gimsuy]+)?", string)
        if not match:
            raise ValueError("Invalid JavaScript RegExp string")
        return cls(string)


class ElementRole(Enum):
    """Role selector does not replace accessibility audits and conformance tests,
    but rather gives early feedback about the ARIA guidelines.

    Many html elements have an implicitly
    [https://w3c.github.io/html-aam/#html-element-role-mappings|defined role]
    that is recognized by the role selector.
    You can find all the [https://www.w3.org/TR/wai-aria-1.2/#role_definitions|supported roles] here.
    ARIA guidelines do not recommend duplicating implicit roles and attributes
    by setting role and/or aria-* attributes to default values."""

    ALERT = auto()
    ALERTDIALOG = auto()
    APPLICATION = auto()
    ARTICLE = auto()
    BANNER = auto()
    BLOCKQUOTE = auto()
    BUTTON = auto()
    CAPTION = auto()
    CELL = auto()
    CHECKBOX = auto()
    CODE = auto()
    COLUMNHEADER = auto()
    COMBOBOX = auto()
    COMPLEMENTARY = auto()
    CONTENTINFO = auto()
    DEFINITION = auto()
    DELETION = auto()
    DIALOG = auto()
    DIRECTORY = auto()
    DOCUMENT = auto()
    EMPHASIS = auto()
    FEED = auto()
    FIGURE = auto()
    FORM = auto()
    GENERIC = auto()
    GRID = auto()
    GRIDCELL = auto()
    GROUP = auto()
    HEADING = auto()
    IMG = auto()
    INSERTION = auto()
    LINK = auto()
    LIST = auto()
    LISTBOX = auto()
    LISTITEM = auto()
    LOG = auto()
    MAIN = auto()
    MARQUEE = auto()
    MATH = auto()
    METER = auto()
    MENU = auto()
    MENUBAR = auto()
    MENUITEM = auto()
    MENUITEMCHECKBOX = auto()
    MENUITEMRADIO = auto()
    NAVIGATION = auto()
    NONE = auto()
    NOTE = auto()
    OPTION = auto()
    PARAGRAPH = auto()
    PRESENTATION = auto()
    PROGRESSBAR = auto()
    RADIO = auto()
    RADIOGROUP = auto()
    REGION = auto()
    ROW = auto()
    ROWGROUP = auto()
    ROWHEADER = auto()
    SCROLLBAR = auto()
    SEARCH = auto()
    SEARCHBOX = auto()
    SEPARATOR = auto()
    SLIDER = auto()
    SPINBUTTON = auto()
    STATUS = auto()
    STRONG = auto()
    SUBSCRIPT = auto()
    SUPERSCRIPT = auto()
    SWITCH = auto()
    TAB = auto()
    TABLE = auto()
    TABLIST = auto()
    TABPANEL = auto()
    TERM = auto()
    TEXTBOX = auto()
    TIME = auto()
    TIMER = auto()
    TOOLBAR = auto()
    TOOLTIP = auto()
    TREE = auto()
    TREEGRID = auto()
    TREEITEM = auto()


class DelayedKeyword:
    def __init__(
        self,
        name: Union[str, None],
        original_name: Union[str, None],
        args: tuple,
        kwargs: dict,
    ):
        self.name = name
        self.original_name = original_name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        args = [str(arg) for arg in self.args]
        kwargs = [f"{key}={value}" for key, value in self.kwargs.items()]
        return f"{self.original_name}  {'  '.join(args)}  {'  '.join(kwargs)}".strip()


class BoundingBox(TypedDict, total=False):
    """Bounding box of an element.

    | =Key= | =Description= |
    | ``x`` | The amount of pixel between the left border of the page and the left border of the element. |
    | ``y`` | The amount of pixel between the top border of the page and the top border of the element. |
    | ``width`` | The width of the element, excluding margins. |
    | ``height`` | The height of the element, excluding margins. |
    """

    x: float
    y: float
    width: float
    height: float


class Coordinates(TypedDict, total=False):
    """Coordinates of an element.

    | =Key= | =Description= |
    | ``x`` | The amount of pixel between the left border of the page and the left border of the element. |
    | ``y`` | The amount of pixel between the top border of the page and the top border of the element. |
    """

    x: float
    y: float


class MouseOptionsDict(TypedDict, total=False):
    x: float
    y: float
    options: dict


class ViewportDimensions(TypedDict):
    """Viewport dimensions.

    Viewport is the browsers inner window size that is used to display the page.

    | =Key= | =Description= |
    | ``width`` | page width in pixels. |
    | ``height`` | page height in pixels. |
    """

    width: int
    height: int


class Dimensions(ViewportDimensions):
    """Dimensions of an object in pixels."""


class RecordVideo(TypedDict, total=False):
    """Enables Video recording

    Examples:
    |  New Context  recordVideo={'dir':'videos', 'size':{'width':400, 'height':200}}
    |  New Context  recordVideo={'dir': 'd:/automation/video'}
    """

    dir: str
    size: ViewportDimensions


class RecordHar(TypedDict, total=False):
    """Enables HAR recording for all pages into to a file.

    If not specified, the HAR is not recorded. Make sure to await context to close for the
    [http://www.softwareishard.com/blog/har-12-spec/|HAR] to be saved.

    `omitContent`: Optional setting to control whether to omit request content
    from the HAR. Default is False

    `path`: Path on the filesystem to write the HAR file to.

    Example:
    | ${har} =    Create Dictionary     path=/path/to/har.file    omitContent=True
    | New Context    recordHar=${har}
    """

    omitContent: bool
    path: str


class _HttpCredentials(TypedDict):
    username: str
    password: str


class HttpCredentials(_HttpCredentials, total=False):
    """Sets the credentials for http basic-auth.

    ``origin``:
    Restrain sending http credentials on specific origin (scheme://host:port).
    Credentials for HTTP authentication. If no origin is specified, the username and password are sent to any servers upon unauthorized responses.

    Can be defined as robot dictionary or as string literal. Does not reveal secrets
    in Robot Framework logs. Instead, username and password values are resolved internally.
    Please note that if ``enable_playwright_debug`` is enabled in the library import,
    secret will be always visible as plain text in the playwright debug logs, regardless
    of the Robot Framework log level.

    Example as literal:
    | ${pwd} =    Set Variable    1234
    | ${username} =    Set Variable    admin
    | `New Context`
    | ...    httpCredentials={'username': '$username', 'password': '$pwd'}

    Example as robot variable
    | ***** *Variables* *****
    | ${username}=       admin
    | ${pwd}=            1234
    | ${credentials}=    username=$username    password=$pwd
    |
    | ***** *Keywords* *****
    | Open Context
    |    `New Context`    httpCredentials=${credentials}

    """

    origin: str


class _GeoCoordinated(TypedDict):
    longitude: float
    latitude: float


class GeoLocation(_GeoCoordinated, total=False):
    """Defines the geolocation.

    - ``latitude`` Latitude between -90 and 90.
    - ``longitude`` Longitude between -180 and 180.
    - ``accuracy`` *Optional* Non-negative accuracy value. Defaults to 0.
    Example usage: ``{'latitude': 59.95, 'longitude': 30.31667}``"""

    accuracy: float


class _Server(TypedDict):
    server: str


class PdfFormat(Enum):
    """PDF format argument options are

    Letter: 8.5in x 11in
    Legal: 8.5in x 14in
    Tabloid: 11in x 17in
    Ledger: 17in x 11in
    A0: 33.1in x 46.8in
    A1: 23.4in x 33.1in
    A2: 16.54in x 23.4in
    A3: 11.7in x 16.54in
    A4: 8.27in x 11.7in
    A5: 5.83in x 8.27in
    A6: 4.13in x 5.83in
    """

    Letter = "Letter"
    Legal = "Legal"
    Tabloid = "Tabloid"
    Ledger = "Ledger"
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"


class PdfMarging(TypedDict):
    """Margins of the pdf.

    Top margin, accepts values labeled with units. Defaults to 0px.
    Right margin, accepts values labeled with units. Defaults to 0px.
    Bottom margin, accepts values labeled with units. Defaults to 0px.
    Left margin, accepts values labeled with units. Defaults to 0px.
    """

    top: str
    right: str
    bottom: str
    left: str


class Media(Enum):
    """Changes the CSS media type of the page.

    The only allowed values are 'screen', 'print' and `null`.
    Passing null disables CSS media emulation.
    Using False will not define media argument.
    """

    screen = "screen"
    print = "print"
    null = "null"


class ReducedMotion(Enum):
    """Emulates 'prefers-reduced-motion' media feature.

    Supported values are 'reduce', 'no-preference' and `null`.
    Passing `null` disables reduced motion emulation.
    """

    reduce = "reduce"
    no_preference = "no-preference"
    null = "null"


class Proxy(_Server, total=False):
    """Network proxy settings.

    ``server`` Proxy to be used for all requests. HTTP and SOCKS proxies are supported,
     for example http://myproxy.com:3128 or socks5://myproxy.com:3128.
     Short form myproxy.com:3128 is considered an HTTP proxy.

    ``bypass`` *Optional* coma-separated domains to bypass proxy,
    for example ".com, chromium.org, .domain.com".

    ``username`` *Optional* username to use if HTTP proxy requires authentication.

    ``password`` *Optional* password to use if HTTP proxy requires authentication.
    """

    bypass: str
    username: str
    password: str


class DownloadInfo(TypedDict):
    """Downloaded file information.

    | =Key= | =Description= |
    | ``saveAs`` | is the path where downloaded file is saved. empty string if the file is not yet fully downloaded. |
    | ``suggestedFilename`` | is the suggested filename that was computed from the ``Content-Disposition`` response header. |
    | ``state`` | is the state of the download. i.e. ``in_progress``, ``finished`` or ``canceled``. |
    | ``downloadID`` | is the unique id of the download. |
    """

    saveAs: str
    suggestedFilename: str
    state: str
    downloadID: Optional[str]


class NewPageDetails(TypedDict):
    """Return value of `New Page` keyword.

    ``page_id`` is the UUID of the opened page.
    ``video_path`` path to the video or empty string if video is not created.
    """

    page_id: str
    video_path: str


class HighLightElement(TypedDict):
    """Presenter mode configuration options.

    ``duration`` Sets for how long the selector shall be highlighted. Defaults to ``5s`` => 5 seconds.

    ``width`` Sets the width of the higlight border. Defaults to 2px.

    ``style`` Sets the style of the border. Defaults to dotted.

    ``color`` Sets the color of the border, default is blue. Valid colors i.e. are:
    ``red``, ``blue``, ``yellow``, ``pink``, ``black``
    """

    duration: timedelta
    width: str
    style: str
    color: str


class HighlightMode(Enum):
    """Highlight mode for the element.

    ``border``: Highlights the element with a border outside of the selected element.
    This is the classic way to highlight an element of Browser librarary.

    ``playwright``: Highlights the element with Playwrights built in function.
    """

    border = auto()
    playwright = auto()


class LambdaFunction:
    @classmethod
    def from_string(cls, string: str) -> "LambdaFunction":
        """Python lambda function.

        The string must start with ``lambda`` and the function must accept one argument.

        Example: ``lambda value: value.lower().replace(' ', '')``
        """
        return eval(string)


FormatterKeywords = Enum(
    "FormatterKeywords",
    {
        "Get Attribute": auto(),
        "Get Browser Catalog": auto(),
        "Get Page Source": auto(),
        "Get Property": auto(),
        "Get Select Options": auto(),
        "Get Style": auto(),
        "Get Text": auto(),
        "Get Title": auto(),
        "Get Url": auto(),
        "LocalStorage Get Item": auto(),
        "SessionStorage Get Item": auto(),
    },
)
FormatterKeywords.__doc__ = """Enum that defines the available keywords for formatters.

Keywords that are not listed here, do not support formatters.
"""

FormatingRules = Enum(
    "FormatingRules",
    {
        "normalize spaces": auto(),
        "strip": auto(),
        "apply to expected": auto(),
        "case insensitive": auto(),
    },
)
FormatingRules.__doc__ = """Enum that defines the available formatters.

    | =Formatter= | =Description= |
    | ``normalize spaces`` | Replaces all kind of spaces with a single space. |
    | ``strip`` | Removes spaces from start and end of the string. |
    | ``apply to expected`` | Applies the formatter also to the expected value. |
    | ``case insensitive`` | Converts the string to lower case. |
"""


# Use Dict instead of dict for setting documenation
FormatterTypes = Dict[  # noqa: UP006
    FormatterKeywords, list[Union[FormatingRules, LambdaFunction]]
]
FormatterTypes.__doc__ = """Dictionary that defines the formatters for keywords.

Example Robot Variable:
| *** Variables ***
| @{normalizing_formatters}    strip    normalize spaces    lambda value: value.replace(' ', '')
| &{formatters}    Get Text    @{normalizing_formatters}

Example as literal:
| `Set Assertion Formatters`    {"Get Text": ["strip", "normalize spaces","lambda x: x.replace(' ', '')"]}

"""


def ensure_formatter_type(input_dict: dict):
    formatter_type = {}
    for formatter_keyword, rules in input_dict.items():
        formatter_rules: list[Union[FormatingRules, LambdaFunction]] = []
        for rule in rules:
            if isinstance(rule, FormatingRules) or callable(rule):
                formatter_rules.append(rule)
                continue
            try:
                formatter_rules.append(FormatingRules[rule])
            except KeyError as original_error:
                if not (isinstance(rule, str) and rule.startswith("lambda")):
                    raise TypeError(
                        f"'{rule}' is not a valid FormattingRule."
                    ) from original_error
                formatter_rules.append(LambdaFunction.from_string(rule))
        formatter_type[
            (
                FormatterKeywords[formatter_keyword]
                if not isinstance(formatter_keyword, FormatterKeywords)
                else formatter_keyword
            )
        ] = formatter_rules
    return formatter_type


class Scale(Enum):
    """Enum that defines the scale of the screenshot.

    When set to "css", screenshot will have a single pixel per each css pixel on the page.
    For high-dpi devices, this will keep screenshots small. Using "device" option will
    produce a single pixel per each device pixel, so screenshots of high-dpi devices will
    be twice as large or even larger.
    """

    css = auto()
    device = auto()


class SelectionType(Enum):
    """Enum that defines if the current id or all ids shall be returned.

    ``ACTIVE`` / ``CURRENT`` defines to return only the id of the currently active
    instance of a Browser/Context/Page.

    ``ALL`` / ``ANY`` defines to return ids of all instances."""

    CURRENT = "CURRENT"
    ACTIVE = CURRENT
    ALL = "ALL"
    ANY = ALL

    @classmethod
    def create(cls, value: Union[str, "SelectionType"]):
        """Returns the enum value from the given string or not."""
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError:
                return value
        return None

    def __str__(self):
        return self.value


class DialogAction(Enum):
    """Enum that defines how to handle a dialog."""

    accept = auto()
    dismiss = auto()


class CookieType(Enum):
    """Enum that defines the Cookie type."""

    dictionary = auto()
    dict = dictionary
    string = auto()
    str = string


CookieSameSite = Enum(
    "CookieSameSite", {"Strict": "Strict", "Lax": "Lax", "None": "None"}
)
CookieSameSite.__doc__ = """Enum that defines the Cookie SameSite type.

It controls whether or not a cookie is sent with cross-site requests, providing some protection against cross-site request forgery attacks (CSRF).

The possible attribute values are:
| = Value = | = Description = |
| ``Strict`` | Means that the browser sends the cookie only for same-site requests, that is, requests originating from the same site that set the cookie. If a request originates from a different domain or scheme (even with the same domain), no cookies with the SameSite=Strict attribute are sent. |
| ``Lax`` | Means that the cookie is not sent on cross-site requests, such as on requests to load images or frames, but is sent when a user is navigating to the origin site from an external site (for example, when following a link). This is the default behavior if the SameSite attribute is not specified. |
| ``None`` | means that the browser sends the cookie with both cross-site and same-site requests. The Secure attribute must also be set when setting this value. |

See [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie|MDN Set-Cookie] for more information.
"""


class RequestMethod(Enum):
    """Enum that defines the request type."""

    HEAD = auto()
    DELETE = auto()
    GET = auto()
    PATCH = auto()
    POST = auto()
    PUT = auto()


class MouseButtonAction(Enum):
    """Enum that defines which `Mouse Button` action to perform."""

    click = auto()
    down = auto()
    up = auto()


class MouseButton(Enum):
    """Enum that defines which mouse button to use."""

    left = auto()
    middle = auto()
    right = auto()


class KeyAction(Enum):
    """Enum that defines which `Keyboard Key` action to perform."""

    down = auto()
    up = auto()
    press = auto()


class KeyboardInputAction(Enum):
    """Enum that defines how `Keyboard Input` adds the text into the page.

    ``insertText`` is mostly similar to pasting of text.

    ``type`` is similar to typing by pressing keys on the keyboard."""

    insertText = auto()
    type = auto()


class KeyboardModifier(Enum):
    """Modifier keys to press while doing other actions.

    Modifiers that are pressed during the `Hover` or `Click`."""

    Alt = auto()
    Control = auto()
    ControlOrMeta = auto()
    Meta = auto()
    Shift = auto()


class SelectAttribute(Enum):
    """Enum that defines the attribute of an <option> element in a <select>-list.

    This defines by what attribute an option is selected/chosen.
    | <select class="my_drop_down">
    |   <option value="0: Object">None</option>
    |   <option value="1: Object">Some</option>
    |   <option value="2: Object">Other</option>
    | </select>

    ``value`` of the first option would be ``0: Object``.

    ``label`` / ``text`` both defines the innerText which would be ``None`` for first element.

    ``index`` 0 indexed number of an option. Would be ``0`` for the first element.

    """

    value = auto()
    label = auto()
    text = label
    index = auto()


class SupportedBrowsers(Enum):
    """Defines which browser shall be started.

    |   =Browser=   | =Browser with this engine=                        |
    | ``chromium``  | Google Chrome, Microsoft Edge (since 2020), Opera |
    | ``firefox``   | Mozilla Firefox                                   |
    | ``webkit``    | Apple Safari, Mail, AppStore on MacOS and iOS     |

    Since [https://github.com/microsoft/playwright|Playwright] comes with a pack of builtin
    binaries for all browsers, no additional drivers e.g. geckodriver are needed.

    All these browsers that cover more than 85% of the world wide used browsers,
    can be tested on Windows, Linux and MacOS.
    Theres is not need for dedicated machines anymore.
    """

    chromium = auto()
    firefox = auto()
    webkit = auto()


ColorScheme = Enum("ColorScheme", ["dark", "light", "no-preference", "null"])
ColorScheme.__doc__ = """Emulates 'prefers-colors-scheme' media feature.
        Supported values are 'light', 'dark', 'no-preference' and `null`.
        Passing `null` disables color scheme emulation.

        See [https://playwright.dev/docs/api/class-page?_highlight=emulatemedia#pageemulatemediaparams |emulateMedia(options)]
        for more details.
"""


Permission = Enum(
    "Permission",
    {
        "accelerometer": "accelerometer",
        "accessibility-events": "accessibility-events",
        "accessibility_events": "accessibility-events",
        "ambient-light-sensor": "ambient-light-sensor",
        "ambient_light_sensor": "ambient-light-sensor",
        "background-sync": "background-sync",
        "background_sync": "background-sync",
        "camera": "camera",
        "clipboard-read": "clipboard-read",
        "clipboard_read": "clipboard-read",
        "clipboard-write": "clipboard-write",
        "clipboard_write": "clipboard-write",
        "geolocation": "geolocation",
        "gyroscope": "gyroscope",
        "magnetometer": "magnetometer",
        "midi": "midi",
        "midi-sysex": "midi-sysex",
        "midi_sysex": "midi-sysex",
        "microphone": "microphone",
        "notifications": "notifications",
        "payment-handler": "payment-handler",
        "payment_handler": "payment-handler",
    },
)
Permission.__doc__ = """Enum that defines the permission to grant to a context.

See [https://playwright.dev/docs/api/class-browsercontext#browser-context-grant-permissions |grantPermissions(permissions)]
for more details.
"""


ScrollBehavior = Enum("ScrollBehavior", ["auto", "smooth"])
ScrollBehavior.__doc__ = """Enum that controls the behavior of scrolling.

``smooth``
"""


class SizeFields(Enum):
    """Enum that defines how the returned size is filtered.

    ``ALL`` defines that the size is returned as a dictionary. ``{'width': <float>, 'height': <float>}.``

    ``width`` / ``height`` will return a single float value of the chosen dimension."""

    width = auto()
    height = auto()
    ALL = auto()


class AreaFields(Enum):
    """Enumeration that defines which coordinates of an area should be selected.

    ``ALL`` defines that all fields are selected and a dictionary with all information
    is returned.
    """

    top = auto()
    left = auto()
    bottom = auto()
    right = auto()
    ALL = auto()


class ScrollPosition(TypedDict):
    """Scroll position of an element.

    | =Key= | =Description= |
    | ``top`` | The amount of pixel between the top border of the page and the top border of visible area. |
    | ``left`` | The amount of pixel between the left border of the page and the left border of visible area. |
    | ``bottom`` | The amount of pixel between the top border of the page and the bottom border of visible area. |
    | ``right`` | The amount of pixel between the left border of the page and the right border of visible area. |
    """

    top: float
    left: float
    bottom: float
    right: float


class BoundingBoxFields(Enum):
    """Enumeration that defines which location information of an element should be selected.

    ``x`` / ``y`` defines the position of the top left corner of an element.

    ``width`` / ``height`` defines the size of an elements bounding box.

    ``ALL`` defines that all fields are selected and a dictionary with all information
    is returned.
    """

    width = auto()
    height = auto()
    x = auto()
    y = auto()
    ALL = auto()


class AutoClosingLevel(Enum):
    """Controls when contexts and pages are closed during the test execution.

    If automatic closing level is `TEST`, contexts and pages that are created during a single test are
    automatically closed when the test ends. Contexts and pages that are created during suite setup are
    closed when the suite teardown ends.

    If automatic closing level is `SUITE`, all contexts and pages that are created during the test suite
    are closed when the suite teardown ends.

    If automatic closing level is `MANUAL`, nothing is closed automatically while the test execution
    is ongoing. All browsers, context and pages are automatically closed when test execution ends.

    If automatic closing level is `KEEP`, nothing is closed automatically while the test execution
    is ongoing. Also, nothing is closed when test execution ends, including the node process. Therefore,
    it is users responsibility to close all browsers, context and pages and ensure that all process
    that are left running after the test execution end are closed. This level is only intended for
    test case development and must not be used when running tests in CI or similar environments.

    Automatic closing can be configured or switched off with the auto_closing_level library import
    parameter.

    See: `Importing`"""

    SUITE = auto()
    TEST = auto()
    MANUAL = auto()
    KEEP = auto()


class ElementState(IntFlag):
    """Enum that defines the state an element can have.

    The following ``states`` are possible:
    | =State=        | =Description= |
    | ``attached``   | to be present in DOM. |
    | ``detached``   | to not be present in DOM. |
    | ``visible``    | to have non or empty bounding box and no visibility:hidden. |
    | ``hidden``     | to be detached from DOM, or have an empty bounding box or visibility:hidden. |
    | ``enabled``    | to not be ``disabled``. |
    | ``disabled``   | to be ``disabled``. Can be used on <button>, <fieldset>, <input>, <optgroup>, <option>, <select> and <textarea>. |
    | ``editable``   | to not be ``readOnly``. |
    | ``readonly``   | to be ``readOnly``. Can be used on <input> and <textarea>. |
    | ``selected``   | to be ``selected``. Can be used on <option>. |
    | ``deselected`` | to not be ``selected``. |
    | ``focused``    | to be the ``activeElement``. |
    | ``defocused``  | to not be the ``activeElement``. |
    | ``checked``    | to be ``checked``. Can be used on <input>. |
    | ``unchecked``  | to not be ``checked``. |
    | ``stable``     | to be both ``visible`` and ``stable``. |
    """

    attached = 1
    detached = 2
    visible = 4
    hidden = 8
    enabled = 16
    disabled = 32
    editable = 64
    readonly = 128
    selected = 256
    deselected = 512
    focused = 1024
    defocused = 2048
    checked = 4096
    unchecked = 8192
    stable = 16384


class ScreenshotFileTypes(Enum):
    """Enum that defines available file types for screenshots."""

    png = auto()
    jpeg = auto()


class ScreenshotReturnType(Enum):
    """Enum that defines what `Take Screenshot` keyword returns.

    - ``path`` returns the path to the screenshot file as ``pathlib.Path`` object.
    - ``path_string`` returns the path to the screenshot file as string.
    - ``bytes`` returns the screenshot itself as bytes.
    - ``base64`` returns the screenshot itself as base64 encoded string.
    """

    path = auto()
    path_string = auto()
    bytes = auto()
    base64 = auto()


class PageLoadStates(Enum):
    """Enum that defines available page load states."""

    load = auto()
    domcontentloaded = auto()
    networkidle = auto()
    commit = auto()


class ReduceMotion(Enum):
    """Emulates `prefers-reduced-motion` media feature, supported values are `reduce`, `no-preference`."""

    reduce = auto()
    no_preference = auto()


class ForcedColors(Enum):
    """Emulates 'forced-colors' media feature.

    Supported values are 'active', 'none' and `null`.
    Passing `null` disables forced colors emulation.
    """

    active = auto()
    none = auto()
    null = auto()


class ConditionInputs(Enum):
    """
    Following values are allowed and represent the assertion keywords to use:
    | =Value= | =Keyword= |
    | ``Attribute`` | `Get Attribute` |
    | ``Attribute Names`` | `Get Attribute Names` |
    | ``BoundingBox`` | `Get BoundingBox` |
    | ``Browser Catalog`` | `Get Browser Catalog` |
    | ``Checkbox State`` | `Get Checkbox State` |
    | ``Classes`` | `Get Classes` |
    | ``Client Size`` | `Get Client Size` |
    | ``Download State`` | `Get Download State` |
    | ``Element Count`` | `Get Element Count` |
    | ``Element States`` | `Get Element States` |
    | ``Page Source`` | `Get Page Source` |
    | ``Property`` | `Get Property` |
    | ``Scroll Position`` | `Get Scroll Position` |
    | ``Scroll Size`` | `Get Scroll Size` |
    | ``Select Options`` | `Get Select Options` |
    | ``Selected Options`` | `Get Selected Options` |
    | ``Style`` | `Get Style` |
    | ``Table Cell Index`` | `Get Table Cell Index` |
    | ``Table Row Index`` | `Get Table Row Index` |
    | ``Text`` | `Get Text` |
    | ``Title`` | `Get Title` |
    | ``Url`` | `Get Url` |
    | ``Viewport Size`` | `Get Viewport Size` |
    """

    attribute = "get_attribute"
    attribute_names = "get_attribute_names"
    bounding_box = "get_bounding_box"
    browser_catalog = "get_browser_catalog"
    checkbox_state = "get_checkbox_state"
    classes = "get_classes"
    client_size = "get_client_size"
    download_state = "get_download_state"
    element_count = "get_element_count"
    element_states = "get_element_states"
    page_source = "get_page_source"
    property = "get_property"
    scroll_position = "get_scroll_position"
    scroll_size = "get_scroll_size"
    select_options = "get_select_options"
    selected_options = "get_selected_options"
    style = "get_style"
    table_cell_index = "get_table_cell_index"
    table_row_index = "get_table_row_index"
    text = "get_text"
    title = "get_title"
    url = "get_url"
    viewport_size = "get_viewport_size"


class Scope(Enum):
    """Some keywords which manipulates library settings have a scope argument.
    With that scope argument one can set the "live time" of that setting.
    Available Scopes are: ``Global``, ``Suite`` and ``Test`` / ``Task``.
    Is a scope finished, this scoped setting, like timeout, will no longer be used and the previous higher scope setting applies again.

    Live Times:

    - A ``Global`` scope will live forever until it is overwritten by another Global scope.
      Or locally temporarily overridden by a more narrow scope.
    - A ``Suite`` scope will locally override the Global scope and
      live until the end of the Suite within it is set, or if it is overwritten
      by a later setting with Global or same scope.
      Children suite does inherit the setting from the parent suite but also may have
      its own local Suite setting that then will be inherited to its children suites.
    - A ``Test`` or ``Task`` scope will be inherited from its parent suite but when set,
      lives until the end of that particular test or task.

    A new set higher order scope will always remove the lower order scope which may be in charge.
    So the setting of a Suite scope from a test, will set that scope to the robot file suite where
    that test is and removes the Test scope that may have been in place."""

    Global = auto()
    Suite = auto()
    Test = auto()
    Task = Test


class ServiceWorkersPermissions(Enum):
    """Whether to allow sites to register Service workers.

    ``allow``: Service Workers can be registered.

    ``block``: Playwright will block all registration of Service Workers.
    """

    allow = auto()
    block = auto()


class PlaywrightLogTypes(Enum):
    """Enable low level debug information from the playwright to playwright-log.txt file.

    It is possible to disable the creation of playwright-log.txt totally. Mainly useful for the library developers
    and for debugging purposes. Will log everything as plain text, also including secrets. If playwright-log.txt file
    can not be deleted, time.time_ns() is added at the end of file name. Example playwright-log-12345.txt

    ``disabled``: playwright-log.txt is not created at all. All node side logging is lost.
    ``library``: Default, only logging from Browser library node side is written to the playwright-log.txt file.
    ``playwright``: Also includes Playwright log messages to the playwright-log.txt file.
    ``false``: Same as `library` and for backwards compatability.
    ``true``: Same as `playwright` and for backwards compatibility.
    """

    disabled = auto()
    library = auto()
    playwright = auto()
    false = library
    true = playwright


class PageInfo(TypedDict):
    type: str
    title: str
    url: str
    id: str
    timestamp: float


class ContextInfo(TypedDict):
    type: str
    id: str
    activePage: str
    pages: list[PageInfo]


class BrowserInfo(TypedDict):
    """Dictionary that contains information about a browser instance.

    | =Key= | =Description= |
    | ``type`` | The browser type. e.g. chromium, firefox or webkit. |
    | ``id`` | The unique id of the browser instance. |
    | ``contexts`` | List of context information opened by the browser. |
    | ``activeContext`` | The id of the active context. |
    | ``activeBrowser`` | Boolean if the browser is the currently active browser. |

    Structure:
    | {
    |   'type': `str`,
    |   'id': `str`,
    |   'contexts': [
    |       {
    |           'type': `str`,
    |           'id': `str`,
    |           'activePage': `str`,
    |           'pages': [
    |               {
    |                   'type': `str`,
    |                   'title': `str`,
    |                   'url': `str`,
    |                   'id': `str`,
    |                   'timestamp': `float`
    |               },
    |               ...
    |           ]
    |       },
    |       ...
    |   ],
    |   'activeContext': `str`,
    |   'activeBrowser': `bool`
    | }
    """

    type: str
    id: str
    contexts: list[ContextInfo]
    activeContext: str
    activeBrowser: bool


class FileUploadBuffer(TypedDict):
    """Dictionary that contains information about a file upload buffer.

    | =Key= | =Description= |
    | ``name`` | The name of the file. |
    | ``mimeType`` | The mime type of the file. |
    | ``buffer`` | The file content. |

    Structure:
    | {
    |   'name': `str`,
    |   'mimeType': `str`,
    |   'buffer': `str`
    | }
    """

    name: str
    mimeType: str
    buffer: str


class CoverageType(Enum):
    """Enum that defines the type of coverage to collect.

    ``js``: [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JavaScript] coverage.
    ``css``: [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS] coverage.
    ``all``: Both [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS] and [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JS] coverage.
    """

    js = auto()
    css = auto()
    all = auto()


class ClockType(Enum):
    """Defines how time is set.

    The recommended approach is to use fixed to set the time to a
    specific value.

    ``fixed``: Sets the fixed time for Date.now() and new Date().
    ``system``: Is only recommended for advanced use cases.
    ``install``: initializes the clock and allows you to:
            `pause_at`: Pauses the time at a specific time.
            `fast_forward`: Fast forwards the time.
            `run_for`: Runs the time for a specific duration.
            `resume`: Resumes the time.
    """

    fixed = auto()
    system = auto()
    install = auto()


class CLockAdvanceType(Enum):
    """Defines how time is advanced.

    ``fast_forward``: Advance the clock by jumping forward in time.
    ``run_for``: Advance the clock, firing all the time-related callbacks.

    fast_forward will Only fires due timers at most once. This is
    equivalent to user closing the laptop lid for a while and reopening it
    later, after given time.
    """

    fast_forward = auto()
    run_for = auto()


class ClientCertificate(TypedDict, total=False):
    """Defines client certificate.

    - ``origin`` Exact origin that the certificate is valid for. Origin includes https protocol, a hostname and optionally a port.
    - ``certPath`` *Optional* Path to the file with the certificate in PEM format.
    - ``keyPath`` *Optional* Path to the file with the private key in PEM format.
    - ``pfxPath`` *Optional* Path to the PFX or PKCS12 encoded private key and certificate chain.
    - ``passphrase`` *Optional* Passphrase for the private key (PEM or PFX).
    Example usage: ``{'origin': 'https://playwright.dev', 'pfxPath': 'certificate.p12', 'passphrase': 'secret'}``
    """

    origin: str
    certPath: str
    keyPath: str
    pfxPath: str
    passphrase: str


class TracingGroupMode(Enum):
    """Defines in what detail level keywords are written to Playwright trace.

    Playwrright trace is a full log of all playwright actions and events that happen in the browser during the test run.
    This includes all API calls, events, logs, network requests, and responses as well as the DOM at every moment during execution.
    This trace can be activated with the ``tracing`` parameter of `New Context` keyword.

    - ``Full`` All keyword calls are written to trace as groups even if they do not call Browser keywords.
    - ``Browser`` Just Browser library keywords are written to the logs as groups.
    - ``Playwright`` No additional keywords are logged, just the Playwright API calls.

    """

    Full = auto()
    Browser = auto()
    Playwright = auto()
