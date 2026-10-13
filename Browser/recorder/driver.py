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
Actions, signals and toolbar commands up. That keeps every end condition -
Stop, Playwright's Record button, closed pages, the idle timeout - in one place.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, Protocol

from robot.api import logger

from .session import RecorderSession

POLL_INTERVAL = 0.2


class RecorderClient(Protocol):
    def poll(self, state: dict, reset: bool) -> dict: ...

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
            reply = client.poll(session.toolbar_state(), reset)
            reset = False
            if _apply(session, reply):
                last_activity = clock()
            session.tick()
            _drain_log(session)
            if session.stopped:
                return "stop"
            if reply.get("mode") == "stopped":
                # Playwright flushes the Action it was holding back when its
                # Record button stops the recording; take it before closing.
                _apply(session, client.poll(session.toolbar_state(), False))
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
            names = session.close()
        except Exception as error:
            logger.debug(f"recorder: close failed: {error!r}")
        _drain_log(session)
        try:
            client.stop()
        except Exception as error:
            logger.debug(f"recorder: stop failed: {error!r}")
        logger.info(f"Recorded {len(names)} keyword(s): {', '.join(names) or '-'}")


def _apply(session: RecorderSession, reply: dict) -> bool:
    """Apply one poll reply. True if it carried any Action or command."""
    events = reply.get("events") or []
    commands = reply.get("commands") or []
    for entry in events:
        _safely(session, "event", entry)
    for command in commands:
        _safely(session, "command", command)
    return bool(events or commands)


def _safely(session: RecorderSession, kind: str, entry: Any) -> None:
    """Survive one malformed event or command: the channel is page-callable (ADR 0010)."""
    try:
        if kind == "event":
            session.handle_event(
                str(entry.get("event", "added")), dict(entry.get("action") or {})
            )
        else:
            session.handle_command(dict(entry))
    except Exception as error:
        logger.warn(f"recorder: ignoring {kind} {entry!r}: {error!r}")


def _drain_log(session: RecorderSession) -> None:
    for entry in session.log:
        logger.info(f"recorder: {entry}")
    session.log.clear()
