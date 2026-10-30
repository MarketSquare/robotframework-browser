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
"""Which frames a Browser selector crosses, read as the Node side splits it.

The splitting rules mirror ``splitSelector`` in
``node/playwright-wrapper/selector-syntax.ts``: clauses are separated at ``>>``
outside quotes, an unquoted ``text=`` or ``label=`` body reads quotes as text,
and ``>>>`` is a frame boundary only with whitespace, or the start or end,
around it.
"""

from __future__ import annotations

import re

_QUOTES = {'"', "'", "`"}
_UNQUOTED_TEXT = re.compile(r"^\s*text\s*=(.+)$")
_UNQUOTED_LABEL = re.compile(r"""^\s*\*?label\s*=\s*[^\s"'/]""")
_FRAME_ENGINES = ("internal:control=enter-frame", "internal:control=any-frame")


def split_selector(selector: str) -> tuple[list[str], list[str]]:
    """The clauses of ``selector`` and the separators (``>>`` or ``>>>``) between them."""
    clauses: list[str] = []
    separators: list[str] = []
    index = start = 0
    quote: str | None = None
    while index < len(selector):
        char = selector[index]
        if char == "\\" and index + 1 < len(selector):
            index += 2
        elif char == quote:
            quote = None
            index += 1
        elif (
            not quote and char in _QUOTES and not _unquoted_body(selector[start:index])
        ):
            quote = char
            index += 1
        elif not quote and selector.startswith(">>", index):
            frame = (
                selector.startswith(">>>", index)
                and (index == 0 or selector[index - 1].isspace())
                and (index + 3 >= len(selector) or selector[index + 3].isspace())
            )
            clauses.append(selector[start:index])
            separators.append(">>>" if frame else ">>")
            index += 3 if frame else 2
            start = index
        else:
            index += 1
    clauses.append(selector[start:])
    return clauses, separators


def crosses_frames(selector: str) -> bool:
    """Whether ``selector`` enters a frame: ``>>>``, or a Playwright frame clause
    as in an element reference from `Get Element`."""
    clauses, separators = split_selector(selector)
    return ">>>" in separators or any(
        clause.strip().startswith(_FRAME_ENGINES) for clause in clauses
    )


def _unquoted_body(prefix: str) -> bool:
    return bool(_UNQUOTED_TEXT.match(prefix) or _UNQUOTED_LABEL.match(prefix))
