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
import re
import time
from datetime import timedelta
from typing import Any, Dict, Optional, Union

from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import ConditionInputs, ElementState, Scope, keyword, logger


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

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the corresponding object. See the `Finding elements` section for details about the selectors. |
        | ``state`` | See `ElementState` for explanation. |
        | ``timeout`` | uses default timeout from library if not set. |
        | ``message`` | overrides the default error message. The ``message`` argument accepts `{selector}`, `{function}`, and `{timeout}` [https://docs.python.org/3/library/stdtypes.html#str.format|format] options. The `{function}` formatter is same ``state`` argument value. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Wait For Elements State`    //h1    visible    timeout=2 s
        | `Wait For Elements State`    //hi    focused    1s

        [https://forum.robotframework.org/t/comments-for-wait-for-elements-state/4345|Comment >>]
        """
        # self.wait_for_condition(ConditionInputs.element_states, selector, AssertionOperator.contains, state, timeout=timeout, message=message)  #For Future Use...

        if state in [ElementState.focused, ElementState.defocused] and (
            (self.selector_prefix and ">>>" in self.selector_prefix)
            or ">>>" in selector
        ):
            escaped_selector = re.sub(r"^#", "\\#", selector)
            raise ValueError(
                f"State '{state.name}' is not supported with iframe selectors.\n"
                f"Use "
                f"'Wait For Condition    Element States    {escaped_selector}   contains    {state.name}'"
                f" instead."
            )

        timeout_as_str = self.millisecs_to_timestr(self.get_timeout(timeout))
        funct = {
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
            ElementState.stable,
            ElementState.enabled,
            ElementState.disabled,
            ElementState.editable,
        ]:
            end = float(
                self.convert_timeout(timeout, False) if timeout else self.timeout / 1000
            )
            end += time.monotonic()
            while True:
                try:
                    return self._wait_for_elements_state(
                        selector, state, timeout, self.strict_mode
                    )
                except Exception as error:
                    if end > time.monotonic():
                        logger.debug(f"Suppress error: {error}")
                    else:
                        if message:
                            selector = self.resolve_selector(selector)
                            message = message.format(
                                selector=selector,
                                function=state.name,
                                timeout=timeout_as_str,
                            )
                            raise AssertionError(message)
                        raise
        else:
            self.wait_for_function(
                funct[state],
                selector=selector,
                timeout=timeout,
                message=message,
            )

    def _wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: Optional[timedelta] = None,
        strict: bool = True,
    ):
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, object] = {"state": state.name}
            if timeout:
                options["timeout"] = self.get_timeout(timeout)
            options_json = json.dumps(options)
            response = stub.WaitForElementsState(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json, strict=strict
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
        """Polls JavaScript expression or function in browser until it returns a (JavaScript) truthy value.

        | =Arguments= | =Description= |
        | ``function`` | A valid javascript function or a javascript function body. For example ``() => true`` and ``true`` will behave similarly. |
        | ``selector`` | Selector to resolve and pass to the JavaScript function. This will be the first argument the function receives. If given a selector a function is necessary, with an argument to capture the elementhandle. For example ``(element) => document.activeElement === element`` See the `Finding elements` section for details about the selectors. |
        | ``polling`` | Default polling value of "raf" polls in a callback for ``requestAnimationFrame``. Any other value for polling will be parsed as a robot framework time for interval between polls. |
        | ``timeout`` | Uses default timeout of the library if not set. |
        | ``message`` | overrides the default error message. The ``message`` argument accepts `{selector}`, `{function}`, and `{timeout}` [https://docs.python.org/3/library/stdtypes.html#str.format|format] options. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example usage:
        | ${promise}      `Promise To`      `Wait For Function`    element => element.style.width=="100%"    selector=\\#progress_bar    timeout=4s
        | `Click`         \\#progress_bar
        | `Wait For`      ${promise}

        [https://forum.robotframework.org/t//4346|Comment >>]
        """
        timeout_as_str = self.millisecs_to_timestr(self.get_timeout(timeout))
        end = float(
            self.convert_timeout(timeout, False) if timeout else self.timeout / 1000
        )
        end += time.monotonic()
        while True:
            try:
                return self._wait_for_function(
                    function, selector, polling, timeout, self.strict_mode
                )
            except Exception as error:
                if end > time.monotonic():
                    logger.debug(f"Suppress {error}")
                else:
                    if message:
                        selector = self.resolve_selector(selector)
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
        strict: bool = True,
    ):
        selector = self.resolve_selector(selector)
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
                    strict=strict,
                )
            )
            logger.debug(response.json)
            logger.info(response.log)

    @keyword(tags=("Wait", "PageContent"))
    def wait_for_condition(
        self,
        condition: ConditionInputs,
        *args: Any,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ) -> Any:
        """Waits for a condition, defined with Browser getter keywords to become True.

        This Keyword is basically just a wrapper around our assertion keywords, but with a timeout.
        It can be used to wait for anything that also can be asserted with our keywords.

        In comparison to Robot Frameworks `Wait Until Keywords Succeeds` this keyword is more
        readable and easier to use but is limited to Browser libraries assertion keywords.

        | =Arguments= | =Description= |
        | ``condition`` | A condition, defined with Browser getter keywords, without the word ``Get``. |
        | ``*args`` | Arguments to pass to the condition keyword. |
        | ``timeout`` | Timout to wait for the condition to become True. Uses default timeout of the library if not set. |
        | ``message`` | Overrides the default error message. |


        The easiest way to use this keyword is first starting with an assertion keyword with assertion like: `Get Text`

        Start:
        | `Get Text`    id=status_bar   contains    Done

        Then you replace the word `Get` with `Wait For Condition    ` and if necessary add the timeout argument.

        End:
        | `Wait For Condition`    Text    id=status_bar   contains    Done


        Example usage:
        | `Wait For Condition`    Element States    id=cdk-overlay-0    ==    detached
        | `Wait For Condition`    Element States     //h1    contains    visible    editable    enabled    timeout=2 s
        | `Wait For Condition`    Title    should start with    Robot
        | `Wait For Condition`    Url    should end with    robotframework.org

        [https://forum.robotframework.org/t//4346|Comment >>]
        """
        if isinstance(timeout, timedelta):
            assertion_timeout = self.library.convert_timeout(timeout)
        elif timeout is None:
            assertion_timeout = self.timeout
        else:
            raise TypeError(f"Invalid timeout type: {type(timeout)}")
        scope = Scope.Test if self.library.is_test_case_running else Scope.Suite
        if message is not None:
            args = args + (f"message={message}",)
        original_assert_retry = self.retry_assertions_for_stack.set(
            assertion_timeout, scope=scope
        )
        try:
            return BuiltIn().run_keyword(condition.value, *args)
        finally:
            self.retry_assertions_for_stack.set(original_assert_retry, scope=scope)
