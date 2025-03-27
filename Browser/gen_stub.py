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
import sys
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import Any

from robotlibcore import KeywordBuilder  # type: ignore

import Browser
from Browser.utils.data_types import Deprecated

PY310 = sys.version_info.major == 3 and sys.version_info.minor >= 10  # noqa: PLR2004


def is_named_method(keyword_name: str) -> bool:
    keyword_attribute = br.attributes[keyword_name]
    return (
        keyword_attribute.robot_name is not None
        and keyword_attribute.robot_name == keyword_name
    )


def get_method_name_for_keyword(keyword_name: str) -> str:
    if is_named_method(keyword_name):
        for key in br.attributes:
            if key != keyword_name and keyword_name == br.attributes[key].robot_name:
                return key
    return keyword_name


def get_type_string_from_type(argument_type: type) -> str:
    if PY310 and str(argument_type).startswith("typing."):
        return str(argument_type).replace("NoneType", "None")
    if hasattr(argument_type, "__name__"):
        if argument_type.__name__ == "datetime":
            return "datetime.datetime"
        return argument_type.__name__
    arg_type_str = str(argument_type.__repr__()).lstrip("typing.")
    return arg_type_str.replace("NoneType", "None")


def get_type_string_from_argument(argument_string: str, argument_types: dict) -> str:
    agrument_name = argument_string.lstrip("*")
    if agrument_name in argument_types:
        type_string = get_type_string_from_type(argument_types[agrument_name])
        return type_string.replace("Browser.utils.data_types.", "")
    return ""


def get_function_list_from_keywords(keywords):
    functions = []
    for keyword in keywords:
        method_name = get_method_name_for_keyword(keyword)
        keyword_arguments = br.get_keyword_arguments(keyword)
        keyword_types = br.get_keyword_types(keyword)
        functions.append(keyword_line(keyword_arguments, keyword_types, method_name))
    functions.sort()
    return functions


def keyword_line(keyword_arguments, keyword_types, method_name) -> str:
    arguments_list = []
    for argument in keyword_arguments:
        if isinstance(argument, tuple):
            arg_str = argument[0]
            default_value = argument[1]
            arg_type_str = get_type_string_from_argument(arg_str, keyword_types)
            if arg_type_str:
                arg_str = f"{arg_str}: {arg_type_str}"
            if isinstance(default_value, str):
                default_value = f"'{default_value}'"
            elif isinstance(default_value, timedelta):
                default_value = f"timedelta(seconds={default_value.total_seconds()})"
            elif isinstance(default_value, Enum):
                default_value = f"{type(default_value).__name__}.{default_value.name}"
            elif isinstance(default_value, Deprecated):
                default_value = "Deprecated()"
            elif isinstance(default_value, Path):
                default_value = f"pathlib.Path('{default_value}')"
            arg_str = f"{arg_str} = {default_value!s}"
        else:
            arg_str = argument
            arg_type_str = get_type_string_from_argument(arg_str, keyword_types)
            if arg_type_str:
                arg_str = arg_str + f": {arg_type_str}"
        arguments_list.append(arg_str)
    arguments_string = (
        f", {', '.join(arguments_list)}" if len(arguments_list) > 0 else ""
    )
    return f"    def {method_name}(self{arguments_string}): ...\n"


br: Any = Browser.Browser()
function_list = get_function_list_from_keywords(br.get_keyword_names())


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

import datetime
import typing
import os
from concurrent.futures import Future
from os import PathLike
import pathlib
from pathlib import Path
from typing import Any

import assertionengine

from robotlibcore import DynamicCore  # type: ignore

from .utils.data_types import *
from .base import LibraryComponent


class Browser(DynamicCore):
    timeout: Any = ...
    scope_stack: typing.Dict = ...
    _old_init_args: typing.Dict = ...
    _playwright_state: Any = ...
    _browser_control: Any = ...


"""

pyi_non_kw_methods = """\
    def get_timeout(self, timeout: Union[timedelta, None]) -> float: ...
    def convert_timeout(self, timeout: Union[timedelta, float], to_ms: bool = True) -> float: ...
    def millisecs_to_timestr(self, timeout: float)  -> str: ...
    def get_strict_mode(self, strict: Union[bool, None]) -> bool: ...
    def _parse_run_on_failure_keyword(self, keyword_name: Union[str, None]) -> DelayedKeyword: ...
    def _create_lib_component_from_jsextension(self, jsextension: str) -> LibraryComponent: ...

"""

init_method = KeywordBuilder.build(br.__init__)
with Path("Browser/browser.pyi").open("w", encoding="utf-8") as stub_file:
    stub_file.write(pyi_boilerplate)
    init_string = keyword_line(
        init_method.argument_specification, init_method.argument_types, "__init__"
    )
    # init methods argument types that are contained within higher order types don't get
    # import syntax stripped correctly so we fix them manually here
    init_string = init_string.replace(
        "Dict[Browser.utils.data_types.SupportedBrowsers, str]",
        "Dict[SupportedBrowsers, str]",
    )

    stub_file.write(init_string)
    stub_file.writelines(function_list)
    stub_file.write(pyi_non_kw_methods)
