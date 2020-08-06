from enum import Enum, auto
from typing import TypedDict


class AlertAction(Enum):
    accept = auto()
    dismiss = auto()


class CookieType(Enum):
    dictionary = auto()
    dict = dictionary
    string = auto()
    str = string


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

ViewportDimensions = TypedDict("ViewportDimensions", {"width": int, "height": int})

MouseOptionsDict = TypedDict(
    "MouseOptionsDict", {"x": float, "y": float, "options": dict}, total=False
)


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


AssertionOperator = Enum(
    "AssertionOperator",
    {
        "equal": "==",
        "==": "==",
        "shouldbe": "==",
        "inequal": "!=",
        "!=": "!=",
        "shouldnotbe": "!=",
        "lessthan": "<",
        "<": "<",
        "greaterthan": ">",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "contains": "*=",
        "*=": "*=",
        "starts": "^=",
        "^=": "^=",
        "shouldstartwith": "^=",
        "ends": "$=",
        "$=": "$=",
        "matches": "$",
        "validate": "validate",
        "then": "then",
        "evaluate": "then",
    },
)
