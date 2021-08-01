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
import time
from datetime import timedelta
from typing import Dict, Optional, Union

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import ElementState, keyword, logger


class Waiter(LibraryComponent):
    @keyword(tags=("Wait", "PageContent"))
    def wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ):
        """Waits for the element found by ``selector`` to satisfy state option.

        Note that Browser library has `Implicit waiting` mechanisms. Depending on
        the situation you might not need to use `Wait for Elements State`.

        State options could be either appear/disappear from dom, or become visible/hidden.
        If at the moment of calling the keyword, the selector already satisfies the condition,
        the keyword will return immediately.

        If the selector doesn't satisfy the condition within the timeout the keyword will FAIL.

        ``selector`` Selector of the corresponding object.
        See the `Finding elements` section for details about the selectors.

        ``state`` See `ElementState` for explaination.

        Note that element without any content or with display:none has an empty bounding box
        and is not considered visible.

        ``timeout`` uses default timeout of 10 seconds if not set.

        ``message`` overrides the default error message. The ``message``
        argument accepts `{selector}`, `{function}`, and `{timeout}`
        [https://docs.python.org/3/library/stdtypes.html#str.format|format] options.
        The `{function}` formatter is same ``state`` argument value.
        """
        timeout_as_str = self.millisecs_to_timestr(self.get_timeout(timeout))
        funct = {
            ElementState.enabled: "e => !e.disabled",
            ElementState.disabled: "e => e.disabled",
            ElementState.editable: "e => !e.readOnly",
            ElementState.readonly: "e => e.readOnly",
            ElementState.selected: "e => e.selected",
            ElementState.deselected: "e => !e.selected",
            ElementState.focused: "e => document.activeElement === e",
            ElementState.defocused: "e => document.activeElement !== e",
            ElementState.checked: "e => e.checked",
            ElementState.unchecked: "e => !e.checked",
        }
        if state in [
            ElementState.attached,
            ElementState.detached,
            ElementState.visible,
            ElementState.hidden,
        ]:
            end = float(
                self.convert_timeout(timeout, False) if timeout else self.timeout / 1000
            )
            end += time.monotonic()
            while True:
                try:
                    return self._wait_for_elements_state(selector, state, timeout)
                except Exception as error:
                    if end > time.monotonic():
                        logger.debug(f"Suppress error: {error}")
                    else:
                        if message:
                            message = message.format(
                                selector=selector,
                                function=state,
                                timeout=timeout_as_str,
                            )
                            raise AssertionError(message)
                        raise
        else:
            self.wait_for_function(
                funct[state], selector=selector, timeout=timeout, message=message
            )

    def _wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: Optional[timedelta] = None,
    ):
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, object] = {"state": state.name}
            if timeout:
                options["timeout"] = self.get_timeout(timeout)
            options_json = json.dumps(options)
            response = stub.WaitForElementsState(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json
                )
            )
            logger.info(response.log)

    @keyword(tags=("Wait", "PageContent"))
    def wait_for_function(
        self,
        function: str,
        selector: str = "",
        polling: Union[str, timedelta] = "raf",
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ):
        """Polls JavaScript expression or function in browser until it returns a
        (JavaScript) truthy value.

        ``function`` A valid javascript function or a javascript function body. For example
        ``() => true`` and ``true`` will behave similarly.

        ``selector`` Selector to resolve and pass to the JavaScript function. This will be the first
        argument the function receives. If given a selector a function is necessary, with an argument
        to capture the elementhandle. For example ``(element) => document.activeElement === element``
        See the `Finding elements` section for details about the selectors.

        ``polling`` Default polling value of "raf" polls in a callback for ``requestAnimationFrame``.
        Any other value for polling will be parsed as a robot framework time for interval between polls.

        ``timeout`` Uses default timeout of 10 seconds if not set.

        ``message`` overrides the default error message. The ``message``
        argument accepts `{selector}`, `{function}`, and `{timeout}`
        [https://docs.python.org/3/library/stdtypes.html#str.format|format] options.

        Example usage:
        | ${promise}    Promise To      Wait For Function    element => element.style.width=="100%"    selector=\\#progress_bar    timeout=4s
        | Click         \\#progress_bar
        | Wait For      ${promise}
        """
        timeout_as_str = self.millisecs_to_timestr(self.get_timeout(timeout))
        end = float(
            self.convert_timeout(timeout, False) if timeout else self.timeout / 1000
        )
        end += time.monotonic()
        while True:
            try:
                return self._wait_for_function(function, selector, polling, timeout)
            except Exception as error:
                if end > time.monotonic():
                    logger.debug(f"Suppress {error}")
                else:
                    if message:
                        message = message.format(
                            selector=selector, function=function, timeout=timeout_as_str
                        )
                        raise AssertionError(message)
                    raise

    def _wait_for_function(
        self,
        function: str,
        selector: str = "",
        polling: Union[str, timedelta] = "raf",
        timeout: Optional[timedelta] = None,
    ):
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, int] = {}
            if polling != "raf":
                options["polling"] = self.convert_timeout(polling)  # type: ignore
            if timeout:
                options["timeout"] = self.convert_timeout(timeout)  # type: ignore
            options_json = json.dumps(options)
            response = stub.WaitForFunction(
                Request().WaitForFunctionOptions(
                    script=function,
                    selector=selector,
                    options=options_json,
                )
            )
            logger.debug(response.json)
            logger.info(response.log)
