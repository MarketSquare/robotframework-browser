from dataclasses import dataclass
from typing import Any, Dict, Optional

from .data_types import Scope


@dataclass
class ScopedSetting:
    typ: Scope
    setting: Any


class SettingsStack:
    def __init__(self, global_setting, ctx):
        self.library = ctx
        self._stack: Dict[str, ScopedSetting] = {
            "g": ScopedSetting(Scope.Global, global_setting)
        }

    @property
    def _last_id(self) -> str:
        return list(self._stack.keys())[-1]

    @property
    def _last_setting(self) -> ScopedSetting:
        return list(self._stack.values())[-1]

    def start(self, id: str, typ: Scope):
        parent_setting = self._last_setting.setting
        self._stack[id] = ScopedSetting(typ, parent_setting)

    def end(self, id):
        self._stack.pop(id, None)

    def set(self, setting: Any, scope: Optional[Scope] = Scope.Global):
        original = self.get()
        if scope == Scope.Global:
            for value in self._stack.values():
                value.setting = setting
        elif scope == Scope.Suite:
            if self._last_setting.typ == Scope.Test:
                self._stack.popitem()
            self._stack[self._last_id] = ScopedSetting(Scope.Suite, setting)
        elif scope == Scope.Test:
            if not self.library.is_test_case_running:
                raise ValueError("Setting for test/task can not be set on suite level}")
            self._stack[self._last_id] = ScopedSetting(Scope.Test, setting)
        else:
            self._stack[self._last_id] = ScopedSetting(self._last_setting.typ, setting)
        return original

    def get(self):
        return self._last_setting.setting
