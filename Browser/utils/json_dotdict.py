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

import base64
from collections import OrderedDict
from collections.abc import ItemsView
from typing import Any

from robot.utils import DotDict


class JsonDotDict(DotDict):
    """A ``DotDict`` that ``json.dumps`` can serialize even when it holds ``bytes``.

    ``json.dumps`` reads a dictionary subclass through ``items()``, so ``items()`` returns
    ``bytes`` values as base64 text. Key and attribute access, and copies, keep the real
    ``bytes``. Robot Framework's ``&{var} =`` assignment copies through ``items()`` too, so
    that variable holds the base64 text.
    """

    def items(self) -> ItemsView[Any, Any]:
        return {key: _base64_if_bytes(value) for key, value in super().items()}.items()

    def __reduce__(self):
        return (self.__class__, (), None, None, iter(OrderedDict.items(self)))


def _base64_if_bytes(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    return value
