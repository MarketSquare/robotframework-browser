from typing import Callable, ContextManager

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.generated.playwright_pb2_grpc import PlaywrightStub
import Browser.generated.playwright_pb2 as playwright_pb2


class Input:
    def __init__(self, insecure_stub: Callable[[], ContextManager[PlaywrightStub]]):
        self._insecure_stub = insecure_stub

    # Input keywords
    @keyword
    def input_text(self, selector: str, text: str):
        """ Types the given ``text`` into the text field identified by ``selector`` """
        with self._insecure_stub() as stub:
            response = stub.InputText(
                playwright_pb2.inputTextRequest(input=text, selector=selector)
            )
            logger.info(response.log)

    @keyword
    def click_button(self, selector: str):
        """ Clicks the button identified by ``selector``. """
        with self._insecure_stub() as stub:
            response = stub.ClickButton(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)

    # TODO: Should this be select_checkbox for consistency with SL or check_checkbox
    # for clarity and PW consistency?
    @keyword
    def check_checkbox(self, selector: str):
        """ Checks the checkbox or selects radio identified by ``selector``.
            If already checked does nothing
        """
        with self._insecure_stub() as stub:
            response = stub.CheckCheckbox(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)

    @keyword
    def uncheck_checkbox(self, selector: str):
        """ Unchecks the checkbox identified by ``selector``.
            If not checked does nothing
        """
        with self._insecure_stub() as stub:
            response = stub.UncheckCheckbox(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)

    @keyword
    def select_from_list_by_value(self, selector: str, *values):
        """Toggles options from selection list ``selector`` by ``values``.
        """
        with self._insecure_stub() as stub:
            response = stub.SelectOption(
                playwright_pb2.selectOptionRequest(selector=selector, matcher=values)
            )
            logger.info(response.log)

    @keyword
    def select_from_list_by_label(self, selector: str, *labels):
        """Toggles options from selection list ``selector`` by ``labels``.
        """
        matchers = ["{ label: " + s + "}" for s in labels]
        with self._insecure_stub() as stub:
            response = stub.SelectOption(
                playwright_pb2.selectOptionRequest(selector=selector, matcher=matchers)
            )
            logger.info(response.log)
