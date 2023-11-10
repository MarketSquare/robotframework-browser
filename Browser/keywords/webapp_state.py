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

from ..assertion_engine import assertion_formatter_used, with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger


class WebAppState(LibraryComponent):
    def eval_js(self, script: str, frame_selector: Optional[str] = None) -> Any:
        with self.playwright.grpc_channel() as stub:
            return stub.EvaluateJavascript(
                Request().EvaluateAll(
                    selector=frame_selector if frame_selector is not None else "",
                    script=script,
                    arg="null",
                    allElements=False,
                    strict=self.strict_mode,
                )
            )

    @keyword(name="LocalStorage Get Item", tags=("PageContent", "Assertion", "Getter"))
    @with_assertion_polling
    @assertion_formatter_used
    def local_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        frame_selector: Optional[str] = None,
    ) -> Any:
        """Get saved data from the local storage.

        | =Arguments= | =Description= |
        | ``key`` | Named key of the item in the storage. |
        | ``assertion_operator`` | Assertion operator to use. See `Assertions` for more information. |
        | ``assertion_expected`` | Expected value to compare with. |
        | ``message`` | Custom error message to use. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the LocalStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |


        See `Assertions` for further details for the assertion arguments. Defaults to None.

        Example:
        | `Local Storage Get Item`    Key    ==    Value    My error
        | ${value} =    `Local Storage Get Item`    Key

        [https://forum.robotframework.org/t//4300|Comment >>]
        """
        response = self.eval_js(f'window.localStorage.getItem("{key}")', frame_selector)
        logger.info(response.log)
        formatter = self.get_assertion_formatter("Local Storage Get Item")
        return verify_assertion(
            json.loads(response.result),
            assertion_operator,
            assertion_expected,
            "localStorage",
            message,
            formatter,
        )

    @keyword(name="LocalStorage Set Item", tags=("Setter", "PageContent"))
    def local_storage_set_item(
        self, key: str, value: str, frame_selector: Optional[str] = None
    ):
        """Save data to the local storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the key under which it should be saved. |
        | ``value`` | The value which shall be saved as a string. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the LocalStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |


        Example:
        | `Local Storage Set Item`    Key    Value

        [https://forum.robotframework.org/t//4302|Comment >>]
        """
        response = self.eval_js(
            f"window.localStorage.setItem({key!r}, {value!r})", frame_selector
        )
        logger.info(response.log)

    @keyword(name="LocalStorage Remove Item", tags=("Setter", "PageContent"))
    def local_storage_remove_item(self, key: str, frame_selector: Optional[str] = None):
        """Remove saved data with key from the local storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the item which shall be deleted. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the LocalStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `Local Storage Set Item`      Foo    bar
        | `LocalStorage Remove Item`    Foo
        | ${item} =    `Local Storage Get Item`    Foo
        | Should Be Equal    ${item}    ${None}

        [https://forum.robotframework.org/t//4301|Comment >>]
        """
        response = self.eval_js(
            f'window.localStorage.removeItem("{key}")', frame_selector
        )
        logger.info(response.log)

    @keyword(name="LocalStorage Clear", tags=("Setter", "PageContent"))
    def local_storage_clear(self, frame_selector: Optional[str] = None):
        """Remove all saved data from the local storage.

        | =Arguments= | =Description= |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the LocalStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `Local Storage Set Item`      Foo    bar
        | `LocalStorage Clear`
        | ${item} =    `Local Storage Get Item`    Foo
        | Should Be Equal    ${item}    ${None}

        [https://forum.robotframework.org/t//4299|Comment >>]
        """
        response = self.eval_js("window.localStorage.clear()", frame_selector)
        logger.info(response.log)

    @keyword(
        name="SessionStorage Get Item", tags=("PageContent", "Assertion", "Getter")
    )
    @with_assertion_polling
    @assertion_formatter_used
    def session_storage_get_item(
        self,
        key: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        frame_selector: Optional[str] = None,
    ) -> Any:
        """Get saved data from from session storage.

        | =Arguments= | =Description= |
        | ``key`` | Named key of the item in the storage. |
        | ``assertion_operator`` | Assertion operator to use. See `Assertions` for more information. |
        | ``assertion_expected`` | Expected value to compare with. |
        | ``message`` | Custom error message to use. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the SessionStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `SessionStorage Set Item`    key2    value2
        | ${item} =    `SessionStorage Get Item`    key1
        | Should Be Equal    ${item}    value2

        [https://forum.robotframework.org/t//4324|Comment >>]
        """
        response = self.eval_js(
            f"window.sessionStorage.getItem({key!r})", frame_selector
        )
        logger.info(response.log)
        formatter = self.get_assertion_formatter("Session Storage Get Item")
        return verify_assertion(
            json.loads(response.result),
            assertion_operator,
            assertion_expected,
            "sessionStorage ",
            message,
            formatter,
        )

    @keyword(name="SessionStorage Set Item", tags=("Setter", "PageContent"))
    def session_storage_set_item(
        self, key: str, value: str, frame_selector: Optional[str] = None
    ):
        """Save data to session storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the key under which it should be saved. |
        | ``value`` | The value which shall be saved as a string. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the SessionStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `SessionStorage Set Item`    key2    value2

        [https://forum.robotframework.org/t//4326|Comment >>]
        """
        response = self.eval_js(
            f"window.sessionStorage.setItem({key!r}, {value!r})", frame_selector
        )
        logger.info(response.log)

    @keyword(name="SessionStorage Remove Item", tags=("Setter", "PageContent"))
    def session_storage_remove_item(
        self, key: str, frame_selector: Optional[str] = None
    ):
        """
        Remove saved data with key from the session storage.

        | =Arguments= | =Description= |
        | ``key`` | The name of the item which shall be deleted. |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the SessionStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `SessionStorage Set Item`       mykey2    myvalue2
        | `SessionStorage Remove Item`    mykey2
        | `SessionStorage Get Item`       mykey2    ==    ${None}

        [https://forum.robotframework.org/t//4325|Comment >>]
        """
        response = self.eval_js(
            f"window.sessionStorage.removeItem({key!r})", frame_selector
        )
        logger.info(response.log)

    @keyword(name="SessionStorage Clear", tags=("Setter", "PageContent"))
    def session_storage_clear(self, frame_selector: Optional[str] = None):
        """Remove all saved data from the session storage.

        | =Arguments= | =Description= |
        | ``frame_selector`` | If this selector points to an element inside an iframe, the SessionStorage of that frame is used. Example: ``iframe[name="test"] >>> body`` |

        Example:
        | `SessionStorage Set Item`    mykey3    myvalue3
        |  `SessionStorage Clear`
        | `SessionStorage Get Item`    mykey3    ==    ${None}

        [https://forum.robotframework.org/t//4323|Comment >>]
        """
        response = self.eval_js("window.sessionStorage.clear()", frame_selector)
        logger.info(response.log)
