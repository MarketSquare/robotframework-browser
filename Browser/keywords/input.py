from robot.api import logger  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request


class Input:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def input_text(self, selector: str, text: str, type=False):
        """ Inputs the given ``text`` into the text field identified by ``selector``

            By default text is inputted via filling (instantly), only triggering the
            input event. By toggling the ``type`` boolean text will be typed into the
            field instead. Typing triggers keydown, keypress/input and keyup events
            for every character of input.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.InputText(
                Request().inputText(input=text, selector=selector, type=type)
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
                stub.InputText(Request().inputText(input=password, selector=selector))
            finally:
                BuiltIn().set_log_level(previous_level)

    @keyword
    def press_keys(self, selector: str, *keys: str):
        """ Inputs given ``key``s into element specifid by selector.

            Supports values like "a, b" which will be automatically inputted.
            Also supports identifiers for keys like ``ArrowLeft`` or ``Backspace``.
            Using + to chain combine modifiers with a single keypress
            ``Control+Shift+T`` is supported.

            See playwright's documentation for a more comprehensive list of
            supported input keys.
            [https://github.com/microsoft/playwright/blob/master/docs/api.md#pagepressselector-key-options | Playwright docs for press.]
        """  # noqa
        with self.playwright.grpc_channel() as stub:
            response = stub.Press(Request.press(selector=selector, key=keys))
            logger.info(response.log)

    @keyword
    def click(self, selector: str):
        """ Clicks element identified by ``selector``. """
        with self.playwright.grpc_channel() as stub:
            response = stub.Click(Request().selector(selector=selector))
            logger.info(response.log)

    @keyword
    def check_checkbox(self, selector: str):
        """ Checks the checkbox identified by ``selector``.
            If already checked does nothing
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(Request().selector(selector=selector))
            logger.info(response.log)

    @keyword
    def uncheck_checkbox(self, selector: str):
        """ Unchecks the checkbox identified by ``selector``.
            If not checked does nothing
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(Request().selector(selector=selector))
            logger.info(response.log)
