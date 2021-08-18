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
import os
from concurrent.futures._base import Future
from copy import deepcopy
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Set, Union

from ..utils import get_variable_value, logger

if TYPE_CHECKING:
    from ..browser import Browser

NOT_FOUND = object()


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
        return self.library.browser_output

    @property
    def screenshots_output(self):
        return self.browser_output / "screenshot"

    @property
    def video_output(self):
        return self.browser_output / "video"

    @property
    def traces_output(self):
        return self.browser_output / "traces"

    @property
    def state_file(self):
        return self.browser_output / "state"

    def get_timeout(self, timeout: Union[timedelta, None]) -> float:
        return self.library.get_timeout(timeout)

    def convert_timeout(
        self, timeout: Union[timedelta, float], to_ms: bool = True
    ) -> float:
        return self.library.convert_timeout(timeout, to_ms)

    def millisecs_to_timestr(self, timeout: float) -> str:
        return self.library.millisecs_to_timestr(timeout)

    def resolve_secret(
        self, secret_variable: Any, original_secret: Any, arg_name: str
    ) -> str:
        secret = self._replace_placeholder_variables(deepcopy(secret_variable))
        if secret == original_secret:
            logger.warn(
                f"Direct assignment of values as '{arg_name}' is deprecated. Use special "
                "variable syntax to resolve variable. Example $var instead of ${var}."
            )
        return secret

    def _replace_placeholder_variables(self, placeholder):
        if isinstance(placeholder, dict):
            for key in placeholder:
                placeholder[key] = self._replace_placeholder_variable(placeholder[key])
            return placeholder
        return self._replace_placeholder_variable(placeholder)

    def _replace_placeholder_variable(self, placeholder):
        if not isinstance(placeholder, str) or placeholder[:1] not in "$%":
            return placeholder
        if placeholder.startswith("%"):
            value = os.environ.get(placeholder[1:], NOT_FOUND)
        else:
            value = get_variable_value(placeholder, NOT_FOUND)
        if value is NOT_FOUND:
            logger.warn("Given variable placeholder could not be resolved.")
            return placeholder
        return value
