import json
from typing import Any

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.time_conversion import timestr_to_millisecs


class Evaluation(LibraryComponent):
    @keyword(name="Execute JavaScript", tags=["Setter", "PageContent", "WebAppState"])
    def execute_javascript(self, function: str, selector: str = "") -> Any:
        """Executes given javascript on the page.

        ``function`` <str> A valid javascript function or a javascript function body. **Required** For example
        ``() => true`` and ``true`` will behave similarly.

        ``selector`` <str> Selector to resolve and pass to the JavaScript function. This will be the first
        argument the function receives. If given a selector a function is necessary, with an argument
        to capture the elementhandle. For example ``(element) => document.activeElement === element``

        [https://github.com/MarketSquare/robotframework-browser/tree/master/atest/test/06_Examples/js_evaluation.robot | Usage examples. ]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script=function, selector=selector)
            )
            logger.info(response.log)
            return json.loads(response.result)

    @keyword(tags=["PageContent"])
    def highlight_elements(
        self,
        selector: str,
        duration: str = "5s",
        width: str = "2px",
        style: str = "dotted",
        color: str = "blue",
    ):
        """Adds a red highlight to elements matched by the ``selector`` for ``duration``.

        ``selector`` <str> Selector which shall be highlighted. **Required**

        ``duration`` <str> Sets for how long the selector shall be highlighted. Defaults to ``5s`` => 5 seconds.
        """
        with self.playwright.grpc_channel() as stub:
            duration_ms = timestr_to_millisecs(duration)
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=selector,
                    duration=duration_ms,
                    width=width,
                    style=style,
                    color=color,
                )
            )
            logger.info(response.log)
