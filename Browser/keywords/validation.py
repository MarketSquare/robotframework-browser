from enum import Enum

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated import playwright_pb2


class Validation:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def location_should_be(self, url: str):
        """ Verifies that the current URL is exactly ``url``. """
        with self.playwright.grpc_channel() as stub:
            page_url = stub.GetUrl(playwright_pb2.Empty()).body
            if url != page_url:
                message = "URL should be `{}`  but was `{}`".format(url, page_url)
                raise AssertionError(message)

    @keyword
    def textfield_value_should_be(self, selector: str, expected: str):
        """Verifies text field ``selector`` has exactly text ``expected``. """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDomProperty(
                playwright_pb2.getDomPropertyRequest(
                    selector=selector, property="value"
                )
            )
            logger.info(response.log)
            if response.body != expected:
                message = "Textfield {} content should be {} but was `{}`".format(
                    selector, expected, response.body
                )
                raise AssertionError(message)

    @keyword
    def title_should_be(self, title: str):
        """ Verifies that the current page title equals ``title`` """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTitle(playwright_pb2.Empty())
            logger.info(response.log)
            if response.body != title:
                message = "Title should be {} but was `{}`".format(title, response.body)
                raise AssertionError(message)

    @keyword
    def page_should_contain(self, text: str):
        """Verifies that current page contains ``text``. """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTextContent(
                playwright_pb2.selectorRequest(selector="text=" + text)
            )
            logger.info(response.log)
            if response.body != text:
                message = "No element with text `{}` on page".format(text)
                raise AssertionError(message)

    class CheckboxState(Enum):
        checked = True
        unchecked = False

    @keyword
    def checkbox_should_be(self, selector: str, expected: CheckboxState):
        """ Verifies that checkbox ``selector`` is in state ``expected`` """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBoolProperty(
                playwright_pb2.getDomPropertyRequest(
                    selector=selector, property="checked"
                )
            )
            logger.info(response.log)
            if response.body != expected.value:
                message = "Checkbox `{}` should be `{}` but was `{}`".format(
                    selector, expected, response.body
                )
                raise AssertionError(message)
