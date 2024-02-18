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
from robot.api.parsing import Token
from robot.parsing.model.statements import KeywordCall
from robotidy.transformers import Transformer  # type: ignore

from Browser.utils.misc import is_same_keyword

OLD_KW_NAME = "wait until network is idle"


class NetworkIdle(Transformer):
    def visit_KeywordCall(self, node: KeywordCall):  # noqa: N802
        keyword_token = node.get_token(Token.KEYWORD)
        if is_same_keyword(keyword_token.value, OLD_KW_NAME):
            return self._keyword_formatter(node)
        return node

    def _keyword_formatter(self, node: KeywordCall):
        separator = self._get_separator(node)
        index = self._find_keyword_index(node)
        new_kw_token = Token(node.tokens[index].type, "Wait For Load State")
        tokens = list(node.tokens[:index])
        tokens.append(new_kw_token)
        tokens.append(separator)
        tokens.append(Token(Token.ARGUMENT, "networkidle"))
        tokens.extend(list(node.tokens[index + 1 :]))
        return KeywordCall.from_tokens(tokens)

    def _find_keyword_index(self, node: KeywordCall) -> int:
        for index, token in enumerate(node.tokens):
            if is_same_keyword(token.value, OLD_KW_NAME):
                return index
        raise ValueError(f"Could not find {OLD_KW_NAME} keyword.")

    def _timeout_present(self, node: KeywordCall):
        second_last_token = node.tokens[-2]
        return second_last_token.type == Token.ARGUMENT

    def _get_separator(self, node: KeywordCall) -> Token:
        return node.get_tokens(Token.SEPARATOR)[-1]
