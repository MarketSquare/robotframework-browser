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
from enum import Enum, IntFlag, auto
from typing import Dict, Union

from typing_extensions import TypedDict


class TypedDictDummy(TypedDict):
    pass


def convert_typed_dict(function_annotations: Dict, params: Dict) -> Dict:
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
                arg_type = union_type
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
                        f"`{lower_case_dict}` cannot be converted to {arg_type.__name__}."
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
    |  New Context  recordVideo={'dir': '${OUTPUT_DIR}/video'}
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

    Can be defined as robot dictionary or as string literal.

    Example as literal:
    | `New Context`    httpCredentials={'username': 'admin', 'password': '123456'}

    Example as robot variable
    | ***** *Variables* *****
    | &{credentials}=    username=admin    password=123456
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
    Username: str
    password: str


class DownloadedFile(TypedDict):
    """Downloaded file information.

    ``saveAs`` is the path where downloaded file is saved.
    ``suggestedFilename`` is the  contains the name suggested name for the download.
    """

    saveAs: str
    suggestedFilename: str


class NewPageDetails(TypedDict):
    """Return value of New Page keyword.

    ``page_id`` is the UUID of the opened page.
    ``video_path`` path to the video or empty string if video is not created.
    """

    page_id: str
    video_path: str


class SelectionType(Enum):
    """Enum that defines if the current id or all ids shall be returned.

    ``ACTIVE`` / ``CURRENT`` defines to return only the id of the currently active
    instance of a Browser/Context/Page.

    ``ALL`` / ``ANY`` defines to return ids of all instances."""

    ACTIVE = auto()
    CURRENT = ACTIVE
    ALL = auto()
    ANY = ALL


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
    type = auto()


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

    If automatic closing level is `MANUAL`, nothing is closed automatically during the test execution
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
