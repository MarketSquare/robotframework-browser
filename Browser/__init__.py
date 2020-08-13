from .browser import Browser
from .utils.data_types import (
    AssertionOperator,
    ColorScheme,
    ElementState,
    KeyboardModifier,
    MouseButton,
    RequestMethod,
    SelectAttribute,
    SupportedBrowsers,
    TypedDict,
    ViewportDimensions,
)
from .version import VERSION

__version__ = VERSION
__all__ = [
    "TypedDict",
    "AssertionOperator",
    "ElementState",
    "ColorScheme",
    "ViewportDimensions",
    "SupportedBrowsers",
    "SelectAttribute",
    "KeyboardModifier",
    "MouseButton",
    "RequestMethod",
    "Browser",
]
