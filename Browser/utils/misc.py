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

import contextlib
import socket

from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robot.running import RUN_KW_REGISTER  # type: ignore

get_variable_value = BuiltIn().get_variable_value
replace_variables = BuiltIn().replace_variables


def find_free_port() -> str:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def is_same_keyword(first: str, second: str) -> bool:
    if isinstance(first, str) and isinstance(second, str):
        return get_normalized_keyword(first) == get_normalized_keyword(second)
    else:
        return False


def get_normalized_keyword(keyword: str) -> str:
    return keyword.lower().replace(" ", "").replace("_", "")


def run_keyword_variant(resolve):
    def decorator(method):
        RUN_KW_REGISTER.register_run_keyword(
            "Browser", method.__name__, resolve, deprecation_warning=False
        )
        return method

    return decorator
