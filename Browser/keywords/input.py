import json
from enum import Enum, auto

from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import keyword  # type: ignore
from typing import Optional, Dict, Any

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils.time_conversion import timestr_to_millisecs


class MouseButton(Enum):
    left = auto()
    middle = auto()
    right = auto()


class KeyboardModifier(Enum):
    Alt = auto()
    Control = auto()
    Meta = auto()
    Shift = auto()


class SelectAttribute(Enum):
    value = auto()
    label = auto()
    text = label
    index = auto()


class Input(LibraryComponent):
    @keyword
    def type_text(
        self, selector: str, text: str, delay: str = "0 ms", clear: bool = True
    ):
        """Types the given ``text`` into the text field found by ``selector``.

        Sends a ``keydown``, ``keypress/input``, and ``keyup`` event for each
        character in the text.

        ``delay``: delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide.
        Example: ``50 ms``

        See `Fill Text` for direct filling of the full text at once.
        """
        with self.playwright.grpc_channel() as stub:
            delay_ms = timestr_to_millisecs(delay)
            response = stub.TypeText(
                Request().TypeText(
                    selector=selector, text=text, delay=int(delay_ms), clear=clear
                )
            )
            self.info(response.log)

    @keyword
    def fill_text(self, selector: str, text: str):
        """Clears and fills the given ``text`` into the text field found by ``selector``.

        This method waits for an element matching the ``selector`` to appear,
        waits for actionability checks, focuses the element, fills it and
        triggers an input event after filling.

        If the element matching selector is not an <input>, <textarea> or
        [contenteditable] element, this method throws an error. Note that
        you can pass an empty string as ``text`` to clear the input field.

        See `Type Text` for emulating typing text character by character.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.FillText(Request().FillText(selector=selector, text=text))
            self.info(response.log)

    @keyword
    def clear_text(self, selector: str):
        """Clears the text field found by ``selector``.

        See `Type Text` for emulating typing text character by character.
        See `Fill Text` for direct filling of the full text at once.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearText(Request().ClearText(selector=selector))
            self.info(response.log)

    @keyword
    def type_secret(
        self, selector: str, secret: str, delay: str = "0 ms", clear: bool = True
    ):
        """Types the given ``secret`` into the text field found by ``selector``.

        The difference to `Type Text` is that this keyword does not log the
        text to be written into the text field.

        See `Type Text` for details.
        """
        previous_level = BuiltIn().set_log_level("NONE")
        try:
            self.type_text(selector, secret, delay, clear)
        finally:
            BuiltIn().set_log_level(previous_level)

    @keyword
    def fill_secret(self, selector: str, secret: str):
        """Fills the given ``secret`` into the text field found by ``selector``.

        The difference to `Fill Text` is that this keyword does not log the
        text to be written into the text field.

        See `Fill Text` for details.
        """
        previous_level = BuiltIn().set_log_level("NONE")
        try:
            self.fill_text(selector, secret)
        finally:
            BuiltIn().set_log_level(previous_level)

    @keyword
    def press_keys(self, selector: str, *keys: str):
        """Types the given key combination into element found by ``selector``.

        Supports values like "a, b" which will be automatically typed.
        .
        Also supports identifiers for keys like ``ArrowLeft`` or ``Backspace``.
        Using + to chain combine modifiers with a single keypress
        ``Control+Shift+T`` is supported.

        See playwright's documentation for a more comprehensive list of
        supported input keys.
        [https://github.com/microsoft/playwright/blob/master/docs/api.md#pagepressselector-key-options | Playwright docs for press.]
        """  # noqa
        with self.playwright.grpc_channel() as stub:
            response = stub.Press(Request().PressKeys(selector=selector, key=keys))
            self.info(response.log)

    @keyword
    def click(self, selector: str):
        """Clicks the element found by ``selector``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.Click(Request().ElementSelector(selector=selector))
            self.info(response.log)

    @keyword
    def click_with_options(
        self,
        selector: str,
        button: MouseButton = MouseButton.left,
        click_count: int = 1,
        delay: Optional[str] = None,
        position_x: Optional[int] = None,
        position_y: Optional[int] = None,
        *modifiers: KeyboardModifier,
    ):
        """Simulates mouse click on the element found by ``selector``.

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
            options = {"button": button.name, "clickCount": click_count}
            if delay:
                options["delay"] = timestr_to_millisecs(delay)
            if position_x and position_y:
                positions: Dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            self.debug(f"Click Options are: {options_json}")
            response = stub.Click(
                Request().ElementSelectorOptions(
                    selector=selector, options=options_json
                )
            )
            self.info(response.log)

    @keyword
    def focus(self, selector: str):
        """Moves focus on to the element found by ``selector``.

        If there's no element matching selector, the method waits until a
        matching element appears in the DOM.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Focus(Request().ElementSelector(selector=selector))
            self.info(response.log)

    @keyword
    def execute_javascript_on_page(self, script: str) -> Any:
        """Executes given javascript on the page.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascriptOnPage(
                Request().JavascriptCode(script=script)
            )
            self.info(response.log)
            return json.loads(response.result)

    @keyword
    def check_checkbox(self, selector: str):
        """Checks the checkbox or selects radio button found by ``selector``.

        Does nothing if the element is already checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(Request().ElementSelector(selector=selector))
            self.info(response.log)

    @keyword
    def uncheck_checkbox(self, selector: str):
        """Unchecks the checkbox found by ``selector``.

        Does nothing if the element is not checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(
                Request().ElementSelector(selector=selector)
            )
            self.info(response.log)

    @keyword
    def select_options_by(self, attribute: SelectAttribute, selector: str, *values):
        """Selects options from select element found by ``selector``.

        Matches based on the chosen attribute with list of ``values``.
        Possible attributes to match options by:
        ``attribute``: ``<"value"|"label"|"text"|"index">``

        If no values to select are passed will deselect options in element.
        """
        matchers = ""
        if not values or len(values) == 1 and not values[0]:
            self.deselect_options(selector)
            return

        if attribute is SelectAttribute.value:
            matchers = json.dumps([{"value": s} for s in values])
        elif attribute is SelectAttribute.label:
            matchers = json.dumps([{"label": s} for s in values])
        elif attribute is SelectAttribute.index:
            matchers = json.dumps([{"index": int(s)} for s in values])
        with self.playwright.grpc_channel() as stub:
            response = stub.SelectOption(
                Request().SelectElementSelector(selector=selector, matcherJson=matchers)
            )
            self.info(response.log)

    @keyword
    def deselect_options(self, selector: str):
        """Deselects all options from select element found by ``selector``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.DeselectOption(Request().ElementSelector(selector=selector))
            self.info(response.log)
