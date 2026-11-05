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

import json
import math
import time
from collections.abc import Callable

from .action_mapper import (
    SILENT_ACTIONS,
    UPLOAD_FOLDER,
    ActionMapper,
    internal_selector_notice,
    is_plain_file_name,
    uploaded_files,
)
from .cells import tokens
from .model import Call, RecordedKeyword
from .names import (
    KnownKeywords,
    NameGuard,
    argument_name_error,
    plain_argument_name,
)
from .picker import PICK_COMMANDS, SelectorPicker
from .target import Target

IDLE = "idle"
RECORDING = "recording"

#: Playwright holds a left click and a navigation back for 500 ms before
#: reporting them (ADR 0011). Finish, Discard, Stop and Pause wait until this
#: long after the last click or page load so such an Action still lands in the
#: keyword it was made in; New and Resume wait so one made while idle or
#: paused does not land in the keyword. The toolbar reports how long the page has been
#: quiet (``quietMs``); without it the whole time is waited.
SETTLE_SECONDS = 0.8
_WRITE_FAILED = "Could not write"
_PAIR = 2
_LOGGED_NAME_LIMIT = 80
#: Longer command ids are ignored; the toolbar's are far shorter.
_ID_LIMIT = 64
_STILL_FINISHING = "Still finishing the last command - please wait."
_STILL_STARTING = "Still starting the keyword - please wait."
_STILL_PICKING = "Use or cancel the picked selector first."
#: The keyword's page was closed; the next Action decides which page is active.
_CLOSED = "closed"
_UNREACHABLE_PAGE = (
    "This Action happened on a page the keyword has no id of, so no Switch Page "
    "was recorded before it."
)
_DEFERRED = ("finish", "discard", "stop", "pause", "resume")
_COMMANDS = frozenset({"pick", "new", "undo", "argument", "replace", *_DEFERRED})
_STARTING = "new"
#: The toolbar shows at most this many characters of one text.
TOOLBAR_TEXT_LIMIT = 200
#: A value whose JSON is longer cannot become an argument in the toolbar.
MAX_RAW_LENGTH = 64 * 1024
#: The ``raw`` values of one toolbar state together stay below this, so the
#: state and the commands quoting them fit one gRPC message.
MAX_RAW_TOTAL = 1024 * 1024


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
        #: Finished keywords the target could not write; retried on close.
        self.unsaved: list[RecordedKeyword] = []
        self._keyword: RecordedKeyword | None = None
        self._pending: tuple[str, float] | None = None
        self._starting: str | None = None
        self._error: str | None = None
        self._notice: str | None = None
        self._offer: dict | None = None
        self._undone = False
        self._skipped = False
        self._discard_on_stop = False
        self._picking = False
        #: The toolbar's Pick button: picks a selector into a comment row.
        self._picker: SelectorPicker | None = None
        #: The highlight switch of the last pick, kept for the next one.
        self._pick_highlight = True
        self._paused = False
        #: The last write error of a keyword left in `unsaved`.
        self.write_error: str | None = None
        self._answered: str | None = None
        #: The page the keyword's next Keyword Call runs on (a Playwright page guid).
        self._page: str | None = None
        #: The page a keyword starts on: where the last one ended.
        self._start_page: str | None = None
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

    def set_active_page(self, page: object) -> None:
        """The page Browser has active when the session starts."""
        if isinstance(page, str) and self._start_page is None:
            self._start_page = self._page = page

    def set_picking(self, picking: bool) -> None:
        """Playwright's Pick locator mode is on: nothing is recorded meanwhile."""
        self._picking = picking

    def request(self) -> dict:
        """What the next poll asks Node to do for the toolbar's Pick button."""
        return self._picker.request() if self._picker is not None else {}

    def handle_picked(self, picked: dict) -> None:
        if self._picker is not None:
            self._picker.handle_picked(picked)

    def handle_count(self, count: dict) -> None:
        if self._picker is not None:
            self._picker.handle_count(count)

    def request_pick(self) -> None:
        """Playwright's Pick locator was turned on; the toolbar picks instead.

        With a selector already picked it picks again, like Reselect.
        """
        if self._picker is None:
            self._open_picker()
        elif not self._picker.picking:
            self._picker.handle_command({"cmd": "reselect"})

    def toolbar_state(self) -> dict:
        keyword = self._keyword
        offer = self._offer and {**self._offer, "text": _shown(self._offer["text"])}
        return {
            "state": self.state,
            "name": keyword.name if keyword is not None else self._starting,
            "fixedName": self._fixed_name is not None,
            "target": self.target.label,
            "keywords": self.keywords,
            "calls": self._toolbar_calls(keyword),
            "arguments": [
                {
                    "name": a.name,
                    "default": _shown(a.default),
                    "useDefault": a.use_default,
                }
                for a in (keyword.arguments if keyword is not None else [])
            ],
            "offer": offer,
            "pending": self._pending[0] if self._pending else None,
            "notice": self._notice,
            "error": self._error,
            "picking": self._picking,
            "paused": self._paused,
            "picker": self._picker.toolbar_state()
            if self._picker is not None
            else None,
            "answered": self._answered,
        }

    @staticmethod
    def _toolbar_calls(keyword: RecordedKeyword | None) -> list[dict]:
        budget = MAX_RAW_TOTAL
        calls = []
        for call in keyword.calls() if keyword is not None else []:
            values = []
            for value, written in zip(call.args, call.rendered_args(), strict=True):
                raw = value.text
                selectable = value.selectable
                if selectable and raw is not None:
                    size = len(json.dumps(raw))
                    if size > MAX_RAW_LENGTH or size > budget:
                        raw, selectable = None, False
                    else:
                        budget -= size
                values.append(
                    {
                        "tokens": _shown_tokens(tokens(written)),
                        "selectable": selectable,
                        "raw": raw,
                    }
                )
            calls.append(
                {
                    "assign": f"${{{call.assign}}}=" if call.assign else None,
                    "keyword": call.keyword,
                    "values": values,
                    "comment": call.comment,
                }
            )
        return calls

    # -- events ------------------------------------------------------------ #

    def _records(self) -> bool:
        """Whether Actions and signals go into the keyword now.

        Not while paused, and not once a selector is picked: the page may be
        tried out until Use or Cancel. While picking, Playwright records
        nothing; what still arrives is an Action it held back from before the
        pick, which belongs to the keyword.
        """
        picked = self._picker is not None and not self._picker.picking
        return self._keyword is not None and not self._paused and not picked

    def handle_event(self, event: str, action: dict, page: str | None = None) -> None:
        keyword = self._keyword
        if keyword is None or not self._records():
            return
        if event == "closed":
            self._close_page(keyword, page)
        elif event == "signal":
            self._signal(keyword, action)
        else:
            self._action(keyword, event, action, page)

    def _action(
        self, keyword: RecordedKeyword, event: str, action: dict, page: str | None
    ) -> None:
        files = uploaded_files(action)
        if files is not None:
            self._upload(keyword, action, files, page)
            return
        call = self._mapper.map(action) if isinstance(action.get("name"), str) else None
        if call is None:
            raw_name = action.get("name")
            name = raw_name if isinstance(raw_name, str) else "?"
            if name not in SILENT_ACTIONS:
                name = name[:_LOGGED_NAME_LIMIT]
                self._notice = f"'{name}' has no Browser keyword and was not recorded."
                self.log.append(f"action {name!r} has no Browser keyword equivalent")
                self._skipped = True
            return
        if event == "updated":
            if self._undone:
                return
            if not self._skipped and keyword.update_last(call):
                self._offer = None
                self._notice = internal_selector_notice(action) or self._notice
                self._save()
                return
        keyword.add(call, self._switch_to(keyword, page), self._page)
        self._offer = None
        self._undone = False
        self._skipped = False
        self._notice = internal_selector_notice(action) or self._notice
        self._save()

    def _signal(self, keyword: RecordedKeyword, signal: dict) -> None:
        effect = self._mapper.map_signal(signal, keyword.unique_variable)
        if effect is None or self._undone or self._skipped:
            return
        popup = signal.get("popupPageGuid")
        popup = popup if isinstance(popup, str) else None
        if keyword.attach(effect.before, effect.after, popup):
            if popup is not None:
                self._left(effect.after[-1], popup)
            self._offer = None
            self._save()

    # -- pages ------------------------------------------------------------- #

    def _left(self, switch: Call, page: str | None) -> None:
        """``switch`` left the keyword's page for ``page``."""
        if self._page not in (None, _CLOSED):
            switch.leaves = self._page
        self._page = page

    def _page_variable(self, keyword: RecordedKeyword, page: str) -> str | None:
        """The variable holding the id of ``page``: the Switch Page that left it
        gets it assigned on first use."""
        switch = keyword.switch_leaving(page)
        if switch is None:
            return None
        if switch.assign is None:
            switch.assign = keyword.unique_variable("page")
        return switch.assign

    def _switch_to(self, keyword: RecordedKeyword, page: str | None) -> list[Call]:
        """The Switch Page before an Action on ``page``, if it is not active."""
        if page is None or page == self._page:
            return []
        if self._page is None:
            self._page = page
            return []
        variable = self._page_variable(keyword, page)
        if variable is None:
            if self._page != _CLOSED:
                self._notice = _UNREACHABLE_PAGE
            self._page = page
            return []
        switch = self._mapper.switch_page(variable)
        self._left(switch, page)
        return [switch]

    def _close_page(self, keyword: RecordedKeyword, page: str | None) -> None:
        if page is None:
            return
        if page == self._page:
            keyword.add(self._mapper.close_page(None), page=_CLOSED)
            self._page = _CLOSED
        else:
            variable = self._page_variable(keyword, page)
            if variable is None:
                self.log.append("a page the keyword has no id of was closed")
                return
            keyword.add(self._mapper.close_page(variable), page=self._page)
        self._offer = None
        self._undone = self._skipped = False
        self._save()

    def _reset_pages(self) -> None:
        """A new keyword starts where the last one ended, with no page ids."""
        self._start_page = self._page

    def _upload(
        self,
        keyword: RecordedKeyword,
        action: dict,
        files: list[str],
        page: str | None = None,
    ) -> None:
        """Wrap the Action that opened the file chooser, as Browser needs the
        promise before it; without one, set the files on the input itself."""
        refused = [name for name in files if not is_plain_file_name(name)]
        if refused:
            self._notice = (
                f"Not recorded: an upload of {_shown(repr(refused[0]))}, which is not a "
                "plain file name."
            )
            self.log.append(
                "upload with a file name that is not plain was not recorded"
            )
            return
        if not files:
            return
        effect = self._mapper.map_upload(files[0], keyword.unique_variable)
        attached = len(files) == 1 and not self._undone and not self._skipped
        if not (attached and keyword.attach(effect.before, effect.after)):
            keyword.add(
                self._mapper.map_upload_by_selector(action, files),
                self._switch_to(keyword, page),
                self._page,
            )
            self._undone = self._skipped = False
        self._offer = None
        self._notice = f"Replace {UPLOAD_FOLDER} with the folder of the uploaded file."
        self._save()

    # -- commands ---------------------------------------------------------- #

    def handle_command(self, command: dict) -> bool:
        """Apply one toolbar command; True if it is a command the toolbar has.

        A command's ``id`` comes back as ``answered`` in the toolbar state, with
        ``error`` saying whether it was refused. Only a known command counts as
        activity: the page under test can send anything (ADR 0010).
        """
        self._error = None
        self._notice = None
        command_id = command.get("id")
        if isinstance(command_id, str) and len(command_id) <= _ID_LIMIT:
            self._answered = command_id
        cmd = str(command.get("cmd", ""))
        known = cmd in _COMMANDS or (
            cmd.startswith("pick-") and cmd[len("pick-") :] in PICK_COMMANDS
        )
        if self._pending is not None and cmd != "stop":
            self._error = (
                _STILL_STARTING if self._pending[0] == _STARTING else _STILL_FINISHING
            )
            return known
        if self._picker is not None and not cmd.startswith("pick") and cmd != "stop":
            # The keyword's buttons are hidden while picking; only ✕ ends everything.
            self._error = _STILL_PICKING
            return known
        if cmd == "pick":
            self._open_picker()
        elif cmd.startswith("pick-"):
            self._picker_command(cmd[len("pick-") :], command)
        elif cmd in _DEFERRED:
            self._picker = None
            self._defer(cmd, _settle_seconds(command))
        elif cmd == "new":
            self._new(command.get("name"), _settle_seconds(command))
        elif cmd == "undo":
            self._undo()
        elif cmd in ("argument", "replace"):
            self._argument_command(cmd, command)
        else:
            self.log.append(f"unknown recorder command {cmd[:_LOGGED_NAME_LIMIT]!r}")
        return known

    def tick(self) -> None:
        if self._pending is None or self._clock() < self._pending[1]:
            return
        cmd = self._pending[0]
        self._pending = None
        if self._error in (_STILL_FINISHING, _STILL_STARTING):
            self._error = None
        if self._discard_on_stop:
            self._discard_on_stop = False
            if self._keyword is not None:
                self._discard(restart=False)
        if cmd == _STARTING:
            self._start()
        elif cmd == "finish":
            self._finish()
        elif cmd == "discard":
            self._discard()
        elif cmd == "pause":
            self._pause()
        elif cmd == "resume":
            self._paused = False
        else:
            self.stopped = True

    def close(self) -> list[str]:
        """End the session now; a running Keyword Recording is saved."""
        self._picker = None
        pending = self._pending
        self._pending = None
        self._starting = None
        discard = self._discard_on_stop or (
            pending is not None and pending[0] == "discard"
        )
        self._discard_on_stop = False
        if self._keyword is not None:
            if discard:
                self._discard(restart=False)
            elif len(self._keyword):
                self._finish()
            else:
                self._keyword = None
        self._retry_unsaved()
        return self.keywords

    def _retry_unsaved(self) -> None:
        """Write what failed before once more: the reason may be gone by now."""
        unsaved, self.unsaved = self.unsaved, []
        for keyword in unsaved:
            try:
                self.target.finish(keyword)
            except (OSError, ValueError) as error:
                self.unsaved.append(keyword)
                self.write_error = f"{_WRITE_FAILED} {self.target.label}: {error}"

    # -- command handlers -------------------------------------------------- #

    def _defer(self, cmd: str, settle: float) -> None:
        if cmd != "stop":
            if self._keyword is None:
                self._error = "No keyword is being recorded."
                return
            if cmd == "finish" and self._fixed_name is not None:
                self._error = "Use Stop to end this recording."
                return
            if cmd == "pause" and self._paused:
                self._error = "The recording is already paused."
                return
            if cmd == "resume" and not self._paused:
                self._error = "The recording is not paused."
                return
        if cmd == "stop" and self._pending is not None:
            # Keep the running settle time; a discard still happens first and
            # a keyword not yet started is never started.
            self._starting = None
            if self._pending[0] == "discard":
                self._discard_on_stop = True
            if self._pending[0] != "stop":
                self._pending = ("stop", self._pending[1])
            return
        self._pending = (cmd, self._clock() + settle)

    def _new(self, name: object, settle: float) -> None:
        if not isinstance(name, str):
            self._error = "'name' must be text."
            return
        if self._fixed_name is not None:
            self._error = f"This recording writes only '{self._fixed_name}'."
            return
        if self._keyword is not None:
            self._error = f"Still recording '{self._keyword.name}'. Finish it first."
            return
        try:
            existing = self.target.existing_names()
        except (OSError, ValueError) as unreadable:
            self._error = f"Could not read {self.target.label}: {unreadable}"
            return
        taken = [*self.keywords, *existing]
        error = self._guard.error(name, taken=taken)
        if error:
            self._error = error
            return
        self._starting = name
        self._pending = (_STARTING, self._clock() + settle)

    def _start(self) -> None:
        name = self._starting
        self._starting = None
        if name is None:
            return
        self._keyword = RecordedKeyword(name)
        self._picker = None
        self._undone = self._skipped = self._paused = False
        self._reset_pages()

    def _pause(self) -> None:
        self._paused = True
        # A signal reported after Resume belongs to an Action made while paused,
        # not to the last recorded one.
        self._skipped = True

    def _finish(self) -> None:
        keyword = self._keyword
        assert keyword is not None
        self._keyword = None
        self._picker = None
        self._offer = None
        self._paused = False
        if not len(keyword):
            self.log.append(f"'{keyword.name}' had no Keyword Calls and was discarded")
            self._remove(keyword.name)
            return
        try:
            self.target.finish(keyword)
        except (OSError, ValueError) as error:
            self._error = f"{_WRITE_FAILED} {self.target.label}: {error}"
            self.unsaved.append(keyword)
        self._finished.append(keyword)
        self.log.append(f"finished '{keyword.name}' with {len(keyword)} Keyword Calls")

    def _open_picker(self) -> None:
        if self._pending is not None:
            self._error = (
                _STILL_STARTING if self._pending[0] == _STARTING else _STILL_FINISHING
            )
            return
        if self._keyword is None:
            self._notice = "Start recording a keyword to pick a selector into it."
            return
        self._offer = None
        self._picker = SelectorPicker(None, "playwright", self._pick_highlight)

    def _picker_command(self, cmd: str, command: dict) -> None:
        picker = self._picker
        if picker is None or self._keyword is None:
            self._error = "No selector is being picked."
            return
        if cmd == "cancel":
            self._picker = None
            return
        picker.handle_command({**command, "cmd": cmd})
        self._pick_highlight = picker.highlight
        if picker.cancelled:
            self._picker = None
        elif picker.result is not None:
            self._keyword.add_picked_selector(picker.result)
            self._picker = None
            self._undone = False
            self._save()

    def _undo(self) -> None:
        if self._keyword is None:
            self._error = "No keyword is being recorded."
            return
        comment = self._keyword.last_is_comment()
        if self._keyword.undo():
            # Undoing a picked selector leaves the Action before it as it was:
            # Playwright may still refine it.
            self._undone = self._undone if comment else True
            self._page = self._keyword.last_page() or self._start_page
            self._keyword.drop_unused_page_ids()
            self._offer = None
            self._save()

    def _discard(self, restart: bool = True) -> None:
        keyword = self._keyword
        assert keyword is not None
        self._keyword = (
            RecordedKeyword(self._fixed_name)
            if restart and self._fixed_name is not None
            else None
        )
        self._picker = None
        self._offer = None
        self._undone = self._skipped = self._paused = False
        self._page = self._start_page
        self.log.append(f"discarded '{keyword.name}'")
        self._remove(keyword.name)

    def _remove(self, name: str) -> None:
        try:
            self.target.remove(name)
        except (OSError, ValueError) as error:
            self._error = f"{_WRITE_FAILED} {self.target.label}: {error}"

    def _argument_command(self, cmd: str, command: dict) -> None:
        keyword = self._keyword
        if keyword is None:
            self._error = "No keyword is being recorded."
            return
        try:
            if cmd == "argument":
                call, value = _int(command, "call"), _int(command, "value")
                start, end = _int(command, "start"), _int(command, "end")
                self._check_raw(keyword, call, value, command)
                name = _text(command, "name")
                if argument_name_error(name) is None:
                    name = plain_argument_name(name)
                use_default = command.get("useDefault", True)
                if not isinstance(use_default, bool):
                    raise ValueError("'useDefault' must be true or false.")
                occurrences = keyword.make_argument(
                    call, value, start, end, name, use_default=use_default
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
            else:
                keyword.replace(
                    _text(command, "argument"), _pairs(command.get("occurrences"))
                )
                self._offer = None
        except ValueError as error:
            self._error = str(error)
            if cmd == "argument":
                self._offer = None
            return
        self._save()

    @staticmethod
    def _check_raw(
        keyword: RecordedKeyword, call: int, value: int, command: dict
    ) -> None:
        """Reject a selection made against a view that has since changed."""
        raw = command.get("raw", _MISSING)
        if raw is not None and not isinstance(raw, str):
            raise ValueError("'raw' must be text.")
        if keyword.value_changed(call, value, raw):
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


_MISSING: object = object()


def _settle_seconds(command: dict) -> float:
    """How much of `SETTLE_SECONDS` is still to wait after the page was quiet."""
    quiet = command.get("quietMs")
    if (
        isinstance(quiet, bool)
        or not isinstance(quiet, int | float)
        or not math.isfinite(quiet)
        or quiet < 0
    ):
        return SETTLE_SECONDS
    return max(0.0, SETTLE_SECONDS - quiet / 1000)


def _text(command: dict, key: str) -> str:
    value = command.get(key)
    if not isinstance(value, str):
        raise ValueError(f"'{key}' must be text.")
    return value


def _int(command: dict, key: str) -> int:
    value = command.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
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
            or not all(
                isinstance(i, int) and not isinstance(i, bool) and i >= 0 for i in item
            )
        ):
            raise ValueError("Each occurrence must be [call, value].")
        pairs.append((item[0], item[1]))
    return pairs


def _shown_tokens(parts: list[tuple[str, str]]) -> list[list[str]]:
    """The tokens of a value, cut like `_shown` cuts a text."""
    if sum(len(text) for _, text in parts) <= TOOLBAR_TEXT_LIMIT:
        return [[kind, text] for kind, text in parts]
    shown: list[list[str]] = []
    room = TOOLBAR_TEXT_LIMIT - 1
    for kind, text in parts:
        if len(text) >= room:
            shown.append([kind, text[:room] + "\u2026"])
            break
        shown.append([kind, text])
        room -= len(text)
    return shown


def _shown(text: str) -> str:
    if len(text) <= TOOLBAR_TEXT_LIMIT:
        return text
    return text[: TOOLBAR_TEXT_LIMIT - 1] + "\u2026"
