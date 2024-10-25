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
from typing import Optional

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger


class LocatorHandler(LibraryComponent):

    @keyword(tags=("Setter", "PageContent"))
    def add_locator_handler_click(
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
        | `Add Locator Handler Click`    id=Overlay    id=ButtonInOverlay     # Add locator handler to page
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
            response = stub.AddLocatorHandlerClick(
                Request.LocatorHandlerAddClick(
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
        """Remove locator handler indicated by selector."""
        logger.info(f"Remove locator handle: {locator}")
        with self.playwright.grpc_channel() as stub:
            response = stub.RemoveLocatorHandler(
                Request.LocatorHandlerRemove(selector=locator)
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def add_locator_handler_custom(
        self,
        selector: str,
        handler_spec: list[dict],
        noWaitAfter: bool = True,
        times: Optional[int] = None,
    ):
        """Add a handler function which will activate when `selector` is visible and performs halder specification.

        When element indicated by `selector` is visible, the handler will perform the actions specified
        in the `handler_spec`. The `handler_spec` is a list of dictionaries, where each dictionary contains
        defines one action. The dictionary must contain the key `action` which defines the action to be
        performed. The action can be one of the following:
        [https://playwright.dev/docs/api/class-locator#locator-click|click],
        [https://playwright.dev/docs/api/class-locator#locator-fill|fill],
        [https://playwright.dev/docs/api/class-locator#locator-check|check] and
        [https://playwright.dev/docs/api/class-locator#locator-uncheck|uncheck]. Dictionary must also contain
        key `selector` which defines the element to be interacted with. The `fill` action must also contain
        the key `value` which defines the value to be filled in the element. Additional keys
        are passed to the action as keyword arguments. Example for the
        [https://playwright.dev/docs/api/class-locator#locator-click|click] action refer to the Playwright's
        documentation which options are posisble.
        """
        logger.info(f"Add locator handler: {selector}")
        handler = Request.LocatorHandlerAddCustom()
        handler.selector = selector
        handler.noWaitAfter = noWaitAfter
        handler.times = str(times) if times is not None else "None"
        for spec in handler_spec:
            if "action" not in spec:
                raise ValueError(
                    f"Action must be defined in the handler specification: {spec}"
                )
            if "selector" not in spec:
                raise ValueError(
                    f"Selector must be defined in the handler specification: {spec}"
                )
            action = spec["action"].lower()
            if action not in ["click", "fill", "check", "uncheck"]:
                raise ValueError(
                    f"Action was {spec['action']}, it must be one of the following: click, fill, check, uncheck"
                )
            if action == "fill" and "value" not in spec:
                raise ValueError("Value must be defined for fill action")
            if action != "fill" and "value" in spec:
                raise ValueError("Value must not be defined for action other than fill")
            handler_action = Request.LocatorHandlerAddCustomAction()
            handler_action.action = action
            if action == "fill":
                handler_action.value = spec["value"]
                spec.pop("value", None)
            else:
                handler_action.value = ""
            spec.pop("action", None)
            handler_action.selector = spec["selector"]
            spec.pop("selector", None)
            handler_action.optionsAsJson = json.dumps(spec)
            handler.handlerSpecs.append(handler_action)
        with self.playwright.grpc_channel() as stub:
            response = stub.AddLocatorHandlerCustom(handler)
            logger.info(response.log)
