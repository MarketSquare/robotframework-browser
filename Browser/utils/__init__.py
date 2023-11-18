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

# flake8: noqa

from .data_types import (
    AutoClosingLevel,
    BrowserInfo,
    ColorScheme,
    ConditionInputs,
    CookieSameSite,
    CookieType,
    DownloadInfo,
    ElementState,
    ForcedColors,
    FormatterKeywords,
    FormatingRules,
    FormatterTypes,
    GeoLocation,
    HighLightElement,
    HttpCredentials,
    LambdaFunction,
    NewPageDetails,
    PageLoadStates,
    Permission,
    PlaywrightLogTypes,
    Proxy,
    RecordHar,
    RecordVideo,
    ReduceMotion,
    RequestMethod,
    Scope,
    ScrollPosition,
    SelectAttribute,
    SelectOptions,
    SelectionType,
    ServiceWorkersPermissions,
    SupportedBrowsers,
    ViewportDimensions,
    convert_typed_dict,
)
from .js_utilities import get_abs_scroll_coordinates, get_rel_scroll_coordinates
from .meta_python import find_by_id, locals_to_params
from .misc import (
    find_free_port,
    get_normalized_keyword,
    get_variable_value,
    is_same_keyword,
    keyword,
    spawn_node_process,
)
from .robot_booleans import is_falsy, is_truthy
from .settings_stack import ScopedSetting, SettingsStack
from robot.utils import DotDict
