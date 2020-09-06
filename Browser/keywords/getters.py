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
from typing import Any, List, Optional, Union

from robotlibcore import keyword  # type: ignore

from ..assertion_engine import (
    bool_verify_assertion,
    dict_verify_assertion,
    float_str_verify_assertion,
    int_dict_verify_assertion,
    list_verify_assertion,
    verify_assertion,
    with_assertion_polling,
)
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import (
    AssertionOperator,
    BoundingBoxFields,
    SelectAttribute,
    ViewportFields,
)


class Getters(LibraryComponent):
    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_url(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> str:
        """Returns the current URL.

        Optionally asserts that it matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, "URL "
            )

    # @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    # Not published as keyword due to missing of good docs.
    @with_assertion_polling
    def get_page_state(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> object:
        """Returns page model state object as a dictionary.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        This must be given on the page to ``window.__SET_RFBROWSER_STATE__``

        For example:

        ``let mystate = {'login': true, 'name': 'George', 'age': 123};``

        ``window.__SET_RFBROWSER_STATE__ && window.__SET_RFBROWSER_STATE__(mystate);``
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageState(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.result)
            return verify_assertion(
                value, assertion_operator, assertion_expected, "State "
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_page_source(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> str:
        """Gets pages HTML source as a string.

        Optionally does a string assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageSource(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.body)
            return verify_assertion(
                value, assertion_operator, assertion_expected, "HTML: "
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_title(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns the title of the current page.

        Optionally asserts that it matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(Request().Empty())
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, "Title "
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_text(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns text attribute of the element found by ``selector``.

        Optionally asserts that the text matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        return self.get_property(
            selector, "innerText", assertion_operator, assertion_expected
        )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_property(
        self,
        selector: str,
        property: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns the ``property`` of the element found by ``selector``.

        Optionally asserts that the property value matches the specified
        assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        ``property`` <str> Requested property name. **Required**

        If ``assertion_operator`` is set and property is not found, ``value`` is ``None``
        and Keyword does not fail. See `Get Attribute` for examples.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(selector=selector, property=property)
            )
            logger.debug(response.log)
            if response.body:
                value = json.loads(response.body)
            elif assertion_operator is not None:
                value = None
            else:
                raise AttributeError(f"Property '{property}' not found!")
            return verify_assertion(
                value, assertion_operator, assertion_expected, f"Property {property}"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns the HTML ``attribute`` of the element found by ``selector``.

        Optionally asserts that the attribute value matches the specified
        assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        ``attribute`` <str> Requested attribute name. **Required**

        When a attribute is selected that is not present and no assertion operator is set,
        the keyword fails. If an assertion operator is set and the attribute is not present,
        the returned value is ``None``.
        This can be used to assert check the presents or the absents of an attribute.

        Example Element:
        | <button class="login button active" id="enabled_button" something>Login</button>

        Example Code:
        | Get Attribute   id=enabled_button    disabled                   # FAIL => "Attribute 'disabled' not found!"
        | Get Attribute   id=enabled_button    disabled     ==    None     # PASS => returns: None
        | Get Attribute   id=enabled_button    something    evaluate    value is not None    # PASS =>  returns: True
        | Get Attribute   id=enabled_button    disabled     evaluate    value is None        # PASS =>  returns: True


        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementAttribute(
                Request().ElementProperty(selector=selector, property=attribute)
            )
            logger.debug(response.log)
            value = json.loads(response.body)
            if assertion_operator is None and value is None:
                raise AttributeError(f"Attribute '{attribute}' not found!")
            logger.debug(f"Attribute is: {value}")
            return verify_assertion(
                value, assertion_operator, assertion_expected, f"Attribute {selector}"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_attribute_names(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
    ):
        """Returns all HTML attribute names of an element as a list.

        Optionally asserts that these match the specified assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        ``assertion_operator`` <AssertionOperator> See `Assertions` for further details. Defaults to None.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains``/``*=`` only accepts one single expected value

        Other operators are not allowed.
        """
        attribute_names = self.library.execute_javascript(
            "(element) => element.getAttributeNames()", selector
        )
        expected = list(assertion_expected)
        return list_verify_assertion(
            attribute_names, assertion_operator, expected, "Attribute names"
        )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_classes(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
    ):
        """Returns all classes of an element as a list.

        Optionally asserts that the value matches the specified assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        ``assertion_operator`` <AssertionOperator> See `Assertions` for further details. Defaults to None.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains``/``*=`` only accepts one single expected value

        Other operators are not allowed.
        """
        class_dict = self.get_property(selector, "classList")
        expected = list(assertion_expected)
        return list_verify_assertion(
            list(class_dict.values()),
            assertion_operator,
            expected,
            f"Classes of {selector}",
        )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_textfield_value(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns value of the textfield found by ``selector``.

        Optionally asserts that the value matches the specified assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        return verify_assertion(
            self.get_property(selector, "value"),
            assertion_operator,
            assertion_expected,
            f"Value {selector}",
        )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_selected_options(
        self,
        selector: str,
        option_attribute: SelectAttribute = SelectAttribute.label,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
    ):
        """Returns the specified attribute of selected options of the ``select`` element.

        Optionally asserts that these match the specified assertion.

        ``selector`` <str> Selector from which the info is to be retrieved. **Required**

        ``option_attribute`` <SelectAttribute.label> Which attribute shall be returned/verified.
        Allowed values are ``< ``value`` | ``label`` | ``text`` | ``index`` >``. Defaults to label.

        ``assertion_operator`` <AssertionOperator> See `Assertions` for further details. Defaults to None.

        - ``==`` and ``!=`` can work with multiple values
        - ``contains``/``*=`` only accepts one single expected value

        Other operators are not allowed.

        Example:

        | `Select Options By`      label                    //select[2]    Email      Mobile
        | ${selected_list}         `Get Selected Options`   //select[2]                                         # getter
        | `Get Selected Options`   //select[2]              label          `==`       Mobile             Mail   #assertion content
        | `Select Options By`      label                    select#names   2          4
        | `Get Selected Options`   select#names             index          `==`       2                  4      #assertion index
        | `Get Selected Options`   select#names             label          *=         Mikko                     #assertion contain
        | `Get Selected Options`   select#names             label          validate   len(value) == 3           #assertion length

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(
                Request().ElementSelector(selector=selector)
            )
            logger.info(response)
            expected = list(assertion_expected)
            selected: Union[List[int], List[str]]
            if option_attribute is SelectAttribute.value:
                selected = [sel.value for sel in response.entry if sel.selected]
            elif option_attribute is SelectAttribute.label:
                selected = [sel.label for sel in response.entry if sel.selected]
            elif option_attribute is SelectAttribute.index:
                selected = [
                    index for index, sel in enumerate(response.entry) if sel.selected
                ]
                expected = [int(exp) for exp in expected]

            return list_verify_assertion(
                selected,
                assertion_operator,
                expected,
                "Selected Options:",
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_checkbox_state(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_state: str = "Unchecked",
    ):
        """Returns the state of the checkbox found by ``selector``.

        ``selector`` <str> Selector which shall be examined

        Optionally asserts that the state matches the specified assertion.

        ``assertion_operator`` <AssertionOperator> See `Assertions` for further details. Defaults to None.

        - ``==`` and ``!=`` and equivalent are allowed on boolean values
        - other operators are not accepted.

        ``expected_state`` <str> boolean value of expected state.
        Strings are interpreted as booleans.
        All strings are ``${True}`` except of the
        following `FALSE, NO, OFF, 0, UNCHECKED, NONE, ${EMPTY}``.
        (case-insensitive). Defaults to unchecked

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().ElementProperty(selector=selector, property="checked")
            )
            logger.info(response.log)
            value: bool = response.body
            logger.info(f"Checkbox is {'checked' if value else 'unchecked'}")
            return bool_verify_assertion(
                value, assertion_operator, expected_state, f"Checkbox {selector} is"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_element_count(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_value: Union[int, str] = 0,
    ):
        """Returns the count of elements found with ``selector``.

        Optionally asserts that the count matches the specified assertion.

        ``selector`` <str> Selector which shall be counted.

        ``assertion_operator`` <AssertionOperator> See `Assertions` for further details. Defaults to None.

        ``expected_value`` <str|int> Expected value for the counting
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementCount(
                Request().ElementSelector(selector=selector)
            )
            count = response.body
            return float_str_verify_assertion(
                int(count),
                assertion_operator,
                expected_value,
                f"Element count for selector `{selector}` is",
            )

    @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    @with_assertion_polling
    def get_viewport_size(
        self,
        key: ViewportFields = ViewportFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns the current viewport dimensions.

        Optionally asserts that the count matches the specified assertion.

        ``key`` < ``width`` | ``height`` | ``ALL`` > Optionally filters the returned values.
        If keys is set to ``ALL``(default) it will return the viewport size as dictionary,
        otherwise it will just return the single value selected by the key.
        Note: If a single value is retrieved, an assertion does *not* need a ``validate``
        combined with a cast of ``value``.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        Example:
        | Get Viewport Size    ALL    ==    {'width':1280, 'height':720}
        | Get Viewport Size    width    >=    1200

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetViewportSize(Request().Empty())
            logger.info(response.log)
            parsed = json.loads(response.json)
            logger.debug(parsed)
            if key == ViewportFields.ALL:
                return int_dict_verify_assertion(
                    parsed, assertion_operator, assertion_expected, "Viewport size is"
                )
            else:
                logger.info(f"Value of '{key}'': {parsed[key.name]}")
                return float_str_verify_assertion(
                    parsed[key.name],
                    assertion_operator,
                    assertion_expected,
                    f"{key} is ",
                )

    @keyword(tags=["Getter", "PageContent"])
    def get_element(self, selector: str):
        """Returns a reference to a Playwright element handle.

        The reference can be used in subsequent selectors.

        ``selector`` <str> Selector from which shall be retrieved.
        See `library introduction` for more details on the selector syntax. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElement(Request().ElementSelector(selector=selector))
            return response.body

    @keyword(tags=["Getter", "PageContent"])
    def get_elements(self, selector: str):
        """Returns a reference to playwright element handle for all matched elements by ``selector``.

        ``selector`` <str> Selector from which shall be retrieved. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElements(Request().ElementSelector(selector=selector))
            return json.loads(response.json)

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    @with_assertion_polling
    def get_style(
        self,
        selector: str,
        key: str = "ALL",
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Gets the computed style properties of the element selected by ``selector``.

        Optionally matches with any sequence assertion operator.

        ``selector`` <str> Selector from which the style shall be retrieved. **Required**

        ``key`` <str> Key of the requested CSS property. Retrieves "ALL" styles by default.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetStyle(Request().ElementSelector(selector=selector))
            parsed = json.loads(response.json)

            if key == "ALL":
                return dict_verify_assertion(
                    parsed, assertion_operator, assertion_expected, "Computed style is"
                )
            else:
                item = parsed.get(key, "NOT_FOUND")
                logger.info(f"Value of key: {key}")
                logger.info(f"Value of selected property: {item}")
                return verify_assertion(
                    item,
                    assertion_operator,
                    assertion_expected,
                    f"Style value for {key} is ",
                )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_boundingbox(
        self,
        selector: str,
        key: BoundingBoxFields = BoundingBoxFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Gets elements size and location as an object {x: float, y: float, width: float, height: float}.

        ``selector`` <str> Selector from which shall be retrieved. **Required**

        ``key`` < ``x`` | ``y`` | ``width`` | ``height`` | ``ALL`` > Optionally filters the returned values.
        If keys is set to ``ALL``(default) it will return the BoundingBox as Dictionary,
        otherwise it will just return the single value selected by the key.
        Note: If a single value is retrieved, an assertion does *not* need a ``validate``
        combined with a cast of ``value``.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        Example use:
        | ${bounding_box}=    Get BoundingBox    id=element                 # unfiltered
        | Log                 ${bounding_box}                               # {'x': 559.09375, 'y': 75.5, 'width': 188.796875, 'height': 18}
        | ${x}=               Get BoundingBox    id=element    x            # filtered
        | Log                 X: ${x}                                       # X: 559.09375
        | # Assertions:
        | Get BoundingBox     id=element         width         >    180
        | Get BoundingBox     id=element         ALL           validate    value['x'] > value['y']*2
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoundingBox(Request.ElementSelector(selector=selector))
            parsed = json.loads(response.json)
            logger.debug(parsed)
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
                    f"{key} is ",
                )
