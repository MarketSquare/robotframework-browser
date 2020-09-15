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
from .version import __version__ as VERSION

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
