import json
from typing import Any, Dict, List, Optional, Union

from robotlibcore import keyword  # type: ignore

from ..assertion_engine import (
    bool_verify_assertion,
    dict_verify_assertion,
    int_dict_verify_assertion,
    int_str_verify_assertion,
    list_verify_assertion,
    verify_assertion,
)
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import AssertionOperator, BoundingBoxFields, SelectAttribute


class Getters(LibraryComponent):
    @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    def get_url(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> str:
        """Returns the current URL.

        Optionally asserts that it matches the specified assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, "URL "
            )

    @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    def get_page_state(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> object:
        """Returns page model state object.

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
    def get_title(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns the title of the current page.

        Optionally asserts that it matches the specified assertion.
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
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(selector=selector, property="innerText")
            )
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, f"Text {selector}"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns ``attribute`` of the element found by ``selector``.

        Optionally asserts that the attribute value matches the specified
        assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(selector=selector, property=attribute)
            )
            logger.debug(response.log)
            value = response.body
            return verify_assertion(
                value, assertion_operator, assertion_expected, f"Attribute {selector}"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_textfield_value(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Returns value of the textfield found by ``selector``.

        Optionally asserts that the value matches the specified assertion.
        """
        return self.get_attribute(
            selector, "value", assertion_operator, assertion_expected
        )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_selected_options(
        self,
        selector: str,
        option_attribute: SelectAttribute = SelectAttribute.label,
        assertion_operator: Optional[AssertionOperator] = None,
        *assertion_expected,
    ):
        """Returns the specified attribute of selected options of the ``select`` element.

        Optionally asserts that these match the specified assertion.

        ``option_attribute``: which attribute shall be returned/verified.
        Allowed values are ``<"value"|"label"|"text"|"index">``

        ``assertion_operator`` see `Assertions`.

        - ``==`` and ``!=`` can work with multiple values
        - ``contains``/``*=`` only accepts one single expected value

        Other operators are not allowed.

        Example:

        | `Select Options By`    | label                 | //select[2] | Email | Mobile | | |
        | ${selected_list}     | `Get Selected Options`  | //select[2] | | | | # getter |
        | `Get Selected Options` | //select[2] | label | == | Mobile | Mail | #assertion content |
        | `Select Options By`    | label                 | select#names | 2 | 4 | |
        | `Get Selected Options` | select#names | index | == | 2      | 4     | #assertion index  |
        | `Get Selected Options` | select#names | label | *= | Mikko  |     | #assertion contains |
        | `Get Selected Options` | select#names | label | validate | len(value) == 3  | | #assertion length |

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
                selected, assertion_operator, expected, "Selected Options:",
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_checkbox_state(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_state: str = "Unchecked",
    ):
        """Returns the state of the checkbox found by ``selector``.

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        Optionally asserts that the state matches the specified assertion.

        ``assertion_operator`` see `Assertions`.

        - ``==`` and ``!=`` are allowed on boolean values
        - other operators are not accepted.

        ``expected_state``: boolean value of expected state.
        Strings are interpreted as booleans.
        All strings are ``${True}`` except of the
        following `FALSE, NO, OFF, 0, UNCHECKED, NONE, ${EMPTY}``.
        (case-insensitive).
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().ElementProperty(selector=selector, property="checked")
            )
            logger.info(f"Checkbox is {'checked' if response.log else 'unchecked'}")
            value: bool = response.body

            return bool_verify_assertion(
                value, assertion_operator, expected_state, f"Checkbox {selector} is"
            )

    @keyword(tags=["Getter", "Assertion", "PageContent"])
    def get_element_count(
        self,
        selector: str,
        assertion_operator: Optional[AssertionOperator] = None,
        expected_value: Union[int, str] = 0,
    ):
        """Returns the count of elements found with ``selector``.

        Optionally asserts that the count matches the specified assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementCount(
                Request().ElementSelector(selector=selector)
            )
            count = response.body
            return int_str_verify_assertion(
                int(count),
                assertion_operator,
                expected_value,
                f"Element count for selector `{selector}` is",
            )

    @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    def get_browser_catalog(self):
        """ Returns all Browsers, open Contexts in them and open Pages in these contexts.

            The data is parsed into a python list containing data representing the open Objects.

            On the root level the data contains a list of open Browsers.

            `` Browser: { type: Literal['chromium', 'firefox', 'webkit'], 'id': int, contexts: List[Context]}``
            `` Context: {type: 'context', 'id': int, pages: List[Page]} ``
            `` Page: {type: 'page', 'id': int, title: str, url: str} ``

            Sample: ``
            [{
                "type": "firefox",
                "id": 0,
                "contexts": [{
                    "type": "context",
                    "id": 0,
                    "pages": [{
                        "type": "page",
                        "title": "prefilled_email_form.html",
                        "url": "http://localhost:7272/prefilled_email_form.html",
                        "id": "0"
                    }]
                }, {
                    "type": "context",
                    "id": 1,
                    "pages": [{
                        "type": "page",
                        "title": "Login Page",
                        "url": "http://localhost:7272/dist/",
                        "id": "0"
                    }]
                }]
            }]

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBrowserCatalog(Request().Empty())
            parsed = json.loads(response.body)
            logger.info(json.dumps(parsed))
            return parsed

    @keyword(tags=["Getter", "Assertion", "BrowserControl"])
    def get_viewport_size(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Dict[str, int]] = None,
    ):
        """Gets the current viewport dimensions """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetViewportSize(Request().Empty())
            parsed = json.loads(response.body)
            return int_dict_verify_assertion(
                parsed, assertion_operator, assertion_expected, "Viewport size is"
            )

    @keyword(tags=["Getter", "BrowserControl"])
    def get_element(self, selector: str):
        """Returns a reference to a Playwright element handle.

        The reference can be used in subsequent selectors.

        See `library introduction` for more details on the selector syntax.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElement(Request().ElementSelector(selector=selector))
            return response.body

    @keyword(tags=["Getter", "BrowserControl"])
    def get_elements(self, selector: str):
        """Returns a reference to playwright element handle for all matched elements by ``selector``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElements(Request().ElementSelector(selector=selector))
            data = json.loads(response.body)
            return data

    @keyword(tags=["Getter", "Assertion"])
    def get_style(
        self,
        selector: str,
        key: str = "ALL",
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ):
        """Gets the computed style properties of the element selected by ``selector``

            With any other value than "ALL" will try to get CSS property with key ``key``

            Optionally matches with any sequence assertion operator.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetStyle(Request().ElementSelector(selector=selector))
            parsed = json.loads(response.body)

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

    @keyword(tags=["Getter", "Assertion"])
    def get_boundingbox(self, selector: str, *keys: BoundingBoxFields):
        """ Gets elements size and location as an object {x: int, y: int, width: int, height: int}.

            Optionally filters the returned values based on ``keys``.

            Example use:
            | unfiltered:       |                  |            |   |   |
            | ${bounding_box}=  | Get BoundingBox  | \\#element |   |   |
            | filtered:         |                  |            |   |   |
            | ${xy}=            | Get BoundingBox  | \\#element | x | y |


        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoundingBox(Request.ElementSelector(selector=selector))
            parsed = json.loads(response.body)
            logger.debug(parsed)
            if keys:
                parsed = {key.value: parsed[key.value] for key in keys}
            return parsed
