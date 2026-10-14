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
"""Where a recorded keyword goes: a `.robot`/`.resource` file, or the log.

`FileTarget` re-reads the file before every save and owns only the block of the
keyword it is recording (AC-35, AC-36): everything outside that block is
whatever is on disk at that moment, so edits made in an IDE meanwhile survive.
"""

from __future__ import annotations

import codecs
import io
import shutil
import tempfile
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from robot.api import get_model, logger
from robot.api.parsing import EmptyLine, SectionHeader, Token
from robot.parsing.model.blocks import Block, File, Keyword, KeywordSection
from robot.parsing.model.statements import Statement

from .model import RecordedKeyword
from .names import existing_keyword_names, normalize_keyword_name

_EOL = "\n"


class Target(Protocol):
    label: str

    def existing_names(self) -> set[str]: ...

    def save(self, keyword: RecordedKeyword) -> str | None: ...

    def remove(self, name: str) -> None: ...

    def finish(self, keyword: RecordedKeyword) -> None: ...


class LogTarget:
    """`file=${None}`: nothing is written; finished keywords go to console and log."""

    label = "the log"

    def __init__(
        self,
        console: Callable[[str], None] = logger.console,
        info: Callable[[str], None] = logger.info,
    ) -> None:
        self._console = console
        self._info = info

    def existing_names(self) -> set[str]:
        return set()

    def save(self, keyword: RecordedKeyword) -> str | None:
        return None

    def remove(self, name: str) -> None:
        return None

    def finish(self, keyword: RecordedKeyword) -> None:
        text = keyword.text()
        self._console(text)
        self._info(text)


@dataclass
class _Owned:
    signature: tuple
    created_section: bool
    separated: bool
    section_separated: bool = False


@dataclass
class _Format:
    bom: bool = False
    eol: str = _EOL
    final_newline: bool = True


class FileTarget:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.label = self.path.name
        self._owned: dict[str, _Owned] = {}
        self._format: _Format | None = None

    def existing_names(self) -> set[str]:
        return existing_keyword_names(self.path)

    def save(self, keyword: RecordedKeyword) -> str | None:
        key = normalize_keyword_name(keyword.name)
        if len(keyword) == 0:
            self.remove(keyword.name)
            return None
        owned = self._owned.get(key)
        model = self._read()
        block = _parse_block(keyword.block())
        notice = None
        found = _find(model, keyword.name)
        if found is not None:
            body, index = found
            old = body[index]
            if owned is None:
                raise ValueError(
                    f"Keyword '{keyword.name}' already exists in {self.path.name} "
                    "and is not part of this recording."
                )
            if _signature(old) != owned.signature:
                notice = (
                    f"'{keyword.name}' was changed outside the recorder and has "
                    "been rewritten."
                )
            block.body.extend(_trailing_empty_lines(old))
            body[index] = block
        else:
            if owned is not None:
                notice = (
                    f"'{keyword.name}' was removed outside the recorder and has "
                    "been written again."
                )
            section, created, section_separated = self._keyword_section(model)
            separated = bool(section.body) and _ensure_blank_line(section.body)
            section.body.append(block)
            owned = _Owned(
                (),
                created or (owned.created_section if owned else False),
                separated,
                section_separated or (owned.section_separated if owned else False),
            )
        owned.signature = _signature(block)
        self._owned[key] = owned
        self._write(model)
        return notice

    def finish(self, keyword: RecordedKeyword) -> None:
        self.save(keyword)
        self._owned.pop(normalize_keyword_name(keyword.name), None)

    def remove(self, name: str) -> None:
        key = normalize_keyword_name(name)
        owned = self._owned.get(key)
        if owned is None or not self.path.exists():
            self._owned.pop(key, None)
            return
        model = self._read()
        found = _find(model, name)
        if found is None:
            self._owned.pop(key, None)
            return
        body, index = found
        del body[index]
        if owned.separated and index > 0:
            _pop_trailing_empty_line(body[index - 1])
        if owned.created_section:
            for position, section in enumerate(model.sections):
                if section.body is body and not any(
                    isinstance(item, Keyword) for item in body
                ):
                    del model.sections[position]
                    if owned.section_separated and position > 0:
                        _pop_trailing_empty_line(model.sections[position - 1])
                    break
        self._write(model, restore_final_newline=len(self._owned) == 1)
        self._owned.pop(key, None)

    # -- helpers ----------------------------------------------------------- #

    def _read(self) -> File:
        """Parse the file as it is on disk right now.

        Byte level details Robot does not keep (BOM, CRLF, a missing final
        newline) are remembered at first touch so `_write` can restore them.
        """
        if not self.path.exists():
            self._format = self._format or _Format()
            return File(source=str(self.path))
        data = self.path.read_bytes()
        bom = data.startswith(codecs.BOM_UTF8)
        try:
            text = data[len(codecs.BOM_UTF8) if bom else 0 :].decode("utf-8")
        except UnicodeDecodeError as error:
            # Replacing the byte would rewrite a part of the file not ours.
            raise ValueError(
                f"it is not valid UTF-8 (byte {error.start + bom * 3})"
            ) from None
        crlf = "\r\n" in text
        if self._format is None:
            self._format = _Format(
                bom=bom,
                eol="\r\n" if crlf else "\n",
                final_newline=not text or text.endswith("\n"),
            )
        return get_model(io.StringIO(text.replace("\r\n", "\n")))

    def _write(self, model: File, restore_final_newline: bool = False) -> None:
        """Write atomically, in the file's own BOM and line ending."""
        fmt = self._format or _Format()
        buffer = io.StringIO()
        model.save(buffer)
        text = buffer.getvalue()
        if restore_final_newline and not fmt.final_newline and text.endswith("\n"):
            text = text[:-1]
        data = text.replace("\n", fmt.eol).encode("utf-8")
        if fmt.bom:
            data = codecs.BOM_UTF8 + data
        directory = self.path.parent
        with tempfile.NamedTemporaryFile(
            "wb", dir=directory, prefix=f".{self.path.name}.", delete=False
        ) as handle:
            temp = Path(handle.name)
            handle.write(data)
        try:
            if self.path.exists():
                shutil.copymode(self.path, temp)
            temp.replace(self.path)
        except BaseException:
            temp.unlink(missing_ok=True)
            raise

    @staticmethod
    def _keyword_section(model: File) -> tuple[KeywordSection, bool, bool]:
        for section in model.sections:
            if isinstance(section, KeywordSection):
                return section, False, False
        separated = False
        if model.sections:
            separated = _ensure_blank_line(model.sections[-1].body)
        header = SectionHeader(
            [Token(Token.KEYWORD_HEADER, "*** Keywords ***"), Token(Token.EOL, _EOL)]
        )
        section = KeywordSection(header=header)
        model.sections.append(section)
        return section, True, separated


def _parse_block(text: str) -> Keyword:
    model = get_model(io.StringIO("*** Keywords ***\n" + text))
    return model.sections[0].body[0]


def _find(model: File, name: str) -> tuple[list, int] | None:
    wanted = normalize_keyword_name(name)
    for section in model.sections:
        if not isinstance(section, KeywordSection):
            continue
        for index, item in enumerate(section.body):
            if (
                isinstance(item, Keyword)
                and item.name
                and normalize_keyword_name(item.name) == wanted
            ):
                return section.body, index
    return None


def _statements(node: Block | Statement) -> Iterator[Statement]:
    if isinstance(node, Statement):
        yield node
        return
    for field in node._fields:
        value = getattr(node, field, None)
        items = value if isinstance(value, list) else [value]
        for item in items:
            if isinstance(item, (Block, Statement)):
                yield from _statements(item)


def _signature(block: Keyword) -> tuple:
    """The block's content, ignoring blank lines, separators and line ends."""
    return tuple(
        tuple(
            token.value
            for token in statement.tokens
            if token.type not in (Token.SEPARATOR, Token.EOL)
        )
        for statement in _statements(block)
        if not isinstance(statement, EmptyLine)
    )


def _trailing_empty_lines(block: Keyword) -> list[EmptyLine]:
    trailing: list[EmptyLine] = []
    for item in reversed(block.body):
        if not isinstance(item, EmptyLine):
            break
        trailing.insert(0, item)
    return trailing


def _ends_with_empty_line(body: list) -> bool:
    if not body:
        return False
    last = body[-1]
    if isinstance(last, EmptyLine):
        return True
    return isinstance(last, Block) and _ends_with_empty_line(getattr(last, "body", []))


def _ensure_blank_line(body: list) -> bool:
    """Append a blank line unless ``body`` already ends with one. True if added."""
    if _ends_with_empty_line(body):
        return False
    body.append(EmptyLine([Token(Token.EOL, _EOL)]))
    return True


def _pop_trailing_empty_line(node: Block) -> None:
    body = getattr(node, "body", None)
    if not body:
        return
    last = body[-1]
    if isinstance(last, EmptyLine):
        body.pop()
    elif isinstance(last, Block):
        _pop_trailing_empty_line(last)
