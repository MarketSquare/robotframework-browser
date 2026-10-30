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
"""Record Selector: the state of one pick and the poll loop that drives it.

Node picks with Playwright's ``page.pickLocator()`` and generates the ``css``
selector; Python translates Playwright's selector, keeps the toolbar state and
decides when the pick ends. Toolbar commands come through the page-callable
``__rfbCommand`` binding, so every one is validated here (ADR 0010).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol

from robot.api import logger

from .action_mapper import internal_engines, to_browser_selector

POLL_INTERVAL = 0.2
GENERATORS = ("playwright", "css")
#: An edited selector longer than this is not counted or used.
MAX_SELECTOR_LENGTH = 10_000


class PickerClient(Protocol):
    def poll(self, state: dict, request: dict, reset: bool) -> dict:
        """One poll reply; raises if Node's reply cannot be read."""
        ...

    def stop(self) -> None: ...


class SelectorPicker:
    """What the toolbar shows while a selector is recorded, and what was chosen."""

    def __init__(self, label: str | None, generator: str) -> None:
        if generator not in GENERATORS:
            raise ValueError(f"Unknown selector generator '{generator}'.")
        self.label = label
        self.generator = generator
        self.picking = True
        self.candidates: dict[str, str] = {}
        self.unavailable: dict[str, str] = {}
        self.selector = ""
        # Raised whenever the selector changes other than by typing, so the
        # toolbar replaces its input only then.
        self.version = 0
        self.count: dict | None = None
        self.notice: str | None = None
        self.error: str | None = None
        self.answered: str | None = None
        self.result: str | None = None
        self.cancelled = False
        # Node counts this selector on the page and highlights what it finds.
        self._count_wanted: str | None = None

    # -- toward Node -------------------------------------------------------- #

    def request(self) -> dict:
        """What the next poll asks Node to do besides rendering the toolbar."""
        request: dict = {"pick": self.picking}
        if self._count_wanted is not None:
            request["count"] = self._count_wanted
            self._count_wanted = None
        return request

    def toolbar_state(self) -> dict:
        return {
            "mode": "selector",
            "label": self.label,
            "phase": "picking" if self.picking else "picked",
            "generator": self.generator,
            "generators": list(GENERATORS),
            "unavailable": self.unavailable,
            "selector": self.selector,
            "version": self.version,
            "count": self.count,
            "notice": self.notice,
            "error": self.error,
            "answered": self.answered,
        }

    # -- from Node ---------------------------------------------------------- #

    def handle_picked(self, picked: dict) -> None:
        selector = picked.get("selector")
        if not isinstance(selector, str) or not selector:
            error = picked.get("error")
            self.error = f"Picking failed: {error}" if error else "Picking failed."
            return
        browser_selector = to_browser_selector(selector)
        self.candidates = {"playwright": browser_selector}
        self.unavailable = {}
        css = picked.get("css")
        if isinstance(css, str) and css:
            self.candidates["css"] = css
        else:
            self.unavailable["css"] = str(
                picked.get("error") or "No css selector found."
            )
        engines = internal_engines(browser_selector)
        self.notice = (
            f"Playwright's selector uses Playwright-internal syntax "
            f"({', '.join(dict.fromkeys(engines))}), which has no public equivalent "
            "and may break with a Playwright upgrade."
            if engines
            else None
        )
        self.error = None
        self.picking = False
        self._show(self.candidates.get(self.generator, ""))

    def handle_count(self, count: dict) -> None:
        if count.get("selector") == self.selector:
            self.count = count

    def handle_command(self, command: dict) -> None:
        name = command.get("cmd")
        handler = {
            "generator": self._generator,
            "edit": self._edit,
            "reselect": self._reselect,
            "use": self._use,
            "stop": self._stop,
        }.get(name if isinstance(name, str) else "")
        if handler is None:
            raise ValueError(f"Unknown command {name!r}.")
        self.error = None
        try:
            handler(command)
        except ValueError as error:
            self.error = str(error)
        finally:
            command_id = command.get("id")
            if isinstance(command_id, str):
                self.answered = command_id

    def _show(self, selector: str) -> None:
        self.selector = selector
        self.version += 1
        self.count = None
        self._count_wanted = selector or None

    def _generator(self, command: dict) -> None:
        name = command.get("name")
        if name not in GENERATORS:
            raise ValueError(f"Unknown selector generator {name!r}.")
        self.generator = name
        if not self.picking:
            self._show(self.candidates.get(name, ""))

    def _edit(self, command: dict) -> None:
        selector = command.get("selector")
        if not isinstance(selector, str) or len(selector) > MAX_SELECTOR_LENGTH:
            raise ValueError("The selector is too long.")
        self.selector = selector
        self.count = None
        self._count_wanted = selector if selector.strip() else None

    def _reselect(self, _command: dict) -> None:
        self.picking = True
        self.candidates = {}
        self.unavailable = {}
        self.notice = None
        self._show("")

    def _use(self, _command: dict) -> None:
        if not self.selector.strip():
            raise ValueError("Pick an element first, or type a selector.")
        self.result = self.selector.strip()

    def _stop(self, _command: dict) -> None:
        self.cancelled = True


def run_picker(
    picker: SelectorPicker,
    client: PickerClient,
    idle_timeout: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Drive ``picker`` until a selector is chosen and return it."""
    last_activity = clock()
    reset = True
    try:
        while True:
            reply = client.poll(picker.toolbar_state(), picker.request(), reset)
            reset = False
            if _apply(picker, reply):
                last_activity = clock()
            if picker.result is not None:
                return picker.result
            if picker.cancelled:
                raise RuntimeError("Record Selector was cancelled.")
            if not reply.get("pages"):
                raise RuntimeError("The page was closed before a selector was chosen.")
            if idle_timeout is not None and clock() - last_activity >= idle_timeout:
                raise TimeoutError(
                    "Record Selector timed out: no selector was chosen within the idle timeout."
                )
            sleep(POLL_INTERVAL)
    finally:
        try:
            client.stop()
        except Exception as error:
            logger.debug(f"selector picker: stop failed: {error!r}")


def _apply(picker: SelectorPicker, reply: dict) -> bool:
    """Apply one poll reply; True if it carried a pick or a toolbar command."""
    active = False
    picked = reply.get("picked")
    if isinstance(picked, dict):
        picker.handle_picked(picked)
        active = True
    entries = reply.get("entries")
    for entry in entries if isinstance(entries, list) else []:
        command = entry.get("command") if isinstance(entry, dict) else None
        if not isinstance(command, dict):
            continue
        active = True
        try:
            picker.handle_command(command)
        except Exception as error:
            logger.warn(f"selector picker: ignoring command: {str(error)[:200]}")
    count = reply.get("count")
    if isinstance(count, dict):
        picker.handle_count(count)
    return active
