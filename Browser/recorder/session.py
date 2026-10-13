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
"""The Recording Session state machine.

It applies recorder events and toolbar commands to a `RecordedKeyword` and tells
its `Target` to save. It has no I/O of its own beyond the target, and its clock
is injected, so the whole interaction model is unit-testable in milliseconds.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .action_mapper import SILENT_ACTIONS, ActionMapper
from .model import RecordedKeyword
from .names import KnownKeywords, NameGuard
from .target import Target

IDLE = "idle"
RECORDING = "recording"

#: Playwright holds a left click back for 500 ms before reporting it (ADR 0011).
#: Finish, Discard and Stop wait this long so such a click still lands in the
#: keyword it was made in (AC-19).
SETTLE_SECONDS = 0.6
_WRITE_FAILED = "Could not write"
_PAIR = 2
_DEFERRED = ("finish", "discard", "stop")


class RecorderSession:
    def __init__(
        self,
        target: Target,
        fixed_name: str | None = None,
        known: KnownKeywords | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.target = target
        self.stopped = False
        self.log: list[str] = []
        self._guard = NameGuard(known or KnownKeywords())
        self._mapper = ActionMapper()
        self._clock = clock
        self._fixed_name = fixed_name
        self._finished: list[RecordedKeyword] = []
        self._keyword: RecordedKeyword | None = None
        self._pending: tuple[str, float] | None = None
        self._error: str | None = None
        self._notice: str | None = None
        self._offer: dict | None = None
        self._undone = False
        self._skipped = False
        if fixed_name is not None:
            error = self._guard.error(fixed_name, taken=target.existing_names())
            if error:
                raise ValueError(error)
            self._keyword = RecordedKeyword(fixed_name)

    # -- introspection ----------------------------------------------------- #

    @property
    def state(self) -> str:
        return RECORDING if self._keyword is not None else IDLE

    @property
    def keywords(self) -> list[str]:
        return [keyword.name for keyword in self._finished]

    def text(self) -> str:
        if not self._finished:
            return ""
        return "*** Keywords ***\n" + "\n".join(k.block() for k in self._finished)

    def toolbar_state(self) -> dict:
        keyword = self._keyword
        return {
            "state": self.state,
            "name": keyword.name if keyword is not None else None,
            "fixedName": self._fixed_name is not None,
            "target": self.target.label,
            "keywords": self.keywords,
            "calls": [
                {
                    "text": call.render(),
                    "keyword": call.keyword,
                    "values": [
                        {
                            "text": value.render(),
                            "selectable": value.selectable,
                            "raw": value.text,
                        }
                        for value in call.args
                    ],
                }
                for call in (keyword.calls() if keyword is not None else [])
            ],
            "arguments": [
                {"name": a.name, "default": a.default, "useDefault": a.use_default}
                for a in (keyword.arguments if keyword is not None else [])
            ],
            "offer": self._offer,
            "pending": self._pending[0] if self._pending else None,
            "notice": self._notice,
            "error": self._error,
        }

    # -- events ------------------------------------------------------------ #

    def handle_event(self, event: str, action: dict) -> None:
        keyword = self._keyword
        if keyword is None:
            return
        if event == "signal":
            effect = self._mapper.map_signal(action, keyword.unique_variable)
            if (
                effect
                and not self._undone
                and not self._skipped
                and keyword.attach(effect.before, effect.after)
            ):
                self._save()
            return
        call = self._mapper.map(action)
        if call is None:
            name = action.get("name")
            if name not in SILENT_ACTIONS:
                self._notice = f"'{name}' has no Browser keyword and was not recorded."
                self.log.append(f"action {name!r} has no Browser keyword equivalent")
                self._skipped = True
            return
        if event == "updated":
            if self._undone:
                return
            if not self._skipped and keyword.update_last(call):
                self._save()
                return
        keyword.add(call)
        self._undone = False
        self._skipped = False
        self._save()

    # -- commands ---------------------------------------------------------- #

    def handle_command(self, command: dict) -> None:
        self._error = None
        self._notice = None
        cmd = str(command.get("cmd", ""))
        if self._pending is not None and cmd != "stop":
            self._error = "Still finishing the last command - please wait."
            return
        if cmd in _DEFERRED:
            self._defer(cmd)
        elif cmd == "new":
            self._new(str(command.get("name", "")))
        elif cmd == "undo":
            self._undo()
        elif cmd in ("argument", "replace", "default"):
            self._argument_command(cmd, command)
        else:
            self.log.append(f"unknown recorder command {cmd!r}")

    def tick(self) -> None:
        if self._pending is None or self._clock() < self._pending[1]:
            return
        cmd = self._pending[0]
        self._pending = None
        if cmd == "finish":
            self._finish()
        elif cmd == "discard":
            self._discard()
        else:
            self.stopped = True

    def close(self) -> list[str]:
        """End the session now; a running Keyword Recording is saved (AC-18)."""
        self._pending = None
        if self._keyword is not None:
            if len(self._keyword):
                self._finish()
            else:
                self._keyword = None
        return self.keywords

    # -- command handlers -------------------------------------------------- #

    def _defer(self, cmd: str) -> None:
        if cmd != "stop":
            if self._keyword is None:
                self._error = "No keyword is being recorded."
                return
            if cmd == "finish" and self._fixed_name is not None:
                self._error = "Use Stop to end this recording."
                return
        self._pending = (cmd, self._clock() + SETTLE_SECONDS)

    def _new(self, name: str) -> None:
        if self._fixed_name is not None:
            self._error = f"This recording writes only '{self._fixed_name}'."
            return
        if self._keyword is not None:
            self._error = f"Still recording '{self._keyword.name}'. Finish it first."
            return
        taken = [*self.keywords, *self.target.existing_names()]
        error = self._guard.error(name, taken=taken)
        if error:
            self._error = error
            return
        self._keyword = RecordedKeyword(name)
        self._undone = self._skipped = False

    def _finish(self) -> None:
        keyword = self._keyword
        assert keyword is not None
        self._keyword = None
        self._offer = None
        if not len(keyword):
            self.log.append(f"'{keyword.name}' had no Keyword Calls and was discarded")
            self.target.remove(keyword.name)
            return
        try:
            self.target.finish(keyword)
        except (OSError, ValueError) as error:
            self._error = f"{_WRITE_FAILED} {self.target.label}: {error}"
        self._finished.append(keyword)
        self.log.append(f"finished '{keyword.name}' with {len(keyword)} Keyword Calls")

    def _undo(self) -> None:
        if self._keyword is None:
            self._error = "No keyword is being recorded."
            return
        if self._keyword.undo():
            self._undone = True
            self._offer = None
            self._save()

    def _discard(self) -> None:
        keyword = self._keyword
        assert keyword is not None
        self.target.remove(keyword.name)
        self.log.append(f"discarded '{keyword.name}'")
        self._keyword = (
            RecordedKeyword(self._fixed_name) if self._fixed_name is not None else None
        )
        self._offer = None
        self._undone = self._skipped = False

    def _argument_command(self, cmd: str, command: dict) -> None:
        keyword = self._keyword
        if keyword is None:
            self._error = "No keyword is being recorded."
            return
        try:
            if cmd == "argument":
                self._check_raw(keyword, command)
                raw_name = command.get("name")
                name = raw_name if isinstance(raw_name, str) else ""
                occurrences = keyword.make_argument(
                    _int(command, "call"),
                    _int(command, "value"),
                    _int(command, "start"),
                    _int(command, "end"),
                    name,
                )
                self._offer = (
                    {
                        "argument": name,
                        "text": keyword.argument(name).default,
                        "occurrences": [list(o) for o in occurrences],
                    }
                    if occurrences
                    else None
                )
            elif cmd == "replace":
                keyword.replace(
                    str(command.get("argument")), _pairs(command.get("occurrences"))
                )
                self._offer = None
            else:
                keyword.set_default(
                    str(command.get("argument")), bool(command.get("use"))
                )
        except ValueError as error:
            self._error = str(error)
            return
        self._save()

    @staticmethod
    def _check_raw(keyword: RecordedKeyword, command: dict) -> None:
        """Reject a selection made against a view that has since changed."""
        call, value = command.get("call"), command.get("value")
        calls = keyword.calls()
        if (
            isinstance(call, int)
            and isinstance(value, int)
            and 0 <= call < len(calls)
            and 0 <= value < len(calls[call].args)
            and calls[call].args[value].text != command.get("raw")
        ):
            raise ValueError("The keyword calls changed - please try again.")

    def _save(self) -> None:
        if self._keyword is None:
            return
        try:
            notice = self.target.save(self._keyword)
        except (OSError, ValueError) as error:
            self._error = f"{_WRITE_FAILED} {self.target.label}: {error}"
            return
        if self._error and self._error.startswith(_WRITE_FAILED):
            # The file is writable again; the keyword in memory was never lost.
            self._error = None
        if notice:
            self._notice = notice


def _int(command: dict, key: str) -> int:
    value = command.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"'{key}' must be a number.")
    return value


def _pairs(value: object) -> list[tuple[int, int]]:
    if not isinstance(value, list):
        raise ValueError("'occurrences' must be a list.")
    pairs = []
    for item in value:
        if (
            not isinstance(item, list)
            or len(item) != _PAIR
            or not all(isinstance(i, int) and not isinstance(i, bool) for i in item)
        ):
            raise ValueError("Each occurrence must be [call, value].")
        pairs.append((item[0], item[1]))
    return pairs
