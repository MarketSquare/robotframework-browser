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

import grpc  # type: ignore
from assertionengine import (
    AssertionOperator,
    bool_verify_assertion,
    dict_verify_assertion,
    float_str_verify_assertion,
    int_dict_verify_assertion,
    list_verify_assertion,
    verify_assertion,
)

from ..assertion_engine import with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import exec_scroll_function, keyword, logger
from ..utils.data_types import (
    AreaFields,
    BoundingBoxFields,
    ElementStateKey,
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

        Optionally asserts that it matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, "URL", message
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

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.

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
                value, assertion_operator, assertion_expected, "State", message
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

        ``message`` overrides the default error message.

        Optionally does a string assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageSource(Request().Empty())
            logger.debug(response.log)
            value = json.loads(response.body)
            return verify_assertion(
                value, assertion_operator, assertion_expected, "HTML:", message
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

        Optionally asserts that it matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(Request().Empty())
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, "Title", message
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
        See the `Finding elements` section for details about the selectors.

        Optionally asserts that the text matches the specified assertion.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetText(Request().ElementSelector(selector=selector))
            logger.debug(response.log)
            return verify_assertion(
                response.body, assertion_operator, assertion_expected, "Text", message
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

        Optionally asserts that the property value matches the specified
        assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``property`` Requested property name.

        If ``assertion_operator`` is set and property is not found, ``value`` is ``None``
        and Keyword does not fail. See `Get Attribute` for examples.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.
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
                value,
                assertion_operator,
                assertion_expected,
                f"Property {property}",
                message,
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

        Optionally asserts that the attribute value matches the specified
        assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``attribute`` Requested attribute name.

        When a attribute is selected that is not present and no assertion operator is set,
        the keyword fails. If an assertion operator is set and the attribute is not present,
        the returned value is ``None``.
        This can be used to assert check the presents or the absents of an attribute.

        ``message`` overrides the default error message.

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
                value,
                assertion_operator,
                assertion_expected,
                f"Attribute {selector}",
                message,
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

        Optionally asserts that these match the specified assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains`` / ``*=`` only accepts one single expected value

        Other operators are not allowed.

        ``message`` overrides the default error message.
        """
        attribute_names = self.library.execute_javascript(
            "(element) => element.getAttributeNames()", selector
        )
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
    ) -> Any:
        """Returns all classes of an element as a list.

        Optionally asserts that the value matches the specified assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        Available assertions:
        - ``==`` and ``!=`` can work with multiple values
        - ``contains`` / ``*=`` only accepts one single expected value

        Other operators are not allowed.
        """
        class_dict = self.get_property(selector, "classList")
        expected = list(assertion_expected)
        return list_verify_assertion(
            list(class_dict.values()),
            assertion_operator,
            expected,
            f"Classes of {selector}",
            message,
        )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_textfield_value(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """*DEPRECATED!!* Use keyword `Get Text` instead."""
        return verify_assertion(
            self.get_property(selector, "value"),
            assertion_operator,
            assertion_expected,
            f"Value {selector}",
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

        Optionally asserts that these match the specified assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        Example:

        | `Get Select Options`     //select[2]    validate  [v["label"] for v in value] == ["Email", "Mobile"]
        | `Get Select Options`   select#names     validate  any(v["label"] == "Mikko" for v in value)
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(
                Request().ElementSelector(selector=selector)
            )
            logger.info(response)
            result = [
                {
                    "index": index,
                    "value": sel.value,
                    "label": sel.label,
                    "selected": bool(sel.selected),
                }
                for index, sel in enumerate(response.entry)
            ]
            return verify_assertion(
                result,
                assertion_operator,
                assertion_expected,
                "Select Options:",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_selected_options(
        self,
        selector: str,
        option_attribute: SelectAttribute = SelectAttribute.label,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
    ) -> Any:
        """Returns the specified attribute of selected options of the ``select`` element.

        Optionally asserts that these match the specified assertion.

        ``selector`` Selector from which the info is to be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``option_attribute`` Which attribute shall be returned/verified.
        Defaults to label.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

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

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_checkbox_state(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_state: Union[bool, str] = "Unchecked",
        message: Optional[str] = None,
    ) -> bool:
        """Returns the state of the checkbox found by ``selector``.

        ``selector`` Selector which shall be examined.
        See the `Finding elements` section for details about the selectors.

        Optionally asserts that the state matches the specified assertion.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        - ``==`` and ``!=`` and equivalent are allowed on boolean values
        - other operators are not accepted.

        ``expected_state`` boolean value of expected state.
        Strings are interpreted as booleans.
        All strings are ``${True}`` except of the
        following `FALSE, NO, OFF, 0, UNCHECKED, NONE, ${EMPTY}``.
        (case-insensitive). Defaults to unchecked

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        ``message`` overrides the default error message.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().ElementProperty(selector=selector, property="checked")
            )
            logger.info(response.log)
            value: bool = response.body
            logger.info(f"Checkbox is {'checked' if value else 'unchecked'}")
            return bool_verify_assertion(
                value,
                assertion_operator,
                expected_state,
                f"Checkbox {selector} is",
                message,
            )

    @keyword(tags=("Getter", "Assertion", "PageContent"))
    @with_assertion_polling
    def get_element_count(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_value: Union[int, str] = 0,
        message: Optional[str] = None,
    ) -> Any:
        """Returns the count of elements found with ``selector``.

        Optionally asserts that the count matches the specified assertion.

        ``selector`` Selector which shall be counted.
        See the `Finding elements` section for details about the selectors.

        ``assertion_operator`` See `Assertions` for further details. Defaults to None.

        ``expected_value`` Expected value for the counting

        ``message`` overrides the default error message.
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

        Optionally asserts that the count matches the specified assertion.

        ``key`` Optionally filters the returned values.
        If keys is set to ``ALL`` (default) it will return the viewport size as dictionary,
        otherwise it will just return the single value selected by the key.
        Note: If a single value is retrieved, an assertion does *not* need a ``validate``
        combined with a cast of ``value``.

        ``message`` overrides the default error message.

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
    def get_element(self, selector: str) -> str:
        """Returns a reference to a Playwright element handle.

        The reference can be used in subsequent selectors.

        ``selector`` Selector from which shall be retrieved .
        See the `Finding elements` section for details about the selectors.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElement(Request().ElementSelector(selector=selector))
            return response.body

    @keyword(tags=("Getter", "PageContent"))
    def get_elements(self, selector: str) -> List[str]:
        """Returns a reference to playwright element handle for all matched elements by ``selector``.

        ``selector`` Selector from which shall be retrieved.
        See the `Finding elements` section for details about the selectors.
        """
        try:
            with self.playwright.grpc_channel(original_error=True) as stub:
                response = stub.GetElements(
                    Request().ElementSelector(selector=selector)
                )
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

        ``selector`` Selector from which the style shall be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``key`` Key of the requested CSS property. Retrieves "ALL" styles by default.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        ``message`` overrides the default error message.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetStyle(Request().ElementSelector(selector=selector))
            parsed = json.loads(response.json)

            if key == "ALL":
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
                )

    @keyword(name="Get BoundingBox", tags=("Getter", "Assertion", "PageContent"))
    def get_boundingbox(
        self,
        selector: str,
        key: BoundingBoxFields = BoundingBoxFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements size and location as an object ``{x: float, y: float, width: float, height: float}``.

        ``selector`` Selector from which shall be retrieved.
        See the `Finding elements` section for details about the selectors.

        ``key`` Optionally filters the returned values.
        If keys is set to ``ALL`` (default) it will return the BoundingBox as Dictionary,
        otherwise it will just return the single value selected by the key.
        Note: If a single value is retrieved, an assertion does *not* need a ``validate``
        combined with a cast of ``value``.

        ``message`` overrides the default error message.

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
            logger.debug(f"BoundingBox: {parsed}")
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
    def get_scroll_size(
        self,
        selector: Optional[str] = None,
        key: SizeFields = SizeFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements or pages scrollable size as object ``{width: float, height: float}``.

        ``selector`` Optional selector from which shall be retrieved.
        If no selector is given the scroll size of the page itself is used.
        See the `Finding elements` section for details about the selectors.

        ``key`` Optionally filters the returned values.
        If keys is set to ``ALL`` (default) it will return the scroll size as dictionary,
        otherwise it will just return the single value selected by the key.

        ``message`` overrides the default error message.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        See `Get BoundingBox` for more similar examples.

        Example use:
        | ${height}=         Get Scroll Size    height                          # filtered page by height
        | Log                Width: ${height}                                   # Height: 58425
        | ${scroll_size}=    Get Scroll Size    id=keyword-shortcuts-container  # unfiltered element
        | Log                ${scroll_size}                                     # {'width': 253, 'height': 3036}
        """
        scroll_size = dict()
        scroll_size["width"] = exec_scroll_function(self, "scrollWidth", selector)
        scroll_size["height"] = exec_scroll_function(self, "scrollHeight", selector)
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

        ``top`` uses js function scrollTop, ``left`` uses scrollLeft and
        ``bottom`` and ``right`` are calculated with the client size.

        ``selector`` Optional selector from which shall be retrieved.
        If no selector is given the client size of the page itself is used (``document.scrollingElement``).
        See the `Finding elements` section for details about the selectors.

        ``key`` Optionally filters the returned values.
        If keys is set to ``ALL`` (default) it will return the scroll position as dictionary,
        otherwise it will just return the single value selected by the key.

        ``message`` overrides the default error message.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        See `Get BoundingBox` or `Get Scroll Size` for examples.
        """
        scroll_position = dict()
        scroll_position["top"] = exec_scroll_function(self, "scrollTop", selector)
        scroll_position["left"] = exec_scroll_function(self, "scrollLeft", selector)
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
    def get_client_size(
        self,
        selector: Optional[str] = None,
        key: SizeFields = SizeFields.ALL,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: Optional[str] = None,
    ) -> Any:
        """Gets elements or pages client size (``clientHeight``, ``clientWidth``) as object {width: float, height: float}.

        ``selector`` Optional selector from which shall be retrieved.
        If no selector is given the client size of the page itself is used (``document.scrollingElement``).
        See the `Finding elements` section for details about the selectors.

        ``key`` Optionally filters the returned values.
        If keys is set to ``ALL`` (default) it will return the scroll size as dictionary,
        otherwise it will just return the single value selected by the key.

        ``message`` overrides the default error message.

        See `Assertions` for further details for the assertion arguments. Defaults to None.

        See `Get BoundingBox` or `Get Scroll Size` for examples.
        """
        client_size = dict()
        client_size["width"] = exec_scroll_function(self, "clientWidth", selector)
        client_size["height"] = exec_scroll_function(self, "clientHeight", selector)
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
    def get_element_state(
        self,
        selector: str,
        state: ElementStateKey = ElementStateKey.visible,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: bool = True,
        message: Optional[str] = None,
    ):
        """Get the given state from the element found by ``selector``.

        If the selector does satisfy the expected state it will return ``True`` otherwise ``False``.

        ``selector`` Selector of the corresponding object.
        See the `Finding elements` section for details about the selectors.

        ``state`` Defaults to visible. Possible states are:
        - ``attached`` : to be present in DOM.
        - ``visible`` : to have non-empty bounding box and no visibility:hidden.
        - ``disabled`` : to be ``disabled``. Can be used on <button>, <fieldset>, <input>, <optgroup>, <option>, <select> and <textarea>.
        - ``readonly`` : to be ``readOnly``. Can be used on <input> and <textarea>.
        - ``selected`` : to be ``selected``. Can be used on <option>.
        - ``focused`` : to be the ``activeElement``.
        - ``checked`` : to be ``checked`` . Can be used on <input>.

        Note that element must be attached to DOM to be able to fetch the state of ``readonly`` , ``selected`` and ``checked``.
        The other states are false if the requested element is not attached.

        Note that element without any content or with display:none has an empty bounding box
        and is not considered visible.

        ``message`` overrides the default error message.
        """
        funct = {
            ElementStateKey.disabled: "e => e.disabled",
            ElementStateKey.readonly: "e => e.readOnly",
            ElementStateKey.selected: "e => e.selected",
            ElementStateKey.focused: "e => document.activeElement === e",
            ElementStateKey.checked: "e => e.checked",
        }

        with self.playwright.grpc_channel() as stub:
            try:
                if state in funct:
                    stub.WaitForFunction(
                        Request().WaitForFunctionOptions(
                            script=funct[state],
                            selector=selector,
                            options=json.dumps({"timeout": 100}),
                        )
                    )
                else:
                    stub.WaitForElementsState(
                        Request().ElementSelectorWithOptions(
                            selector=selector,
                            options=json.dumps({"state": state.name, "timeout": 100}),
                        )
                    )
                result = True
            except Exception as e:
                if "Timeout 100ms exceeded." in e.args[0].details:
                    result = False
                else:
                    raise e
            return bool_verify_assertion(
                result,
                assertion_operator,
                assertion_expected,
                f"State '{state.name}' of '{selector}' is",
                message,
            )
