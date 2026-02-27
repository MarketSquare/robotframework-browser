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

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import NewPageDetails, keyword, logger


class Electron(LibraryComponent):
    """Keywords for launching and controlling Electron applications."""

    @keyword(tags=("Setter", "BrowserControl"))
    def new_electron_application(
        self,
        executable_path: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        timeout: timedelta | None = None,
    ) -> tuple[str, str, NewPageDetails]:
        """Launches an Electron application and sets its first window as the active page.

        Uses Playwright's Electron API internally: ``_electron.launch()`` →
        ``ElectronApplication`` → ``firstWindow()`` → ``Page`` → ``page.context()``
        → ``BrowserContext``.

        After this keyword, all existing page-level Browser keywords (Click,
        Get Text, Wait For Elements State, etc.) work unchanged against the
        Electron window.

        Returns a tuple of ``(browser_id, context_id, page_details)`` — the same
        shape as `New Persistent Context` — so you can switch between windows using
        the standard ``Switch Page`` keyword if needed.

        | =Argument=           | =Description= |
        | ``executable_path``  | Absolute path to the Electron ``.exe`` / binary. Paths with spaces are supported. |
        | ``args``             | Optional list of command-line arguments passed to the Electron process. |
        | ``env``              | Optional dictionary of environment variables to merge with the current environment. |
        | ``timeout``          | Optional timeout for ``firstWindow()``. Defaults to the library default timeout. |

        Example:
        | ${browser}    ${context}    ${page}=    `New Electron Application`
        | ...    executable_path=C:/Users/me/AppData/Local/MyApp/myapp.exe
        | `Get Title`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        timeout_ms = int(timeout.total_seconds() * 1000) if timeout else int(self.timeout)

        with self.playwright.grpc_channel() as stub:
            req = Request().ElectronLaunch(
                executable_path=executable_path,
                args=args or [],
                timeout=timeout_ms,
            )
            if env:
                req.env.update(env)
            response = stub.LaunchElectron(req)
            logger.info(response.log)
            return (
                response.browserId,
                response.id,
                NewPageDetails(page_id=response.pageId, video_path=None),
            )

    @keyword(tags=("Wait", "BrowserControl"))
    def wait_for_electron_app_ready(
        self,
        state: str = "domcontentloaded",
        timeout: timedelta | None = None,
    ) -> str:
        """Waits for the Electron window to finish loading and confirms the Browser
        library is connected and ready for page-level keywords.

        Call this immediately after `New Electron Application` to ensure the DOM is
        ready before using ``Get Text``, ``Click``, ``Wait For Elements State``, etc.
        Returns the window title so you can verify the correct window is active.

        | =Argument=  | =Description= |
        | ``state``   | Page load state to wait for: ``domcontentloaded`` (default), ``load``, or ``networkidle``. |
        | ``timeout`` | Timeout for the load-state wait. Defaults to the library default timeout. |

        Example:
        | `New Electron Application`    executable_path=C:/path/to/app.exe
        | `Wait For Electron App Ready`
        | Get Text    css=h1    ==    Welcome

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        timeout_ = int(timeout.total_seconds() * 1000) if timeout else int(self.timeout)
        with self.playwright.grpc_channel() as stub:
            load_resp = stub.WaitForPageLoadState(
                Request().PageLoadState(state=state, timeout=timeout_)
            )
            logger.info(load_resp.log)
            title_resp = stub.GetTitle(Request().Empty())
        title = title_resp.body
        logger.info(f"Electron app ready — active window: '{title}'")
        return title

    @keyword(tags=("Setter", "BrowserControl"))
    def close_electron_application(self):
        """Closes the currently running Electron application and cleans up state.

        Closes the ``ElectronApplication`` handle obtained via `New Electron Application`
        and removes the associated browser/context/page from the Browser library state
        stack.  After this keyword there is no active browser; call `New Browser` or
        another state-creating keyword before issuing further page interactions.

        Example:
        | `Close Electron Application`

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseElectron(Request().Empty())
            logger.info(response.log)
