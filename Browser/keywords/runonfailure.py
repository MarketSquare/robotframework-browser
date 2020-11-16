# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-2020 Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Derived from https://github.com/robotframework/SeleniumLibrary and
# modified my René Rohner under
# Copyright 2020-     Robot Framework Foundation


from typing import Optional

from ..base import LibraryComponent
from ..utils import is_falsy, keyword, logger


class RunOnFailureKeywords(LibraryComponent):
    @keyword(tags=("Config",))
    def register_keyword_to_run_on_failure(
        self, keyword: Optional[str]
    ) -> Optional[str]:
        """Sets the keyword to execute, when a Browser keyword fails.

        ``keyword`` is the name of a keyword that will be executed if a
        Browser keyword fails. It is possible to use any available
        keyword, including user keywords or keywords from other libraries,
        but the keyword must not take any arguments.

        The initial keyword to use is set when `importing` the library, and
        the keyword that is used by default is `Take Screenshot`.
        Taking a screenshot when something failed is a very useful
        feature, but notice that it can slow down the execution.

        It is possible to use string ``NONE`` or any other robot falsy name,
        case-insensitively, as well as Python ``None`` to disable this
        feature altogether.

        This keyword returns the name of the previously registered
        failure keyword or Python ``None`` if this functionality was
        previously disabled. The return value can be always used to
        restore the original value later.

        Example:
        | `Register Keyword To Run On Failure`    Take Screenshot
        | ${previous kw}=    `Register Keyword To Run On Failure`    NONE
        | `Register Keyword To Run On Failure`    ${previous kw}

        """
        old_keyword = self.library.run_on_failure_keyword
        keyword = None if is_falsy(keyword) else keyword
        self.library.run_on_failure_keyword = keyword
        logger.info(f"{keyword or 'No keyword'} will be run on failure.")
        return old_keyword
