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
from typing import Any, Optional

from ..assertion_engine import verify_assertion, with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import AssertionOperator


class WebAppState(LibraryComponent):
    @keyword(name="localStorage get Item", tags=("PageContent", "Assertion", "Getter"))
    @with_assertion_polling
    def local_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """
        Get saved data from the local storage.

        ``key`` Named key of the item in the storage.

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
                "localStorage",
                message,
            )

    @keyword(name="localStorage set Item", tags=("Setter", "PageContent"))
    def local_storage_set_item(self, key: str, value: str):
        """
        Save data to the local storage.

        ``key`` The name of the key under which it should be saved.

        ``value`` The value which shall be saved as a string.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.localStorage.setItem("{key}", "{value}")'
                )
            )
            logger.info(response.log)

    @keyword(name="localStorage remove Item", tags=("Setter", "PageContent"))
    def local_storage_remove_item(self, key: str):
        """
        Remove saved data with key from the local storage.

        ``key`` Name of the item which shall be deleted.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.localStorage.removeItem("{key}")'
                )
            )
            logger.info(response.log)

    @keyword(name="localStorage clear", tags=("Setter", "PageContent"))
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
        name="sessionStorage get Item", tags=("PageContent", "Assertion", "Getter")
    )
    @with_assertion_polling
    def session_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Any:
        """
        Get saved data from from session storage.

        ``key`` Named key of the item in the storage.

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

    @keyword(name="sessionStorage set Item", tags=("Setter", "PageContent"))
    def session_storage_set_item(self, key: str, value: str):
        """
        Save data to session storage.

        ``key`` The name of the key under which it should be saved.

        ``value`` The value which shall be saved as a string.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.setItem("{key}", "{value}")'
                )
            )
            logger.info(response.log)

    @keyword(name="sessionStorage remove Item", tags=("Setter", "PageContent"))
    def session_storage_remove_item(self, key: str):
        """
        Remove saved data with key from the session storage.

        ``key`` Name of the item which shall be deleted.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.removeItem("{key}")'
                )
            )
            logger.info(response.log)

    @keyword(name="sessionStorage clear", tags=("Setter", "PageContent"))
    def session_storage_clear(self):
        """
        Remove all saved data from the session storage.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script="window.sessionStorage.clear()")
            )
            logger.info(response.log)
