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
keyword it is recording: everything outside that block is
whatever is on disk at that moment, so edits made in an IDE meanwhile survive.
"""

from __future__ import annotations

import codecs
import io
import os
import shutil
import tempfile
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from robot.api import get_model, logger
from robot.api.parsing import EmptyLine, SectionHeader, Token
from robot.conf.languages import En, Language, Languages
from robot.parsing.model.blocks import (
    Block,
    File,
    Keyword,
    KeywordSection,
    TestCase,
    TestCaseSection,
)
from robot.parsing.model.statements import Statement

from .model import RecordedKeyword, SettingNames
from .names import existing_keyword_names, normalize_keyword_name

_EOL = "\n"
_SECTION_SEPARATOR = 2
_KEYWORD_SEPARATOR = 1


class Target(Protocol):
    label: str

    settings: SettingNames

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
        languages: Iterable[Language] = (),
    ) -> None:
        self._console = console
        self._info = info
        self.settings = SettingNames.of(_first_with_keywords_header(languages))

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
    separator_lines: int
    section_separator_lines: int = 0


@dataclass
class _Format:
    bom: bool = False
    eol: str = _EOL
    final_newline: bool = True


@dataclass(frozen=True)
class CallSite:
    """The step of a test that the calls of recorded keywords are inserted before.

    Found by content, not by line: every inserted call moves the lines below it.
    ``test_index`` counts the tests of that name before it, ``step_index`` the
    steps of the test with the same content before it.
    """

    test: str
    test_index: int
    signature: tuple
    step_index: int


def call_site(model: File, line: int) -> CallSite:
    """The step of a test body at ``line`` of ``model``, the file as Robot read it."""
    for test, test_index in _tests(model):
        if not test.lineno < line <= test.end_lineno:
            continue
        for step in _steps(test):
            if step.lineno == line:
                signature = _signature(step)
                same = [s for s in _steps(test) if _signature(s) == signature]
                step_index = next(i for i, s in enumerate(same) if s is step)
                return CallSite(test.name, test_index, signature, step_index)
    raise ValueError(f"line {line} is not a step of a test body")


def unwritable_reason(path: Path) -> str | None:
    """Why ``path`` cannot be written, or ``None``.

    The write itself replaces the file by renaming a temporary one, which only
    needs the folder's permission - so a read-only file is checked here, or it
    would be overwritten anyway.
    """
    if not path.parent.is_dir():
        return f"the folder {path.parent} does not exist"
    if path.exists() and not os.access(path, os.W_OK):
        return f"{path.name} is read-only"
    return None


class FileTarget:
    def __init__(self, path: Path, languages: Iterable[Language] = ()) -> None:
        self.path = Path(path)
        self.label = self.path.name
        self._configured = tuple(languages)
        self._languages = Languages(self._configured)
        self._owned: dict[str, _Owned] = {}
        self._format: _Format | None = None
        declared = self._read().languages
        self._language = _first_with_keywords_header(
            [*Languages(declared, add_english=False), *self._configured]
        )
        self._languages.add_language(self._language)
        self.settings = SettingNames.of(self._language)

    def existing_names(self) -> set[str]:
        return existing_keyword_names(self.path, self._languages)

    def save(self, keyword: RecordedKeyword) -> str | None:
        key = normalize_keyword_name(keyword.name)
        if len(keyword) == 0:
            self.remove(keyword.name)
            return None
        owned = self._owned.get(key)
        model = self._read()
        self._check_language(model)
        block = _parse_block(keyword.block(), self._languages)
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
            section, created, section_separator_lines = self._keyword_section(model)
            separator_lines = (
                _ensure_empty_lines(section, _KEYWORD_SEPARATOR) if section.body else 0
            )
            section.body.append(block)
            owned = _Owned(
                (),
                created or (owned.created_section if owned else False),
                separator_lines,
                section_separator_lines
                or (owned.section_separator_lines if owned else 0),
            )
        # Owned only once written: a failed first write must not let a later
        # retry overwrite a keyword of that name that someone else added meanwhile.
        self._write(model)
        owned.signature = _signature(block)
        self._owned[key] = owned
        return notice

    def finish(self, keyword: RecordedKeyword) -> None:
        self.save(keyword)
        self._owned.pop(normalize_keyword_name(keyword.name), None)

    def parsed(self) -> File:
        """The file as it is on disk now."""
        return self._read()

    def insert_call(self, site: CallSite, keyword: RecordedKeyword) -> None:
        """Insert a call of ``keyword`` before the step ``site``, indented like it."""
        model = self._read()
        body, index = self._step(model, site)
        body.insert(
            index, _parse_call(_indent(body[index]) + keyword.call(), self._languages)
        )
        self._write(model)

    def _step(self, model: File, site: CallSite) -> tuple[list, int]:
        tests = [test for test, _ in _tests(model) if test.name == site.test]
        if len(tests) <= site.test_index:
            raise ValueError(f"test '{site.test}' is no longer in {self.path.name}")
        test = tests[site.test_index]
        same = [step for step in _steps(test) if _signature(step) == site.signature]
        if len(same) <= site.step_index:
            raise ValueError(
                f"the step to insert before is no longer in test '{site.test}'"
            )
        step = same[site.step_index]
        return test.body, next(i for i, s in enumerate(test.body) if s is step)

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
        if index > 0:
            _pop_trailing_empty_lines(body[index - 1], owned.separator_lines)
        if owned.created_section:
            for position, section in enumerate(model.sections):
                if section.body is body and not any(
                    isinstance(item, Keyword) for item in body
                ):
                    del model.sections[position]
                    if position > 0:
                        _pop_trailing_empty_lines(
                            model.sections[position - 1],
                            owned.section_separator_lines,
                        )
                    break
        self._write(model, restore_final_newline=len(self._owned) == 1)
        self._owned.pop(key, None)

    # -- helpers ----------------------------------------------------------- #

    def _check_language(self, model: File) -> None:
        enabled = Languages([*self._configured, *model.languages])
        if self._language not in enabled:
            raise ValueError(
                f"{self.path.name} no longer enables {self._language.name}, the "
                "language the recording started with; enable it with a "
                "'Language:' line or record again."
            )

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
        return get_model(io.StringIO(text.replace("\r\n", "\n")), lang=self._languages)

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
        reason = unwritable_reason(self.path)
        if reason:
            raise PermissionError(reason)
        directory = self.path.parent
        with tempfile.NamedTemporaryFile(
            "wb", dir=directory, prefix=f".{self.path.name}.", delete=False
        ) as handle:
            temp = Path(handle.name)
            handle.write(data)
        try:
            if self.path.exists():
                shutil.copymode(self.path, temp)
            else:
                # The temporary file is private (0600); a new file gets the
                # permissions any other new file would.
                temp.chmod(0o666 & ~_umask())
            temp.replace(self.path)
        except BaseException:
            temp.unlink(missing_ok=True)
            raise

    def _keyword_section(self, model: File) -> tuple[KeywordSection, bool, int]:
        for section in model.sections:
            if isinstance(section, KeywordSection):
                return section, False, 0
        separator_lines = 0
        if model.sections:
            separator_lines = _ensure_empty_lines(
                model.sections[-1], _SECTION_SEPARATOR
            )
        header = SectionHeader(
            [
                Token(
                    Token.KEYWORD_HEADER, f"*** {self._language.keywords_header} ***"
                ),
                Token(Token.EOL, _EOL),
            ]
        )
        section = KeywordSection(header=header)
        model.sections.append(section)
        return section, True, separator_lines


def _umask() -> int:
    mask = os.umask(0o077)
    os.umask(mask)
    return mask


def _first_with_keywords_header(languages: Iterable[Language]) -> Language:
    return next((lang for lang in languages if lang.keywords_header), En())


def _parse_block(text: str, languages: Languages) -> Keyword:
    model = get_model(io.StringIO("*** Keywords ***\n" + text), lang=languages)
    return model.sections[0].body[0]


def _parse_call(row: str, languages: Languages) -> Statement:
    model = get_model(io.StringIO(f"*** Test Cases ***\nT\n{row}\n"), lang=languages)
    return model.sections[0].body[0].body[0]


def _tests(model: File) -> Iterator[tuple[TestCase, int]]:
    """Every test with the number of tests of the same name before it."""
    seen: dict[str, int] = {}
    for section in model.sections:
        if not isinstance(section, TestCaseSection):
            continue
        for item in section.body:
            if isinstance(item, TestCase):
                yield item, seen.get(item.name, 0)
                seen[item.name] = seen.get(item.name, 0) + 1


def _steps(test: TestCase) -> Iterator[Block | Statement]:
    """The executed top-level steps: no settings, comments or empty lines."""
    for node in test.body:
        if isinstance(node, Block) or node.type not in (
            *Token.SETTING_TOKENS,
            Token.COMMENT,
            Token.EOL,
        ):
            yield node


def _indent(node: Block | Statement) -> str:
    first = next(_statements(node)).tokens[0]
    return first.value if first.type == Token.SEPARATOR else "    "


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


def _signature(block: Block | Statement) -> tuple:
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


def _ensure_empty_lines(node: Block, wanted: int) -> int:
    """Append line ends until ``node`` ends with ``wanted`` empty lines.

    Counted in the text, so a last line without a line end, or with only
    spaces, is handled too. Returns how many line ends were appended.
    """
    text = "".join(
        token.value for statement in _statements(node) for token in statement.tokens
    )
    trailing = text[len(text.rstrip()) :]
    missing = max(0, wanted + 1 - trailing.count(_EOL))
    node.body.extend(EmptyLine([Token(Token.EOL, _EOL)]) for _ in range(missing))
    return missing


def _pop_trailing_empty_lines(node: Block, count: int) -> None:
    for _ in range(count):
        _pop_trailing_empty_line(node)


def _pop_trailing_empty_line(node: Block) -> None:
    body = getattr(node, "body", None)
    if not body:
        return
    last = body[-1]
    if isinstance(last, EmptyLine):
        if "".join(token.value for token in last.tokens) == _EOL:
            body.pop()
    elif isinstance(last, Block):
        _pop_trailing_empty_line(last)
