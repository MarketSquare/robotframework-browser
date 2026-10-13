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
"""``Record Keyword`` / ``Record Keywords`` - a recorder plugin for Browser.

Drives Playwright's programmatic recorder through the bundled ``recorder.js``
JS extension and turns the recorded, *semantic* action stream into Robot
Framework User Keywords, written live into a ``.robot`` / ``.resource`` file.

Load it with::

    Library    Browser    plugins=Browser.recorder.plugin.RecorderPlugin
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from datetime import timedelta
from pathlib import Path

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request

from .names import collect_known_keywords
from .session import RecorderSession

_JS_EXTENSION = Path(__file__).parent.resolve() / "recorder.js"
_POLL_KEYWORD = "rfbRecorderPoll"
_STOP_KEYWORD = "rfbRecorderStop"
_POLL_INTERVAL = 0.2


class RecorderPlugin(LibraryComponent):
    """Record interactions in the live browser and emit Browser User Keywords."""

    # -- keywords ---------------------------------------------------------- #

    @keyword(name="Record Keyword", tags=("Recorder",))
    def record_keyword(
        self, name: str, file: Path | None = None, timeout: timedelta | None = None
    ) -> str:
        """Record browser interactions into a User Keyword named ``name``.

        Opens the Playwright recorder in the *currently active* browser context
        and shows the Robot Framework recorder toolbar on the page. Each action
        is converted to a Browser keyword and written **live** as you go; the
        toolbar's *Undo* and *Discard* buttons correct mistakes without leaving
        the browser.

        To finish, press *Stop* in the header of the Robot Framework toolbar, or
        the red *Record* button in the Playwright toolbar. The keyword text is
        returned.

        | =Arguments= | =Description= |
        | ``name`` | Name of the User Keyword to create. Mandatory. |
        | ``file`` | Target ``.robot`` / ``.resource`` file. Defaults to the source file of the running suite. |
        | ``timeout`` | Safety net that ends the recording unattended. Defaults to no timeout, i.e. the keyword blocks until you stop the recording. |

        The name must not collide with a keyword the suite already knows -
        libraries, imported resources and the suite's own keywords - because a
        recorded keyword would silently take the existing one's place.

        Example:
        | ${keyword_text}=    Record Keyword    Login As Admin
        | Record Keyword    Search For Product    ${CURDIR}/resources/shop.resource

        See also `Record Keywords` to record several keywords in one session.
        """
        session = self._run_session(file, timeout, fixed_name=name)
        return session.text()

    @keyword(name="Record Keywords", tags=("Recorder",))
    def record_keywords(
        self, file: Path | None = None, timeout: timedelta | None = None
    ) -> list[str]:
        """Record several User Keywords in one browser session.

        Opens the Playwright recorder and shows the Robot Framework recorder
        toolbar on the page. Use *+ New Keyword* to name and start a keyword,
        record it, then *Finish* it and start the next one. Actions performed
        while no keyword is being recorded are **not** captured, so navigating
        between keywords is free.

        *Undo* removes the last recorded step and *Discard* abandons the current
        keyword entirely. Press *Stop* in the header of the Robot Framework
        toolbar, or the red *Record* button in the Playwright toolbar, to end
        the session.

        Returns the list of keyword names recorded.

        Names that collide with a keyword the suite already knows are rejected
        in the toolbar: a recorded keyword would otherwise silently take the
        existing one's place. Unlike `Record Keyword`, a name already present
        in the target file is rejected too - a session started with
        *+ New Keyword* always creates a new keyword and can never append to
        one that already exists there.

        | =Arguments= | =Description= |
        | ``file`` | Target ``.robot`` / ``.resource`` file. Defaults to the source file of the running suite. |
        | ``timeout`` | Safety net that ends the session unattended. Defaults to no timeout. |

        Example:
        | @{names}=    Record Keywords
        | Record Keywords    ${CURDIR}/resources/shop.resource
        """
        session = self._run_session(file, timeout, fixed_name=None)
        return session.keywords

    # -- session driver ---------------------------------------------------- #

    def _run_session(
        self,
        file: Path | None,
        timeout: timedelta | None,
        fixed_name: str | None,
    ) -> RecorderSession:
        target = Path(file).resolve() if file else self._default_target()
        known = collect_known_keywords()
        session = RecorderSession(
            target,
            fixed_name=fixed_name,
            known=known,
        )
        logger.info(f"Recording into {target}")

        # Registered once per session rather than cached on the plugin: node's
        # extension list lives on a per-peer state that can be re-created, and a
        # stale "already registered" would then fail with an unknown keyword.
        # Registering again is harmless - node's `require` is cached.
        self.initialize_js_extension(_JS_EXTENSION)
        deadline = (
            None if timeout is None else time.monotonic() + timeout.total_seconds()
        )
        first = True
        try:
            while True:
                reply = self._poll(session.toolbar_state(), reset=first)
                first = False
                for entry in reply.get("events") or []:
                    self._safely(
                        lambda entry=entry: session.handle_event(
                            str(entry.get("event", "added")),
                            entry.get("action") or {},
                        ),
                        f"event {entry!r}",
                    )
                for command in reply.get("commands") or []:
                    self._safely(
                        lambda command=command: session.handle_command(command or {}),
                        f"command {command!r}",
                    )
                self._drain_log(session)
                if session.stopped:
                    break
                if reply.get("mode") == "stopped":
                    break
                if not reply.get("pages"):
                    logger.info("recorder: all pages closed, ending the session")
                    break
                if deadline is not None and time.monotonic() > deadline:
                    logger.info("recorder: timeout reached, ending the session")
                    break
                time.sleep(_POLL_INTERVAL)
        finally:
            # An aborted suite must still leave a well-formed keyword behind.
            # Both cleanup steps below must always be attempted, and neither
            # may replace an exception already propagating out of the loop.
            names: list[str] = []
            try:
                names = session.close()
            except Exception as error:
                logger.debug(f"recorder: close failed: {error}")
            self._drain_log(session)
            try:
                self._call(_STOP_KEYWORD, {})
            except Exception as error:
                # Never mask the real failure with a cleanup failure.
                logger.debug(f"recorder: stop failed: {error}")
            logger.info(f"Recorded {len(names)} keyword(s): {', '.join(names) or '-'}")
        return session

    def _poll(self, state: dict, reset: bool) -> dict:
        return self._call(_POLL_KEYWORD, {"state": json.dumps(state), "reset": reset})

    def _call(self, name: str, arguments: dict) -> dict:
        """One extension-keyword round trip.

        Uses the gRPC stub rather than `call_js_keyword` because the latter logs
        every response at INFO, which at this poll rate would flood the log.
        """
        payload = {"arguments": list(arguments.items())}
        with self.playwright.grpc_channel() as stub:
            request = Request().KeywordCall(name=name, arguments=json.dumps(payload))
            body = ""
            for response in stub.CallExtensionKeyword(request):
                if response.bodyPart:
                    body += response.bodyPart
                elif response.json:
                    body = response.json
        return json.loads(body) if body else {}

    @staticmethod
    def _safely(action: Callable[[], None], what: str) -> None:
        """Run one recorder step, surviving a malformed event or command.

        Events and commands arrive over a channel the page under test can call,
        so a single bogus payload must not tear down a recording the user has
        been building for minutes. The failure is reported and the loop goes on.
        """
        try:
            action()
        except Exception as error:
            logger.warn(f"recorder: ignoring {what}: {error!r}")

    @staticmethod
    def _drain_log(session: RecorderSession) -> None:
        for entry in session.log:
            logger.info(f"recorder: {entry}")
        session.log.clear()

    @staticmethod
    def _default_target() -> Path:
        try:
            source = BuiltIn().get_variable_value("${SUITE_SOURCE}")
        except RobotNotRunningError:
            source = None
        if not source:
            raise ValueError(
                "No 'file' argument given and no running suite source is available. "
                "Provide the target file explicitly, e.g. "
                "Record Keywords    ${CURDIR}/keywords.resource"
            )
        # `${SUITE_SOURCE}` is an abspath, not a realpath: resolve it so a suite
        # reached through a symlink names the same file as its resolved path.
        return Path(source).resolve()
