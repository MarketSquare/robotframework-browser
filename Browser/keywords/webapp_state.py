import json
from typing import Any, Optional

from robotlibcore import keyword  # type: ignore

from ..assertion_engine import verify_assertion, with_assertions
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import AssertionOperator


class WebAppState(LibraryComponent):
    @keyword(name="localStorage get Item", tags=["WebAppState", "Assertion", "Getter"])
    @with_assertions
    def local_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Any:
        """
        Get saved data from the local storage.

        ``key`` <str> Named key of the item in the storage. **Required**

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script=f'window.localStorage.getItem("{key}")')
            )
            logger.info(response.log)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "localStorage ",
            )

    @keyword(name="localStorage set Item", tags=["WebAppState"])
    def local_storage_set_item(self, key: str, value: str):
        """
        Save data to the local storage.

        ``key`` <str> The name of the key under which it should be saved. **Required**

        ``value`` <str> The value which shall be saved as a string. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.localStorage.setItem("{key}", "{value}")'
                )
            )
            logger.info(response.log)

    @keyword(name="localStorage remove Item", tags=["WebAppState"])
    def local_storage_remove_item(self, key: str):
        """
        Remove saved data with key from the local storage.

        ``key`` <str> Name of the item which shall be deleted. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.localStorage.removeItem("{key}")'
                )
            )
            logger.info(response.log)

    @keyword(name="localStorage clear", tags=["WebAppState"])
    def local_storage_clear(self):
        """
        Remove all saved data from the local storage.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script="window.localStorage.clear()")
            )
            logger.info(response.log)

    @keyword(
        name="sessionStorage get Item", tags=["WebAppState", "Assertion", "Getter"]
    )
    @with_assertions
    def session_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Any:
        """
        Get saved data from from session storage.

        ``key`` <str> Named key of the item in the storage. **Required**

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.getItem("{key}")'
                )
            )
            logger.info(response.log)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "sessionStorage ",
            )

    @keyword(name="sessionStorage set Item", tags=["WebAppState"])
    def session_storage_set_item(self, key: str, value: str):
        """
        Save data to session storage.

        ``key`` <str> The name of the key under which it should be saved. **Required**

        ``value`` <str> The value which shall be saved as a string. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.setItem("{key}", "{value}")'
                )
            )
            logger.info(response.log)

    @keyword(name="sessionStorage remove Item", tags=["WebAppState"])
    def session_storage_remove_item(self, key: str):
        """
        Remove saved data with key from the session storage.

        ``key`` <str> Name of the item which shall be deleted. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.removeItem("{key}")'
                )
            )
            logger.info(response.log)

    @keyword(name="sessionStorage clear", tags=["WebAppState"])
    def session_storage_clear(self):
        """
        Remove all saved data from the session storage.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script="window.sessionStorage.clear()")
            )
            logger.info(response.log)
