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

from enum import Enum, auto
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


class HttpCredentials(TypedDict):
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


class SelectionType(Enum):
    ACTIVE = auto()
    CURRENT = ACTIVE
    ALL = auto()
    ANY = ALL


class DialogAction(Enum):
    accept = auto()
    dismiss = auto()


class CookieType(Enum):
    dictionary = auto()
    dict = dictionary
    string = auto()
    str = string


CookieSameSite = Enum(
    "CookieSameSite", {"Strict": "Strict", "Lax": "Lax", "None": "None"}
)


class RequestMethod(Enum):
    HEAD = auto()
    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()


class MouseButtonAction(Enum):
    click = auto()
    down = auto()
    up = auto()


class MouseButton(Enum):
    left = auto()
    middle = auto()
    right = auto()


class KeyAction(Enum):
    down = auto()
    up = auto()
    press = auto()


class KeyboardInputAction(Enum):
    insertText = auto()
    type = auto()


class KeyboardModifier(Enum):
    Alt = auto()
    Control = auto()
    Meta = auto()
    Shift = auto()


class SelectAttribute(Enum):
    value = auto()
    label = auto()
    text = label
    index = auto()


class SupportedBrowsers(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()


ColorScheme = Enum("ColorScheme", ["dark", "light", "no-preference"])


ScrollBehavior = Enum("ScrollBehavior", ["auto", "smooth"])


class SizeFields(Enum):
    width = auto()
    height = auto()
    ALL = auto()


class AreaFields(Enum):
    top = auto()
    left = auto()
    bottom = auto()
    right = auto()
    ALL = auto()


class BoundingBoxFields(Enum):
    width = auto()
    height = auto()
    x = auto()
    y = auto()
    ALL = auto()


class AutoClosingLevel(Enum):
    SUITE = auto()
    TEST = auto()
    MANUAL = auto()


class ElementState(Enum):
    attached = auto()
    detached = auto()
    visible = auto()
    hidden = auto()
    enabled = auto()
    disabled = auto()
    editable = auto()
    readonly = auto()
    selected = auto()
    deselected = auto()
    focused = auto()
    defocused = auto()
    checked = auto()
    unchecked = auto()


class ElementStateKey(Enum):
    attached = auto()
    visible = auto()
    disabled = auto()
    readonly = auto()
    selected = auto()
    focused = auto()
    checked = auto()


AssertionOperator = Enum(
    "AssertionOperator",
    {
        "equal": "==",
        "==": "==",
        "should be": "==",
        "inequal": "!=",
        "!=": "!=",
        "should not be": "!=",
        "less than": "<",
        "<": "<",
        "greater than": ">",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "contains": "*=",
        "*=": "*=",
        "starts": "^=",
        "^=": "^=",
        "should start with": "^=",
        "ends": "$=",
        "should end with": "$=",
        "$=": "$=",
        "matches": "$",
        "validate": "validate",
        "then": "then",
        "evaluate": "then",
    },
)
AssertionOperator.__doc__ = """
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


    The keywords will provide an error message if the assertion fails.
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
    """
