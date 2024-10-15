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
    def add_locator_handler(
        self,
        selector: str,
        click_selector: str,
        *,
        noWaitAfter: bool = True,
        times: Optional[int] = None,
        click_clickCount: int = 1,
        click_delay: int = 0,
        click_force: bool = False,
        position_x: Optional[int] = None,
        position_y: Optional[int] = None,
    ):
        """Add locator handle which will click the element indicated by locator.

        | =Arguments= | =Description= |
        | ``selector`` | Is the selector to the element which indicated that locator handler should be called. |
        | ``noWaitAfter`` | By default, after calling the handler Playwright will wait until the overlay becomes hidden, and only then library will continue with the action/assertion that triggered the handler. This option allows to opt-out of this behavior, so that overlay can stay visible after the handler has run. |
        | ``times`` | Is the number of times to how often locator handler is is called. None is unlimited. |
        | ``click_selector`` | Is the selector to the element to be clicked. |
        | ``click_clickCount`` | Is the number of times to click the element. |
        | ``click_delay`` | Time to wait between mousedown and mouseup in milliseconds. Defaults to 0. |
        | ``click_force`` | Whether to bypass checks and dispatch the event directly. Defaults to false. |
        | ``position_x`` | A point to use relative to the top-left corner of element padding box. If not specified, uses some visible point of the element. |
        | ``position_y`` | A point to use relative to the top-left corner of element padding box. If not specified, uses some visible point of the element. |

        The arguments `click_clickCount`, `click_delay`, `click_force` `position_x` and `position_y`
        are for Playwright's `click` method. The `selector`, `noWaitAfter` and `times` are for
        the locator handler.

        Example
        | `New Page`    ${URL}
        | `Add Locator Handler`    id:button     # Add locator handler to click button with id="button"
        |  Type Text`    id:username    user     # If overlay is shown with element id="button" after interactios, element is clicked
        | `Type Text`    id:password    password
        | `Click`    id:login
        | `Remove Locator Handler`    id:button    # Removes the locator handler from page
        """
        logger.info(
            f"{position_x=}, {position_y=} {type(position_x)} {type(position_y)}"
        )
        if position_x and position_y:
            click_position = Request.Position(x=str(position_x), y=str(position_y))
        elif position_x is None and position_y is None:
            click_position = Request.Position(x="None", y="None")
        else:
            raise ValueError(
                f"Both position_x and position_y must be given, now position_x is {position_x} "
                f"{type(position_x)} and position_y is {position_y} {type(position_y)}"
            )
        logger.info(click_selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.AddLocatorHandler(
                Request.LocatorHandlerAdd(
                    selector=selector,
                    noWaitAfter=noWaitAfter,
                    times=str(times) if times is not None else "",
                    clickSelector=click_selector,
                    clickClickCount=click_clickCount,
                    clickDelay=click_delay,
                    clickForce=click_force,
                    clickPosition=click_position,
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def remove_locator_hanler(self, locator: str):
        """Remove locator handle indicated by selector."""
        logger.info(f"Remove locator handle: {locator}")
