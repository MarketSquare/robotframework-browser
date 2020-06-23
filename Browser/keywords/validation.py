from enum import Enum
from typing import Callable, ContextManager

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.generated.playwright_pb2_grpc import PlaywrightStub
from Browser.generated.playwright_pb2 import Empty
import Browser.generated.playwright_pb2 as playwright_pb2


class Validation:
    def __init__(self, insecure_stub: Callable[[], ContextManager[PlaywrightStub]]):
        self._insecure_stub = insecure_stub

    @keyword
    def location_should_be(self, url: str):
        """ Verifies that the current URL is exactly ``url``. """
        with self._insecure_stub() as stub:
            page_url = stub.GetUrl(Empty()).body
            if url != page_url:
                message = "URL should be `{}`  but was `{}`".format(url, page_url)
                raise AssertionError(message)

    @keyword
    def textfield_value_should_be(self, selector: str, expected: str):
        """Verifies text field ``selector`` has exactly text ``expected``. """
        with self._insecure_stub() as stub:
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
        with self._insecure_stub() as stub:
            response = stub.GetTitle(Empty())
            logger.info(response.log)
            if response.body != title:
                message = "Title should be {} but was `{}`".format(title, response.body)
                raise AssertionError(message)

    @keyword
    def page_should_contain_element(self, selector: str):
        """Verifies that current page contains element specified by ``selector``. """
        with self._insecure_stub() as stub:
            response = stub.GetTextContent(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)
            if not response.body:
                message = "No element matching ``{}`` on page".format(selector)
                raise AssertionError(message)

    @keyword
    def page_should_contain_list(self, selector: str):
        """ Verifies that current page contains a list matching ``selector`` """
        self.page_should_contain_element(selector + ">> list")

    class CheckboxState(Enum):
        checked = True
        unchecked = False

    @keyword
    def checkbox_should_be(self, selector: str, expected: CheckboxState):
        """ Verifies that checkbox or radio button ``selector`` is in state ``expected`` """
        with self._insecure_stub() as stub:
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

    @keyword
    def list_selection_should_be(self, selector: str, *expected):
        """ Verifies list ``selector`` has ``expected`` options selected.
            If no ``expected`` selections are given will verify none are selected.
        """
        with self._insecure_stub() as stub:
            response = stub.GetSelectContent(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response)
            raise AssertionError("Assertion not implemented yet")
