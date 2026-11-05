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
"""The in-memory model of one User Keyword being recorded.

It is the single source of truth for a Keyword Recording: targets only render
it. Keyword Calls are kept in *groups*, one per Action, because one Action may
need several Keyword Calls (a dialog handler before a click, a download promise
around it) and Undo must remove all of them together.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from .cells import cell
from .names import argument_name_error, normalize_keyword_name
from .parameters import KEYWORD_PARAMETERS

TAG = "recorded"
_INDENT = "    "


@dataclass(frozen=True)
class ArgRef:
    """A reference to a Keyword Argument (or an assigned variable) in a value."""

    name: str


@dataclass
class Value:
    """One argument cell of a Keyword Call.

    ``selectable`` is False for structural values (buttons, operators, option
    strategies): those can never become Keyword Arguments.
    ``named`` marks a deliberate named argument such as ``action=accept``; every
    other value that looks like one is escaped.
    """

    segments: list[str | ArgRef]
    selectable: bool = True
    named: bool = False

    @classmethod
    def literal(cls, text: str, selectable: bool = True) -> Value:
        return cls([text] if text else [], selectable)

    @property
    def text(self) -> str | None:
        """The literal text, or ``None`` once a reference is part of it."""
        if any(isinstance(s, ArgRef) for s in self.segments):
            return None
        return "".join(s for s in self.segments if isinstance(s, str))

    def references(self) -> set[str]:
        return {s.name for s in self.segments if isinstance(s, ArgRef)}

    def render(self, parameters: frozenset[str] | None = frozenset()) -> str:
        """The cell; ``parameters`` are those of the called keyword (see `cell`)."""
        if not self.segments:
            return "${EMPTY}"
        last = len(self.segments) - 1
        rendered = []
        for i, segment in enumerate(self.segments):
            if isinstance(segment, ArgRef):
                rendered.append(f"${{{segment.name}}}")
                continue
            text = cell(
                segment,
                at_start=i == 0,
                at_end=i == last,
                parameters=frozenset() if self.named else parameters,
            )
            # `${name}[0]` would be item access.
            if i > 0 and isinstance(self.segments[i - 1], ArgRef) and text[:1] == "[":
                text = "\\" + text
            rendered.append(text)
        return "".join(rendered)


#: The first cell of the comment row a picked selector is written as.
PICKED_SELECTOR = "# Picked Selector"


@dataclass
class Call:
    """One Keyword Call: ``[${assign}=]    Keyword    args...``.

    A ``comment`` is a comment row instead, ``keyword`` its first cell: the
    picked selector of the toolbar's Pick button, written as a cell.
    """

    keyword: str
    args: list[Value]
    assign: str | None = None
    comment: bool = False
    #: The page a Switch Page left (a Playwright page guid): it returns that page's id.
    leaves: str | None = None

    def rendered_args(self) -> list[str]:
        """The argument cells as written into the file."""
        parameters = (
            frozenset() if self.comment else KEYWORD_PARAMETERS.get(self.keyword)
        )
        return [value.render(parameters) for value in self.args]

    def render(self) -> str:
        cells = [f"${{{self.assign}}}="] if self.assign else []
        cells.append(self.keyword)
        cells.extend(self.rendered_args())
        return _INDENT.join(cells)


@dataclass
class Argument:
    name: str
    default: str
    use_default: bool = True

    def render(self) -> str:
        if self.use_default:
            return f"${{{self.name}}}={cell(self.default)}"
        return f"${{{self.name}}}"


@dataclass
class _Group:
    primary: Call
    before: list[Call] = field(default_factory=list)
    after: list[Call] = field(default_factory=list)
    #: The page the keyword is on after these Keyword Calls.
    page: str | None = None

    def calls(self) -> list[Call]:
        return [*self.before, self.primary, *self.after]


class RecordedKeyword:
    def __init__(self, name: str) -> None:
        self.name = name
        self.arguments: list[Argument] = []
        self._groups: list[_Group] = []

    def __len__(self) -> int:
        return sum(len(group.calls()) for group in self._groups)

    def calls(self) -> list[Call]:
        return [call for group in self._groups for call in group.calls()]

    # -- recording --------------------------------------------------------- #

    def add(
        self, call: Call, before: list[Call] | None = None, page: str | None = None
    ) -> None:
        self._groups.append(_Group(call, list(before or []), page=page))

    def last_page(self) -> str | None:
        """The page the keyword is on after its last Action."""
        group = self._last_action()
        return None if group is None else group.page

    def switch_leaving(self, page: str) -> Call | None:
        """A Switch Page of the keyword that left ``page``, one with a variable first."""
        switches = [c for c in self.calls() if c.leaves == page]
        assigned = [c for c in switches if c.assign]
        candidates = assigned or switches
        return candidates[-1] if candidates else None

    def drop_unused_page_ids(self) -> None:
        """Remove the assignment of a Switch Page no Keyword Call uses any more."""
        used = self._used_names()
        for call in self.calls():
            if call.leaves is not None and call.assign not in used:
                call.assign = None

    def add_picked_selector(self, selector: str) -> None:
        """A comment row with a selector picked with the toolbar's Pick button."""
        self._groups.append(
            _Group(
                Call(
                    PICKED_SELECTOR,
                    [Value.literal(selector, selectable=False)],
                    comment=True,
                )
            )
        )

    def _last_action(self) -> _Group | None:
        """The group of the last Action: Playwright refines and wraps it even
        after a picked selector was added."""
        for group in reversed(self._groups):
            if not group.primary.comment:
                return group
        return None

    def update_last(self, call: Call) -> bool:
        """Replace the last Action's Keyword Call with Playwright's refinement.

        Values that were turned into Keyword Arguments stay arguments; their
        default follows the newly typed text.
        """
        group = self._last_action()
        if group is None:
            return False
        old = group.primary
        if old.keyword == call.keyword and len(old.args) == len(call.args):
            call.args = [
                self._carry(o, n) for o, n in zip(old.args, call.args, strict=True)
            ]
        group.primary = call
        self._drop_unused()
        return True

    def attach(
        self, before: list[Call], after: list[Call], page: str | None = None
    ) -> bool:
        """Wrap the last Action's Keyword Call with signal handling; ``page``
        is the page a popup switched to."""
        group = self._last_action()
        if group is None:
            return False
        group.before.extend(before)
        group.after.extend(after)
        if page is not None:
            group.page = page
        return True

    def last_is_comment(self) -> bool:
        return bool(self._groups) and self._groups[-1].primary.comment

    def undo(self) -> bool:
        if not self._groups:
            return False
        self._groups.pop()
        self._drop_unused()
        return True

    # -- variables and arguments ------------------------------------------ #

    def _taken_variables(self) -> set[str]:
        names = {normalize_keyword_name(a.name) for a in self.arguments}
        names.update(normalize_keyword_name(c.assign) for c in self.calls() if c.assign)
        return names

    def unique_variable(self, base: str) -> str:
        taken = self._taken_variables()
        candidate, number = base, 1
        while normalize_keyword_name(candidate) in taken:
            number += 1
            candidate = f"{base}_{number}"
        return candidate

    def argument(self, name: str) -> Argument:
        for argument in self.arguments:
            if argument.name == name:
                return argument
        raise ValueError(f"No argument '{name}'.")

    def make_argument(
        self,
        call: int,
        value: int,
        start: int,
        end: int,
        name: str,
        *,
        use_default: bool = True,
    ) -> list[tuple[int, int]]:
        """Turn ``text[start:end]`` of one value into ``${name}``.

        With ``use_default`` the marked text becomes the argument's default.
        Returns the other values that contain the same text, for the toolbar
        to offer.
        """
        error = argument_name_error(name)
        if error:
            raise ValueError(error)
        if normalize_keyword_name(name) in self._taken_variables():
            raise ValueError(f"A variable named '{name}' already exists.")
        target = self._value(call, value)
        if not target.selectable:
            raise ValueError("Fixed options cannot become arguments.")
        text = target.text
        if text is None:
            raise ValueError("This value already contains an argument.")
        if not (0 <= start < end <= len(text)):
            raise ValueError("Mark a non-empty part of the value.")
        marked = text[start:end]
        target.segments = _split(text, start, end, ArgRef(name))
        self.arguments.append(Argument(name, marked, use_default))
        return [
            (c, v)
            for c, v, other in self._values()
            if (c, v) != (call, value)
            and other.selectable
            and other.text is not None
            and marked in other.text
        ]

    def replace(self, name: str, occurrences: list[tuple[int, int]]) -> None:
        marked = self.argument(name).default
        for call, value in occurrences:
            target = self._value(call, value)
            text = target.text
            if not target.selectable or text is None or marked not in text:
                continue
            target.segments = _split_all(text, marked, ArgRef(name))

    # -- rendering --------------------------------------------------------- #

    def lines(self) -> list[str]:
        """The keyword's body rows, unindented."""
        rows = [f"[Tags]{_INDENT}{TAG}"]
        if self.arguments:
            ordered = [a for a in self.arguments if not a.use_default] + [
                a for a in self.arguments if a.use_default
            ]
            rows.append(_INDENT.join(["[Arguments]", *(a.render() for a in ordered)]))
        rows.extend(call.render() for call in self.calls())
        return rows

    def block(self) -> str:
        return "\n".join([self.name, *(_INDENT + row for row in self.lines())]) + "\n"

    def text(self) -> str:
        return "*** Keywords ***\n" + self.block()

    # -- helpers ----------------------------------------------------------- #

    def value_changed(self, call: int, value: int, raw: object) -> bool:
        """Whether the value exists and no longer reads ``raw``."""
        try:
            return self._value(call, value).text != raw
        except ValueError:
            return False

    def _values(self) -> Iterator[tuple[int, int, Value]]:
        for c, call in enumerate(self.calls()):
            for v, value in enumerate(call.args):
                yield c, v, value

    def _value(self, call: int, value: int) -> Value:
        try:
            return self.calls()[call].args[value]
        except (IndexError, TypeError):
            raise ValueError("No such value.") from None

    def _carry(self, old: Value, new: Value) -> Value:
        text = new.text
        refs = [s for s in old.segments if isinstance(s, ArgRef)]
        if text is None or len(refs) != 1:
            return new
        index = old.segments.index(refs[0])
        prefix = "".join(s for s in old.segments[:index] if isinstance(s, str))
        suffix = "".join(s for s in old.segments[index + 1 :] if isinstance(s, str))
        if not (
            text.startswith(prefix)
            and text.endswith(suffix)
            and len(text) > len(prefix) + len(suffix)
        ):
            return new
        argument = next((a for a in self.arguments if a.name == refs[0].name), None)
        if argument is None:
            return new
        argument.default = text[len(prefix) : len(text) - len(suffix)]
        return Value(
            [*_nonempty(prefix), refs[0], *_nonempty(suffix)], old.selectable, old.named
        )

    def _used_names(self) -> set[str]:
        """The arguments and variables the Keyword Calls' values refer to."""
        used: set[str] = set()
        for call in self.calls():
            for value in call.args:
                used |= value.references()
        return used

    def _drop_unused(self) -> None:
        used = self._used_names()
        self.arguments = [a for a in self.arguments if a.name in used]


def _nonempty(text: str) -> list[str]:
    return [text] if text else []


def _split(text: str, start: int, end: int, ref: ArgRef) -> list[str | ArgRef]:
    return [*_nonempty(text[:start]), ref, *_nonempty(text[end:])]


def _split_all(text: str, marked: str, ref: ArgRef) -> list[str | ArgRef]:
    parts = text.split(marked)
    segments: list[str | ArgRef] = list(_nonempty(parts[0]))
    for part in parts[1:]:
        segments.append(ref)
        segments.extend(_nonempty(part))
    return segments
