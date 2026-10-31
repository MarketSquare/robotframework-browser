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
from ..recorder.cells import cell
from ..recorder.driver import run_session
from ..recorder.names import collect_known_keywords
from ..recorder.picker import SelectorPicker, run_picker
from ..recorder.session import RecorderSession
from ..recorder.target import FileTarget, LogTarget, Target, unwritable_reason
from ..utils import SelectorGenerator, keyword, logger

__all__ = ["Recorder"]

SUITE_SOURCE = "${SUITE_SOURCE}"
DEFAULT_IDLE_TIMEOUT = timedelta(minutes=5)


def _suite_source() -> str | None:
    try:
        return BuiltIn().get_variable_value("${SUITE_SOURCE}")
    except RobotNotRunningError:
        return None


def _suite_file() -> Path:
    """The file of the running suite; for a directory suite its ``__init__.robot``.

    Robot reports a directory suite's source as the directory, and keeps no
    record of which initialisation file it read.
    """
    source = _suite_source()
    if not source:
        raise ValueError(
            "No 'file' given and no running suite to record into. Give the "
            "target file explicitly, e.g. Record Keywords    ${CURDIR}/keywords.resource"
        )
    path = Path(source).resolve()
    if not path.is_dir():
        return path
    init = path / "__init__.robot"
    if init.is_file():
        return init
    raise ValueError(
        f"The running suite is the directory {path}, which has no __init__.robot to "
        "record into. Give the target file explicitly, e.g. file=${CURDIR}/keywords.resource"
    )


class _GrpcRecorderClient:
    def __init__(self, library: LibraryComponent) -> None:
        self._library = library
        # Set by an accepted reset poll. A start refused because another session
        # runs in the context must not stop that one.
        self._started = False

    def poll(self, state: dict, reset: bool, request: dict | None = None) -> dict:
        body = json.dumps(
            {
                **(request or {}),
                "state": state,
                "reset": reset,
                "allowHeadless": self._library.recorder_allows_headless,
            }
        )
        with self._library.playwright.grpc_channel() as stub:
            response = stub.RecorderPoll(Request().Json(body=body))
        self._started = True
        try:
            reply = json.loads(response.json)
        except ValueError:
            reply = None
        if not isinstance(reply, dict):
            raise RuntimeError(
                f"The recorder sent an unreadable reply: {response.json[:200]!r}"
            )
        return reply

    def stop(self) -> None:
        if not self._started:
            return
        with self._library.playwright.grpc_channel() as stub:
            stub.RecorderStop(Request().Empty())


class _GrpcPickerClient:
    def __init__(self, library: LibraryComponent) -> None:
        self._library = library
        # As for the recorder: a refused start does not stop the session running.
        self._started = False

    def poll(self, state: dict, request: dict, reset: bool) -> dict:
        body = json.dumps(
            {
                **request,
                "state": state,
                "reset": reset,
                "allowHeadless": self._library.recorder_allows_headless,
            }
        )
        with self._library.playwright.grpc_channel() as stub:
            response = stub.SelectorPickerPoll(Request().Json(body=body))
        self._started = True
        try:
            reply = json.loads(response.json)
        except ValueError:
            reply = None
        if not isinstance(reply, dict):
            raise RuntimeError(
                f"The selector picker sent an unreadable reply: {response.json[:200]!r}"
            )
        return reply

    def stop(self) -> None:
        if not self._started:
            return
        with self._library.playwright.grpc_channel() as stub:
            stub.SelectorPickerStop(Request().Empty())


class Recorder(LibraryComponent):
    @keyword(tags=("Recorder",))
    def record_keyword(
        self,
        name: str,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = DEFAULT_IDLE_TIMEOUT,
    ) -> str:
        """Record browser interactions as one User Keyword named ``name``.

        Shows the Robot Framework recorder toolbar on the pages of the *current* browser
        context and blocks until the recording ends. Every Action becomes a Keyword Call
        to a Browser keyword, is listed in the toolbar and is written to ``file``
        immediately.

        Toolbar buttons (each has a tooltip):

        - *✕* in the header: ends the session.
        - *Minimize* in the header (a dash): minimizes the toolbar.
        - *Discard*: drops the Keyword Calls recorded so far and starts the keyword again, empty.
        - *Undo*: removes the Keyword Calls of the last Action.
        - *Pause* (two bars): stops recording until *Resume*; Actions in between are not
          recorded.
        - *Pick* in the header: picks an element on the page, as `Record Selector` does,
          and adds its selector to the keyword as a comment row
          ``# Picked Selector    <selector>``. Playwright's own Pick locator button opens
          the same picker. While picking, nothing is recorded; *Cancel* returns to
          recording without a row.

        The toolbar is in the recording state from the start. Click a value or a selector in
        the toolbar to turn the whole of it, or a marked part, into a Keyword Argument, named
        like ``email`` or ``${email}``. The same dialog asks whether the marked value
        becomes the argument's default. The toolbar also offers to use the new argument
        for the same value elsewhere in the keyword (replacing repeated values).

        The keyword is always created new: an existing keyword is never extended.

        The recording ends with *Save* or *✕* in the toolbar, with Playwright's Record button,
        when ``idle_timeout`` passes without any Action or toolbar command, when all
        pages are closed, or on an error. The keyword being recorded is saved unless it
        has no Keyword Calls.

        | =Arguments= | =Description= |
        | ``name`` | Name of the User Keyword to create. It must not exist in ``file`` and must not shadow any keyword the running suite can call. |
        | ``file`` | Target ``.robot`` or ``.resource`` file. Defaults to ``${SUITE_SOURCE}``, the file of the running suite; in a suite initialisation file that is its ``__init__.robot``, and a keyword recorded there can only be used in that file. A relative path is resolved against the current working directory, not against the suite; use ``${CURDIR}`` for a file next to the suite. The folder must exist and an existing file must be writable; both are checked before recording starts. With ``${None}`` nothing is written; the keyword is logged to the console and to the log at INFO level instead. |
        | ``idle_timeout`` | Ends the recording after this long without an Action or toolbar command. Must be greater than zero. Default: 5 minutes, so a forgotten recording does not block the run for good. ``${None}`` waits without limit. |

        Returns the text of the recorded keyword, including the ``*** Keywords ***`` header.
        If a recorded keyword cannot be written - the file became read-only, the disk is
        full - the keyword fails, and the recorded text is logged as a warning so
        nothing is lost.

        What is generated: every keyword gets ``[Tags]    recorded``. A popup or new tab
        becomes ``Switch Page    NEW``. An Action on another open page gets a
        ``Switch Page`` to it first, using the id the Switch Page that left that page
        returned (``${page}=    Switch Page    NEW``); a page closed by hand becomes
        ``Close Page``, or ``Close Page    ${page}`` when it is not the active one. A page
        the keyword has no id of, for example one open before the recording, cannot be
        switched to, and the toolbar says so. A dialog gets ``Handle Future Dialogs    action=accept``
        before the Action (Playwright does not report whether the dialog was accepted);
        a download is wrapped in ``Promise To Wait For Download`` and ``Wait For``. A file
        chosen in a file chooser wraps the click that opened it in ``Promise To Upload File``
        and ``Wait For``; the page never reveals the file's folder, so the path reads
        ``<define_path_to_file>/<file name>`` and must be completed (or made an argument).
        Playwright's Assert snapshot becomes ``Get Aria Snapshot`` with an exact YAML
        comparison, and Assert visibility becomes ``Get Element States    ...    *=    visible``.
        Playwright folds a navigation that happens within 5 seconds after a click, fill or
        key press into that Action, so it is not recorded as a ``Go To`` of its own.
        Hovers are not recorded,
        because Playwright does not report them. Other Actions without a
        Browser keyword are only reported in the toolbar.

        Needs a visible browser: fails if the active browser was opened headless, since
        nobody could use the toolbar there. A browser attached with `Connect To Browser`
        is assumed to be visible.

        Limitations: only the *current* browser context is recorded; other contexts are
        ignored. Playwright's own recorder toolbar is shown at the top centre of the page
        during the recording and cannot be hidden, so it covers the page there. The
        toolbar does not appear on a page whose Content-Security-Policy allows only
        Trusted Types policies it names, nor in a document without a body, such as an
        SVG file. A modal ``<dialog>`` of the page covers the toolbar until it is
        closed, and a click there is recorded on the dialog.

        *Review a recorded keyword before you commit it.* Its values come from the page
        under test, including anything typed into password fields. During the session
        the toolbar state, including the recorded values and typed text, is readable by
        scripts of every page in the context, and those scripts can send toolbar commands.
        Keystrokes typed into the toolbar do not reach the page, except to a ``window``
        capture listener the page registered before the toolbar was injected.

        Requires a Playwright version that offers the programmatic recorder. The context
        stays prepared for recording after the session ends.

        Example:
        | ${text} =    Record Keyword    Login As Admin
        | Record Keyword    Search Product    ${CURDIR}/shop.resource    idle_timeout=15 min
        | Record Keyword    Try Something    file=${None}

        See `Record Keywords` to record several keywords in one session.
        """
        return self._record(file, idle_timeout, fixed_name=name).text()

    @keyword(tags=("Recorder",))
    def record_keywords(
        self,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = DEFAULT_IDLE_TIMEOUT,
    ) -> str:
        """Record several User Keywords in one session.

        Use *Record keyword* in the toolbar to name and start a keyword, record it, and
        *Save* it; then start the next one. Actions while no keyword is being recorded
        are not captured, so you can navigate freely between keywords. A name must not
        exist in ``file``, must not have been recorded earlier in the session, and must
        not shadow any keyword the running suite can call - such names are rejected in
        the toolbar.

        Shows the Robot Framework recorder toolbar on the pages of the *current* browser
        context and blocks until the recording ends. Every Action becomes a Keyword Call
        to a Browser keyword, is listed in the toolbar and is written to ``file``
        immediately.

        Toolbar buttons (each has a tooltip):

        - *✕* in the header: ends the session.
        - *Minimize* in the header (a dash): minimizes the toolbar.
        - *Record keyword*: names and starts a keyword.
        - *Discard*: drops the keyword being recorded, also from ``file``, and returns to idle.
        - *Undo*: removes the Keyword Calls of the last Action.
        - *Pause* (two bars): stops recording until *Resume*; Actions in between are not
          recorded.
        - *Pick* in the header: picks an element on the page, as `Record Selector` does,
          and adds its selector to the keyword as a comment row
          ``# Picked Selector    <selector>``. Playwright's own Pick locator button opens
          the same picker. While picking, nothing is recorded; *Cancel* returns to
          recording without a row.
        - *Save*: saves the keyword being recorded and returns to idle.

        While the toolbar is minimized, its header offers *Start* (idle) or *Save*
        (recording).

        The toolbar is idle until a keyword is started; Actions while idle are not recorded.
        While recording, click a value or a selector in the toolbar to turn the whole of it,
        or a marked part, into a Keyword Argument, named like ``email`` or ``${email}``. The same
        dialog asks whether the marked value becomes the argument's default. The toolbar
        also offers to use the new argument for the same value elsewhere in the keyword
        (replacing repeated values).

        Existing keywords are never extended.

        The recording ends with *✕* in the toolbar header, with Playwright's Record button,
        when ``idle_timeout`` passes without any Action or toolbar command, when all
        pages are closed, or on an error. The keyword being recorded is saved unless it
        has no Keyword Calls.

        | =Arguments= | =Description= |
        | ``file`` | Target ``.robot`` or ``.resource`` file. Defaults to ``${SUITE_SOURCE}``, the file of the running suite; in a suite initialisation file that is its ``__init__.robot``, and a keyword recorded there can only be used in that file. A relative path is resolved against the current working directory, not against the suite; use ``${CURDIR}`` for a file next to the suite. The folder must exist and an existing file must be writable; both are checked before recording starts. With ``${None}`` nothing is written; the keywords are logged to the console and to the log at INFO level instead. |
        | ``idle_timeout`` | Ends the recording after this long without an Action or toolbar command. Must be greater than zero. Default: 5 minutes, so a forgotten recording does not block the run for good. ``${None}`` waits without limit. |

        Returns the text of all keywords recorded in the session, under one
        ``*** Keywords ***`` header.
        If a recorded keyword cannot be written - the file became read-only, the disk is
        full - the keyword fails, and the recorded text is logged as a warning so
        nothing is lost.

        What is generated: every keyword gets ``[Tags]    recorded``. A popup or new tab
        becomes ``Switch Page    NEW``. An Action on another open page gets a
        ``Switch Page`` to it first, using the id the Switch Page that left that page
        returned (``${page}=    Switch Page    NEW``); a page closed by hand becomes
        ``Close Page``, or ``Close Page    ${page}`` when it is not the active one. A page
        the keyword has no id of, for example one open before the recording, cannot be
        switched to, and the toolbar says so. A dialog gets ``Handle Future Dialogs    action=accept``
        before the Action (Playwright does not report whether the dialog was accepted);
        a download is wrapped in ``Promise To Wait For Download`` and ``Wait For``. A file
        chosen in a file chooser wraps the click that opened it in ``Promise To Upload File``
        and ``Wait For``; the page never reveals the file's folder, so the path reads
        ``<define_path_to_file>/<file name>`` and must be completed (or made an argument).
        Playwright's Assert snapshot becomes ``Get Aria Snapshot`` with an exact YAML
        comparison, and Assert visibility becomes ``Get Element States    ...    *=    visible``.
        Playwright folds a navigation that happens within 5 seconds after a click, fill or
        key press into that Action, so it is not recorded as a ``Go To`` of its own.
        Hovers are not recorded,
        because Playwright does not report them. Other Actions without a
        Browser keyword are only reported in the toolbar.

        Needs a visible browser: fails if the active browser was opened headless, since
        nobody could use the toolbar there. A browser attached with `Connect To Browser`
        is assumed to be visible.

        Limitations: only the *current* browser context is recorded; other contexts are
        ignored. Playwright's own recorder toolbar is shown at the top centre of the page
        during the recording and cannot be hidden, so it covers the page there. The
        toolbar does not appear on a page whose Content-Security-Policy allows only
        Trusted Types policies it names, nor in a document without a body, such as an
        SVG file. A modal ``<dialog>`` of the page covers the toolbar until it is
        closed, and a click there is recorded on the dialog.

        *Review recorded keywords before you commit them.* Their values come from the page
        under test, including anything typed into password fields. During the session
        the toolbar state, including the recorded values and typed text, is readable by
        scripts of every page in the context, and those scripts can send toolbar commands.
        Keystrokes typed into the toolbar do not reach the page, except to a ``window``
        capture listener the page registered before the toolbar was injected.

        Requires a Playwright version that offers the programmatic recorder. The context
        stays prepared for recording after the session ends.

        Example:
        | ${text} =    Record Keywords
        | Record Keywords    ${CURDIR}/resources/shop.resource    idle_timeout=${None}

        See `Record Keyword` to record exactly one keyword.
        """
        return self._record(file, idle_timeout, fixed_name=None).text()

    @keyword(tags=("Recorder", "PageContent"))
    def record_selector(
        self,
        label: str | None = None,
        generator: SelectorGenerator = SelectorGenerator.playwright,
        idle_timeout: timedelta | None = DEFAULT_IDLE_TIMEOUT,
    ) -> str:
        """Pick an element on the active page and return a selector for it.

        Shows the Robot Framework toolbar on the active page and blocks until a selector
        is chosen. Move the pointer over the page: Playwright highlights the element under
        it and names it in a tooltip. Click to pick it; the click does not reach the page.
        Elements inside frames and open shadow roots can be picked too.

        The toolbar then shows the selector for the picked element:

        - *Playwright* / *CSS*: switches between the selector generators for the same
          element, see `SelectorGenerator`.
        - The selector itself can be edited. The elements it finds stay highlighted on the
          page, and the toolbar counts them; after an edit both follow once typing pauses
          for a second. One match is what most keywords need, several are shown as a
          warning, none as an error. The highlight ends with the keyword.
        - *Highlight* (a dashed square): switches the highlight off and on; it is on by
          default.
        - *Reselect*: picks another element.
        - *Use*: returns the selector, also when it does not find exactly one element.
        - *✕* in the header, or Escape in the toolbar: cancels, and the keyword fails.
        - Minimized, the header offers *Reselect* and *Use* once an element is picked.

        | =Arguments= | =Description= |
        | ``label`` | Shown in the toolbar header, to say which element to pick. |
        | ``generator`` | The generator the toolbar starts with; the toolbar can switch it. ``playwright`` (default) or ``css``. |
        | ``idle_timeout`` | Fails the keyword after this long without a pick or toolbar command. Must be greater than zero. Default: 5 minutes. ``${None}`` waits without limit. |

        Fails in a headless browser, while a `Record Keyword` or `Record Keywords` session
        runs in the browser context, when the page is closed, on cancel and when the
        ``idle_timeout`` passes.

        The toolbar has the limits of the `Record Keyword` toolbar: it does not appear on a
        page whose Content-Security-Policy allows only Trusted Types policies it names, nor
        in a document without a body.

        Like the recorder toolbar, the toolbar's commands are reachable by scripts of the
        page under test: use it on applications you trust, and check the selector you get.

        Example:
        | ${selector} =    `Record Selector`    Login button
        | `Click`    ${selector}
        | ${heading} =    `Record Selector`    Page header    generator=css
        | `Get Text`    ${heading}    ==    Expected text

        [https://forum.robotframework.org/t//4315|Comment >>]
        """
        if idle_timeout is not None and idle_timeout <= timedelta(0):
            raise ValueError(
                f"'idle_timeout' must be greater than zero, got {idle_timeout}."
            )
        picker = SelectorPicker(label or None, generator.name)
        selector = run_picker(
            picker,
            _GrpcPickerClient(self),
            idle_timeout=idle_timeout.total_seconds()
            if idle_timeout is not None
            else None,
        )
        # As a cell of a Keyword Call, ready to be pasted into a test.
        shown = cell(selector)
        logger.console(f"\nSelector{' for ' + label if label else ''}: {shown}")
        logger.info(f"Selector{' for ' + label if label else ''}: {shown}")
        return selector

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
        try:
            run_session(
                session,
                self._client(),
                idle_timeout=idle_timeout.total_seconds()
                if idle_timeout is not None
                else None,
            )
        finally:
            # Nothing recorded may be lost silently: what could not be written
            # is logged in full, to be copied from there.
            if session.unsaved:
                logger.warn(
                    "Recorded keyword(s) that could not be written:\n*** Keywords ***\n"
                    + "\n".join(keyword.block() for keyword in session.unsaved)
                )
        if session.unsaved:
            names = ", ".join(f"'{keyword.name}'" for keyword in session.unsaved)
            raise RuntimeError(
                f"{session.write_error}. {names} not saved; the recorded text is in the log."
            )
        return session

    def _client(self) -> _GrpcRecorderClient:
        return _GrpcRecorderClient(self)

    @staticmethod
    def _target(file: str | None) -> Target:
        if file is None:
            return LogTarget()
        if file == SUITE_SOURCE:
            path = _suite_file()
        else:
            path = Path(file).resolve()
            if path.is_dir():
                raise ValueError(
                    f"'file' must be a .robot or .resource file, but {path} is a directory."
                )
        reason = unwritable_reason(path)
        if reason:
            raise ValueError(f"Cannot record into {path}: {reason}.")
        return FileTarget(path)
