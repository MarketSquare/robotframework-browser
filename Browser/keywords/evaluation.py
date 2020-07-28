import json

from robotlibcore import keyword  # type: ignore
from typing import Any

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.time_conversion import timestr_to_millisecs


class Evaluation(LibraryComponent):
    @keyword(
        name="Execute JavaScript On Page", tags=["Setter", "PageContent", "WebAppState"]
    )
    def execute_javascript_on_page(self, script: str) -> Any:
        """Executes given javascript on the page.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(script=script)
            )
            logger.info(response.log)
            return json.loads(response.result)

    @keyword(tags=["PageContent"])
    def highlight_elements(self, selector: str, duration: str = "5s"):
        """Adds a red highlight to elements matched by ``selector`` for ``duration``"""
        with self.playwright.grpc_channel() as stub:
            duration_ms = timestr_to_millisecs(duration)
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=selector, duration=duration_ms
                )
            )
            logger.info(response.log)
