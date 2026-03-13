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

import json
from copy import copy
from datetime import timedelta
from pathlib import Path

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    ColorScheme,
    GeoLocation,
    HttpCredentials,
    NewPageDetails,
    RecordHar,
    RecordVideo,
    ViewportDimensions,
    keyword,
    locals_to_params,
    logger,
)


class Electron(LibraryComponent):
    """Keywords for launching and controlling Electron applications."""

    @keyword(tags=("Setter", "BrowserControl"))
    def new_electron_application(
        self,
        executable_path: Path,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        timeout: timedelta = timedelta(seconds=30),
        *,
        acceptDownloads: bool = True,
        bypassCSP: bool = False,
        colorScheme: ColorScheme | None = None,
        cwd: str | None = None,
        extraHTTPHeaders: dict[str, str] | None = None,
        geolocation: GeoLocation | None = None,
        hasTouch: bool | None = None,
        httpCredentials: HttpCredentials | None = None,
        ignoreHTTPSErrors: bool = False,
        isMobile: bool | None = None,
        javaScriptEnabled: bool = True,
        locale: str | None = None,
        offline: bool = False,
        recordHar: RecordHar | None = None,
        recordVideo: RecordVideo | None = None,
        slowMo: timedelta = timedelta(seconds=0),
        timezoneId: str | None = None,
        tracesDir: str | None = None,
        viewport: ViewportDimensions | None = ViewportDimensions(
            width=1280, height=720
        ),
    ) -> tuple[str, str, NewPageDetails]:
        """Launches an Electron application and sets its first window as the active page.

        Uses Playwright's ``_electron.launch()`` API to start the application, then
        attaches the first window as the active ``Page``.  All standard Browser library
        page keywords (``Click``, ``Get Text``, ``Wait For Elements State``, …) work
        against the Electron window without any extra setup.

        Returns a ``(browser_id, context_id, page_details)`` tuple — the same shape as
        `New Persistent Context` — so ``Switch Page`` and friends work if multiple
        windows are open.

        *Note on headless mode*

        Playwright does not expose a ``headless`` option for Electron — the application
        always opens a native GUI window.  On Linux CI machines, run the process inside a
        virtual display:

        | # Before running tests, start a virtual display:
        | Xvfb :99 -screen 0 1280x720x24 &
        | export DISPLAY=:99

        | =Argument=            | =Description= |
        | ``executable_path``   | Path to the Electron binary or packaged application executable. When using the bare ``electron`` npm package pass the path to ``main.js`` via ``args``. |
        | ``args``              | Additional command-line arguments forwarded to the Electron process. Use this to pass the entry-point script when running the bare Electron binary, e.g. ``[node/my-app/main.js]``. |
        | ``env``               | Environment variables for the launched process. Merged on top of the current process environment so ``PATH`` and other system variables are still inherited. |
        | ``timeout``           | Maximum time to wait for the first window to appear. Defaults to ``30 seconds``. Pass ``0`` to disable. |
        | ``acceptDownloads``   | Whether to automatically download all attachments. Defaults to ``True``. |
        | ``bypassCSP``         | Toggles bypassing page's Content-Security-Policy. Defaults to ``False``. |
        | ``colorScheme``       | Emulates ``prefers-color-scheme`` media feature: ``dark``, ``light``, ``no-preference``, or ``null`` to disable emulation. |
        | ``cwd``               | Working directory for the launched Electron process. Defaults to the current working directory. |
        | ``extraHTTPHeaders``  | Additional HTTP headers sent with every renderer request. |
        | ``geolocation``       | Geolocation to emulate. Dictionary with ``latitude``, ``longitude``, and optional ``accuracy`` keys. |
        | ``hasTouch``          | Whether the viewport should support touch events. |
        | ``httpCredentials``   | Credentials for HTTP Basic Authentication. Dictionary with ``username`` and ``password`` keys. |
        | ``ignoreHTTPSErrors`` | Whether to ignore HTTPS errors during navigation. Defaults to ``False``. |
        | ``isMobile``          | Whether to emulate a mobile device (meta-viewport tag, touch events, …). |
        | ``javaScriptEnabled`` | Whether to enable JavaScript in the renderer. Defaults to ``True``. |
        | ``locale``            | Renderer locale, e.g. ``en-GB``. Affects ``navigator.language`` and date/number formatting. |
        | ``offline``           | Emulates network being offline. Defaults to ``False``. |
        | ``recordHar``         | Enable HAR recording. Dictionary with ``path`` (required) and optional ``omitContent``. |
        | ``recordVideo``       | Enable video recording. Dictionary with ``dir`` (required) and optional ``size``. |
        | ``slowMo``            | Slows down all Playwright operations by the given duration. Useful for visual debugging. Defaults to no delay. |
        | ``timezoneId``        | Overrides the system timezone for the renderer, e.g. ``Europe/Berlin``. |
        | ``tracesDir``         | Directory where Playwright trace files are written. |
        | ``viewport``          | Initial viewport dimensions. Defaults to ``{'width': 1280, 'height': 720}``. Pass ``None`` to use the native window size. |

        Example — bare Electron binary with a source checkout:
        | ${ELECTRON}=    Set Variable    node_modules/.bin/electron
        | @{ARGS}=        Create List     node/electron-test-app/main.js
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=${ELECTRON}    args=@{ARGS}
        | `Get Title`    ==    My App

        Example — packaged application executable:
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=/usr/share/myapp/myapp
        | `Get Title`    ==    My App

        Example — French locale, larger viewport, video recording:
        | &{VIDEO}=    Create Dictionary    dir=videos
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=/usr/share/myapp/myapp
        | ...    locale=fr-FR
        | ...    viewport={'width': 1920, 'height': 1080}
        | ...    recordVideo=${VIDEO}

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        options = locals_to_params(locals())
        timeout_ms = int(timeout.total_seconds() * 1000)
        slow_mo_ms = int(slowMo.total_seconds() * 1000)

        options["executablePath"] = str(options.pop("executable_path"))
        options["timeout"] = timeout_ms
        options.pop("slowMo", None)
        if slow_mo_ms > 0:
            options["slowMo"] = slow_mo_ms
        if viewport is not None:
            options["viewport"] = copy(viewport)

        with self.playwright.grpc_channel() as stub:
            response = stub.LaunchElectron(
                Request().ElectronLaunch(
                    rawOptions=json.dumps(options, default=str),
                    defaultTimeout=timeout_ms,
                )
            )
            logger.info(response.log)

            if recordVideo is not None:
                self.context_cache.add(
                    response.id, self.library._playwright_state._get_video_size(options)
                )
            video_path = self.library._playwright_state._embed_video(
                json.loads(response.video)
            )

            return (
                response.browserId,
                response.id,
                NewPageDetails(page_id=response.pageId, video_path=video_path),
            )

    @keyword(tags=("Setter", "BrowserControl"))
    def close_electron_application(self) -> None:
        """Closes the running Electron application and cleans up library state.

        Equivalent to `Close Browser` for Electron apps. Closes the
        ``ElectronApplication`` handle and removes the associated browser, context,
        and page from the Browser library state stack.

        After this keyword there is no active browser; call `New Electron Application`,
        `New Browser`, or `New Persistent Context` before issuing further page
        interactions.

        Calling this keyword when no Electron app is open is safe — it logs a message
        and does nothing.

        Example:
        | `New Electron Application`    executable_path=/path/to/app
        | # ... test steps ...
        | [Teardown]    `Close Electron Application`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseElectron(Request().Empty())
            logger.info(response.log)

    @keyword(tags=("Getter", "BrowserControl"))
    def open_electron_dev_tools(self) -> None:
        """Opens Chromium DevTools for every window of the running Electron application.

        Calls ``BrowserWindow.getAllWindows()`` in the Electron **main process** via
        ``ElectronApplication.evaluate()``.  Node.js and Electron APIs are only
        available in the main process — renderer contexts (where `Evaluate JavaScript`
        runs) cannot access them.

        Intended as a development-time debugging aid: use it to inspect the live DOM,
        find element selectors, and debug JavaScript.

        Example:
        | `New Electron Application`    executable_path=/path/to/app
        | `Open Electron Dev Tools`
        | Sleep    30s    # manually inspect the DevTools panel
        | `Close Electron Application`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.OpenElectronDevTools(Request().Empty())
            logger.info(response.log)
