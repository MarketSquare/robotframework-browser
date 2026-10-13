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

from collections.abc import Callable, Iterable
from pathlib import Path

from .action_mapper import ActionMapper
from .keyword_writer import (
    LiveKeywordWriter,
    existing_keyword_names,
    keyword_name_error,
    normalize_keyword_name,
)

IDLE = "idle"
RECORDING = "recording"


class RecorderSession:
    """Turn recorder events and toolbar commands into written User Keywords.

    ``fixed_name`` selects the single-keyword mode used by ``Record Keyword``:
    recording starts immediately, ``new`` is rejected, and ``discard`` restarts
    the same keyword instead of returning to idle. It comes from the suite
    author, so an unusable name raises rather than being reported to a toolbar
    nobody is looking at yet.

    ``known_keywords`` are the keyword names already visible in the running
    Robot suite - every imported library and resource file. A recorded keyword
    lands in a *resource*, and resource keywords outrank library keywords in
    Robot's resolution order, so a name that merely repeats an existing one
    silently replaces it on the next suite run. Since the ``new`` command is
    callable by the page under test, that is a way for a page to substitute its
    own body for `Log`, `No Operation` or `Click`.

    ``embedded_keywords`` covers the keywords a *literal* name can shadow
    without repeating it: ``Open ${page} Page`` is instantiated by a call to
    ``Open Login Page``, so a recording under that name takes its place. Each
    entry pairs the declared name with a predicate that says whether a candidate
    would be matched by it.

    ``bdd_prefixes`` are the suite's ``Given``/``When``/... markers, which Robot
    strips *before* resolving a keyword; a candidate is therefore checked with
    each prefix stripped as well.

    All three are injected rather than collected here so this class stays free
    of any Robot runtime context.
    """

    def __init__(
        self,
        target: Path,
        fixed_name: str | None = None,
        known_keywords: Iterable[str] | None = None,
        embedded_keywords: Iterable[tuple[str, Callable[[str], bool]]] | None = None,
        bdd_prefixes: Iterable[str] | None = None,
    ) -> None:
        self.target = Path(target)
        # normalized name -> the name as the user would see it in the message
        self._known: dict[str, str] = {
            normalize_keyword_name(name): name for name in known_keywords or ()
        }
        self._embedded = tuple(embedded_keywords or ())
        self._bdd_prefixes = tuple(bdd_prefixes or ())
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
            # Same collision surface as the `new` command, minus the literal
            # duplicate: repeating a name the target file already has *is* the
            # documented way to extend an existing keyword.
            in_file = {
                normalize_keyword_name(k): k
                for k in existing_keyword_names(self.target)
            }
            error = keyword_name_error(fixed_name) or self._shadow_error(
                fixed_name, also=in_file
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
        mapped = self._mapper.map(action)
        if mapped is None:
            self.log.append(
                f"action {action.get('name')!r} has no Browser keyword "
                "equivalent and was skipped"
            )
            # An update of a skipped action must not overwrite an earlier line.
            self._written = False
            return
        kw_name, args = mapped
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
        error = keyword_name_error(name) or self._duplicate_error(name)
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

    def _duplicate_error(self, name: str) -> str | None:
        """Why ``name`` must not be recorded now, or ``None``.

        Names are compared the way Robot compares them - caseless, ignoring
        spaces and underscores - not as raw strings. Robot would otherwise
        accept ``l_ogin as admin`` next to an existing ``Login As Admin`` and
        then refuse *both* at run time, so a page could disable a keyword the
        user already relies on just by re-spelling its name.
        """
        normalized = normalize_keyword_name(name)
        recorded = {normalize_keyword_name(k): k for k in self._keywords}
        in_file = {
            normalize_keyword_name(k): k for k in existing_keyword_names(self.target)
        }
        for existing in (recorded, in_file):
            if normalized in existing:
                return f"Keyword '{existing[normalized]}' already exists."
        return self._shadow_error(name, also={**recorded, **in_file})

    def _shadow_error(
        self, name: str, also: dict[str, str] | None = None
    ) -> str | None:
        """Why ``name`` would shadow a keyword the running suite already has.

        Checked for the name itself *and* for every BDD-prefix-stripped form of
        it. The stripped forms are refused for the opposite reason to the rest:
        ``Namespace._get_bdd_style_runner`` runs *before* the full name is tried
        and only falls through when the stripped name resolves to nothing, so a
        recorded ``Given User Is Logged In`` can never take a call away from an
        existing ``User Is Logged In`` - it is simply *unreachable*, and a
        keyword the user can never call is not a recording worth writing. The
        refusal is therefore conservative, not a hijack defence.

        ``also`` are names that are only reachable in this direction - already
        recorded ones and the target file's own - whose *literal* collision is
        handled by the caller (for the target file it is a legitimate reuse), so
        the candidate's own form is not looked up in them.
        """
        own = normalize_keyword_name(name)
        for form in self._name_forms(name):
            normalized = normalize_keyword_name(form)
            existing = self._known.get(normalized)
            if existing is None and normalized != own:
                existing = (also or {}).get(normalized)
            if existing is None:
                existing = self._embedded_shadow(form)
            if existing is not None:
                return (
                    f"Keyword '{existing}' already exists in this suite and would be "
                    f"shadowed by '{name}'. Please choose another name."
                )
        return None

    def _name_forms(self, name: str) -> list[str]:
        """``name`` and every form Robot would resolve a call to it as."""
        forms = [name]
        for prefix in self._bdd_prefixes:
            marker = f"{prefix} "
            if name.lower().startswith(marker.lower()) and name[len(marker) :].strip():
                forms.append(name[len(marker) :])
        return forms

    def _embedded_shadow(self, name: str) -> str | None:
        """The embedded-argument keyword ``name`` would instantiate, if any."""
        for declared, matches in self._embedded:
            try:
                matched = matches(name)
            except Exception as error:
                self.log.append(
                    f"could not match '{name}' against '{declared}': {error!r}"
                )
                continue
            if matched:
                return declared
        return None

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
