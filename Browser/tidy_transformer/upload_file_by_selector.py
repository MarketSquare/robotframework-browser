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


KW_NAME = "Upload File By Selector"
KW_NAME_WITH_LIB = "browser.Upload File By Selector"


class UploadFileBySelector(Transformer):

    def visit_KeywordCall(self, node: KeywordCall):  # noqa: N802
        keyword_token = node.get_token(Token.KEYWORD)
        if is_same_keyword(keyword_token.value, KW_NAME) or is_same_keyword(
            keyword_token.value, KW_NAME_WITH_LIB
        ):
            return self._keyword_formatter(node)
        return node

    def _keyword_formatter(self, node: KeywordCall):
        path = node.tokens[5]
        if path.value.startswith("path="):
            new_path = Token(path.type, path.value[5:])
        else:
            new_path = path
        tokens = list(node.tokens)
        tokens[5] = new_path
        return KeywordCall.from_tokens(tokens)
