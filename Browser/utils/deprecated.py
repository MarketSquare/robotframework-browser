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
from functools import wraps
from typing import Callable, Tuple

from robot.api import logger  # type: ignore


def attribute_warning(old_args: Tuple[str, str], new_args: Tuple[str, str]):
    def actual_decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kw_name = _method_to_keyword(method.__name__)
            for index, old_arg in enumerate(old_args):
                if _is_deprecated_attribute(method, old_arg, args, kwargs):
                    logger.warn(
                        f"Browser library {kw_name} keyword "
                        f"has deprecated {old_arg}, use {new_args[index]}",
                    )
            return method(*args, **kwargs)

        return wrapper

    return actual_decorator


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
        if argspec_arg in deprecated_arg:
            if len(args) == index + 1:
                deprecated = True
    return deprecated
