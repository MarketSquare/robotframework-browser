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

from .network_idle import is_same_keyword

KW_NAME = "Upload File By Selector"
KW_NAME_WITH_LIB = "browser.Upload File By Selector"


class UploadFileBySelector(Transformer):

    def visit_KeywordCall(self, node: KeywordCall):  # noqa: N802
        keyword_token = node.get_token(Token.KEYWORD)
        if is_same_keyword(keyword_token.value, KW_NAME) or is_same_keyword(keyword_token.value, KW_NAME_WITH_LIB):
            return self._keyword_formatter(node, False)
        return node

    def _keyword_formatter(self, node: KeywordCall, lib_name: bool):
        path: str = node.tokens[2]
        if path.startswith("path="):
            node.tokens[2] = path[5:]
        return node
