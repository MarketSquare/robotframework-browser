import json
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum, auto

from robot.running import EXECUTION_CONTEXTS  # type: ignore
from robotlibcore import keyword  # type: ignore
from typing import Dict

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils.time_conversion import timestr_to_millisecs


class ElementState(Enum):
    attached = auto()
    detached = auto()
    visible = auto()
    hidden = auto()


class Waiter(LibraryComponent):
    def __init__(self, library):
        LibraryComponent.__init__(self, library)
        self._executor = ThreadPoolExecutor(max_workers=256)

    @keyword(tags=["Wait", "PageContent"])
    def wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: str = "",
    ):
        """Waits for the element found by ``selector`` to satisfy state option.

        State options could be either appear/disappear from dom, or become visible/hidden.
        If at the moment of calling the keyword, the selector already satisfies the condition,
        the keyword will return immediately.

        If the selector doesn't satisfy the condition within the timeout the keyword will FAIL.

        ``state``
        - ``attached``: to be present in DOM.
        - ``detached``: to not be present in DOM.
        - ``visible``: to have non-empty bounding box and no visibility:hidden.
        - ``hidden``: to be detached from DOM, or have an empty bounding box or visibility:hidden.

        Note that element without any content or with display:none has an empty bounding box
        and is not considered visible.

        ``timeout``: (optional) uses default timeout if not set.
        """
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, object] = {"state": state.name}
            if timeout:
                timeout_ms = timestr_to_millisecs(timeout)
                options["timeout"] = timeout_ms
            options_json = json.dumps(options)
            response = stub.WaitForElementsState(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json
                )
            )
            self.info(response.log)

    @keyword(tags=["Wait", "PageContent"])
    def wait_for_function(
        self, function: str, args: str = "", polling: str = "raf", timeout: str = "",
    ):
        """Executes JavaScript function in browser and waits for function to return
        (JavaScript) truthy value. Returns the value if the wait completes.

        ``args`` Are values to pass to the JavaScript function.

        Default polling value of "raf" polls in a callback for ``requestAnimationFrame``.
        Any other value for polling will be parsed as a robot framework time for interval between polls.

        ``timeout``: (optional) uses default timeout if not set.
        """
        with self.playwright.grpc_channel() as stub:
            if polling != "raf":
                polling_interval = timestr_to_millisecs(polling)
            response = stub.WaitForFunction(
                Request().WaitForFunctionOptions(
                    function=function,
                    args=args,
                    polling=polling_interval,
                    timeout=timeout,
                )
            )
            self.info(response.log)
            return response

    @keyword(tags=["Wait"])
    def promise_to(self, keyword: str, *args):
        """
        *EXPERIMENTAL* *WORK IN PROGRESS*
        Wrap a Browser library keyword and make it a promise.
        Returns that promise and executes the keyword on background.
        """
        browser_lib = EXECUTION_CONTEXTS.current.namespace._kw_store.get_library(
            self.library
        )
        handler = browser_lib.handlers[keyword]
        positional, named = handler.resolve_arguments(
            args, EXECUTION_CONTEXTS.current.variables
        )
        return self._executor.submit(handler.current_handler(), *positional, *named)

    @keyword(tags=["Wait"])
    def wait_for(self, *promises: Future):
        """
        *EXPERIMENTAL* *WORK IN PROGRESS*
        Waits for promises to finish and returns results from them.
        Returns one result if one promise waited. Otherwise returns an array of results.
        If one fails, then this keyword will fail.
        """
        if len(promises) == 1:
            return promises[0].result()
        return [promise.result() for promise in promises]
