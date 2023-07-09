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
from typing import Dict, Union

from typing_extensions import TypedDict


class TypedDictDummy(TypedDict):
    pass


def convert_typed_dict(function_annotations: Dict, params: Dict) -> Dict:  # noqa: C901
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
            for req_key in arg_type.__required_keys__:  # type: ignore
                if req_key.lower() not in lower_case_dict:
                    raise RuntimeError(
                        f"`{lower_case_dict}` cannot be converted to {arg_type.__name__} for argument '{arg_name}'."
                        f"\nThe required key '{req_key}' in not set in given value."
                        f"\nExpected types: {arg_type.__annotations__}"
                    )
                typed_dict[req_key] = struct[req_key](lower_case_dict[req_key.lower()])  # type: ignore
            for opt_key in arg_type.__optional_keys__:  # type: ignore
                if opt_key.lower() not in lower_case_dict:
                    continue
                typed_dict[opt_key] = struct[opt_key](lower_case_dict[opt_key.lower()])  # type: ignore
            params[arg_name] = typed_dict
    return params


class Deprecated:
    def __str__(self) -> str:
        return ""


deprecated = Deprecated()


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
    x: float
    y: float
    width: float
    height: float


class Coordinates(TypedDict, total=False):
    x: float
    y: float


class MouseOptionsDict(TypedDict, total=False):
    x: float
    y: float
    options: dict


class ViewportDimensions(TypedDict):
    width: int
    height: int


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


class HttpCredentials(TypedDict):
    """Sets the credentials for http basic-auth.

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

    username: str
    password: str


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


class DownloadedFile(TypedDict):
    """Downloaded file information.

    ``saveAs`` is the path where downloaded file is saved.
    ``suggestedFilename`` is the  contains the name suggested name for the download.
    """

    saveAs: str
    suggestedFilename: str


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
    dict = dictionary  # noqa: A003
    string = auto()
    str = string  # noqa: A003


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
    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()


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
    type = auto()  # noqa: A003


class KeyboardModifier(Enum):
    """Modifier keys to press while doing other actions.

    Modifiers that are pressed during the `Hover` or `Click`."""

    Alt = auto()
    Control = auto()
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


ColorScheme = Enum("ColorScheme", ["dark", "light", "no-preference"])
ColorScheme.__doc__ = """Emulates 'prefers-colors-scheme' media feature.

        See [https://playwright.dev/docs/api/class-page?_highlight=emulatemedia#pageemulatemediaparams |emulateMedia(options)]
        for more details.
"""


class Permission(Enum):
    """Enum that defines the permission to grant to a context.

    See [https://playwright.dev/docs/api/class-browsercontext#browser-context-grant-permissions |grantPermissions(permissions)]
    for more details.
    """

    geolocation = auto()
    midi = auto()
    midi_sysex = auto()
    notifications = auto()
    push = auto()
    camera = auto()
    microphone = auto()
    background_sync = auto()
    ambient_light_sensor = auto()
    accelerometer = auto()
    gyroscope = auto()
    magnetometer = auto()
    accessibility_events = auto()
    clipboard_read = auto()
    clipboard_write = auto()
    payment_handler = auto()


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
    is ongoing.

    All browsers are automatically closed, always and regardless of the automatic closing level at
    the end of the test execution. This will also close all remaining pages and contexts.

    Automatic closing can be configured or switched off with the auto_closing_level library import
    parameter.

    See: `Importing`"""

    SUITE = auto()
    TEST = auto()
    MANUAL = auto()


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


ElementStateKey = (
    ElementState  # Deprecated. Remove after `Get Element State` is removed.
)


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
    bytes = auto()  # noqa: A003
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
    """Emulates `forced-colors` media feature, supported values are `active`, `none`."""

    active = auto()
    none = auto()


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
    element_count = "get_element_count"
    element_states = "get_element_states"
    page_source = "get_page_source"
    property = "get_property"  # noqa: A003
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
