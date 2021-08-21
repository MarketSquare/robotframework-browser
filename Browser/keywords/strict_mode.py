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
from ..utils import keyword, logger


class StrictMode(LibraryComponent):
    @keyword(tags=("Setter", "BrowserControl"))
    def set_strict_mode(self, mode: bool):
        """Controls library level strict mode.

        When set to ```True``, keyword that searching elements will use Playwright
        [https://playwright.dev/docs/api/class-page#page-query-selector|strict mode].
        Keyword changes library level default value, which can be overwritten in
        individual keywords by the keywords ``strict`` argument.
        """
        old_mode = self.strict_mode
        self.strict_mode = mode
        logger.debug(f"Old mode was {old_mode}")
        return old_mode
