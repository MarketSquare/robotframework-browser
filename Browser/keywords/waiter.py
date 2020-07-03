import json
from enum import Enum, auto

from robot.api import logger  # type: ignore
from robot.utils.robottime import timestr_to_secs  # type: ignore
from robotlibcore import keyword  # type: ignore
from typing import Optional, Dict

from ..generated.playwright_pb2 import Request


class ElementState(Enum):
    attached = auto()
    detached = auto()
    visible = auto()
    hidden = auto()


class Waiter:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: Optional[str] = None,
    ):
        """ Wait for the element with the specified selector to satisfy state option.

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
                timeout_ms: int = int(timestr_to_secs(timeout) * 1000)
                options["timeout"] = timeout_ms
            options_json = json.dumps(options)
            response = stub.WaitForElemntsState(
                Request().selectorOptions(selector=selector, options=options_json)
            )
            logger.info(response.log)
