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
from contextlib import suppress
from typing import Any, Optional, Union

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
from robot.utils import DotDict

from Browser.utils.misc import get_download_id

from ..assertion_engine import assertion_formatter_used, with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import (
    AreaFields,
    BoundingBox,
    BoundingBoxFields,
    Dimensions,
    DownloadInfo,
    ElementRole,
    ElementState,
    RegExp,
    ScrollPosition,
    SelectAttribute,
    SelectionStrategy,
    SelectOptions,
    SizeFields,
    ViewportDimensions,
)


class Getters(LibraryComponent):
    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    @assertion_formatter_used
    def get_url(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> str:
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
            formatter = self.get_assertion_formatter("Get Url")
            return verify_assertion(
                value, assertion_operator, assertion_expected, "URL", message, formatter
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    @assertion_formatter_used
    def get_page_source(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> str:
        """Gets pages HTML source as a string.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the state |
        | ``message`` | overrides the default error message for assertion. |

        Optionally does a string assertion. See `Assertions` for further details for
        the assertion arguments. By default assertion is not done.

        If there need to get element html, use `Get Property` instead.
        Example:
        | ${html1} = [ `Get Property` | ${selector} | innerHTML |
        | ${html2} = [ `Get Property` | ${selector} | outerHTML |

        [https://forum.robotframework.org/t//4275|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageSource(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.body)
            formatter = self.get_assertion_formatter("Get Page Source")
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
    @assertion_formatter_used
    def get_title(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> str:
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
            logger.info(f"Title: {value!r}")
            formatter = self.get_assertion_formatter("Get Title")
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
    @assertion_formatter_used
    def get_text(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> str:
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

               [https://forum.robotframework.org/t//4285|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        response = self._get_text(selector)
        logger.debug(response.log)
        logger.info(f"Text: {response.body!r}")
        formatter = self.get_assertion_formatter("Get Text")
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
    @assertion_formatter_used
    def get_property(
        self,
        selector: str,
        property: str,  # noqa:  A002
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
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
            logger.info(f"Property: {value!r}")
        elif assertion_operator is not None:
            value = None
        else:
            raise AttributeError(f"Property '{property}' not found!")
        formatter = self.get_assertion_formatter("Get Property")
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
    @assertion_formatter_used
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Optional[str]:
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
        logger.info(f"Attribute is: {value!r}")
        formatter = self.get_assertion_formatter("Get Attribute")
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
    ) -> list[str]:
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
        - ``==`` , ``!=`` and ``contains`` / ``*=`` can work with multiple values
        - ``validate`` and ``evaluate`` only accepts one single expected value

        Other operators are not allowed.

        Example:
        | `Get Attribute Names`    [name="readonly_input"]    ==    type    name    value    readonly    # Has exactly these attribute names.
        | `Get Attribute Names`    [name="readonly_input"]    contains    disabled    # Contains at least this attribute name.

        [https://forum.robotframework.org/t//4257|Comment >>]
        """
        attribute_names = self.library.evaluate_javascript(
            selector, "(element) => element.getAttributeNames()"
        )
        if "__playwright_target__" in attribute_names:
            logger.debug("Remove __playwright_target__ from attribute names")
            attribute_names.remove("__playwright_target__")
        if attribute_names:
            logger.debug(
                f"Received attributes names: {', '.join(attribute_names)} for selector {selector}"
            )
        else:
            logger.debug(f"Did not receive attribute names for selector {selector}")
        expected = list(assertion_expected)
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
    ) -> list[str]:
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
        - ``==`` , ``!=`` and ``contains`` / ``*=`` can work with multiple values
        - ``validate`` and ``evaluate`` only accepts one single expected value

        Other operators are not allowed.

        Example:
        | `Get Classes`    id=draggable    ==    react-draggable    box    # Element contains exactly this class name.
        | `Get Classes`    id=draggable    validate    "react-draggable-dragged" not in value    # Element does not contain react-draggable-dragged class.

        [https://forum.robotframework.org/t//4262|Comment >>]
        """
        class_dict = self.get_property(selector, "classList")
        expected = list(assertion_expected)
        return list_verify_assertion(
            list(class_dict.values()),
            assertion_operator,
            expected,
            f"Classes of {self.resolve_selector(selector)}",
            message,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    @assertion_formatter_used
    def get_select_options(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> list[SelectOptions]:
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
        formatter = self.get_assertion_formatter("Get Select Options")
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
    ) -> list[Union[str, int]]:
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

        - ``==`` , ``!=`` and ``contains`` / ``*=`` can work with multiple values
        - ``validate`` and ``evaluate`` only accepts one single expected value

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
        selected: Union[list[int], list[str]]

        if option_attribute is SelectAttribute.index:
            expected = [int(exp) for exp in expected]
        selected = [
            getattr(sel, option_attribute.name)
            for sel in response.entry
            if sel.selected
        ]
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
    ) -> int:
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
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Optional[ViewportDimensions]:
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
                return None
            parsed = DotDict(response_json)
            logger.debug(parsed)
            if key == SizeFields.ALL:
                return int_dict_verify_assertion(
                    parsed,
                    assertion_operator,
                    assertion_expected,
                    "Viewport size is",
                    message,
                )
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
        node_name = str(self.library.evaluate_javascript(table, "e => e.nodeName"))
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
    ) -> int:
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
    ) -> int:
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

        [https://forum.robotframework.org/t//4269|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElement(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
            logger.info(response.log)
            return self._disable_selector_prefix(response.body)

    @keyword(tags=("Getter", "PageContent"))
    def get_elements(self, selector: str) -> list[str]:
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
                return self._disable_selector_prefix(json.loads(response.json))
        except grpc.RpcError as error:
            logger.info(error)
            if (
                error.code() == grpc.StatusCode.DEADLINE_EXCEEDED
                and error.details().startswith("Error: page.waitForSelector:")
            ):
                return []
            raise error

    @keyword(tags=("Getter", "PageContent"))
    def get_element_by_role(
        self,
        role: ElementRole,
        *,
        all_elements: bool = False,
        checked: Optional[bool] = None,
        disabled: Optional[bool] = None,
        exact: Optional[bool] = None,
        expanded: Optional[bool] = None,
        include_hidden: Optional[bool] = None,
        level: Optional[int] = None,
        name: Union[str, RegExp, None] = None,
        pressed: Optional[bool] = None,
        selected: Optional[bool] = None,
    ) -> str:
        """Returns a reference to Playwright [https://playwright.dev/docs/api/class-locator|Locator]
        for the matched element by ``role`` or a list of references if ``all_elements`` is set to ``True``.

        Allows locating elements by their [https://www.w3.org/TR/wai-aria-1.2/#roles|ARIA role],
        [https://www.w3.org/TR/wai-aria-1.2/#aria-attributes|ARIA attributes] and
        [https://w3c.github.io/accname/#dfn-accessible-name|accessible name].


        Consider the following DOM structure.

        | <h3>Sign up</h3>
        | <label>
        |   <input type="checkbox" /> Subscribe
        | </label>
        | <br/>
        | <button>Submit</button>

        You can locate each element by it's implicit role:
        | ${heading}    Get Element By Role    heading    name=Sign up
        | ${checkbox}   Get Element By Role    checkbox    name=Subscribe
        | ${button}     Get Element By Role    button    name=/submit/i

        | =Arguments= | =Description= |
        | ``all_elements`` | If True, returns all matched elements as a list. |
        | ``role`` | Role from which shall be retrieved. |
        | ``checked`` | An attribute that is usually set by aria-checked or native <input type=checkbox> controls. |
        | ``disabled`` | An attribute that is usually set by aria-disabled or disabled. |
        | ``exact`` | Whether name is matched exactly: case-sensitive and whole-string. Defaults to false. Ignored when name is a regular expression. Note that exact match still trims whitespace. |
        | ``expanded`` | An attribute that is usually set by aria-expanded. |
        | ``include_hidden`` | Option that controls whether hidden elements are matched. By default, only non-hidden elements, as defined by ARIA, are matched by role selector. |
        | ``level`` | A number attribute that is usually present for roles heading, list item, row, treeitem, with default values for <h1>-<h6> elements. |
        | ``name`` | Option to match the accessible name. By default, matching is case-insensitive and searches for a substring, use exact to control this behavior. |
        | ``pressed`` | An attribute that is usually set by aria-pressed. |
        | ``selected`` | An attribute that is usually set by aria-selected. |

        If an element shall be fetched from an iframe, a selector prefix must be set using `Set Selector Prefix` keyword including ``>>>`` as ending.

        [https://forum.robotframework.org/t//5938|Comment >>]
        """
        options = {
            key: value
            for key, value in locals().items()
            if value is not None
            and key
            in [
                "checked",
                "disabled",
                "exact",
                "expanded",
                "include_hidden",
                "level",
                "name",
                "pressed",
                "selected",
            ]
        }
        with self.playwright.grpc_channel() as stub:
            response = stub.GetByX(
                Request().GetByOptions(
                    strategy="Role",
                    text=role.name.lower(),
                    options=json.dumps(options),
                    strict=self.strict_mode,
                    all=all_elements,
                    frameSelector=self.get_frame_selector(),
                )
            )
            logger.info(response.log)
            return self._disable_selector_prefix(json.loads(response.json))

    def _disable_selector_prefix(self, selector: Union[str, list[str]]):
        if isinstance(selector, list):
            return (
                selector
                if not self.selector_prefix
                else [f"!prefix {element}" for element in selector]
            )
        return selector if not self.selector_prefix else f"!prefix {selector}"

    @keyword(tags=("Getter", "PageContent"))
    def get_element_by(
        self,
        selection_strategy: SelectionStrategy,
        text: Union[str, RegExp],
        exact: bool = False,
        all_elements: bool = False,
    ) -> str:
        """Allows locating elements by their features.

        Selection strategies can be several Playwright strategies like AltText or Label.
        See [https://playwright.dev/docs/locators|Playwright Locators] for more information.

        | =Arguments= | =Description= |
        | ``locator_type`` | SelectionStrategy to be used. Refers to Playwrights ``page.getBy***`` functions. See https://playwright.dev/docs/locators |
        | ``text`` | Text to locate the element for. |
        | ``exact`` | Whether to find an exact match: case-sensitive and whole-string. Default to false. Ignored when locating by a regular expression. Note that exact match still trims whitespace. This has no effect if RegExp is used or if TestID is used as strategy. |
        | ``all_elements`` | If True, returns all matched elements as a list. |

        This keywords implements the following Playwright functions:
        - [https://playwright.dev/docs/api/class-page#page-get-by-alt-text|page.getByAltText]
        - [https://playwright.dev/docs/api/class-page#page-get-by-label|page.getByLabel]
        - [https://playwright.dev/docs/api/class-page#page-get-by-placeholder|page.getByPlaceholder]
        - [https://playwright.dev/docs/api/class-page#page-get-by-test-id|page.getByTestId]
        - [https://playwright.dev/docs/api/class-page#page-get-by-text|page.getByText]
        - [https://playwright.dev/docs/api/class-page#page-get-by-title|page.getByTitle]

        ``page.getByRole`` is supported by `Get Element By Role` keyword.

        If an element shall be fetched from an iframe, a selector prefix must be set using `Set Selector Prefix` keyword including ``>>>`` as ending.

        [https://forum.robotframework.org/t//5937|Comment >>]
        """
        options = {"exact": exact} if exact is not None else {}
        with self.playwright.grpc_channel() as stub:
            response = stub.GetByX(
                Request().GetByOptions(
                    strategy=selection_strategy.value,
                    text=text,
                    options=json.dumps(options),
                    strict=self.strict_mode,
                    all=all_elements,
                    frameSelector=self.get_frame_selector(),
                )
            )
            logger.info(response.log)
            return self._disable_selector_prefix(json.loads(response.json))

    def get_frame_selector(self) -> str:
        if (
            self.selector_prefix
            and self.selector_prefix.strip().endswith(">>>")
            and self.library.get_property(
                f"!prefix {self.selector_prefix.rstrip('>').strip()}", "nodeName"
            )
            in ["IFRAME", "FRAME"]
        ):
            return self.selector_prefix.rstrip(">").strip()
        return ""

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    @assertion_formatter_used
    def get_style(
        self,
        selector: str,
        key: Optional[str] = "ALL",
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        pseudo_element: Optional[str] = None,
    ) -> Union[dict[str, str], str]:
        """Gets the computed style properties of the element selected by ``selector``.

        Optionally matches with any sequence assertion operator.


        | =Arguments= | =Description= |
        | ``selector`` | Selector from which the style shall be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``key`` | Key of the requested CSS property. Retrieves "ALL" styles as dictionary by default. All css settings can be used as keys even if they are not all returned in the dictionary. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |
        | ``pseudo_element`` | Pseudo element to match. Defaults to None. Pseudo elements are special css |

        [ https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements | Pseudo element ] is a css fuctionality to add styles. Example `::before` or `::after`.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Optionally asserts that the style matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        [https://forum.robotframework.org/t//4281|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        if key == "ALL" or key is None:
            key = ""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetStyle(
                Request().ElementStyle(
                    selector=selector,
                    styleKey=key,
                    pseudo=pseudo_element or "",
                    strict=self.strict_mode,
                )
            )
        parsed_response = json.loads(response.json)
        formatter = self.get_assertion_formatter("Get Style")
        if not key or isinstance(parsed_response, dict):
            if formatter:
                logger.warn(
                    "Formatter is not supported by Get Style keyword with key 'ALL'."
                )
            return dict_verify_assertion(
                DotDict(parsed_response),
                assertion_operator,
                assertion_expected,
                "Computed style is",
                message,
            )
        logger.info(f"Value of key: {key}")
        logger.info(f"Value of selected property: {parsed_response}")
        return verify_assertion(
            parsed_response,
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
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        *,
        allow_hidden: bool = False,
    ) -> Union[BoundingBox, float, int, None]:
        """Gets elements size and location as an object ``{x: float, y: float, width: float, height: float}``.

        Alternatively you can select a single attribute of the bounding box by setting the ``key`` argument.

        If an element is hidden and has no bounding box, the keyword will fail.
        Depending on the method used to make an element invisible, an element might still have a bounding box which can be retrieved.
        To allow also hidden elements without a bounding box, set ``allow_hidden`` to ``True``,
        which results in a return value of `None` in case of no bounding box.

        | =Arguments= | =Description= |
        | ``selector`` | Selector from which shall be retrieved. See the `Finding elements` section for details about the selectors. |
        | ``key`` | Optionally filters the returned values. If keys is set to ``ALL`` (default) it will return the BoundingBox as Dictionary, otherwise it will just return the single value selected by the key. Note: If a single value is retrieved, an assertion does *not* need a ``validate`` combined with a cast of ``value``. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the counting |
        | ``message`` | overrides the default error message for assertion. |
        | ``allow_hidden`` | (named only) If True, hidden elements are not causing a failure and will return `None`. Otherwise hidden element will fail. Defaults to False. |

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
        parsed = json.loads(response.json)
        if parsed is not None:
            with suppress(Exception):
                parsed = DotDict(parsed)
        elif allow_hidden and ElementState.hidden in self.get_element_states(
            selector, return_names=False
        ):
            return verify_assertion(
                None, assertion_operator, assertion_expected, "BoundingBox is", message
            )
        else:
            raise ValueError(
                f"Element is not visible and has no bounding box: {selector}"
            )
        logger.debug(f"BoundingBox: {parsed}")
        if key == BoundingBoxFields.ALL:
            return int_dict_verify_assertion(
                parsed,
                assertion_operator,
                assertion_expected,
                "BoundingBox is",
                message,
            )
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
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Union[Dimensions, float, int]:
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
        if key == SizeFields.ALL:
            return int_dict_verify_assertion(
                scroll_size,
                assertion_operator,
                assertion_expected,
                "Scroll size is",
                message,
            )
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
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Union[ScrollPosition, float]:
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
        if key == AreaFields.ALL:
            return int_dict_verify_assertion(
                scroll_position,
                assertion_operator,
                assertion_expected,
                "Scroll position is",
                message,
            )
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
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Dimensions:
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
        if key == SizeFields.ALL:
            return int_dict_verify_assertion(
                client_size,
                assertion_operator,
                assertion_expected,
                "Client size is",
                message,
            )
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
    def get_element_states(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected: Union[ElementState, str],
        message: Optional[str] = None,
        return_names=True,
    ) -> Union[list[str], ElementState]:
        """Get the active states from the element found by ``selector``.

        This Keyword returns a list of states that are valid for the selected element.


        | =Arguments= | =Description= |
        | ``selector`` | Selector of the corresponding object. See the `Finding elements` section for details about the selectors. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``*assertion_expected`` | Expected states |
        | ``message`` | overrides the default error message for assertion. |
        | ``return_names`` | If set to ``False`` the keyword does return an IntFlag object (`ElementState`) instead of a list. `ElementState` may contain multiple states at the same time. Defaults to ``True``. |

        Optionally asserts that the state matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default, assertion
        is not done.

        This keyword internally works with Python IntFlag.
        Flags can be processed using bitwise operators like & (bitwise AND) and | (bitwise OR).
        When using the assertion operators ``then``, ``evaluate`` or ``validate`` the ``value``
        contain the states as `ElementState`.

        Example:
        | `Get Element States`    h1    validate    value & visible   # Fails in case of an invisible element
        | `Get Element States`    h1    then    value & (visible | hidden)  # Returns either ``['visible']`` or ``['hidden']``
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

        [https://forum.robotframework.org/t//4272|Comment >>]
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
            return state_list  # type: ignore
        return result

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_download_state(
        self,
        download: Union[DownloadInfo, str],
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> DownloadInfo:
        """Gets the state of a download.

        Returns a dictionary of type `DownloadInfo` with the following keys:
        | {
        |   saveAs: str
        |   suggestedFilename: str
        |   state: str
        |   downloadID: Optional[str]
        | }

        | =Arguments= | =Description= |
        | ``download`` | `DownloadInfo` dictionary returned from `Promise To Wait For Download` or download id as string. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected state of the download. Be aware that the returned value is a dictionary |
        | ``message`` | overrides the default error message for assertion. |

        [https://forum.robotframework.org/t//6479|Comment >>]
        """
        download_id = get_download_id(download)
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDownloadState(Request().DownloadID(id=download_id))
            logger.info(response.log)
            return verify_assertion(
                json.loads(response.json),
                assertion_operator,
                assertion_expected,
                f"Download state is {download_id}",
                message,
            )
