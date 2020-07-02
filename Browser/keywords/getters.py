from typing import Any

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request
from ..assertion_engine import verify_assertion, AssertionOperator


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
        verify_assertion(value, assertion_operator, assertion_expected, "URL ")
        return value

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
        verify_assertion(value, assertion_operator, assertion_expected, "Title ")
        return value

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
        verify_assertion(
            value, assertion_operator, assertion_expected, f"Text {selector}"
        )
        return value

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
        verify_assertion(
            value, assertion_operator, assertion_expected, f"Attribute {selector}"
        )
        return value

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
