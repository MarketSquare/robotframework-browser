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
from pathlib import Path

import Browser

BR: Browser.Browser = Browser.Browser()
KW_METHOD_NAMES = [kw.__name__ for kw in BR.keywords.values()]
ADDED_KW = []


def parse_kw_module_lines(lines: list[str]):
    for line in lines:
        for method_name in KW_METHOD_NAMES:
            if f"def {method_name}(" in line and method_name not in ADDED_KW:
                ADDED_KW.append(method_name)
                yield line


def parse_kw_stubs():
    for file in Path("mypy_stub/Browser/keywords").rglob("*.pyi"):
        with file.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            yield from parse_kw_module_lines(lines)


pyi_boilerplate = """\
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
from datetime import datetime
from concurrent.futures import Future
from os import PathLike

from assertionengine import AssertionOperator

from robot.utils import DotDict

from Browser.utils import (
    ClockType, CLockAdvanceType, FormatterTypes, CookieType, CookieSameSite, DownloadInfo, NewPageDetails,
    BrowserInfo, PageLoadStates,ViewportDimensions, ServiceWorkersPermissions,
    ReduceMotion, RecordVideo, RecordHar, Proxy, Permission, HttpCredentials,
    GeoLocation, ForcedColors, ColorScheme, ClientCertificate, HighlightMode, ScreenshotReturnType,
    Scale, ScreenshotFileTypes, BoundingBox, ReducedMotion, Media, PdfMarging,
    PdfFormat, CoverageType, RequestMethod, ElementState, ScrollPosition,
    SelectAttribute, SelectOptions, ConditionInputs, FileUploadBuffer, SelectAttribute
)
from Browser.utils .data_types import (
    MouseButton, KeyboardModifier, ScrollBehavior, ScrollBehavior, DialogAction, MouseButtonAction, NotSet, Dimensions,
    SizeFields, AreaFields, BoundingBoxFields, SelectionStrategy, ElementRole, AriaSnapshotReturnType,
    KeyboardInputAction, KeyAction
)
"""
with Path("Browser/browser.pyi").open("w", encoding="utf-8") as stub_file:
    stub_file.write(pyi_boilerplate)
    with Path("mypy_stub/Browser/browser.pyi").open("r", encoding="utf-8") as init_file:
        stub_file.write(init_file.read())
    stub_file.write("\n")
    for line in parse_kw_stubs():
        stub_file.write(line)

lines = []
with Path("Browser/browser.pyi").open("r", encoding="utf-8") as stub_file:
    for line in stub_file.readlines():
        if "from robotlibcore import DynamicCore" in line:
            lines.append("from robotlibcore import DynamicCore # type: ignore\n")
        else:
            lines.append(line)
with Path("Browser/browser.pyi").open("w", encoding="utf-8") as stub_file:
    stub_file.writelines(lines)
