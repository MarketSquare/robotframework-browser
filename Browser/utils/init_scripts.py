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


class InitScripts:
    def __init__(self):
        self._scopes: dict[tuple[str, str], str] = {}

    def added(self, context_id: str, script_id: str, scope_id: str | None) -> None:
        if scope_id is not None:
            self._scopes[(context_id, script_id)] = scope_id

    def end_scope(self, scope_id: str) -> list[tuple[str, str]]:
        ended = [key for key, owner in self._scopes.items() if owner == scope_id]
        for key in ended:
            del self._scopes[key]
        return ended
