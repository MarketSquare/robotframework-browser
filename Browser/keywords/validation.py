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

        Optionally verifies that the element contains ``text``.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetTextContent(Request().ElementSelector(selector=selector))
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
