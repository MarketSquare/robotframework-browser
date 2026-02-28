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

from datetime import timedelta
from pathlib import Path

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import NewPageDetails, keyword, logger
from ..utils.data_types import PageLoadStates


class Electron(LibraryComponent):
    """Keywords for launching and controlling Electron applications."""

    @keyword(tags=("Setter", "BrowserControl"))
    def new_electron_application(
        self,
        executable_path: Path,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        timeout: timedelta | None = None,
        wait_until: PageLoadStates = PageLoadStates.domcontentloaded,
    ) -> tuple[str, str, NewPageDetails]:
        """Launches an Electron application and sets its first window as the active page.

        Uses Playwright's Electron API: ``_electron.launch()`` →
        ``ElectronApplication`` → ``firstWindow()`` → ``Page`` → ``page.context()``.

        After this keyword, standard Browser library page keywords (``Click``,
        ``Get Text``, ``Wait For Elements State``, etc.) work against the
        Electron window without any extra setup.

        Returns a tuple of ``(browser_id, context_id, page_details)`` — the same
        shape as `New Persistent Context` — so ``Switch Page`` works if multiple
        windows are open.

        | =Argument=           | =Description= |
        | ``executable_path``  | Path to the Electron runtime binary (e.g. ``node_modules/.bin/electron``) or a packaged application executable. |
        | ``args``             | Optional list of command-line arguments forwarded to the Electron process. Pass the path to ``main.js`` here when using the bare Electron binary. |
        | ``env``              | Optional mapping of environment variables merged with the current process environment. |
        | ``timeout``          | Timeout for ``firstWindow()``. Defaults to the library default timeout. |
        | ``wait_until``       | Page load state to wait for before returning. One of ``load``, ``domcontentloaded`` (default), or ``networkidle``. |

        Example — bare Electron binary with source:
        | ${ELECTRON}=    Set Variable    node_modules/.bin/electron
        | @{ARGS}=        Create List     node/electron-test-app/main.js
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=${ELECTRON}    args=@{ARGS}
        | `Get Title`    ==    My App

        Example — packaged executable:
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=/usr/share/myapp/myapp
        | `Get Title`    ==    My App

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        timeout_ms = int(timeout.total_seconds() * 1000) if timeout else int(self.timeout)

        with self.playwright.grpc_channel() as stub:
            req = Request().ElectronLaunch(
                executable_path=str(executable_path),
                args=args or [],
                timeout=timeout_ms,
            )
            if env:
                req.env.update(env)
            response = stub.LaunchElectron(req)
            logger.info(response.log)

            load_resp = stub.WaitForPageLoadState(
                Request().PageLoadState(state=wait_until.name, timeout=timeout_ms)
            )
            logger.info(load_resp.log)

            return (
                response.browserId,
                response.id,
                NewPageDetails(page_id=response.pageId, video_path=None),
            )

    @keyword(tags=("Setter", "BrowserControl"))
    def close_electron_application(self) -> None:
        """Closes the running Electron application and cleans up library state.

        Removes the associated browser, context, and page from the Browser library
        state stack.  After this keyword there is no active browser; use
        `New Browser` or another state-creating keyword before issuing further
        page interactions.

        Calling this keyword when no Electron app is open is safe and does nothing.

        Example:
        | `New Electron Application`    executable_path=/path/to/app
        | # ... test steps ...
        | `Close Electron Application`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseElectron(Request().Empty())
            logger.info(response.log)

    @keyword(tags=("Getter", "BrowserControl"))
    def open_electron_dev_tools(self) -> None:
        """Opens Chromium DevTools for every window of the running Electron application.

        Calls ``BrowserWindow.getAllWindows()`` in the Electron **main process**
        via ``ElectronApplication.evaluate()``.  This is necessary because Node.js
        and Electron APIs are only available in the main process, not in renderer
        contexts where ``Evaluate JavaScript`` executes.

        Intended as a development-time debugging aid for locating element selectors.

        Example:
        | `New Electron Application`    executable_path=/path/to/app
        | `Open Electron Dev Tools`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.OpenElectronDevTools(Request().Empty())
            logger.info(response.log)
