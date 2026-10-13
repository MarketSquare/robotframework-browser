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
"""Write a recorded User Keyword into a ``.robot`` / ``.resource`` file.

Uses the Robot Framework parsing API (AST) so existing file content and
formatting are preserved. The target keyword is created once; every recorded
action appends one ``KeywordCall`` to it and the whole model is saved again -
so the file is updated *live*, one line per action.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

from robot.api import get_model
from robot.api.parsing import (
    EmptyLine,
    KeywordCall,
    KeywordName,
    SectionHeader,
    Token,
)
from robot.parsing.model.blocks import File, Keyword, KeywordSection
from robot.utils import normalize

_INDENT = "    "
_EOL = "\n"

# Robot's variable/list/dict/environment syntax, which must not be resolved in
# a recorded literal.
_VARIABLE_START = re.compile(r"[$@&%]\{")
_MULTI_SPACE = re.compile(r"  +")
# Anything Robot cannot carry inside a single keyword-name cell. A newline in
# particular would end the row and let the rest of the "name" be parsed as
# further Robot source.
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f]")
# Two adjacent whitespace characters of *any* kind. Robot's own tokenizer uses
# `re.compile(r"(\s{2,}|\t)", re.UNICODE)` to split cells, so `\s` here has to
# have exactly the same unicode semantics - matching only ASCII spaces would
# let U+00A0, U+3000 and friends through as a separator Robot still honours.
_ANY_DOUBLE_WHITESPACE = re.compile(r"\s\s")
# A pipe surrounded by whitespace separates cells in Robot's pipe-separated
# format.
_PIPE_SEPARATOR = re.compile(r"\s\|\s")


def _surrogates(name: str) -> bool:
    """True if ``name`` cannot be written to a UTF-8 file.

    A lone surrogate (``\\ud800``) survives every structural check above and
    only blows up inside ``model.save()`` with a ``UnicodeEncodeError``, which
    used to abort the whole recording session.
    """
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        return True
    return False


#: Shapes Robot's lexer would read as something other than one plain name cell,
#: in the order they are reported. Checked after `_exotic_whitespace_error`,
#: which needs the offending character for its message.
_NAME_RULES: tuple[tuple[Callable[[str], object], str], ...] = (
    (lambda name: not name, "Keyword name must not be empty."),
    (_surrogates, "Keyword name must not contain unpaired surrogate characters."),
    (
        _CONTROL_CHARS.search,
        "Keyword name must not contain control characters such as newlines or tabs.",
    ),
    (
        lambda name: name != name.strip(),
        "Keyword name must not start or end with whitespace.",
    ),
    (
        _ANY_DOUBLE_WHITESPACE.search,
        "Keyword name must not contain two or more consecutive spaces.",
    ),
    (
        lambda name: name.startswith(("#", "*", "|")),
        "Keyword name must not start with '#', '*' or '|'.",
    ),
    (
        _PIPE_SEPARATOR.search,
        "Keyword name must not contain a '|' surrounded by spaces.",
    ),
    # `...` is Robot's continuation marker: the row folds into the section
    # header instead of defining a keyword, and the recorded steps become an
    # unnamed keyword that makes the whole file unimportable.
    (
        lambda name: name == "...",
        "Keyword name must not be Robot's continuation marker '...'.",
    ),
    # `${...}` in a *name* declares embedded arguments, so `${a} ${b}` matches
    # every two-word keyword call in the suite - `No Operation` included - and
    # silently runs the recorded body instead. An *unclosed* `${` is the other
    # half of the same hole: Robot refuses to create the keyword and the
    # recorded steps are lost. Neither shape has any legitimate use in a
    # recorded name, so all of Robot's variable openers are rejected.
    (
        _VARIABLE_START.search,
        (
            "Keyword name must not contain Robot Framework variable syntax "
            "such as '${...}'."
        ),
    ),
)


def _exotic_whitespace_error(name: str) -> str | None:
    """Reject every whitespace character except a plain ASCII space.

    ``str.isspace()`` is exactly the set Robot's unicode-aware ``\\s`` and
    ``str.splitlines()`` react to, so this one check covers U+0085, U+00A0,
    U+2028, U+2029, U+3000, the C0/C1 separators and the rest at once.
    """
    for char in name:
        if char.isspace() and char != " ":
            return (
                "Keyword name must not contain whitespace other than a plain "
                f"space (found U+{ord(char):04X})."
            )
    return None


def keyword_name_error(name: str) -> str | None:
    """Why ``name`` is unusable as a User Keyword name, or ``None`` if it is fine.

    A keyword name is written into the file verbatim - it cannot be escaped the
    way an argument cell can, because escapes would become part of the name a
    caller has to type. So the shapes that would change the *structure* of the
    written file are rejected outright instead. This matters beyond typos: the
    ``new`` command arrives over a page-callable binding, so a hostile page
    could otherwise smuggle whole Robot statements into the user's source file
    through a keyword name.

    The rules mirror what the Robot lexer actually does, not what looks
    dangerous: it splits cells on ``\\s{2,}`` with *unicode* semantics, splits
    lines with ``str.splitlines()`` (which breaks on U+0085, U+2028, U+2029 and
    the C1 separators as well as ``\\n``), and switches a line to the
    pipe-separated format when it starts with ``|``. Every whitespace character
    other than a plain ASCII space is therefore rejected outright - a name is
    the one place where nothing can be escaped.
    """
    if not isinstance(name, str):
        return "Keyword name must be a string."
    exotic = _exotic_whitespace_error(name)
    if exotic:
        return exotic
    for is_unusable, message in _NAME_RULES:
        if is_unusable(name):
            return message
    return None


def normalize_keyword_name(name: str) -> str:
    """The form Robot itself compares keyword names in.

    Robot resolves a keyword call case-insensitively and ignoring spaces and
    underscores, so ``l_ogin as admin`` and ``Login As Admin`` are the *same*
    keyword to it. Any duplicate or collision check that compares raw strings
    therefore lets through names that Robot will later reject as duplicates -
    breaking the user's pre-existing keyword.
    """
    return normalize(name, ignore="_", caseless=True, spaceless=True)


def existing_keyword_names(target: Path) -> set[str]:
    """Names of the User Keywords already defined in ``target``."""
    target = Path(target)
    if not target.exists():
        return set()
    names: set[str] = set()
    for section in get_model(str(target)).sections:
        if isinstance(section, KeywordSection):
            names.update(
                item.name
                for item in section.body
                if isinstance(item, Keyword) and item.name
            )
    return names


class LiveKeywordWriter:
    """Append a User Keyword to a file, saving after every added statement."""

    def __init__(self, target: Path, keyword_name: str) -> None:
        self.target = Path(target)
        self.keyword_name = keyword_name
        self._statements: list[tuple[str, list[str]]] = []
        self.reused = False
        self.created_section = False
        # EmptyLine nodes this writer inserted as separators, removed again on
        # discard so an abandoned recording leaves no trace.
        self._section_separator: tuple[object, EmptyLine] | None = None
        self._keyword_separator: EmptyLine | None = None
        self._model: File = self._load_or_create_model()
        found = self._find_keyword()
        if found is not None:
            # A file may hold several `*** Keywords ***` sections; the keyword
            # must be reused wherever it lives, or Robot sees a duplicate.
            self._section, self._keyword = found
            self.reused = True
        else:
            self._section = self._ensure_keyword_section()
            self._keyword = self._create_keyword_block()

    # -- public API -------------------------------------------------------- #

    def append(self, keyword: str, args: list[str]) -> None:
        """Add ``keyword    args...`` to the recorded keyword and save the file."""
        self._keyword.body.append(self._keyword_call(keyword, args))
        self._statements.append((keyword, args))
        self.save()

    def replace_last(self, keyword: str, args: list[str]) -> None:
        """Overwrite the most recently recorded call and save the file.

        Playwright's recorder refines an action in place instead of adding a new
        one (every keystroke of a ``fill``, a single click becoming a double
        click). Only calls written by *this* writer are replaced - if nothing has
        been recorded yet this appends, so pre-existing body content of a reused
        keyword is never touched.
        """
        if not self._statements:
            self.append(keyword, args)
            return
        self._keyword.body[-1] = self._keyword_call(keyword, args)
        self._statements[-1] = (keyword, args)
        self.save()

    def undo_last(self) -> bool:
        """Remove the most recently recorded call. False if there was none."""
        if not self._statements:
            return False
        self._keyword.body.pop()
        self._statements.pop()
        self.save()
        return True

    def discard(self) -> None:
        """Remove everything this writer added, then save.

        Only this writer's own statements are removed, so a keyword that already
        existed in the file keeps its original body. The keyword block and the
        section are removed only if this writer created them. A file created by
        this writer is left in place - the recorder never deletes a file.
        """
        for _ in range(len(self._statements)):
            self._keyword.body.pop()
        self._statements.clear()
        if not self.reused:
            self._remove(self._section.body, self._keyword)
            if self._keyword_separator is not None:
                self._remove(self._section.body, self._keyword_separator)
        if self.created_section and not any(
            isinstance(item, Keyword) for item in self._section.body
        ):
            self._remove(self._model.sections, self._section)
            if self._section_separator is not None:
                previous, separator = self._section_separator
                self._remove(previous.body, separator)
        self.save()

    def lines(self) -> list[str]:
        """The recorded calls as un-indented Robot Framework text."""
        return [
            _INDENT.join([keyword, *[self._display(a) for a in args]])
            for keyword, args in self._statements
        ]

    @staticmethod
    def _remove(container: list, item: object) -> None:
        for index, existing in enumerate(container):
            if existing is item:
                del container[index]
                return

    def __len__(self) -> int:
        return len(self._statements)

    def save(self) -> None:
        self._model.save(str(self.target))

    def text(self) -> str:
        """Return the recorded keyword block as plain text (for the return value)."""
        rows = ["*** Keywords ***", self.keyword_name]
        rows.extend(_INDENT + line for line in self.lines())
        return _EOL.join(rows) + _EOL

    # -- model construction ------------------------------------------------ #

    def _load_or_create_model(self) -> File:
        if self.target.exists():
            return get_model(str(self.target))
        return File(source=str(self.target))

    def _ensure_keyword_section(self) -> KeywordSection:
        for section in self._model.sections:
            if isinstance(section, KeywordSection):
                return section
        # Separate the new section from any preceding content with a blank line.
        if self._model.sections:
            separator = EmptyLine([Token(Token.EOL, _EOL)])
            previous = self._model.sections[-1]
            previous.body.append(separator)
            self._section_separator = (previous, separator)
        header = SectionHeader(
            [Token(Token.KEYWORD_HEADER, "*** Keywords ***"), Token(Token.EOL, _EOL)]
        )
        section = KeywordSection(header=header)
        self._model.sections.append(section)
        self.created_section = True
        return section

    def _find_keyword(self) -> tuple[KeywordSection, Keyword] | None:
        """The existing keyword block with this name, in *any* keyword section.

        Compared with `normalize_keyword_name`, the same way `_shadow_error`
        decides a name is reusable rather than colliding: Robot matches
        keyword names case-, space- and underscore-insensitively, so a raw
        comparison here would miss a name that was deliberately *accepted* as
        a reuse (e.g. ``existing_in_target`` against ``Existing In Target``)
        and write a second, duplicate keyword block instead of appending to
        the first - both then fail at run time as "defined multiple times".
        """
        target_name = normalize_keyword_name(self.keyword_name)
        for section in self._model.sections:
            if not isinstance(section, KeywordSection):
                continue
            for item in section.body:
                if (
                    isinstance(item, Keyword)
                    and item.name
                    and normalize_keyword_name(item.name) == target_name
                ):
                    return section, item
        return None

    def _create_keyword_block(self) -> Keyword:
        if self._section.body:
            self._keyword_separator = EmptyLine([Token(Token.EOL, _EOL)])
            self._section.body.append(self._keyword_separator)
        name = KeywordName(
            [Token(Token.KEYWORD_NAME, self.keyword_name), Token(Token.EOL, _EOL)]
        )
        keyword = Keyword(name)
        self._section.body.append(keyword)
        return keyword

    @staticmethod
    def _keyword_call(keyword: str, args: list[str]) -> KeywordCall:
        tokens = [Token(Token.SEPARATOR, _INDENT), Token(Token.KEYWORD, keyword)]
        for arg in args:
            tokens.append(Token(Token.SEPARATOR, _INDENT))
            tokens.append(Token(Token.ARGUMENT, LiveKeywordWriter._cell(arg)))
        tokens.append(Token(Token.EOL, _EOL))
        return KeywordCall(tokens)

    @staticmethod
    def _cell(value: str) -> str:
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
        """
        # Robot cannot represent an empty cell literally.
        if value == "":
            return "${EMPTY}"
        # Backslash first, so the escapes added below stay intact.
        cell = value.replace("\\", "\\\\")
        # A literal tab is a cell separator and a literal newline ends the row;
        # Robot resolves these escapes back to the characters at run time.
        for char, escape in (("\t", "\\t"), ("\r", "\\r"), ("\n", "\\n")):
            cell = cell.replace(char, escape)
        # Everything else that Robot or `str.splitlines()` counts as whitespace.
        cell = "".join(
            f"\\u{ord(char):04x}" if char.isspace() and char != " " else char
            for char in cell
        )
        cell = _VARIABLE_START.sub(r"\\\g<0>", cell)
        if cell.startswith("#"):
            cell = "\\" + cell
        # Two or more consecutive spaces are a cell separator; a leading or
        # trailing space is stripped.
        cell = _MULTI_SPACE.sub(lambda m: "${SPACE}" * len(m.group()), cell)
        if cell.startswith(" "):
            cell = "${SPACE}" + cell[1:]
        if cell.endswith(" "):
            cell = cell[:-1] + "${SPACE}"
        return cell

    @staticmethod
    def _display(value: str) -> str:
        return LiveKeywordWriter._cell(value)
