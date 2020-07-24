import json
from typing import Dict

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import ElementState
from ..utils.time_conversion import timestr_to_millisecs


class Waiter(LibraryComponent):
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
            logger.info(response.log)

    @keyword(tags=["Wait", "PageContent"])
    def wait_for_function(
        self, function: str, args: str = "", polling: str = "raf", timeout: str = "",
    ):
        """Polls JavaScript expression or function in browser until it returns a
        (JavaScript) truthy value.

        ``function`` a valid javascript function or a javascript function body. For example
        ``() => true`` and ``true`` will behave similarly.

        ``args`` Are values to pass to the JavaScript function.

        Default polling value of "raf" polls in a callback for ``requestAnimationFrame``.
        Any other value for polling will be parsed as a robot framework time for interval between polls.

        ``timeout``: (optional) uses default timeout if not set.
        """
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, int] = {}
            if polling != "raf":
                options["polling"] = timestr_to_millisecs(polling)
            if timeout:
                options["timeout"] = timestr_to_millisecs(timeout)
            options_json = json.dumps(options)
            response = stub.WaitForFunction(
                Request().WaitForFunctionOptions(
                    script=function, args=args, options=options_json,
                )
            )
            logger.info(response.log)
