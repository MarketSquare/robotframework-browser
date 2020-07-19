import json
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum, auto

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

        ``timeout``: (optional) uses default timout if not set.
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

    @keyword(tags=["Wait"])
    def promise_to(
        self, keyword: str, selector: str, state: ElementState, timeout: str
    ):
        return self._executor.submit(
            self.wait_for_elements_state, selector, state, timeout
        )

    @keyword(tags=["Wait"])
    def wait_for(self, *promises: Future):
        return [promise.result() for promise in promises]
