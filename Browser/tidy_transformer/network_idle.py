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
import string

from robot.api.parsing import Token
from robot.parsing.model.statements import KeywordCall
from robotidy.transformers import Transformer  # type: ignore


def is_same_keyword(first: str, second: str) -> bool:
    if isinstance(first, str) and isinstance(second, str):
        return get_normalized_keyword(first) == get_normalized_keyword(second)
    return False


def get_normalized_keyword(keyword: str) -> str:
    if " " not in keyword:
        for index, char in enumerate(keyword):
            if index == 0:
                new_keyword = char.lower()
            elif char in string.ascii_uppercase and keyword[index - 1] != " ":
                new_keyword = f"{new_keyword} {char.lower()}"
            else:
                new_keyword = f"{new_keyword}{char}"
    else:
        new_keyword = keyword
    return new_keyword.lower().replace(" ", "_")


OLD_KW_NAME = "wait until network is idle"
OLD_KW_NAME_WITH_LIB = "browser.wait until network is idle"


class NetworkIdle(Transformer):
    def visit_KeywordCall(self, node: KeywordCall):  # noqa: N802
        keyword_token = node.get_token(Token.KEYWORD)
        if is_same_keyword(keyword_token.value, OLD_KW_NAME):
            return self._keyword_formatter(node, False)
        if is_same_keyword(keyword_token.value, OLD_KW_NAME_WITH_LIB):
            return self._keyword_formatter(node, True)
        return node

    def _keyword_formatter(self, node: KeywordCall, lib_name: bool):
        separator = self._get_separator(node)
        index = self._find_keyword_index(node)
        if lib_name:
            new_kw_token = Token(node.tokens[index].type, "Browser.Wait For Load State")
        else:
            new_kw_token = Token(node.tokens[index].type, "Wait For Load State")
        tokens = list(node.tokens[:index])
        tokens.append(new_kw_token)
        tokens.append(separator)
        tokens.append(Token(Token.ARGUMENT, "networkidle"))
        tokens.extend(list(node.tokens[index + 1 :]))
        return KeywordCall.from_tokens(tokens)

    def _find_keyword_index(self, node: KeywordCall) -> int:
        for index, token in enumerate(node.tokens):
            if is_same_keyword(token.value, OLD_KW_NAME) or is_same_keyword(
                token.value, OLD_KW_NAME_WITH_LIB
            ):
                return index
        raise ValueError(
            f"Could not find {OLD_KW_NAME} or ${OLD_KW_NAME_WITH_LIB} keyword."
        )

    def _timeout_present(self, node: KeywordCall):
        second_last_token = node.tokens[-2]
        return second_last_token.type == Token.ARGUMENT

    def _get_separator(self, node: KeywordCall) -> Token:
        return node.get_tokens(Token.SEPARATOR)[-1]
