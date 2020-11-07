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
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Set, Union

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
    def timeout(self) -> float:
        return self.library.timeout

    @timeout.setter
    def timeout(self, value: float):
        self.library.timeout = value

    @property
    def retry_assertions_for(self) -> float:
        return self.library.retry_assertions_for

    @retry_assertions_for.setter
    def retry_assertions_for(self, value: float):
        self.library.retry_assertions_for = value

    @property
    def unresolved_promises(self):
        return self.library._unresolved_promises

    @unresolved_promises.setter
    def unresolved_promises(self, value: Set[Future]):
        self.library._unresolved_promises = value

    @property
    def context_cache(self):
        return self.library._context_cache

    @property
    def outputdir(self) -> str:
        return self.library.outputdir

    @property
    def browser_output(self):
        return Path(self.outputdir, "browser")

    @property
    def screenshots_output(self):
        return self.browser_output / "screenshot"

    @property
    def video_output(self):
        return self.browser_output / "video"

    def get_timeout(self, timeout: Union[timedelta, None]) -> float:
        return self.library.get_timeout(timeout)

    def convert_timeout(self, timeout: Union[timedelta, float]) -> float:
        return self.library.convert_timeout(timeout)

    def millisecs_to_timestr(self, timeout: float) -> str:
        return self.library.millisecs_to_timestr(timeout)
