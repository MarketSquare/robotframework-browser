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

import re
from typing import Any, Optional


def get_abs_scroll_coordinates(
    query: Any, scroll_size: int, min_str: str, max_str: str
):
    try:
        return int(round(float(query)))
    except ValueError:
        pass
    if isinstance(query, str):
        m = re.search(f"^(?:({min_str})|({max_str}))$", query, re.IGNORECASE)
        if m:
            return 0 if m.group(1) else scroll_size
        m = re.search(r"^(\d+(?:.\d+)?)%$", query)
        if m:
            return (scroll_size * float(m.group(1))) // 100
    raise ValueError(
        f"Argument must be positive int, percentage or string <{min_str}|{max_str}> but was {type(query)} with value `{query}`."
    )


def get_rel_scroll_coordinates(query: Any, full: int, client: int, dimension_str: str):
    try:
        return int(round(float(query)))
    except ValueError:
        pass
    if isinstance(query, str):
        m = re.search(f"^([-+]?)({dimension_str})$", query, re.IGNORECASE)
        if m:
            return int(f"{m.group(1)}{client}")
        m = re.search(r"^([+-]?\d+(?:.\d+)?)%$", query)
        if m:
            return (full * float(m.group(1))) // 100
    raise ValueError(
        f"Argument must be int, percentage or string <width|height> but was {type(query)} with value `{query}`."
    )


def exec_scroll_function(Browser, function: str, selector: Optional[str] = None):
    if selector:
        element_selector = "(element) => element"
    else:
        element_selector = "document.scrollingElement"
    return Browser.library.execute_javascript(
        f"{element_selector}.{function}", selector
    )
