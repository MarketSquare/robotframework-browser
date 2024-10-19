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

from typing import Optional

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger


class LocatorHandler(LibraryComponent):

    @keyword(tags=("Setter", "PageContent"))
    def add_click_locator_handler(
        self,
        selector: str,
        click_selector: str,
        *,
        noWaitAfter: bool = True,
        times: Optional[int] = None,
        click_clickCount: int = 1,
        click_delay: int = 0,
        click_force: bool = False,
    ):
        """Add a handler function which will activate when `selector` is visible and click.

        The handler will click the element indicated by `click_selector`.

        When testing a web page, sometimes unexpected overlkays, exaple "Accept Coocies" dialog
        might appear and block the interaction with the page, like `Click` keyword. These
        overlays can be problematic to handle, because they might appear randomly in the page.
        This keyword allows to create automatic method, which will close those overlays by
        clicking the element indicated by ``click_selector``. Handler is activaed when
        element indicated by ``selector`` is visible. For furhter information, see Playwright's
        [https://playwright.dev/docs/api/class-page#page-add-locator-handler|addLocatorHandler]
        method.

        | =Arguments= | =Description= |
        | ``selector`` | Is the selector to the element which indicated that locator handler should be called. |
        | ``noWaitAfter`` | By default, after calling the handler Playwright will wait until the overlay becomes hidden, and only then library will continue with the action/assertion that triggered the handler. This option allows to opt-out of this behavior, so that overlay can stay visible after the handler has run. |
        | ``times`` | Is the number of times to how often locator handler is is called. None is unlimited. |
        | ``click_selector`` | Is the selector to the element to be clicked. |
        | ``click_clickCount`` | Is the number of times to click the element. |
        | ``click_delay`` | Time to wait between mousedown and mouseup in milliseconds. Defaults to 0. |
        | ``click_force`` | Whether to bypass checks and dispatch the event directly. Defaults to false. |

        The arguments `click_selector`, `click_clickCount`, `click_delay` and `click_force` are same as
        `Click` keyword. The `selector`, `noWaitAfter` and `times` are for the locator handler. The
        handler is tied to the active page, if there is need to add handler to another page, this keyword
        needs to be called separetly for each page. If the `times` argument is set to positive value,
        the locator handler is removed after the handler has been called the specified number of times.

        Example add locator handler to click button with id="ButtonInOverlay" when id=Overlay is visible:
        | `New Page`    ${URL}
        | `Add Click Locator Handler`    id=Overlay    id=ButtonInOverlay     # Add locator handler to page
        | `Type Text`    id:username    user    # If element with id=Overlay appears, the handler will click the button id=ButtonInOverlay
        | `Type Text`    id:password    password    # Or if overlay is visible here, then handler is called here
        | `Click`    id:login
        | `Remove Locator Handler`    id:button    # Removes the locator handler from page

        The keyword only clicks the, example it is possible to accept or dismiss possible cookie
        consent popups. If there is a need for more complex interactions, it is recommended to create a custom
        js extension to handle the interactions.

        Example:
        | async function customLocatorHandler(locator, clickLocator, page) {
        |     console.log("Adding custom locator handler for: " + locator);
        |     const pageLocator = page.locator(locator).first();
        |     await page.addLocatorHandler(
        |         pageLocator,
        |         async () => {
        |             console.log("Handling custom locator: " + clickLocator);
        |             await page.locator(clickLocator).click();
        |             // More complex interactions can be added here
        |         }
        |     );
        | }
        | exports.__esModule = true;
        | exports.customLocatorHandler = customLocatorHandler;
        """
        logger.info(
            f"Add locator handlee: {selector} and clicking element: {click_selector}"
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.AddLocatorHandler(
                Request.LocatorHandlerAdd(
                    selector=selector,
                    noWaitAfter=noWaitAfter,
                    times=str(times) if times is not None else "None",
                    clickSelector=click_selector,
                    clickClickCount=click_clickCount,
                    clickDelay=click_delay,
                    clickForce=click_force,
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def remove_locator_handler(self, locator: str):
        """Remove locator handle indicated by selector."""
        logger.info(f"Remove locator handle: {locator}")
        with self.playwright.grpc_channel() as stub:
            response = stub.RemoveLocatorHandler(
                Request.LocatorHandlerRemove(selector=locator)
            )
            logger.info(response.log)
