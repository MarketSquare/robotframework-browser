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
"""Escaping of recorded values into Robot Framework data cells."""

from __future__ import annotations

import re

# Robot's variable/list/dict/environment syntax, which must not be resolved in
# a recorded literal.
VARIABLE_START = re.compile(r"[$@&%]\{")
_MULTI_SPACE = re.compile(r"  +")
# `txt=hello` in a Keyword Call is a named argument when `txt` is an argument name.
_NAMED_ARGUMENT = re.compile(r"^([^\W\d]\w*)=")


def cell(
    value: str, *, at_start: bool = True, at_end: bool = True, data: bool = False
) -> str:
    """Escape a recorded value so Robot reads it back as that exact string.

    Recorded selectors and texts are arbitrary strings, and several of them
    mean something to the Robot parser. All of these really occur:
    Playwright's recorder emits ``#id`` selectors (a leading ``#`` starts a
    comment, silently dropping the argument), typed text may contain
    ``${...}`` (variable syntax) or runs of two or more spaces (a cell
    separator).

    Unlike a keyword name an argument is legitimate user data - a filled
    form field really can hold a non-breaking space - so exotic whitespace
    is *escaped*, not rejected. Every whitespace character that is not a
    plain ASCII space becomes a ``\\uHHHH`` escape, which also closes the
    structural hole: U+2028 ends a line for ``str.splitlines()`` and U+00A0
    pairs up into a cell separator for Robot's unicode-aware tokenizer, so
    an unescaped one in a recorded selector would write a second executable
    keyword into the file.

    ``at_start`` / ``at_end`` say whether ``value`` begins / ends the whole
    cell. A value split around a Keyword Argument (`id-${n}`) is escaped part
    by part, and only the real cell edges need the `#`, edge-space and empty
    rules.

    ``data`` marks recorded data, as opposed to a selector or a fixed value
    such as ``action=accept``: an identifier followed by ``=`` at its start
    gets the ``=`` escaped, so ``txt=hello`` is not passed as a named argument.
    """
    if value == "":
        return "${EMPTY}" if at_start and at_end else ""
    cell = value.replace("\\", "\\\\")
    for char, escape in (("\t", "\\t"), ("\r", "\\r"), ("\n", "\\n")):
        cell = cell.replace(char, escape)
    cell = "".join(
        f"\\u{ord(char):04x}" if char.isspace() and char != " " else char
        for char in cell
    )
    cell = VARIABLE_START.sub(r"\\\g<0>", cell)
    if at_start and data:
        cell = _NAMED_ARGUMENT.sub(r"\1\\=", cell, count=1)
    if at_start and cell.startswith("#"):
        cell = "\\" + cell
    cell = _MULTI_SPACE.sub(lambda m: "${SPACE}" * len(m.group()), cell)
    if at_start and cell.startswith(" "):
        cell = "${SPACE}" + cell[1:]
    if at_end and cell.endswith(" "):
        cell = cell[:-1] + "${SPACE}"
    return cell
