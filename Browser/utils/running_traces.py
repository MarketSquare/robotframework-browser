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
from collections.abc import Iterable

from .data_types import TracingGroupMode


class RunningTraces:
    def __init__(self, group_mode: TracingGroupMode):
        self._group_mode = group_mode
        self._scopes: dict[str, str | None] = {}

    def __contains__(self, context_id: object) -> bool:
        return context_id in self._scopes

    @property
    def group_mode(self) -> TracingGroupMode:
        return self._group_mode

    @property
    def any_running(self) -> bool:
        return bool(self._scopes)

    @property
    def sends_groups(self) -> bool:
        return self.any_running and self._group_mode != TracingGroupMode.Playwright

    def started(self, context_id: str, scope_id: str | None = None) -> None:
        self._scopes[context_id] = scope_id

    def stopped(self, context_id: str) -> None:
        self._scopes.pop(context_id, None)

    def end_scope(self, scope_id: str) -> list[str]:
        ended = [
            context_id
            for context_id, trace_scope in self._scopes.items()
            if trace_scope == scope_id
        ]
        for context_id in ended:
            del self._scopes[context_id]
        return ended

    def keep_only(self, open_context_ids: Iterable[str]) -> None:
        open_ids = set(open_context_ids)
        self._scopes = {
            context_id: scope_id
            for context_id, scope_id in self._scopes.items()
            if context_id in open_ids
        }
