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
"""The poll loop of a Recording Session.

Python is the only clock: each poll pushes the toolbar state down and drains
Actions, signals and toolbar commands up, in the order they happened. That keeps every end condition -
Stop, Playwright's Record button, closed pages, the idle timeout - in one place.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol

from robot.api import logger

from .session import RecorderSession

POLL_INTERVAL = 0.2
#: Ignored entries come from the page under test and may be huge (ADR 0010).
LOGGED_REPR_LIMIT = 200


class RecorderClient(Protocol):
    def poll(self, state: dict, reset: bool, request: dict | None = None) -> dict:
        """One poll reply; raises if Node's reply cannot be read. ``request``
        carries what the toolbar's Pick button needs of Node."""
        ...

    def stop(self) -> None: ...


def run_session(
    session: RecorderSession,
    client: RecorderClient,
    idle_timeout: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Drive ``session`` until it ends and return why it ended."""
    last_activity = clock()
    reset = True
    try:
        while True:
            reply = client.poll(session.toolbar_state(), reset, session.request())
            reset = False
            session.set_active_page(reply.get("activePage"))
            session.set_picking(reply.get("picking") is True)
            if _apply_pick(session, reply):
                last_activity = clock()
            if _apply(session, reply):
                last_activity = clock()
            session.tick()
            _drain_log(session)
            if session.stopped:
                return "stop"
            if reply.get("mode") == "stopped":
                # Playwright flushes the Action it was holding back when its
                # Record button stops the recording; take it before closing.
                _drain_after_stop(session, client)
                return "playwright"
            if not reply.get("pages"):
                logger.info("recorder: all pages closed, ending the session")
                return "pages"
            if idle_timeout is not None and clock() - last_activity >= idle_timeout:
                logger.info("recorder: idle timeout reached, ending the session")
                return "idle"
            sleep(POLL_INTERVAL)
    finally:
        # An aborted run must still leave a well-formed keyword behind, and no
        # cleanup failure may replace an exception already propagating.
        names: list[str] = []
        try:
            try:
                names = session.close()
            except Exception as error:
                logger.warn(f"recorder: close failed: {error!r}")
            _drain_log(session)
        finally:
            try:
                client.stop()
            except Exception as error:
                logger.debug(f"recorder: stop failed: {error!r}")
        logger.info(f"Recorded {len(names)} keyword(s): {', '.join(names) or '-'}")


def _entries(reply: dict) -> list[dict]:
    """The well-formed entries of the reply, in the order they happened.

    An entry is an Action or signal (``{"event": ..., "action": ...}``) or a
    toolbar command (``{"command": {...}}``); anything else is dropped.
    """
    value = reply.get("entries")
    if not isinstance(value, list):
        return []
    return [
        entry
        for entry in value
        if isinstance(entry, dict)
        and ("command" not in entry or isinstance(entry["command"], dict))
    ]


def _apply_pick(session: RecorderSession, reply: dict) -> bool:
    """The Pick button's part of a reply; True if something was picked or asked for."""
    active = False
    if reply.get("pickRequested") is True:
        session.request_pick()
        active = True
    picked = reply.get("picked")
    if isinstance(picked, dict):
        session.handle_picked(picked)
        active = True
    count = reply.get("count")
    if isinstance(count, dict):
        session.handle_count(count)
    return active


#: A reply carries a bounded number of entries; this many more polls take what
#: Playwright still had when its Record button stopped the recording.
FINAL_POLLS = 20


def _drain_after_stop(session: RecorderSession, client: RecorderClient) -> None:
    try:
        for _ in range(FINAL_POLLS):
            reply = client.poll(session.toolbar_state(), False)
            _apply(session, reply)
            if not _entries(reply):
                return
    except Exception as error:
        logger.warn(f"recorder: final poll failed: {error!r}")


def _apply(session: RecorderSession, reply: dict) -> bool:
    """Apply one poll reply in order: an Undo clicked before an Action undoes
    the Action before it, not that one.

    True if it carried an Action or a command the toolbar has: junk from the
    page under test must not keep an idle session alive.
    """
    active = False
    for entry in _entries(reply):
        if "command" in entry:
            what = f"command {entry['command']!r}"
            active = _safely(what, _handle_command, session, entry) or active
        else:
            active = (
                _safely(f"event {entry!r}", _handle_event, session, entry) or active
            )
    return active


def _handle_event(session: RecorderSession, entry: dict) -> bool:
    page = entry.get("page")
    session.handle_event(
        str(entry.get("event", "added")),
        dict(entry.get("action") or {}),
        page if isinstance(page, str) else None,
    )
    return True


def _handle_command(session: RecorderSession, entry: dict) -> bool:
    return session.handle_command(entry["command"])


def _safely(
    what: str,
    handler: Callable[[RecorderSession, dict], bool],
    session: RecorderSession,
    entry: dict,
) -> bool:
    """Survive one malformed event or command: the channel is page-callable (ADR 0010)."""
    try:
        return handler(session, entry)
    except Exception as error:
        logger.warn(f"recorder: ignoring {_truncate(what)}: {_truncate(repr(error))}")
        return False


def _truncate(text: str) -> str:
    if len(text) <= LOGGED_REPR_LIMIT:
        return text
    return text[:LOGGED_REPR_LIMIT] + "..."


def _drain_log(session: RecorderSession) -> None:
    for entry in session.log:
        logger.info(f"recorder: {entry}")
    session.log.clear()
