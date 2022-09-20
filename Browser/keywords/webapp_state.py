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

from assertionengine import AssertionOperator, verify_assertion

from ..assertion_engine import with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger


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
        """Get saved data from the local storage.

        | =Arguments= | =Description= |
        | ``key`` | Named key of the item in the storage. |
        | ``assertion_operator`` | Assertion operator to use. See `Assertions` for more information. |
        | ``assertion_expected`` | Expected value to compare with. |
        | ``message`` | Custom error message to use. |

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        Example:
        | `Local Storage Get Item`    Key    ==    Value    My error
        | ${value} =    `Local Storage Get Item`    Key

        [https://forum.robotframework.org/t//4300|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script=f'window.localStorage.getItem("{key}")')
            )
            logger.info(response.log)
            formatter = self.keyword_formatters.get(self.local_storage_get_item)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "localStorage",
                message,
                formatter,
            )

    @keyword(name="localStorage set Item", tags=("Setter", "PageContent"))
    def local_storage_set_item(self, key: str, value: str):
        """Save data to the local storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the key under which it should be saved. |
        | ``value`` | The value which shall be saved as a string. |

        Example:
        | `Local Storage Set Item`    Key    Value

        [https://forum.robotframework.org/t//4302|Comment >>]
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
        """Remove saved data with key from the local storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the item which shall be deleted. |

        Example:
        | `Local Storage Set Item`      Foo    bar
        | `LocalStorage Remove Item`    Foo
        | ${item} =    `Local Storage Get Item`    Foo
        | Should Be Equal    ${item}    ${None}

        [https://forum.robotframework.org/t//4301|Comment >>]
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
        """Remove all saved data from the local storage.

        Example:
        | `Local Storage Set Item`      Foo    bar
        | `LocalStorage Clear`
        | ${item} =    `Local Storage Get Item`    Foo
        | Should Be Equal    ${item}    ${None}

        [https://forum.robotframework.org/t//4299|Comment >>]
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
        """Get saved data from from session storage.

        | =Arguments= | =Description= |
        | ``key`` | Named key of the item in the storage. |
        | ``assertion_operator`` | Assertion operator to use. See `Assertions` for more information. |
        | ``assertion_expected`` | Expected value to compare with. |

        Example:
        | `SessionStorage Set Item`    key2    value2
        | ${item} =    `SessionStorage Get Item`    key1
        | Should Be Equal    ${item}    value2

        [https://forum.robotframework.org/t//4324|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=f'window.sessionStorage.getItem("{key}")'
                )
            )
            logger.info(response.log)
            formatter = self.keyword_formatters.get(self.session_storage_get_item)
            return verify_assertion(
                json.loads(response.result),
                assertion_operator,
                assertion_expected,
                "sessionStorage ",
                formatter,
            )

    @keyword(name="sessionStorage set Item", tags=("Setter", "PageContent"))
    def session_storage_set_item(self, key: str, value: str):
        """Save data to session storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the key under which it should be saved. |
        | ``value`` | The value which shall be saved as a string. |

        Example:
        | `SessionStorage Set Item`    key2    value2

        [https://forum.robotframework.org/t//4326|Comment >>]
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

        | =Arguments= | =Description= |
        | ``key`` | The name of the item which shall be deleted. |

        Example:
        | `SessionStorage Set Item`       mykey2    myvalue2
        | `SessionStorage Remove Item`    mykey2
        | `SessionStorage Get Item`       mykey2    ==    ${None}

        [https://forum.robotframework.org/t//4325|Comment >>]
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
        """Remove all saved data from the session storage.

        Example:
        | `SessionStorage Set Item`    mykey3    myvalue3
        |  `SessionStorage Clear`
        | `SessionStorage Get Item`    mykey3    ==    ${None}

        [https://forum.robotframework.org/t//4323|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script="window.sessionStorage.clear()")
            )
            logger.info(response.log)
