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

from concurrent.futures._base import Future
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from ..browser import Browser


class LibraryComponent:
    def __init__(self, library: "Browser") -> None:
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        """
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @property
    def timeout(self) -> str:
        return self.library.timeout

    @timeout.setter
    def timeout(self, value: str):
        self.library.timeout = value

    @property
    def retry_assertions_for(self) -> str:
        return self.library.retry_assertions_for

    @retry_assertions_for.setter
    def retry_assertions_for(self, value: str):
        self.library.retry_assertions_for = value

    @property
    def unresolved_promises(self):
        return self.library._unresolved_promises

    @unresolved_promises.setter
    def unresolved_promises(self, value: Set[Future]):
        self.library._unresolved_promises = value
