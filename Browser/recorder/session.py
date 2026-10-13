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
"""The recording session state machine.

Deliberately free of I/O beyond the keyword writer: no browser, no gRPC, no
parsing of streamed frames. Everything about *what should happen* when an
action or a toolbar command arrives lives here, so the whole interaction model
is unit testable in milliseconds.
"""

from __future__ import annotations

from pathlib import Path

from .action_mapper import SILENT_ACTIONS, ActionMapper
from .keyword_writer import LiveKeywordWriter
from .names import KnownKeywords, NameGuard, existing_keyword_names

IDLE = "idle"
RECORDING = "recording"


class RecorderSession:
    """Turn recorder events and toolbar commands into written User Keywords.

    ``fixed_name`` selects the single-keyword mode used by ``Record Keyword``:
    recording starts immediately, ``new`` is rejected, and ``discard`` restarts
    the same keyword instead of returning to idle. It comes from the suite
    author, so an unusable name raises rather than being reported to a toolbar
    nobody is looking at yet.

    ``known`` are the keyword names already visible in the running Robot suite
    (see `KnownKeywords`). A recorded keyword lands in a *resource*, and resource
    keywords outrank library keywords in Robot's resolution order, so a name that
    merely repeats - or can be instantiated from - an existing one silently
    replaces it on the next suite run. Since the ``new`` command is callable by
    the page under test, `NameGuard` checks every name against it. A name the
    target file already defines is rejected too: a Keyword Recording never
    extends an existing keyword.

    It is injected rather than collected here so this class stays free of any
    Robot runtime context.
    """

    def __init__(
        self,
        target: Path,
        fixed_name: str | None = None,
        known: KnownKeywords | None = None,
    ) -> None:
        self.target = Path(target)
        self._guard = NameGuard(known or KnownKeywords())
        self.stopped = False
        self.log: list[str] = []
        self._mapper = ActionMapper()
        self._fixed_name = fixed_name
        self._writer: LiveKeywordWriter | None = None
        self._name: str | None = None
        self._keywords: list[str] = []
        self._error: str | None = None
        self._text = ""
        # Whether the last event produced a line that an `actionUpdated` may
        # overwrite, and whether that action was undone (updates stay dead).
        self._written = False
        self._dead = False
        if fixed_name is not None:
            error = self._guard.error(
                fixed_name, taken=existing_keyword_names(self.target)
            )
            if error:
                raise ValueError(error)
            self._start(fixed_name)

    # -- introspection ----------------------------------------------------- #

    @property
    def state(self) -> str:
        return RECORDING if self._writer is not None else IDLE

    @property
    def keywords(self) -> list[str]:
        return list(self._keywords)

    def text(self) -> str:
        """Text of the most recently finished keyword."""
        return self._text

    def toolbar_state(self) -> dict:
        return {
            "state": self.state,
            "name": self._name,
            "steps": self._writer.lines() if self._writer else [],
            "keywords": list(self._keywords),
            "file": self.target.name,
            "error": self._error,
            "fixedName": self._fixed_name is not None,
        }

    # -- recorder events --------------------------------------------------- #

    def handle_event(self, event: str, action: dict) -> None:
        if event == "signal" or self._writer is None:
            return
        call = self._mapper.map(action)
        if call is None:
            if action.get("name") in SILENT_ACTIONS:
                return
            self.log.append(
                f"action {action.get('name')!r} has no Browser keyword "
                "equivalent and was skipped"
            )
            # An update of a skipped action must not overwrite an earlier line.
            self._written = False
            return
        kw_name = call.keyword
        args = [v.text or "" for v in call.args]
        if event == "updated":
            if self._dead:
                return
            if self._written:
                self._writer.replace_last(kw_name, args)
                return
        self._writer.append(kw_name, args)
        self._written = True
        self._dead = False

    # -- toolbar commands -------------------------------------------------- #

    def handle_command(self, command: dict) -> None:
        self._error = None
        cmd = str(command.get("cmd", ""))
        if cmd == "new":
            self._new(str(command.get("name", "")))
        elif cmd == "finish":
            self._finish()
        elif cmd == "undo":
            self._undo()
        elif cmd == "discard":
            self._discard()
        elif cmd == "stop":
            self.stopped = True
        else:
            self.log.append(f"unknown recorder command {cmd!r}")

    def close(self) -> list[str]:
        """Finish any in-progress keyword and return every recorded name."""
        if self._writer is not None:
            self._finish()
        return list(self._keywords)

    # -- command handlers -------------------------------------------------- #

    def _new(self, name: str) -> None:
        if self._fixed_name is not None:
            self._error = f"This recording writes only '{self._fixed_name}'."
            return
        if self._writer is not None:
            self._error = f"Still recording '{self._name}'. Finish it first."
            return
        # The command channel is callable by the page under test, so the name
        # is untrusted input, not just a typo risk.
        error = self._guard.error(
            name, taken=[*self._keywords, *existing_keyword_names(self.target)]
        )
        if error:
            self._error = error
            return
        self._start(name)

    def _finish(self) -> None:
        if self._writer is None:
            self._error = "No keyword is being recorded."
            return
        if len(self._writer) == 0:
            self.log.append(f"'{self._name}' had no steps and was discarded")
            self._writer.discard()
        else:
            self._text = self._writer.text()
            self._keywords.append(str(self._name))
            self.log.append(f"finished '{self._name}' with {len(self._writer)} steps")
        self._reset()

    def _undo(self) -> None:
        if self._writer is None:
            self._error = "No keyword is being recorded."
            return
        if self._writer.undo_last():
            # Playwright keeps refining the action behind the removed line; that
            # refinement must not resurrect it.
            self._dead = True
            self._written = False

    def _discard(self) -> None:
        if self._writer is None:
            self._error = "No keyword is being recorded."
            return
        self._writer.discard()
        self.log.append(f"discarded '{self._name}'")
        name = self._name
        self._reset()
        if self._fixed_name is not None:
            self._start(str(name))

    # -- helpers ----------------------------------------------------------- #

    def _start(self, name: str) -> None:
        self._name = name
        self._writer = LiveKeywordWriter(self.target, name)
        if self._writer.reused:
            self.log.append(
                f"keyword '{name}' already exists; recorded steps are appended to it"
            )
        self._written = False
        self._dead = False

    def _reset(self) -> None:
        self._writer = None
        self._name = None
        self._written = False
        self._dead = False
