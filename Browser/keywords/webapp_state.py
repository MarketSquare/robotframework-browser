import json
from typing import Optional, Any

from robotlibcore import keyword  # type: ignore

from ..assertion_engine import AssertionOperator, verify_assertion
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request


class WebAppState(LibraryComponent):
    @keyword
    def local_storage_get(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Any:
        """
        Get saved data from from localStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(script=f'window.localStorage.getItem("{key}")')
            )
            self.info(response.log)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "localStorage ",
            )

    @keyword
    def local_storage_set(self, key: str, value: str):
        """
        Save data to localStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(
                    script=f'window.localStorage.setItem("{key}", "{value}")'
                )
            )
            self.info(response.log)

    @keyword
    def local_storage_remove(self, key: str):
        """
        Remove saved data with key from localStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(
                    script=f'window.localStorage.removeItem("{key}")'
                )
            )
            self.info(response.log)

    @keyword
    def local_storage_clear(self):
        """
        Remove all saved data from localStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(script="window.localStorage.clear()")
            )
            self.info(response.log)

    @keyword
    def session_storage_get(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Any:
        """
        Get saved data from from sessionStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.getItem("{key}")'
                )
            )
            self.info(response.log)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "sessionStorage ",
            )

    @keyword
    def session_storage_set(self, key: str, value: str):
        """
        Save data to sessionStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.setItem("{key}", "{value}")'
                )
            )
            self.info(response.log)

    @keyword
    def session_storage_remove(self, key: str):
        """
        Remove saved data with key from sessionStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.removeItem("{key}")'
                )
            )
            self.info(response.log)

    @keyword
    def session_storage_clear(self):
        """
        Remove all saved data from sessionStorage
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(script="window.sessionStorage.clear()")
            )
            self.info(response.log)
