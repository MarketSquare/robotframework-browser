from dataclasses import dataclass
from typing import Any, Dict

from .data_types import Scope


@dataclass
class ScopedSetting:
    typ: Scope
    setting: Any


class SettingsStack:
    def __init__(self, global_setting):
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

    def set(self, setting: Any, scope: Scope = Scope.Global):
        if scope == Scope.Global:
            self._stack = {"g": ScopedSetting(Scope.Global, setting)}
        elif scope == Scope.Suite:
            if self._last_setting.typ == Scope.Test:
                self._stack.popitem()
            self._stack[self._last_id] = ScopedSetting(Scope.Suite, setting)
        elif scope == Scope.Test:
            if self._last_setting.typ != Scope.Test:
                raise ValueError("Setting for test/task can not be set on suite level}")
            self._stack[self._last_id] = ScopedSetting(Scope.Test, setting)

    def get(self):
        return self._last_setting.setting
