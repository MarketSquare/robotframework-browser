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
from collections.abc import Collection

from robot.api.parsing import Token
from robot.errors import DataError

# Robot's variable/list/dict/environment syntax, and the `*{` it reserves for
# future use, none of which may be resolved in a recorded literal.
VARIABLE_START = re.compile(r"[$@&%*]\{")
_SPACES = re.compile(r" +")
# `txt=hello` in a Keyword Call is a named argument when `txt` is an argument name.
_NAMED_ARGUMENT = re.compile(r"^([^\W\d]\w*)=")


def cell(
    value: str,
    *,
    at_start: bool = True,
    at_end: bool = True,
    parameters: Collection[str] | None = (),
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

    ``parameters`` are the names the called keyword accepts as named
    arguments: ``txt=hello`` gets its ``=`` escaped when ``txt`` is one of
    them, so it is not passed as a named argument. ``None`` means the keyword
    is unknown, and every identifier followed by ``=`` is escaped.

    Spaces Robot would strip or read as a separator are escaped with
    backslashes: ``\\ \\ lead``, ``a \\ b``, ``trail \\ \\``.
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
    if at_start:
        cell = _escape_named_argument(cell, parameters)
    if at_start and cell.startswith("#"):
        cell = "\\" + cell
    return _SPACES.sub(lambda m: _escaped_spaces(m, cell, at_start, at_end), cell)


def _escaped_spaces(run: re.Match, cell: str, at_start: bool, at_end: bool) -> str:
    r"""A run of spaces, written so that no two plain spaces meet.

    At the start of a cell the run begins with a backslash (``\ \ a``), at
    its end it ends with one (``a \ \``): Robot strips spaces at cell edges,
    and a backslash before the next separator or the line end is dropped. A
    cell of spaces only gets both (``\ \ \``). Inside a cell only runs of two
    or more change: ``a \ b``.
    """
    count = len(run.group())
    starts = at_start and run.start() == 0
    ends = at_end and run.end() == len(cell)
    if starts:
        return "\\ " * count + ("\\" if ends else "")
    if ends:
        return " \\" * count
    if count == 1:
        return " "
    return " " + "\\ " * (count - 1)


def tokens(cell: str) -> list[tuple[str, str]]:
    r"""How Robot reads a written cell: its ``argument`` and ``variable`` parts.

    Robot's own tokenizer, so escapes count as Robot counts them: ``\${x}`` is
    an argument, ``${SPACE}`` a variable.
    """
    try:
        parts = Token(Token.ARGUMENT, cell).tokenize_variables()
        return [
            ("variable" if token.type == Token.VARIABLE else "argument", token.value)
            for token in parts
        ]
    except DataError:
        # Partial syntax like an unclosed `${x`, which `cell()` never writes; shown
        # uncoloured if one turns up anyway.
        return [("argument", cell)]


def _escape_named_argument(cell: str, parameters: Collection[str] | None) -> str:
    match = _NAMED_ARGUMENT.match(cell)
    if match is None:
        return cell
    if parameters is not None and _normalized(match.group(1)) not in {
        _normalized(name) for name in parameters
    }:
        return cell
    return f"{match.group(1)}\\={cell[match.end() :]}"


def _normalized(name: str) -> str:
    return name.lower().replace("_", "")
