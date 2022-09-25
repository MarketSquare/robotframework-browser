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
from copy import copy, deepcopy
from datetime import timedelta
from time import sleep
from typing import TYPE_CHECKING, Any, Optional, Set, Union

from robot.utils import timestr_to_secs  # type: ignore

from ..utils import SettingsStack, get_variable_value, logger
from ..utils.data_types import DelayedKeyword, HighLightElement

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
        return self.library.timeout_stack.get()

    @property
    def timeout_stack(self) -> SettingsStack:
        return self.library.timeout_stack

    @timeout_stack.setter
    def timeout_stack(self, stack: SettingsStack):
        self.library.timeout_stack = stack

    @property
    def retry_assertions_for(self) -> float:
        return self.library.retry_assertions_for_stack.get()

    @property
    def retry_assertions_for_stack(self) -> SettingsStack:
        return self.library.retry_assertions_for_stack

    @retry_assertions_for_stack.setter
    def retry_assertions_for_stack(self, stack: SettingsStack):
        self.library.retry_assertions_for_stack = stack

    @property
    def selector_prefix(self) -> str:
        return self.library.selector_prefix_stack.get()

    @property
    def selector_prefix_stack(self) -> SettingsStack:
        return self.library.selector_prefix_stack

    @selector_prefix_stack.setter
    def selector_prefix_stack(self, stack: SettingsStack):
        self.library.selector_prefix_stack = stack

    def resolve_selector(self, selector: Optional[str]) -> str:
        if not selector:
            return ""
        if selector.startswith("!prefix "):
            logger.trace("Using selector prefix, but muting Prefix.")
            return selector[8:]
        if selector.startswith("element=") or not self.selector_prefix:
            return selector
        if selector.startswith(f"{self.selector_prefix} "):
            return selector
        logger.debug(
            f"Using selector prefix. Selector: '{self.selector_prefix} {selector}'"
        )
        return f"{self.selector_prefix} {selector}"

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
        return self.library.screenshots_output

    @property
    def video_output(self):
        return self.library.video_output

    @property
    def traces_output(self):
        return self.library.traces_output

    @property
    def state_file(self):
        return self.library.state_file

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
        if isinstance(placeholder, str) and len(placeholder) == 0:
            return placeholder
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

    @property
    def strict_mode(self) -> bool:
        return self.library.strict_mode_stack.get()

    @property
    def strict_mode_stack(self) -> SettingsStack:
        return self.library.strict_mode_stack

    @strict_mode_stack.setter
    def strict_mode_stack(self, stack: SettingsStack):
        self.library.strict_mode_stack = stack

    def parse_run_on_failure_keyword(
        self, keyword_name: Union[str, None]
    ) -> DelayedKeyword:
        return self.library._parse_run_on_failure_keyword(keyword_name)

    @property
    def keyword_formatters(self) -> dict:
        return self.library._keyword_formatters

    @property
    def get_presenter_mode(self) -> HighLightElement:
        mode: dict = {}
        if isinstance(self.library.presenter_mode, dict):
            mode = copy(self.library.presenter_mode)  # type: ignore
        duration = timedelta(seconds=timestr_to_secs(mode.get("duration", "2 seconds")))
        width = mode.get("width", "2px")
        style = mode.get("style", "dotted")
        color = mode.get("color", "blue")
        return {"duration": duration, "width": width, "style": style, "color": color}

    def presenter_mode(self, selector, strict):
        selector = self.resolve_selector(selector)
        if self.library.presenter_mode:
            mode = self.get_presenter_mode
            try:
                self.library.scroll_to_element(selector)
                self.library.highlight_elements(
                    selector,
                    duration=mode["duration"],
                    width=mode["width"],
                    style=mode["style"],
                    color=mode["color"],
                )
            except Exception as error:
                selector = self.library.record_selector(f'"{selector}" failure')
                logger.debug(f"On presenter more supress {error}")
            else:
                sleep(mode["duration"].seconds)
        return selector

    def exec_scroll_function(self, function: str, selector: Optional[str] = None):
        if selector:
            element_selector = "(element) => element"
        else:
            element_selector = "document.scrollingElement"
        return self.library.execute_javascript(
            f"{element_selector}.{function}", selector
        )
