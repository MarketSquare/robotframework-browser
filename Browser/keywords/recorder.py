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

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..recorder.driver import run_session
from ..recorder.names import KnownKeywords, collect_known_keywords
from ..recorder.session import RecorderSession
from ..recorder.target import FileTarget, LogTarget, Target
from ..utils import keyword, logger

__all__ = ["KnownKeywords", "Recorder"]

SUITE_SOURCE = "${SUITE_SOURCE}"


def _suite_source() -> str | None:
    try:
        return BuiltIn().get_variable_value("${SUITE_SOURCE}")
    except RobotNotRunningError:
        return None


class _GrpcRecorderClient:
    def __init__(self, library: LibraryComponent) -> None:
        self._library = library

    def poll(self, state: dict, reset: bool) -> dict:
        body = json.dumps({"state": state, "reset": reset})
        with self._library.playwright.grpc_channel() as stub:
            response = stub.RecorderPoll(Request().Json(body=body))
        if not response.json:
            return {}
        try:
            reply = json.loads(response.json)
        except ValueError:
            logger.debug("Ignoring a recorder reply that is not valid JSON")
            return {}
        return reply if isinstance(reply, dict) else {}

    def stop(self) -> None:
        with self._library.playwright.grpc_channel() as stub:
            stub.RecorderStop(Request().Empty())


class Recorder(LibraryComponent):
    @keyword(tags=("Recorder",))
    def record_keyword(
        self,
        name: str,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = None,
    ) -> str:
        """Record browser interactions as one User Keyword named ``name``.

        Shows the Robot Framework recorder toolbar on the page of the *current* browser
        context and blocks until the recording ends. Every Action becomes a Keyword Call
        to a Browser keyword and is written to ``file`` immediately. The toolbar shows
        the Keyword Calls; *Undo* removes the last Action's Keyword Calls, *Discard*
        starts the keyword again empty. Click a value in the toolbar to turn it, or a
        marked part of it, into a Keyword Argument; its recorded value becomes the
        default, which can be deselected.

        Toolbar buttons:

        - *Stop*: ends the session.
        - *Undo*: removes the Keyword Calls of the last Action.
        - *Discard*: starts the keyword being recorded again, empty.

        The toolbar is in the recording state from the start. Click a value in the toolbar
        to turn the whole value, or a marked part of it, into a Keyword Argument; its
        recorded value becomes the default, which can be deselected. The toolbar also
        offers to use the new argument for the same value elsewhere in the keyword
        (replacing repeated values).

        The keyword is always created new: an existing keyword is never extended.
        Only the *current* browser context is recorded (limitation); other contexts are ignored.

        The recording ends with *Stop* in the toolbar, with Playwright's Record button,
        when ``idle_timeout`` passes without any Action or toolbar command, when all
        pages are closed, or on an error. The keyword being recorded is saved in every case.

        | =Arguments= | =Description= |
        | ``name`` | Name of the User Keyword to create. It must not exist in ``file`` and must not shadow any keyword the running suite can call. |
        | ``file`` | Target ``.robot`` or ``.resource`` file. Defaults to ``${SUITE_SOURCE}``, the file of the running suite. With ``${None}`` nothing is written; the keyword is logged to the console and to the log at INFO level instead. |
        | ``idle_timeout`` | Ends the recording after this long without activity. Must be greater than zero. Default: no timeout. |

        Returns the text of the recorded keyword, including the ``*** Keywords ***`` header.

        What is generated: every keyword gets ``[Tags]    recorded``. A popup or new tab
        becomes ``Switch Page    NEW``; a dialog gets ``Handle Future Dialogs`` before the
        Action; a download is wrapped in ``Promise To Wait For Download`` and ``Wait For``.
        Playwright's Assert snapshot becomes ``Get Aria Snapshot`` with an exact YAML
        comparison, and Assert visibility becomes ``Get Element States    ...    *=    visible``.
        While Playwright's Pick locator is on, nothing is recorded. File uploads and hovers
        are not recorded, because Playwright does not report them. Other Actions without a
        Browser keyword are only reported in the toolbar.

        *Review a recorded keyword before you commit it.* Its values come from the page
        under test, including anything typed into password fields.

        Requires a Playwright version that offers the programmatic recorder. The context
        stays prepared for recording after the session ends.

        Example:
        | ${text} =    Record Keyword    Login As Admin
        | Record Keyword    Search Product    ${CURDIR}/shop.resource    idle_timeout=5 min
        | Record Keyword    Try Something    file=${None}

        See `Record Keywords` to record several keywords in one session.
        """
        return self._record(file, idle_timeout, fixed_name=name).text()

    @keyword(tags=("Recorder",))
    def record_keywords(
        self,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = None,
    ) -> str:
        """Record several User Keywords in one session.

        Use *+ New Keyword* in the toolbar to name and start a keyword, record it, and
        *Finish* it; then start the next one. Actions while no keyword is being recorded
        are not captured, so you can navigate freely between keywords. A name must not
        exist in ``file``, must not have been recorded earlier in the session, and must
        not shadow any keyword the running suite can call - such names are rejected in
        the toolbar.

        Shows the Robot Framework recorder toolbar on the page of the *current* browser
        context and blocks until the recording ends. Every Action becomes a Keyword Call
        to a Browser keyword and is written to ``file`` immediately. The toolbar shows
        the Keyword Calls; *Undo* removes the last Action's Keyword Calls, *Discard*
        starts the keyword again empty. Click a value in the toolbar to turn it, or a
        marked part of it, into a Keyword Argument; its recorded value becomes the
        default, which can be deselected.

        Toolbar buttons:

        - *Stop*: ends the session.
        - *+ New Keyword*: names and starts a keyword (only in `Record Keywords`).
        - *Finish*: saves the keyword being recorded and returns to idle (only in `Record Keywords`).
        - *Undo*: removes the Keyword Calls of the last Action.
        - *Discard*: starts the keyword being recorded again, empty.

        The toolbar is idle until a keyword is started; Actions while idle are not recorded.
        While recording, click a value in the toolbar to turn the whole value, or a marked
        part of it, into a Keyword Argument; its recorded value becomes the default, which
        can be deselected. The toolbar also offers to use the new argument for the same
        value elsewhere in the keyword (replacing repeated values).

        Existing keywords are never extended. Only the *current* browser context is
        recorded (limitation); other contexts are ignored.

        The recording ends with *Stop* in the toolbar, with Playwright's Record button,
        when ``idle_timeout`` passes without any Action or toolbar command, when all
        pages are closed, or on an error. The keyword being recorded is saved in every case.

        | =Arguments= | =Description= |
        | ``file`` | Target ``.robot`` or ``.resource`` file. Defaults to ``${SUITE_SOURCE}``, the file of the running suite. With ``${None}`` nothing is written; the keyword is logged to the console and to the log at INFO level instead. |
        | ``idle_timeout`` | Ends the recording after this long without activity. Must be greater than zero. Default: no timeout. |

        Returns the text of all keywords recorded in the session, under one
        ``*** Keywords ***`` header.

        What is generated: every keyword gets ``[Tags]    recorded``. A popup or new tab
        becomes ``Switch Page    NEW``; a dialog gets ``Handle Future Dialogs`` before the
        Action; a download is wrapped in ``Promise To Wait For Download`` and ``Wait For``.
        Playwright's Assert snapshot becomes ``Get Aria Snapshot`` with an exact YAML
        comparison, and Assert visibility becomes ``Get Element States    ...    *=    visible``.
        While Playwright's Pick locator is on, nothing is recorded. File uploads and hovers
        are not recorded, because Playwright does not report them. Other Actions without a
        Browser keyword are only reported in the toolbar.

        *Review recorded keywords before you commit them.* Their values come from the page
        under test, including anything typed into password fields.

        Requires a Playwright version that offers the programmatic recorder. The context
        stays prepared for recording after the session ends.

        Example:
        | ${text} =    Record Keywords
        | Record Keywords    ${CURDIR}/resources/shop.resource    idle_timeout=10 min

        See `Record Keyword` to record exactly one keyword.
        """
        return self._record(file, idle_timeout, fixed_name=None).text()

    def _record(
        self, file: str | None, idle_timeout: timedelta | None, fixed_name: str | None
    ) -> RecorderSession:
        if idle_timeout is not None and idle_timeout <= timedelta(0):
            raise ValueError(
                f"'idle_timeout' must be greater than zero, got {idle_timeout}."
            )
        target = self._target(file)
        session = RecorderSession(
            target, fixed_name=fixed_name, known=collect_known_keywords()
        )
        logger.info(f"Recording into {target.label}")
        run_session(
            session,
            self._client(),
            idle_timeout=idle_timeout.total_seconds()
            if idle_timeout is not None
            else None,
        )
        return session

    def _client(self) -> _GrpcRecorderClient:
        return _GrpcRecorderClient(self)

    @staticmethod
    def _target(file: str | None) -> Target:
        if file is None:
            return LogTarget()
        if file == SUITE_SOURCE:
            source = _suite_source()
            if not source:
                raise ValueError(
                    "No 'file' given and no running suite to record into. Give the "
                    "target file explicitly, e.g. Record Keywords    ${CURDIR}/keywords.resource"
                )
            file = source
        path = Path(file).resolve()
        if path.is_dir():
            raise ValueError(
                f"'file' must be a .robot or .resource file, but {path} is a directory. "
                "A suite initialisation file cannot hold recorded keywords; give the "
                "target file explicitly."
            )
        return FileTarget(path)
