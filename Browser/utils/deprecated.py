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
import inspect
from typing import Any, Callable

from Browser.utils import logger

from ..utils.data_types import RobotTypeConverter as TypeConverter


def _method_to_keyword(method: str) -> str:
    keyword = ""
    for word in method.split("_"):
        keyword = f"{keyword} {word.capitalize()}"
    return keyword.strip()


def _is_deprecated_attribute(method: Callable, deprecated_arg, args, kwargs):
    if not deprecated_arg:
        return False
    args = list(args)
    args.pop(0)
    argspec = inspect.getfullargspec(method)
    argspec_args = argspec.args
    argspec_args.pop(0)
    deprecated = False
    if not args and not kwargs:
        deprecated = False
    if deprecated_arg in kwargs:
        deprecated = True
    for index, argspec_arg in enumerate(argspec_args):
        if argspec_arg in deprecated_arg and len(args) == index + 1:
            deprecated = True
    return deprecated


def convert_pos_args_to_named(
    deprecated_pos_args: tuple[Any, ...],
    old_args: dict[str, Any],
    keyword_name: str,
    additional_msg: str = "",
):
    old_args_list = list(old_args.items())
    pos_params = {}
    for index, pos_arg in enumerate(deprecated_pos_args):
        argument_name = old_args_list[index][0]
        argument_type = old_args_list[index][1]
        converted_pos = TypeConverter.converter_for(argument_type).convert(
            name=argument_name, value=pos_arg
        )
        pos_params[argument_name] = converted_pos
    if pos_params:
        logger.warn(
            f"Deprecated positional arguments are used in '{keyword_name}'. "
            f"Please use named arguments instead.{additional_msg}"
        )
    return pos_params
