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
from ..base import LibraryComponent
from ..utils import Scope, keyword, logger


class StrictMode(LibraryComponent):
    @keyword(tags=("Setter", "BrowserControl"))
    def set_strict_mode(self, mode: bool, scope: Scope = Scope.Suite):
        """Controls library strict mode.

        | =Arguments= | =Description= |
        | ``mode`` | When set to ``True``, keywords that are searching elements will use Playwright [https://playwright.dev/docs/api/class-page#page-query-selector|strict mode]. Keyword changes library strict mode value and keyword also return the previous strict mode value. |
        | ``scope``   | Scope defines the live time of that setting. Available values are ``Global``, ``Suite`` or ``Test`` / ``Task``. See `Scope` for more details. |


        Example:
        | ${old_mode} =      Set Strict Mode    False
        | Get Text           //input            # Does not fail if selector points to one or more elements
        | Set Strict Mode    ${old_mode}

        [https://forum.robotframework.org/t//4332|Comment >>]
        """
        old_mode = self.strict_mode
        self.strict_mode_stack.set(mode, scope)
        logger.debug(f"Old mode was {old_mode}")
        return old_mode
