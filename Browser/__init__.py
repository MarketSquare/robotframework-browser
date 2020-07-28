from .utils.data_types import (
    TypedDict,
    AssertionOperator,
    ElementState,
    ColorScheme,
    ViewportDimensions,
    SupportedBrowsers,
    SelectAttribute,
    KeyboardModifier,
    MouseButton,
    RequestMethod,
)
from .version import VERSION
from .browser import Browser

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

from .entry import init_node_dependencies

init_node_dependencies()
