from robot.api import logger  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated import playwright_pb2


class Input:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def input_text(self, selector: str, text: str):
        """ Types the given ``text`` into the text field identified by ``selector`` """
        with self.playwright.grpc_channel() as stub:
            response = stub.InputText(
                playwright_pb2.inputTextRequest(input=text, selector=selector)
            )
            logger.info(response.log)

    @keyword
    def input_password(self, selector: str, password: str):
        """ Types the given ``password`` into the field identified by ``selector``
            Disables logging to avoid leaking sensitive information.
        Difference compared to `Input Text` is that this keyword does not
        log the given password on the INFO level. Notice that if you use
        the keyword like
        | Input Password | password_field | password |
        the password is shown as a normal keyword argument. A way to avoid
        that is using variables like
        | Input Password | password_field | ${PASSWORD} |
        Please notice that Robot Framework logs all arguments using
        the TRACE level and tests must not be executed using level below
        DEBUG if the password should not be logged in any format.
        """
        with self.playwright.grpc_channel() as stub:
            try:
                # Should prevent logging in case of failure keywords
                previous_level = BuiltIn().set_log_level("NONE")
                stub.InputText(
                    playwright_pb2.inputTextRequest(input=password, selector=selector)
                )
            finally:
                BuiltIn().set_log_level(previous_level)

    @keyword
    def click_button(self, selector: str):
        """ Clicks the button identified by ``selector``. """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClickButton(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)

    # TODO: Should this be select_checkbox for consistency with SL or check_checkbox
    # for clarity and PW consistency?
    @keyword
    def check_checkbox(self, selector: str):
        """ Checks the checkbox identified by ``selector``.
            If already checked does nothing
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)

    @keyword
    def uncheck_checkbox(self, selector: str):
        """ Unchecks the checkbox identified by ``selector``.
            If not checked does nothing
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(
                playwright_pb2.selectorRequest(selector=selector)
            )
            logger.info(response.log)
