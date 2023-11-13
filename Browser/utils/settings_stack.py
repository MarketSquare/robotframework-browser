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

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional

from .data_types import Scope

if TYPE_CHECKING:
    from ..browser import Browser


@dataclass
class ScopedSetting:
    typ: Scope
    setting: Any


class SettingsStack:
    def __init__(
        self,
        global_setting: Any,
        ctx: Browser,
        setter_function: Optional[Callable] = None,
    ):
        self.library = ctx
        self.setter_function = setter_function
        self._stack: dict[str, ScopedSetting] = {
            "g": ScopedSetting(Scope.Global, global_setting)
        }

    @property
    def _last_id(self) -> str:
        return list(self._stack.keys())[-1]

    @property
    def _last_setting(self) -> ScopedSetting:
        return list(self._stack.values())[-1]

    def start(self, identifier: str, typ: Scope):
        parent_setting = self._last_setting.setting
        self._stack[identifier] = ScopedSetting(typ, parent_setting)

    def end(self, identifier: str):
        previous = self._stack.pop(identifier, None)
        if (
            previous is not None
            and self.setter_function is not None
            and previous != self._last_setting
        ):
            self.setter_function(self._last_setting.setting)

    def set(self, setting: Any, scope: Optional[Scope] = Scope.Global):  # noqa: A003
        if not self.library.suite_ids:
            scope = Scope.Global
        original = self.get()
        if scope == Scope.Global:
            for value in self._stack.values():
                value.setting = setting
        elif scope == Scope.Suite or scope is None:
            if self._last_setting.typ == Scope.Test:
                self._stack.popitem()
            self._stack[list(self.library.suite_ids)[-1]] = ScopedSetting(
                Scope.Suite, setting
            )
        elif scope == Scope.Test:
            if not self.library.is_test_case_running:
                raise ValueError("Setting for test/task can not be set on suite level}")
            self._stack[self.library.current_test_id] = ScopedSetting(
                Scope.Test, setting
            )
        else:
            raise ValueError(f"Unknown scope {scope}")
        if self.setter_function and original != setting:
            self.setter_function(setting)
        return original

    def get(self):
        return self._last_setting.setting
