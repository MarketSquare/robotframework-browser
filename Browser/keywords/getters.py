from typing import Any
from enum import Enum

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated import playwright_pb2


AssertionOperator = Enum("AssertionOperator", "NO_ASSERTION == !=")


def _verify_assertion(value: Any, operator: AssertionOperator, expected, message=""):
    if operator.name == "==" and value != expected:
        raise AssertionError(f"{message} `{value}` should be `{expected}`")
    if operator.name == "!=" and value == expected:
        raise AssertionError(f"{message} `{value}` should not be `{expected}`")
    elif operator.name not in AssertionOperator.__members__:
        raise AssertionError(
            f"{message} `{operator.name}` is not a valid assertion operator"
        )


class Getters:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def get_url(
        self,
        assertion_operator=AssertionOperator.NO_ASSERTION,
        assertion_value: Any = None,
    ) -> str:
        """ Returns current URL.

            Optionally asserts that it matches the specified assertion.
        """
        value = ""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetUrl(playwright_pb2.Empty())
            logger.info(response.log)
            value = response.body
        _verify_assertion(value, assertion_operator, assertion_value, "URL ")
        return value

    @keyword
    def get_title(
        self,
        assertion_operator=AssertionOperator.NO_ASSERTION,
        assertion_value: Any = None,
    ):
        """ Returns current page Title.

            Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(playwright_pb2.Empty())
            logger.info(response.log)
            value = response.body
        _verify_assertion(value, assertion_operator, assertion_value, "Title ")
        return value

    @keyword
    def get_text(
        self,
        selector: str,
        assertion_operator=AssertionOperator.NO_ASSERTION,
        assertion_value: Any = None,
    ):
        """ Returns element's text attribute.

            Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                playwright_pb2.getDomPropertyRequest(
                    selector=selector, property="innerText"
                )
            )
            logger.info(response.log)
            value = response.body
        _verify_assertion(
            value, assertion_operator, assertion_value, f"Text {selector}"
        )
        return value

    @keyword
    def get_element_attribute(
        self,
        selector: str,
        attribute: str,
        assertion_operator=AssertionOperator.NO_ASSERTION,
        assertion_value: Any = None,
    ):
        """ Returns specified attribute.

            Optionally asserts that it matches the specified assertion.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                playwright_pb2.getDomPropertyRequest(
                    selector=selector, property=attribute
                )
            )
            logger.info(response.log)
            value = response.body
        _verify_assertion(
            value, assertion_operator, assertion_value, f"Attribute {selector}"
        )
        return value

    @keyword
    def get_textfield_value(
        self,
        selector: str,
        assertion_operator=AssertionOperator.NO_ASSERTION,
        assertion_value: Any = None,
    ):
        """ Returns textfieds value.

            Optionally asserts that it matches the specified assertion.
        """
        value = None
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                playwright_pb2.getDomPropertyRequest(
                    selector=selector, property="value"
                )
            )
            logger.info(response.log)
            value = response.body
        _verify_assertion(
            value, assertion_operator, assertion_value, f"Element {selector} value "
        )
        return value
