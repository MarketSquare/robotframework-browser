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
import re
import traceback
from concurrent.futures._base import Future
from copy import copy, deepcopy
from datetime import timedelta
from functools import cached_property
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import timestr_to_secs

from ..generated.playwright_pb2 import Response
from ..utils import SettingsStack, get_variable_value, logger
from ..utils.data_types import (
    AutoClosingLevel,
    DelayedKeyword,
    HighLightElement,
)

if TYPE_CHECKING:
    from ..browser import Browser

NOT_FOUND = object()


class LibraryComponent:
    def __init__(self, library: "Browser") -> None:
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        """
        self.library = library
        self._crypto: Optional[Any] = None
        self.browser_arg_mapping: dict[int, str] = {}

    @property
    def playwright(self):
        return self.library.playwright

    @property
    def _auto_closing_level(self) -> AutoClosingLevel:
        return self.library._auto_closing_level

    @property
    def keyword_call_banner_add_style(self) -> str:
        return self.library.scope_stack["keyword_call_banner_add_style"].get()

    @property
    def keyword_call_banner_add_style_stack(self) -> SettingsStack:
        return self.library.scope_stack["keyword_call_banner_add_style"]

    @keyword_call_banner_add_style_stack.setter
    def keyword_call_banner_add_style_stack(self, stack: SettingsStack):
        self.library.scope_stack["keyword_call_banner_add_style"] = stack

    @property
    def show_keyword_call_banner(self) -> bool:
        return self.library.scope_stack["show_keyword_call_banner"].get()

    @property
    def show_keyword_call_banner_stack(self) -> SettingsStack:
        return self.library.scope_stack["show_keyword_call_banner"]

    @show_keyword_call_banner_stack.setter
    def show_keyword_call_banner_stack(self, stack: SettingsStack):
        self.library.scope_stack["show_keyword_call_banner"] = stack

    @property
    def run_on_failure_keyword(self) -> DelayedKeyword:
        return self.library.scope_stack["run_on_failure"].get()

    @property
    def run_on_failure_keyword_stack(self) -> SettingsStack:
        return self.library.scope_stack["run_on_failure"]

    @run_on_failure_keyword_stack.setter
    def run_on_failure_keyword_stack(self, stack: SettingsStack):
        self.library.scope_stack["run_on_failure"] = stack

    @property
    def assertion_formatter_stack(self) -> SettingsStack:
        return self.library.scope_stack["assertion_formatter"]

    @assertion_formatter_stack.setter
    def assertion_formatter_stack(self, stack: SettingsStack):
        self.library.scope_stack["assertion_formatter"] = stack

    def get_assertion_formatter(self, keyword: str) -> list:
        return self.library._get_assertion_formatter(keyword)

    def method_to_kw_str(self, keyword: Callable) -> str:
        return self.library._assertion_formatter.method_to_kw_str(keyword)

    @property
    def timeout(self) -> float:
        return self.library.scope_stack["timeout"].get()

    @property
    def timeout_stack(self) -> SettingsStack:
        return self.library.scope_stack["timeout"]

    @timeout_stack.setter
    def timeout_stack(self, stack: SettingsStack):
        self.library.scope_stack["timeout"] = stack

    @property
    def retry_assertions_for(self) -> float:
        return self.library.scope_stack["retry_assertions_for"].get()

    @property
    def retry_assertions_for_stack(self) -> SettingsStack:
        return self.library.scope_stack["retry_assertions_for"]

    @retry_assertions_for_stack.setter
    def retry_assertions_for_stack(self, stack: SettingsStack):
        self.library.scope_stack["retry_assertions_for"] = stack

    @property
    def selector_prefix(self) -> str:
        return self.library.scope_stack["selector_prefix"].get()

    @property
    def selector_prefix_stack(self) -> SettingsStack:
        return self.library.scope_stack["selector_prefix"]

    @selector_prefix_stack.setter
    def selector_prefix_stack(self, stack: SettingsStack):
        self.library.scope_stack["selector_prefix"] = stack

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
    def unresolved_promises(self, value: set[Future]):
        self.library._unresolved_promises = value

    @property
    def context_cache(self):
        return self.library._context_cache

    @property
    def outputdir(self) -> str:
        return self.library.outputdir

    @property
    def browser_output(self) -> Path:
        return self.library.browser_output

    @property
    def screenshots_output(self) -> Path:
        return self.library.screenshots_output

    @property
    def video_output(self) -> Path:
        return self.library.video_output

    @property
    def traces_output(self) -> Path:
        return self.library.traces_output

    @property
    def traces_temp(self) -> Path:
        return self.library.traces_temp

    @property
    def state_file(self):
        return self.library.state_file

    @property
    def coverage_ouput(self) -> Path:
        return self.library.coverage_output

    def initialize_js_extension(
        self, js_extension_path: Union[Path, str]
    ) -> Response.Keywords:
        return self.library.init_js_extension(js_extension_path=js_extension_path)

    def call_js_keyword(self, keyword_name: str, **args) -> Any:
        return self.library.call_js_keyword(keyword_name, **args)

    def get_timeout(self, timeout: Union[timedelta, None]) -> float:
        return self.library.get_timeout(timeout)

    def convert_timeout(
        self, timeout: Union[timedelta, float], to_ms: bool = True
    ) -> float:
        return self.library.convert_timeout(timeout, to_ms)

    def millisecs_to_timestr(self, timeout: float) -> str:
        return self.library.millisecs_to_timestr(timeout)

    @cached_property
    def robot_running(self):
        try:
            get_variable_value("${EXECDIR}")
        except RobotNotRunningError:
            return False
        return True

    def resolve_secret(self, secret_variable: Any, arg_name: str) -> str:
        secret = self._replace_placeholder_variables(deepcopy(secret_variable))
        secret = self.decrypt_with_crypto_library(secret)
        if secret == secret_variable and self.robot_running:
            raise ValueError(
                f"Direct assignment of values or variables as '{arg_name}' is not allowed. "
                "Use special variable syntax ($var instead of ${var}) "
                "to prevent variable values from being spoiled."
            )
        return secret

    def decrypt_with_crypto_library(self, secret):
        if not isinstance(secret, str) or not re.match(r"^crypt:(.*)", secret):
            return secret
        logger.trace("CryptoLibrary string pattern found.")
        self._import_crypto_library()
        if self._crypto:
            try:
                plain_text = self._crypto.decrypt_text(secret)
                logger.trace("Successfully decrypted secret with CryptoLibrary.")
                return plain_text
            except Exception as excep:
                logger.warn(excep)
                logger.trace(traceback.format_exc())
        return secret

    def _import_crypto_library(self):
        if self._crypto is None:
            try:
                try:
                    logger.trace(
                        "Trying to import CryptoLibrary instance from Robot Framework."
                    )
                    crypto_library = BuiltIn().get_library_instance("CryptoLibrary")
                    self._crypto = crypto_library.crypto
                except RuntimeError:
                    logger.trace(
                        "Getting CryptoLibrary failed, trying to import directly."
                    )
                    from CryptoLibrary.utils import CryptoUtility  # type: ignore

                    self._crypto = CryptoUtility()
            except ImportError:
                logger.trace(traceback.format_exc())
                logger.trace("CryptoLibrary import failed, using plain string.")
                self._crypto = False
                return
            logger.trace("CryptoLibrary import succeeded.")

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
        return self.library.scope_stack["strict_mode"].get()

    @property
    def strict_mode_stack(self) -> SettingsStack:
        return self.library.scope_stack["strict_mode"]

    @strict_mode_stack.setter
    def strict_mode_stack(self, stack: SettingsStack):
        self.library.scope_stack["strict_mode"] = stack

    def parse_run_on_failure_keyword(
        self, keyword_name: Union[str, None]
    ) -> DelayedKeyword:
        return self.library._parse_run_on_failure_keyword(keyword_name)

    @property
    def keyword_formatters(self) -> dict:
        return self.library._keyword_formatters

    @property
    def get_presenter_mode(self) -> HighLightElement:
        mode: Union[HighLightElement, dict] = {}
        if isinstance(self.library.presenter_mode, dict):
            mode = copy(self.library.presenter_mode)
        duration = mode.get("duration", "2 seconds")
        if not isinstance(duration, timedelta):
            duration = timedelta(seconds=timestr_to_secs(duration))
        width = mode.get("width", "2px")
        style = mode.get("style", "dotted")
        color = mode.get("color", "blue")
        return HighLightElement(
            duration=duration, width=width, style=style, color=color
        )

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
        return self.library.evaluate_javascript(
            selector, f"{element_selector}.{function}"
        )
