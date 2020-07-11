import json
from typing import Any
from copy import copy

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..assertion_engine import verify_assertion, AssertionOperator
from .input import SelectAttribute


class Getters(LibraryComponent):
    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def get_url(
        self,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ) -> str:
        """Returns the current URL.

        Optionally asserts that it matches the specified assertion.
        """
        value = ""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            self.debug(response.log)
            value = response.body
        return verify_assertion(value, assertion_operator, assertion_expected, "URL ")

    @keyword
    def get_page_state(
        self,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ) -> object:
        """Returns page model state object.

        This must be given on the page to ``window.__RFBROWSER__``

        For example:

        ``let mystate = {'login': true, 'name': 'George', 'age': 123};``

        ``window.__RFBROWSER__ && window.__RFBROWSER__(mystate);``
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetPageState(Request().Empty())
            self.debug(response.log)
            value = json.loads(response.result)
        return verify_assertion(value, assertion_operator, assertion_expected, "State ")

    @keyword
    def get_title(
        self,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """Returns the title of the current page.

        Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(Request().Empty())
            self.debug(response.log)
            value = response.body
        return verify_assertion(value, assertion_operator, assertion_expected, "Title ")

    @keyword
    def get_text(
        self,
        selector: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """Returns text attribute of the element found by ``selector``.

        Optionally asserts that the text matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(selector=selector, property="innerText")
            )
            self.debug(response.log)
            value = response.body
        return verify_assertion(
            value, assertion_operator, assertion_expected, f"Text {selector}"
        )

    @keyword
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """Returns ``attribute`` of the element found by ``selector``.

        Optionally asserts that the attribuyte value matches the specified
        assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().ElementProperty(selector=selector, property=attribute)
            )
            self.debug(response.log)
            value = response.body
        return verify_assertion(
            value, assertion_operator, assertion_expected, f"Attribute {selector}"
        )

    @keyword
    def get_textfield_value(
        self,
        selector: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """Returns value of the textfield found by ``selector``.

        Optionally asserts that the value matches the specified assertion.
        """
        return self.get_attribute(
            selector, "value", assertion_operator, assertion_expected
        )

    @keyword
    def get_selected_options(
        self,
        selector: str,
        option_attribute: SelectAttribute = SelectAttribute.label,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
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
        selected = list()
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(
                Request().ElementSelector(selector=selector)
            )
            self.info(response)

            expected = list(assertion_expected)

            if option_attribute is SelectAttribute.value:
                selected = [sel.value for sel in response.entry if sel.selected]
            elif option_attribute is SelectAttribute.label:
                selected = [sel.label for sel in response.entry if sel.selected]
            elif option_attribute is SelectAttribute.index:
                selected = [
                    index for index, sel in enumerate(response.entry) if sel.selected
                ]
                expected = [int(exp) for exp in expected]

            expected.sort()
            expected_value: object = expected
            sorted_selected = copy(selected)
            sorted_selected.sort()
            value: object = sorted_selected

            if assertion_operator in [
                AssertionOperator["*="],
                AssertionOperator["validate"],
            ]:
                if len(expected) != 1:
                    raise AttributeError(
                        f"Operator '{assertion_operator.name}' expects '1'"
                        f" expected value but got '{len(expected)}'."
                    )
                expected_value = expected[0]
            elif assertion_operator not in [
                AssertionOperator["=="],
                AssertionOperator["!="],
                AssertionOperator["noassertion"],
            ]:
                raise AttributeError(
                    f"Operator '{assertion_operator.name}' is not allowed "
                    f"in this Keyword."
                )
            verify_assertion(
                value, assertion_operator, expected_value, "Selected Options:"
            )
            if len(selected) == 0:
                return None
            elif len(selected) == 1:
                return selected[0]
            else:
                return list(selected)

    @keyword
    def get_checkbox_state(
        self,
        selector: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        state: bool = False,
    ):
        """Returns the state of the checkbox found by ``selector``.

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        Optionally asserts that the state matches the specified assertion.

        ``assertion_operator`` see `Assertions`.

        - ``==`` and ``!=`` are allowed on boolean values
        - other operators are not accepted.

        ``state``: boolean value of expected state.
        Strings are parsed as booleans.
        All strings are ``${True}`` except of the following ``unchecked, FALSE, NO, OFF, 0``.
        (case-insensitive) The string ``checked`` can be used as True value.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().ElementProperty(selector=selector, property="checked")
            )
            self.info(f"Checkbox is {'checked' if response.log else 'unchecked'}")
            value: bool = response.body

            if assertion_operator not in [
                AssertionOperator["=="],
                AssertionOperator["!="],
            ]:
                raise ValueError(
                    f"Operators '==' and '!=' are allowed,"
                    f" not '{assertion_operator.name}'."
                )

            if isinstance(state, str):
                state = state.lower() != "unchecked"

        return verify_assertion(
            value, assertion_operator, state, f"Checkbox {selector} is"
        )

    @keyword
    def get_element_count(
        self,
        selector: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        expected_count: str = "-1",
    ):
        """Returns the count of elements found with ``selector``.

        Optionally asserts that the count matches the specified assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetElementCount(
                Request().ElementSelector(selector=selector)
            )
            count = response.body

        try:
            int(expected_count)
        except ValueError:
            raise AssertionError(
                f"Invalid value for argument `expected_count`: `${expected_count}`"
            )

        return verify_assertion(
            str(count),
            assertion_operator,
            expected_count,
            f"Element count for selector `{selector}` is",
        )
