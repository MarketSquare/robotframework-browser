from enum import Enum

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request


class Validation:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword  # Optional[str] didn't seem to work for text param here
    def page_should_have(self, selector: str, text=""):
        """Verifies that current page contains an element matching ``selector``.
            Optionally verifies that the element contains ``text``
            Page_should_contain keyword is syntactic sugar for page_should_have

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTextContent(Request().selector(selector=selector))
            logger.info(response.log)
            if response.body == "":
                message = "No element matching selector `{}` on page".format(selector)
                raise AssertionError(message)
            if text and text not in response.body:
                message = (
                    f"Element `{selector}` should have "
                    + f"contained {text} but it contained {response.body}"
                )

    @keyword
    def page_should_contain(self, text: str):
        """Verifies that current page contains ``text``. """
        self.page_should_have("text=" + text)

    class CheckboxState(Enum):
        checked = True
        unchecked = False

    @keyword
    def checkbox_should_be(self, selector: str, expected: CheckboxState):
        """ Verifies that checkbox or radio button ``selector`` is in state ``expected`` """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                Request().getDomProperty(selector=selector, property="checked")
            )
            logger.info(response.log)
            if response.body != expected.value:
                message = "Checkbox `{}` should be `{}` but was `{}`".format(
                    selector, expected, response.body
                )
                raise AssertionError(message)

    @keyword
    def list_selection_should_be(self, selector: str, *expected):
        """ Verifies list ``selector`` has ``expected`` options selected.
            If no ``expected`` selections are given will verify none are selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetSelectContent(Request().selector(selector=selector))
            logger.info(response)
            labels = {}
            values = {}
            for i in response.entry:
                if i.selected:
                    labels[i.label] = True
                    values[i.value] = True

            unexpected_false = []
            for i in expected:
                if not (i in labels or i in values):
                    unexpected_false.append(i)

            # When expected is empty we verify no elements are selected
            unexpected_true = []
            if not expected:
                for i in labels:
                    unexpected_true.append(i)

            message = ""
            if unexpected_false:
                message += f"""Select {selector} options {unexpected_false} \
                    should have been selected."""
            if unexpected_true:
                message += f""""Select {selector} options {unexpected_true} \
                    should not have been selected."""
            if message:
                raise AssertionError(message)
