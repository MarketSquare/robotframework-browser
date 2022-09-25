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
import re
from typing import Any, List, Optional, Union

import grpc  # type: ignore
from assertionengine import (
    AssertionOperator,
    bool_verify_assertion,
    dict_verify_assertion,
    flag_verify_assertion,
    float_str_verify_assertion,
    int_dict_verify_assertion,
    list_verify_assertion,
    verify_assertion,
)
from robot.utils import DotDict  # type: ignore

from ..assertion_engine import with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import (
    AreaFields,
    BoundingBoxFields,
    ElementState,
    SelectAttribute,
    SizeFields,
)


class Getters(LibraryComponent):
    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_url(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the current URL.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Optionally asserts that it matches the specified assertion. See `Assertions` for further details
        for the assertion arguments. By default assertion is not done.

        [https://forum.robotframework.org/t//4287|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            logger.debug(response.log)
            value = response.body
            formatter = self.keyword_formatters.get(self.get_url)
            return verify_assertion(
                value, assertion_operator, assertion_expected, "URL", message, formatter
            )

    # @keyword(tags=("Getter", "Assertion", "BrowserControl"))
    # Not published as keyword due to missing of good docs.
    @with_assertion_polling
    def get_page_state(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns page model state object as a dictionary.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        This must be given on the page to ``window.__SET_RFBROWSER_STATE__``

        For example:

        ``let mystate = {'login': true, 'name': 'George', 'age': 123};``

        ``window.__SET_RFBROWSER_STATE__ && window.__SET_RFBROWSER_STATE__(mystate);``
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageState(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.result)
            formatter = self.keyword_formatters.get(self.get_page_state)
            return verify_assertion(
                value,
                assertion_operator,
                assertion_expected,
                "State",
                message,
                formatter,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_page_source(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets pages HTML source as a string.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Optionally does a string assertion. See `Assertions` for further details for
        the assertion arguments. By default assertion is not done.

        [https://forum.robotframework.org/t//4275|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageSource(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.body)
            formatter = self.keyword_formatters.get(self.get_page_source)
            return verify_assertion(
                value,
                assertion_operator,
                assertion_expected,
                "HTML:",
                message,
                formatter,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_title(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the title of the current page.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Optionally asserts that title matches the specified assertion. See `Assertions`
        for further details for the assertion arguments. By default assertion is not done.

        [https://forum.robotframework.org/t//4286|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(Request().Empty())
            logger.debug(response.log)
            value = response.body
            formatter = self.keyword_formatters.get(self.get_title)
            return verify_assertion(
                value,
                assertion_operator,
                assertion_expected,
                "Title",
                message,
                formatter,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_text(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns text attribute of the element found by ``selector``.

               Keyword can also return `input` or `textarea` value property text.
        See the `Finding elements` section for details about the selectors.

               | =Arguments= | =Description= |
               | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
               | ``assertion_expected`` | Expected value for the state |
               | ``message`` | overrides the default error message for assertion. |

               Keyword uses strict mode, see `Finding elements` for more details about strict mode.

               Optionally asserts that the text matches the specified assertion. See `Assertions`
               for further details for the assertion arguments. By default, assertion is not done.

               Example:
               | ${text} =    `Get Text`    id=important                            # Returns element text without assertion.
               | ${text} =    `Get Text`    id=important    ==    Important text    # Returns element text with assertion.
               | ${text} =    `Get Text`    //input         ==    root              # Returns input element text with assertion.

               [https://forum.robotframework.org/t/comments-for-get-text/4285|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        response = self._get_text(selector)
        logger.debug(response.log)
        formatter = self.keyword_formatters.get(self.get_text)
        return verify_assertion(
            response.body,
            assertion_operator,
            assertion_expected,
            "Text",
            message,
            formatter,
        )

    def _get_text(self, selector: str):  # To ease unit testing
        with self.playwright.grpc_channel() as stub:
            return stub.GetText(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_property(
        self,
        selector: str,
        property: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the ``property`` of the element found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``property`` | Requested property name. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the property value matches the expected value. See `Assertions`
        for further details for the assertion arguments. By default assertion is not done.

        If ``assertion_operator`` is set and property is not found, ``value`` is ``None``
        and Keyword does not fail. See `Get Attribute` for examples.

        Example:
        | `Get Property`    h1    innerText    ==    Login Page
        | ${property} =    `Get Property`    h1    innerText

        [https://forum.robotframework.org/t//4276|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(
                    selector=selector, property=property, strict=self.strict_mode
                )
            )
        logger.debug(response.log)
        if response.body:
            value = json.loads(response.body)
        elif assertion_operator is not None:
            value = None
        else:
            raise AttributeError(f"Property '{property}' not found!")
        formatter = self.keyword_formatters.get(self.get_property)
        return verify_assertion(
            value,
            assertion_operator,
            assertion_expected,
            f"Property {property}",
            message,
            formatter,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the HTML ``attribute`` of the element found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``attribute`` | Requested attribute name. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the attribute value matches the expected value. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        When a attribute is selected that is not present and no assertion operator is set,
        the keyword fails. If an assertion operator is set and the attribute is not present,
        the returned value is ``None``. This can be used to assert check the presents or
        the absents of an attribute.

        Example Element:
        | <button class="login button active" id="enabled_button" something>Login</button>

        Example Code:
        | `Get Attribute`   id=enabled_button    disabled                   # FAIL => "Attribute 'disabled' not found!"
        | `Get Attribute`   id=enabled_button    disabled     ==    ${None}     # PASS => returns: None
        | `Get Attribute`   id=enabled_button    something    evaluate    value is not None    # PASS =>  returns: True
        | `Get Attribute`   id=enabled_button    disabled     evaluate    value is None        # PASS =>  returns: True

        [https://forum.robotframework.org/t//4256|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementAttribute(
                Request().ElementProperty(
                    selector=selector, property=attribute, strict=self.strict_mode
                )
            )
        logger.debug(response.log)
        value = json.loads(response.body)
        if assertion_operator is None and value is None:
            raise AttributeError(f"Attribute '{attribute}' not found!")
        logger.debug(f"Attribute is: {value}")
        formatter = self.keyword_formatters.get(self.get_attribute)
        return verify_assertion(
            value,
            assertion_operator,
            assertion_expected,
            f"Attribute {selector}",
            message,
            formatter,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_attribute_names(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
        message: Optional[str] = None,
    ) -> Any:
        """Returns all HTML attribute names of an element as a list.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``*assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that attribute names do match to the expected value. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains`` / ``*=`` only accepts one single expected value

        Other operators are not allowed.

        Example:
        | `Get Attribute Names`    [name="readonly_input"]    ==    type    name    value    readonly    # Has exactly these attribute names.
        | `Get Attribute Names`    [name="readonly_input"]    contains    disabled    # Contains at least this attribute name.

        [https://forum.robotframework.org/t//4257|Comment >>]
        """
        attribute_names = self.library.execute_javascript(
            "(element) => element.getAttributeNames()", selector
        )
        expected = list(assertion_expected)
        if self.keyword_formatters.get(self.get_attribute_names):
            logger.warn("Formatter is not supported by Get Attribute Names keyword.")
        return list_verify_assertion(
            attribute_names, assertion_operator, expected, "Attribute names", message
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_classes(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
        message: Optional[str] = None,
    ) -> Any:
        """Returns all classes of an element as a list.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``*assertion_expected`` | Expected values for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the value matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains`` / ``*=`` only accepts one single expected value

        Other operators are not allowed.

        Example:
        | `Get Classes`    id=draggable    ==    react-draggable    box    # Element contains exactly this class name.
        | `Get Classes`    id=draggable    validate    "react-draggable-dragged" not in value    # Element does not contain react-draggable-dragged class.

        [https://forum.robotframework.org/t//4262|Comment >>]
        """
        class_dict = self.get_property(selector, "classList")
        expected = list(assertion_expected)
        if self.keyword_formatters.get(self.get_classes):
            logger.warn("Formatter is not supported by Get Classes keyword.")
        return list_verify_assertion(
            list(class_dict.values()),
            assertion_operator,
            expected,
            f"Classes of {self.resolve_selector(selector)}",
            message,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_select_options(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns attributes of options of a ``select`` element as a list of dictionaries.

        Returned dictionaries have the following keys and their values
        "index", "value", "label" and "selected".


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that these match the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:

        | `Get Select Options`     //select[2]    validate  [v["label"] for v in value] == ["Email", "Mobile"]
        | `Get Select Options`   select#names     validate  any(v["label"] == "Mikko" for v in value)

        [https://forum.robotframework.org/t//4279|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
        logger.info(response)
        result = [
            {
                "index": sel.index,
                "value": sel.value,
                "label": sel.label,
                "selected": sel.selected,
            }
            for sel in response.entry
        ]
        formatter = self.keyword_formatters.get(self.get_select_options)
        return verify_assertion(
            result,
            assertion_operator,
            assertion_expected,
            "Select Options:",
            message,
            formatter,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_selected_options(
        self,
        selector: str,
        option_attribute: SelectAttribute = SelectAttribute.label,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the specified attribute of selected options of the ``select`` element.

        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the info is to be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``option_attribute`` | Which attribute shall be returned/verified. Defaults to label. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``*assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that these match the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        - ``==`` and ``!=`` can work with multiple values
        - ``contains`` / ``*=`` only accepts one single expected value

        Other operators are not allowed.

        Example:

        | `Select Options By`      label                    //select[2]    Email      Mobile
        | ${selected_list}         `Get Selected Options`   //select[2]                                         # getter
        | `Get Selected Options`   //select[2]              label          `==`       Mobile             Mail   #assertion content
        | `Select Options By`      label                    select#names   2          4
        | `Get Selected Options`   select#names             index          `==`       2                  4      #assertion index
        | `Get Selected Options`   select#names             label          *=         Mikko                     #assertion contain
        | `Get Selected Options`   select#names             label          validate   len(value) == 3           #assertion length

        [https://forum.robotframework.org/t//4280|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
        logger.info(response)
        expected = list(assertion_expected)
        selected: Union[List[int], List[str]]

        if option_attribute is SelectAttribute.index:
            expected = [int(exp) for exp in expected]
        selected = [
            getattr(sel, option_attribute.name)
            for sel in response.entry
            if sel.selected
        ]
        if self.keyword_formatters.get(self.get_selected_options):
            logger.warn("Formatter is not supported by Get Selected Options keyword.")
        return list_verify_assertion(
            selected, assertion_operator, expected, "Selected Options:", message
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_checkbox_state(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Union[bool, str] = "Unchecked",
        message: Optional[str] = None,
    ) -> bool:
        """Returns the state of the checkbox found by ``selector``.


        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        | =Arguments= | =Description= |
        | ``selector`` | Selector which shall be examined. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | ``==`` and ``!=`` and equivalent are allowed on boolean values. Other operators are not accepted. |
        | ``assertion_expected`` | Boolean value of expected state. Strings are interpreted as booleans. All strings are ``${True}`` except of the following `FALSE, NO, OFF, 0, UNCHECKED, NONE, ${EMPTY}`` (case-insensitive). Defaults to unchecked. |
        | ``message`` | overrides the default error message for assertion. |

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Get Checkbox State`    [name=can_send_email]    ==    checked

        [https://forum.robotframework.org/t//4261|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().ElementProperty(
                    selector=selector, property="checked", strict=self.strict_mode
                )
            )
        logger.info(response.log)
        value: bool = response.body
        logger.info(f"Checkbox is {'checked' if value else 'unchecked'}")
        if self.keyword_formatters.get(self.get_checkbox_state):
            logger.warn("Formatter is not supported by Get Checkbox State keyword.")
        return bool_verify_assertion(
            value,
            assertion_operator,
            assertion_expected,
            f"Checkbox {selector} is",
            message,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_element_count(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Union[int, str] = 0,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the count of elements found with ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector which shall be counted. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | `Get Element Count`    label    >    1

        [https://forum.robotframework.org/t//4270|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementCount(
                Request().ElementSelector(selector=selector, strict=False)
            )
            count = response.body
            if self.keyword_formatters.get(self.get_element_count):
                logger.warn("Formatter is not supported by Get Element Count keyword.")
            return float_str_verify_assertion(
                int(count),
                assertion_operator,
                assertion_expected,
                f"Element count for selector `{selector}` is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "BrowserControl"))
    @with_assertion_polling
    def get_viewport_size(
        self,
        key: SizeFields = SizeFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the current viewport dimensions.

        | =Arguments= | =Description= |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the viewport size as dictionary, otherwise it will just return the single value selected by the key. Note: If a single value is retrieved, an assertion does *not* need a ``validate`` combined with a cast of ``value``. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | `Get Viewport Size`    ALL    ==    {'width':1280, 'height':720}
        | `Get Viewport Size`    width    >=    1200

        [https://forum.robotframework.org/t//4288|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetViewportSize(Request().Empty())
            logger.info(response.log)
            response_json = json.loads(response.json)
            if response_json is None:
                return
            parsed = DotDict(response_json)
            logger.debug(parsed)
            if self.keyword_formatters.get(self.get_viewport_size):
                logger.warn("Formatter is not supported by Get Viewport Size keyword.")
            if key == SizeFields.ALL:
                return int_dict_verify_assertion(
                    parsed,
                    assertion_operator,
                    assertion_expected,
                    "Viewport size is",
                    message,
                )
            else:
                logger.info(f"Value of '{key}'': {parsed[key.name]}")
                return float_str_verify_assertion(
                    parsed[key.name],
                    assertion_operator,
                    assertion_expected,
                    f"{key} is",
                    message,
                )

    @keyword(tags=("Getter", "PageContent"))
    def get_table_cell_element(self, table: str, column: str, row: str) -> str:
        """Returns the Web Element that has the same column index and same row index as the selected elements.

        | =Arguments= | =Description= |
        | ``table`` | selector must select the ``<table>`` element that contains both selected elements |
        | ``column`` | selector can select any ``<th>`` or ``<td>`` element or one of their descendants. |
        | ``row`` | selector can select any ``<tr>`` element or one of their descendant like ``<td>`` elements. |

        ``column`` and ``row`` can also consume index numbers instead of selectors.
        Indexes are starting from ``0`` and ``-1`` is specific for the last element.

        Selectors for ``column`` and ``row`` are directly appended to ``table`` selector like this: ``f"{table} >> {row}" .``

        | = GitHub = |   = Slack =      | = Real Name =   |
        | mkorpela   | @mkorpela        | Mikko Korpela   |
        | aaltat     | @aaltat          | Tatu Aalto      |
        | xylix      | @Kerkko Pelttari | Kerkko Pelttari |
        | Snooz82    | @René            | René Rohner     |


        Example:
        | ${table}=    Set Variable    [id="Get Table Cell Element"] >> div.kw-docs table >> nth=1
        | ${e}=    `Get Table Cell Element`    ${table}    "Real Name"    "aaltat"   # Returns element with text ``Tatu Aalto``
        | Get Text    ${e}    ==    Tatu Aalto
        | ${e}=    `Get Table Cell Element`    ${table}    "Slack"    "Mikko Korpela"   # Returns element with text ``@mkorpela``
        | Get Text    ${e}    ==    @mkorpela
        | ${e}=    `Get Table Cell Element`    ${table}    "mkorpela"    "Kerkko Pelttari"   # column does not need to be in row 0
        | Get Text    ${e}    ==    @mkorpela
        | ${e}=    `Get Table Cell Element`    ${table}    2    -1   # Index is also directly possible
        | Get Text    ${e}    ==    René Rohner

        [https://forum.robotframework.org/t//4282|Comment >>]
        """
        node_name = str(self.library.execute_javascript("e => e.nodeName", table))
        if node_name != "TABLE":
            raise ValueError(
                f"Selector {self.resolve_selector(table)} must select a "
                f"<table> element but selects <{node_name.lower()}>."
            )
        column_idx = (
            column
            if re.fullmatch(r"-?\d+", column)
            else self.get_table_cell_index(f"{table} >> {column}")
        )
        row_idx = (
            row
            if re.fullmatch(r"-?\d+", row)
            else self.get_table_row_index(f"{table} >> {row}")
        )
        return self.get_element(
            f"{table} >> tr >> nth={row_idx} >> > * >> nth={column_idx}"
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_table_cell_index(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Union[int, str] = 0,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the index (0 based) of a table cell within its row.

        | =Arguments= | =Description= |
        | ``selector`` | can select any ``<th>`` or ``<td>`` element or one of their descendants. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Example:
        | ${table}=    Set Variable    id=`Get Table Cell Element` >> div.kw-docs table   #Table of keyword `Get Table Cell Element`
        | ${idx}=    `Get Table Cell Index`    ${table} >> "Real Name"
        | Should Be Equal    ${idx}    ${2}
        | `Get Table Cell Index`    ${table} >> "@aaltat"    ==    1

        Optionally asserts that the index matches the specified assertion. See
        `Assertions` for further details for the assertion arguments.
        By default assertion is not done.

        [https://forum.robotframework.org/t//4283|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTableCellIndex(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
            count = response.body
            if self.keyword_formatters.get(self.get_table_cell_index):
                logger.warn(
                    "Formatter is not supported by Get Table Cell Index keyword."
                )
            return float_str_verify_assertion(
                int(count),
                assertion_operator,
                assertion_expected,
                f"Element cell index for selector `{selector}` is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_table_row_index(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Union[int, str] = 0,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the index (0 based) of a table row.


        | =Arguments= | =Description= |
        | ``selector`` | can select any ``<th>`` or ``<td>`` element or one of their descendants. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Example:
        | ${table}=    Set Variable    id=`Get Table Cell Element` >> div.kw-docs table   #Table of keyword `Get Table Cell Element`
        | ${idx}=    `Get Table Row Index`    ${table} >> "@René"
        | Should Be Equal    ${idx}    ${4}
        | `Get Table Row Index`    ${table} >> "@aaltat"    ==    2

        Optionally asserts that the index matches the specified assertion. See
        `Assertions` for further details for the assertion arguments.
        By default assertion is not done.

        [https://forum.robotframework.org/t//4284|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTableRowIndex(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
            count = response.body
            if self.keyword_formatters.get(self.get_table_row_index):
                logger.warn(
                    "Formatter is not supported by Get Table Row Index keyword."
                )
            return float_str_verify_assertion(
                int(count),
                assertion_operator,
                assertion_expected,
                f"Element row index for selector `{selector}` is",
                message,
            )

    @keyword(tags=("Getter", "PageContent"))
    def get_element(self, selector: str) -> str:
        """Returns a reference to a Playwright [https://playwright.dev/docs/api/class-locator|Locator].

        The reference can be used in subsequent selectors.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which shall be retrieved . See the `Finding elements` section for details about the selectors. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | ${element} =    `Get Element`    \\#username_field
        | ${option_value} =    `Get Property`    ${element} >> optionOne    value    # Locator is resolved from the page.
        | ${option_value} =    `Get Property`    ${element} >> optionTwo    value    # Locator is resolved again from the page.

        [https://forum.robotframework.org/t/comments-for-get-element/4269|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElement(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=("Getter", "PageContent"))
    def get_elements(self, selector: str) -> List[str]:
        """Returns a reference to Playwright [https://playwright.dev/docs/api/class-locator|Locator]
        for all matched elements by ``selector``.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which shall be retrieved. See the `Finding elements` section for details about the selectors. |

        Example:
        | ${elements} =    `Get Elements`
        | ${elem} =    Get From List    ${elements}    0
        | ${option_value} =    `Get Property`    ${elem} >> option    value

        [https://forum.robotframework.org/t//4273|Comment >>]
        """
        selector = self.resolve_selector(selector)
        try:
            with self.playwright.grpc_channel(original_error=True) as stub:
                response = stub.GetElements(
                    Request().ElementSelector(selector=selector, strict=False)
                )
                logger.info(response.log)
                logger.debug(response.json)
                return json.loads(response.json)
        except grpc.RpcError as error:
            logger.info(error)
            if (
                error.code() == grpc.StatusCode.DEADLINE_EXCEEDED
                and error.details().startswith("TimeoutError: page.waitForSelector:")
            ):
                return []
            raise error

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_style(
        self,
        selector: str,
        key: str = "ALL",
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets the computed style properties of the element selected by ``selector``.

        Optionally matches with any sequence assertion operator.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the style shall be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``key`` | Key of the requested CSS property. Retrieves "ALL" styles by default. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the style matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        [https://forum.robotframework.org/t//4281|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetStyle(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
        parsed = DotDict(json.loads(response.json))
        formatter = self.keyword_formatters.get(self.get_style)
        if key == "ALL":
            if formatter:
                logger.warn(
                    "Formatter is not supported by Get Style keyword with key 'ALL'."
                )
            return dict_verify_assertion(
                parsed,
                assertion_operator,
                assertion_expected,
                "Computed style is",
                message,
            )
        else:
            item = parsed.get(key, "NOT_FOUND")
            logger.info(f"Value of key: {key}")
            logger.info(f"Value of selected property: {item}")
            return verify_assertion(
                item,
                assertion_operator,
                assertion_expected,
                f"Style value for {key} is",
                message,
                formatter,
            )

    @keyword(name="Get BoundingBox", tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_boundingbox(
        self,
        selector: str,
        key: BoundingBoxFields = BoundingBoxFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements size and location as an object ``{x: float, y: float, width: float, height: float}``.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which shall be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the BoundingBox as Dictionary, otherwise it will just return the single value selected by the key. Note: If a single value is retrieved, an assertion does *not* need a ``validate`` combined with a cast of ``value``. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the value matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example use:
        | ${bounding_box}=    `Get BoundingBox`    id=element                 # unfiltered
        | Log                 ${bounding_box}                                 # {'x': 559.09375, 'y': 75.5, 'width': 188.796875, 'height': 18}
        | ${x}=               `Get BoundingBox`    id=element    x            # filtered
        | Log                 X: ${x}                                         # X: 559.09375
        | # Assertions:
        | `Get BoundingBox`     id=element         width         >    180
        | `Get BoundingBox`     id=element         ALL           validate    value['x'] > value['y']*2

        [https://forum.robotframework.org/t//4258|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoundingBox(
                Request.ElementSelector(selector=selector, strict=self.strict_mode)
            )
        parsed = DotDict(json.loads(response.json))
        logger.debug(f"BoundingBox: {parsed}")
        if self.keyword_formatters.get(self.get_boundingbox):
            logger.warn("Formatter is not supported by Get Boundingbox keyword.")
        if key == BoundingBoxFields.ALL:
            return int_dict_verify_assertion(
                parsed, assertion_operator, assertion_expected, "BoundingBox is"
            )
        else:
            logger.info(f"Value of '{key}'': {parsed[key.name]}")
            return float_str_verify_assertion(
                parsed[key.name],
                assertion_operator,
                assertion_expected,
                f"BoundingBox {key.name} is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_scroll_size(
        self,
        selector: Optional[str] = None,
        key: SizeFields = SizeFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements or pages scrollable size as object ``{width: float, height: float}``.


        | =Arguments= | =Description= |
        | ``selector`` | Optional selector from which shall be retrieved. If no selector is given the scroll size of the page itself is used. See the `Finding elements` section for details about the selectors. |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the scroll size as dictionary, otherwise it will just return the single value selected by the key. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        See `Get BoundingBox` for more similar examples.

        Example use:
        | ${height}=         `Get Scroll Size`    height                          # filtered page by height
        | Log                Width: ${height}                                   # Height: 58425
        | ${scroll_size}=    `Get Scroll Size`    id=keyword-shortcuts-container  # unfiltered element
        | Log                ${scroll_size}                                     # {'width': 253, 'height': 3036}

        [https://forum.robotframework.org/t//4278|Comment >>]
        """
        scroll_size = DotDict()
        scroll_size["width"] = self.exec_scroll_function("scrollWidth", selector)
        scroll_size["height"] = self.exec_scroll_function("scrollHeight", selector)
        if self.keyword_formatters.get(self.get_scroll_size):
            logger.warn("Formatter is not supported by Get Scroll Size keyword.")
        if key == SizeFields.ALL:
            return int_dict_verify_assertion(
                scroll_size,
                assertion_operator,
                assertion_expected,
                "Scroll size is",
                message,
            )
        else:
            logger.info(f"Value of '{key}'': {scroll_size[key.name]}")
            return float_str_verify_assertion(
                scroll_size[key.name],
                assertion_operator,
                assertion_expected,
                f"Scroll {key.name} is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_scroll_position(
        self,
        selector: Optional[str] = None,
        key: AreaFields = AreaFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements or pages current scroll position as object ``{top: float, left: float, bottom: float, right: float}``.

        It describes the rectangle which is visible of the scrollable content of that element.
        all values are measured from position {top: 0, left: 0}.


        | =Arguments= | =Description= |
        | ``selector`` | Optional selector from which shall be retrieved. If no selector is given the client size of the page itself is used (``document.scrollingElement``). See the `Finding elements` section for details about the selectors. |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the scroll position as dictionary, otherwise it will just return the single value selected by the key. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the value matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        See `Get BoundingBox` or `Get Scroll Size` for examples.

        [https://forum.robotframework.org/t//4277|Comment >>]
        """
        scroll_position = DotDict()
        scroll_position["top"] = self.exec_scroll_function("scrollTop", selector)
        scroll_position["left"] = self.exec_scroll_function("scrollLeft", selector)
        client_size = self.get_client_size(selector)
        scroll_position["bottom"] = scroll_position["top"] + client_size["height"]
        scroll_position["right"] = scroll_position["left"] + client_size["width"]
        if self.keyword_formatters.get(self.get_scroll_position):
            logger.warn("Formatter is not supported by Get Scroll Position keyword.")
        if key == AreaFields.ALL:
            return int_dict_verify_assertion(
                scroll_position,
                assertion_operator,
                assertion_expected,
                "Scroll position is",
                message,
            )
        else:
            logger.info(f"Value of '{key}'': {scroll_position[key.name]}")
            return float_str_verify_assertion(
                scroll_position[key.name],
                assertion_operator,
                assertion_expected,
                f"Scroll position {key.name} is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_client_size(
        self,
        selector: Optional[str] = None,
        key: SizeFields = SizeFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements or pages client size (``clientHeight``, ``clientWidth``) as object {width: float, height: float}.


        | =Arguments= | =Description= |
        | ``selector`` | Optional selector from which shall be retrieved. If no selector is given the client size of the page itself is used (``document.scrollingElement``). See the `Finding elements` section for details about the selectors. |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the scroll size as dictionary, otherwise it will just return the single value selected by the key. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the value matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        See `Get BoundingBox` or `Get Scroll Size` for examples.

        [https://forum.robotframework.org/t//4263|Comment >>]
        """
        client_size = DotDict()
        client_size["width"] = self.exec_scroll_function("clientWidth", selector)
        client_size["height"] = self.exec_scroll_function("clientHeight", selector)
        if self.keyword_formatters.get(self.get_client_size):
            logger.warn("Formatter is not supported by Get Clinet Size keyword.")
        if key == SizeFields.ALL:
            return int_dict_verify_assertion(
                client_size,
                assertion_operator,
                assertion_expected,
                "Client size is",
                message,
            )
        else:
            logger.info(f"Value of '{key}'': {client_size[key.name]}")
            return float_str_verify_assertion(
                client_size[key.name],
                assertion_operator,
                assertion_expected,
                f"Client {key.name} is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_element_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[str] = None,
        message: Optional[str] = None,
    ):
        """*DEPRECATED!!* Use keyword `Get Element States` instead. This keyword will be removed end of 2022.

        Get the given state from the element found by ``selector``.

        Refactoring example assertion:
        | -    `Get Element State`    h1    readonly    ==    False
        | +    `Get Element States`    h1    not contains    readonly

         Refactoring example asserting multiple states:
        | -    `Get Element State`    id=password    visible    ==    True
        | -    `Get Element State`    id=password    readonly    ==    False
        | -    `Get Element State`    id=password    disabled    ==    False
        | +    `Get Element States`    h1    contains    visible    editable    enabled

        Refactoring example for getting state:
        | -    ${visibility}    `Get Element State`    h1    visible
        | +    ${visibility}    `Get Element States`    h1    then    bool(value & visible)  # Returns ``${True}`` if element is visible.


        If the selector does satisfy the expected state it will return ``True`` otherwise ``False``.

        ``selector`` Selector of the corresponding object. See the `Finding elements` section for details about the selectors.

        ``state`` Defaults to visible. Possible states are

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        ``assertion_expected`` Expected value for the counting

        ``message`` overrides the default error message for assertion.

        Note that element must be attached to DOM to be able to fetch the state of ``readonly`` , ``selected`` and ``checked``.
        The other states are false if the requested element is not attached.

        Note that element without any content or with display:none has an empty bounding box
        and is not considered visible.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | `Get Element State`    h1    readonly    ==    False

        [https://forum.robotframework.org/t//4271|Comment >>]
        """
        result = self.get_element_states(
            selector, AssertionOperator["evaluate"], f"bool(value & {state.name})"
        )

        if self.keyword_formatters.get(self.get_element_state):
            logger.warn("Formatter is not supported by Get Element State keyword.")
        selector = self.resolve_selector(selector)
        return bool_verify_assertion(
            result,
            assertion_operator,
            assertion_expected,
            f"State '{state.name}' of '{selector}' is",
            message,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_element_states(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected: Union[ElementState, str],
        message: Optional[str] = None,
        return_names=True,
    ) -> Any:
        """Get the active states from the element found by ``selector``.

        This Keyword returns a list of states that are valid for the selected element.


        | =Arguments= | =Description= |
        | ``selector`` | Selector of the corresponding object. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``*assertion_expected`` | Expected states |
        | ``message`` | overrides the default error message for assertion. |
        | ``return_names`` | If set to ``False`` the keyword does return an IntFlag object instead of a list. Defaults to ``True``. |

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default, assertion
        is not done.

        This keyword internally works with Python IntFlag.
        Flags can be processed using bitwise operators like & (bitwise AND) and | (bitwise OR).
        When using the assertion operators ``then``, ``evaluate`` or ``validate`` the ``value``
        contain the states as `ElementState`.

        Example:
        | `Get Element States`    h1    validate    value | visible
        | `Get Element States`    h1    then    value & (visible | hidden)  # returns either ``['visible']`` or ``['hidden']``
        | `Get Element States`    h1    then    bool(value & visible)  # Returns ``${True}`` if element is visible

        The most typical use case would be to verify if an element contains a specific state or multiple states.

        Example:
        | `Get Element States`    id=checked_elem      *=    checked
        | `Get Element States`    id=checked_elem      not contains    checked
        | `Get Element States`    id=invisible_elem    contains    hidden    attached
        | `Get Element States`    id=disabled_elem     contains    visible    disabled    readonly

        Elements do return the positive and negative values if applicable.
        As example, a checkbox does return either ``checked`` or ``unchecked`` while a text input
        element has none of those two states.
        Select elements have also either ``selected`` or ``unselected``.

        The state of ``animating`` will be set if an element is not considered ``stable``
        within 300 ms.

        If an element is not attached to the dom, so it can not be found within 250ms
        it is marked as ``detached`` as the only state.

        ``stable`` state is not returned, because it would cause too high delay in that keyword.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        [https://forum.robotframework.org/t/comments-for-get-element-states/4272|Comment >>]
        """
        selector = self.resolve_selector(selector)

        def convert_str(f):
            return f.name if isinstance(f, ElementState) else f

        assertion_expected_str = [convert_str(flag) for flag in assertion_expected]
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementStates(
                Request.ElementSelector(selector=selector, strict=self.strict_mode)
            )
        states = ElementState(json.loads(response.json))
        logger.debug(f"States: {states}")
        result = flag_verify_assertion(
            states,
            assertion_operator,
            assertion_expected_str,
            "Elements states",
            message,
        )
        if return_names and isinstance(result, ElementState):
            state_list = [flag.name for flag in ElementState if flag in result]
            logger.info(f"States are: {state_list}")
            return state_list
        else:
            return result
