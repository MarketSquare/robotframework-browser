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
    ViewportDimensions,
)
from .version import VERSION

__version__ = VERSION
__all__ = [
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
