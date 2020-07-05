from typing import Any
from copy import copy

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request
from ..assertion_engine import verify_assertion, AssertionOperator
from .input import SelectAttribute


class Getters:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def get_url(
        self,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ) -> str:
        """ Returns current URL.

            Optionally asserts that it matches the specified assertion.
        """
        value = ""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(Request().Empty())
            logger.debug(response.log)
            value = response.body
        return verify_assertion(value, assertion_operator, assertion_expected, "URL ")

    @keyword
    def get_title(
        self,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """ Returns current page Title.

            Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(Request().Empty())
            logger.debug(response.log)
            value = response.body
        return verify_assertion(value, assertion_operator, assertion_expected, "Title ")

    @keyword
    def get_text(
        self,
        selector: str,
        assertion_operator: AssertionOperator = AssertionOperator.NO_ASSERTION,
        assertion_expected: Any = None,
    ):
        """ Returns element's text attribute.

            Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().getDomProperty(selector=selector, property="innerText")
            )
            logger.debug(response.log)
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
        """ Returns specified attribute.

            Optionally asserts that it matches the specified assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                Request().getDomProperty(selector=selector, property=attribute)
            )
            logger.debug(response.log)
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
        """ Returns textfieds value.

            Optionally asserts that it matches the specified assertion.
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

        """ Returns the specified Attribute of selected Options of the Select List.

        Optionally asserts that these match the specified assertion.

        ``option_attribute``: which attribute shall be returned/verified.
        Allowed values are ``<"value"|"label"|"text"|"index">``

        ``assertion_operator`` see `Assertions`.

        - ``==`` and ``!=`` can work with multiple values
        - ``contains``/``*=`` only accepts one single expected value
        - ``>``, ``>=``, ``<=`` and ``<`` do compare amount of selected options and accept numbers.
        - ``^=``, ``matches``, ``$=`` are invalid operators in this context and are not allowed.

        Example:

        | `Select Options By`    | label                 | //select[2] | Email | Mobile | | |
        | ${selected_list}     | `Get Selected Options`  | //select[2] | | | | # getter |
        | `Get Selected Options` | //select[2] | label | == | Mobile | Mail | #assertion content |
        | `Get Selected Options` | //select[2] | label | <= | 2      |       | #assertion amount |
        | `Select Options By`    | label                 | select#names | 2 | 4 | 5  |
        | `Get Selected Options` | select#names | index | == | 2      | 4     | #assertion index  |
        | `Get Selected Options` | select#names | label | *= | Mikko  |     | #assertion contains |

        """
        selected = list()
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(Request().selector(selector=selector))
            logger.info(response)

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

            if assertion_operator == AssertionOperator["*="]:
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
        """ Returns the specified the checkbox state as boolean value.

        - ``checked`` => ``True``
        - ``unchecked`` => ``False``

        Optionally asserts that these match the specified assertion.

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
                Request().getDomProperty(selector=selector, property="checked")
            )
            logger.info(f"Checkbox is {'checked' if response.log else 'unchecked'}")
            value: bool = response.body

            if assertion_operator not in [
                AssertionOperator["=="],
                AssertionOperator["!="],
            ]:
                raise ValueError(
                    f"Operators '==' and '!=' are allowsed,"
                    f" not '{assertion_operator.name}'."
                )

            if isinstance(state, str):
                state = state.lower() != "unchecked"

        return verify_assertion(
            value, assertion_operator, state, f"Checkbox {selector} is"
        )
