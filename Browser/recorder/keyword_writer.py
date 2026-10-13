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

from .cells import cell
from .names import normalize_keyword_name

_INDENT = "    "
_EOL = "\n"


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

        Compared with `normalize_keyword_name`: Robot matches
        keyword names case-, space- and underscore-insensitively, so a raw
        comparison here would miss an existing block (e.g. ``existing_in_target``
        against ``Existing In Target``) and write a second, duplicate keyword block instead of appending to
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
            tokens.append(Token(Token.ARGUMENT, cell(arg)))
        tokens.append(Token(Token.EOL, _EOL))
        return KeywordCall(tokens)

    @staticmethod
    def _display(value: str) -> str:
        return cell(value)
