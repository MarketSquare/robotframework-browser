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

import json
from collections.abc import Callable
from typing import get_args

from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.types import Secret

SECRET_ARGUMENT = "secret"
SECRET_MASK = "***"
BANNER_MUTED_KEYWORDS = ("take_screenshot", "get_page_source")

KW_CALL_CONTENT_TEMPLATE = """body::before {{
    content: '{keyword_call}';
    position: fixed;
    z-index: 9999;
    border: 1px solid lightblue;
    border-radius: 1rem;
    background: #00008b90;
    color: white;
    padding: 2px 10px;
    pointer-events: none;
    font-family: monospace;
    font-size: medium;
    font-weight: normal;
    white-space: pre;
    bottom: 5px;
    left: 5px;
    {additional_styles}
}}"""

KW_CALL_BANNER_FUNCTION = """(content) => {
    const kwCallBanner = document.getElementById('kwCallBanner');
    if (kwCallBanner) {
        kwCallBanner.textContent = content;
    } else {
        const kwCallBanner = document.createElement("style");
        kwCallBanner.setAttribute("id", 'kwCallBanner');
        kwCallBanner.textContent = content;
        document.head.appendChild(kwCallBanner);
    }
}"""


class KeywordCallObserver(LibraryComponent):
    """Paints the keyword call banner and hides secrets while a keyword runs.

    Both decisions are made on the resolved Python function rather than the
    displayed keyword name, so an aliased or translated import behaves like a
    plain one.
    """

    def __init__(self, library):
        super().__init__(library)
        self._secret_arguments: dict[str, set[str]] = {}
        self._current_loglevel: str | None = None
        self._logging_suppressions = 0

    def is_secret_keyword(self, name: str) -> bool:
        return bool(self._secret_argument_names(name))

    def suppress_logging(self):
        self._set_logging(False)

    def restore_logging(self):
        self._set_logging(True)

    def show(self, name: str):
        if not self._banner_enabled() or not self.library.keyword_call_stack:
            return
        try:
            if self._is_banner_muted_keyword(name):
                self.set_banner()
                return
            entry = self.library.keyword_call_stack[-1]
            content = self._banner_content(name, entry["kwname"], entry["args"])
            if not self.is_secret_keyword(name):
                # Robot Framework returns the value itself, not a string, when
                # the text is exactly one variable. The banner content always
                # starts with the keyword name, so this one is always a string.
                content = str(BuiltIn().replace_variables(content))
            self.set_banner(content)
        except Exception as error:
            logger.trace(f"Keyword call banner could not be painted: {error}")

    def set_banner(self, keyword_call=None):
        if keyword_call:
            keyword_call = keyword_call.replace("'", "\\'")
            content = KW_CALL_CONTENT_TEMPLATE.format(
                keyword_call=keyword_call,
                additional_styles=self.keyword_call_banner_add_style,
            )
        else:
            content = "body::before{}"
        with self.playwright.grpc_channel() as stub:
            stub.EvaluateJavascript(
                Request().EvaluateAll(
                    selector="",
                    script=KW_CALL_BANNER_FUNCTION,
                    arg=json.dumps(content),
                    allElements=False,
                    strict=False,
                )
            )

    def _set_logging(self, status: bool):
        try:
            context = BuiltIn()._context.output
        except DataError:
            context = BuiltIn()
        if status:
            self._logging_suppressions = max(0, self._logging_suppressions - 1)
            if self._logging_suppressions == 0 and self._current_loglevel:
                context.set_log_level(self._current_loglevel)
                self._current_loglevel = None
        else:
            if self._logging_suppressions == 0:
                self._current_loglevel = context.set_log_level("NONE")
            self._logging_suppressions += 1

    def _resolve_keyword_function(self, name: str) -> Callable | None:
        """A translation replaces the registered name, the function stays the same."""
        return self.library.keywords.get(name)

    def _keyword_argument_names(self, name: str) -> list[str]:
        try:
            arguments = self.library.get_keyword_arguments(name)
        except Exception:
            return []
        names = [
            argument[0] if isinstance(argument, tuple) else argument
            for argument in arguments
        ]
        return [argument for argument in names if not argument.startswith("*")]

    def _secret_argument_names(self, name: str) -> set[str]:
        if name not in self._secret_arguments:
            self._secret_arguments[name] = self._find_secret_arguments(name)
        return self._secret_arguments[name]

    def _find_secret_arguments(self, name: str) -> set[str]:
        """Both rules are needed: the annotation misses a plugin that types its
        secret as a string, the name misses `Create Credential`, whose secrets
        are called ``privateKey`` and ``publicKey``.
        """
        if self._resolve_keyword_function(name) is None:
            return set()
        secret_arguments = {
            argument
            for argument in self._keyword_argument_names(name)
            if argument == SECRET_ARGUMENT
        }
        try:
            argument_types = self.library.get_keyword_types(name) or {}
        except Exception:
            argument_types = {}
        secret_arguments.update(
            argument
            for argument, annotation in argument_types.items()
            if annotation is Secret or Secret in get_args(annotation)
        )
        return secret_arguments

    def _is_banner_muted_keyword(self, name: str) -> bool:
        function = self._resolve_keyword_function(name)
        return function is not None and function.__name__ in BANNER_MUTED_KEYWORDS

    def _mask_secret_arguments(self, name: str, args: list[str]) -> list[str]:
        """Counting positions is only correct because Robot Framework rejects a
        positional argument that follows a named one, so every cell before the
        first named argument fills its parameter in declaration order.
        """
        secret_arguments = self._secret_argument_names(name)
        if not secret_arguments:
            return list(args)
        argument_names = self._keyword_argument_names(name)
        masked = []
        position = 0
        for arg in args:
            argument_name, separator, _ = arg.partition("=")
            if separator and argument_name in argument_names:
                masked.append(
                    f"{argument_name}={SECRET_MASK}"
                    if argument_name in secret_arguments
                    else arg
                )
                continue
            is_secret = (
                position < len(argument_names)
                and argument_names[position] in secret_arguments
            )
            masked.append(SECRET_MASK if is_secret else arg)
            position += 1
        return masked

    def _banner_content(self, name: str, kwname: str, args: list[str]) -> str:
        """Resolving the variables is left to the caller, so that a masked secret
        can never be resolved back into the banner.
        """
        masked = self._mask_secret_arguments(name, args)
        return f"{kwname}{'    ' * bool(masked)}{'    '.join(masked)}"

    def _banner_enabled(self) -> bool:
        if self.library.show_keyword_call_banner is None:
            return bool(self.library.presenter_mode)
        return bool(self.library.show_keyword_call_banner)
