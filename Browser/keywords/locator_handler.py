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
        self, selector: str, noWaitAfter: bool = True, times: Optional[int] = None
    ):
        """Add locator handle which will click the element indicated by locator.

        | =Arguments= | =Description= |
        | ``selector`` | Is the locator to the element to be clicked. |
        | ``noWaitAfter`` | By default, after calling the handler Playwright will wait until the overlay becomes hidden, and only then Playwright will continue with the action/assertion that triggered the handler. This option allows to opt-out of this behavior, so that overlay can stay visible after the handler has run. |
        | ``times`` | Is the number of times to click the element. None is unlimited. |

        Example
        | `New Page`    ${URL}
        | `Add Locator Handler`    id:button     # Add locator handler to click button with id="button"
        |  Type Text`    id:username    user     # If overlay is shown with element id="button" after interactios, element is clicked
        | `Type Text`    id:password    password
        | `Click`    id:login
        | `Remove Locator Handler`    id:button    # Removes the locator handler from page
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddLocatorHandler(
                Request.LocatorHandlerAdd(
                    selector=selector,
                    noWaitAfter=noWaitAfter,
                    times=str(times) if times is not None else "",
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def remove_locator_hanler(self, locator: str):
        """Remove locator handle indicated by selector."""
        logger.info(f"Remove locator handle: {locator}")
