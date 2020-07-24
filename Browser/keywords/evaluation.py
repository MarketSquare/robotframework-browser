import json

from robotlibcore import keyword  # type: ignore
from typing import Any

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger


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
