import json

from robot.api import logger  # type: ignore
from robot.utils.robottime import timestr_to_secs  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import keyword  # type: ignore
from typing import Optional

from ..generated.playwright_pb2 import Request


class Input:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def input_text(self, selector: str, text: str, type=False):
        """ DEPRECATED Inputs the given ``text`` into the text field identified by ``selector``

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
    def type_text(
            self, selector: str, text: str, delay: str = "0 ms",
            clear: bool = True
    ):
        """ Types the given ``text`` into the text field identified by ``selector``.

        Sends a ``keydown``, ``keypress/input``, and ``keyup`` event for each
        character in the text.

        ``delay``: delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide.
        Example: ``50 ms``

        See `Fill Text` for direct filling of the full text at once.
        """
        with self.playwright.grpc_channel() as stub:
            delay_ms = timestr_to_secs(delay) * 1000
            response = stub.TypeText(
                Request().typeText(
                    selector=selector,
                    text=text,
                    delay=int(delay_ms),
                    clear=clear
                )
            )
            logger.info(response.log)

    @keyword
    def fill_text(self, selector: str, text: str):
        """ Clears and Fills the given ``text`` into the text field identified by ``selector``.

        This method waits for an element matching selector, waits for
        actionability checks, focuses the element, fills it and triggers an
        input event after filling. If the element matching selector is not
        an <input>, <textarea> or [contenteditable] element, this method
        throws an error. Note that you can pass an empty string to clear
        the input field.

        See `Type Text` for keyboard like typing of single characters.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.FillText(
                Request().fillText(selector=selector, text=text))
            logger.info(response.log)

    @keyword
    def clear_text(self, selector: str):
        """ Clears the text field identified by ``selector``.

        See `Type Text` for keyboard like typing of single characters.
        See `Fill Text` for direct filling of the full text at once.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearText(Request().clearText(selector=selector))
            logger.info(response.log)

    @keyword
    def type_secret(
            self,
            selector: str,
            secret: str,
            delay: str = "0 ms",
            clear: bool = True
    ):
        """ Types the given ``secret`` into the text field identified by ``selector`` without logging.

        See `Type Text` for details.
        """
        previous_level = BuiltIn().set_log_level("NONE")
        try:
            self.type_text(selector, secret, delay, clear)
        finally:
            BuiltIn().set_log_level(previous_level)

    @keyword
    def fill_secret(self, selector: str, secret: str):
        """ Fills the given ``secret`` into the text field identified by ``selector`` without logging.

        See `Fill Text` for details.
        """
        previous_level = BuiltIn().set_log_level("NONE")
        try:
            self.fill_text(selector, secret)
        finally:
            BuiltIn().set_log_level(previous_level)

    @keyword
    def input_password(self, selector: str, password: str):
        """ DEPRECATED Types the given ``password`` into the field identified by ``selector``
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
                    Request().inputText(input=password, selector=selector))
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
            response = stub.Press(Request().press(selector=selector, key=keys))
            logger.info(response.log)

    @keyword
    def click(self, selector: str):
        """ Clicks element identified by ``selector``. """
        with self.playwright.grpc_channel() as stub:
            response = stub.Click(Request().selector(selector=selector))
            logger.info(response.log)

    @keyword
    def click_with_options(self,
                           selector: str,
                           button: str,
                           click_count: Optional[int] = None,
                           delay: Optional[str] = None,
                           position_x: Optional[int] = None,
                           position_y: Optional[int] = None,
                           *modifiers: str
                           ):
        """ Clicks element identified by ``selector``. 
        
        ``button``: ``<"left"|"right"|"middle">`` Defaults to ``left`` if invalid.

        ``clickCount``: <int> defaults to 1.

        ``delay``: <robot time> Time to wait between mousedown and mouseup.
        Defaults to 0.

        ``position_x`` & ``position_y``: <int> A point to click relative to the
        top-left corner of element padding box.
        If not specified, clicks to some visible point of the element.

        ``*modifiers``: ``<list<"Alt"|"Control"|"Meta"|"Shift">>``
        Modifier keys to press. Ensures that only these modifiers are pressed
        during the click, and then restores current modifiers back.
        If not specified, currently pressed modifiers are used.
        """
        with self.playwright.grpc_channel() as stub:
            options = dict()
            if button.lower() in ["left", "middle", "right"]:
                options["button"] = button.lower()
            if click_count:
                options["clickCount"] = int(click_count)
            if delay:
                options["delay"] = int(timestr_to_secs(delay) * 1000)
            if position_x and position_y:
                options["position"] = dict()
                options["position"]["x"] = int(position_x)
                options["position"]["y"] = int(position_y)
            if modifiers:
                options["modifiers"] = modifiers
            options_json = json.dumps(options)
            logger.debug(f"Click Options are: {options_json}")
            response = stub.Click(
                Request().selectorOptions(
                    selector=selector, options=options_json))
            logger.info(response.log)

    @keyword
    def focus(self, selector: str):
        """ This method fetches an element with selector and focuses it.

        If there's no element matching selector, the method waits until a
        matching element appears in the DOM. """
        with self.playwright.grpc_channel() as stub:
            response = stub.Focus(Request().selector(selector=selector))
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
            response = stub.UncheckCheckbox(
                Request().selector(selector=selector))
            logger.info(response.log)
