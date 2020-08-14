import json
from pathlib import Path
from typing import Dict, Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import (
    AlertAction,
    KeyAction,
    KeyboardInputAction,
    KeyboardModifier,
    MouseButton,
    MouseButtonAction,
    MouseOptionsDict,
    SelectAttribute,
)
from ..utils.time_conversion import timestr_to_millisecs


class Interaction(LibraryComponent):
    @keyword(tags=["Setter", "PageContent"])
    def type_text(
        self, selector: str, text: str, delay: str = "0 ms", clear: bool = True
    ):
        """Types the given ``text`` into the text field found by ``selector``.

        Sends a ``keydown``, ``keypress/input``, and ``keyup`` event for each
        character in the text.

        ``selector`` <str> Selector of the text field. **Required**

        ``text`` <str> Text for the text field. **Required**

        ``delay`` <str> Delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``.
        Example: ``50 ms``

        ``clear`` <bool> Set to false, if the field shall not be cleared before typing.
        Defaults to true.

        See `Fill Text` for direct filling of the full text at once.
        """
        self._type_text(selector, text, delay, clear)

    @keyword(tags=["Setter", "PageContent"])
    def fill_text(self, selector: str, text: str):
        """Clears and fills the given ``text`` into the text field found by ``selector``.

        This method waits for an element matching the ``selector`` to appear,
        waits for actionability checks, focuses the element, fills it and
        triggers an input event after filling.

        If the element matching selector is not an <input>, <textarea> or
        [contenteditable] element, this method throws an error. Note that
        you can pass an empty string as ``text`` to clear the input field.

        ``selector`` <str> Selector of the text field. **Required**

        ``text`` <str> Text for the text field. **Required**

        See `Type Text` for emulating typing text character by character.
        """
        self._fill_text(selector, text)

    @keyword(tags=["Setter", "PageContent"])
    def clear_text(self, selector: str):
        """Clears the text field found by ``selector``.

        ``selector`` <str> Selector of the text field. **Required**

        See `Type Text` for emulating typing text character by character.
        See `Fill Text` for direct filling of the full text at once.

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearText(Request().ClearText(selector=selector))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def type_secret(
        self, selector: str, secret: str, delay: str = "0 ms", clear: bool = True
    ):
        """Types the given ``secret`` into the text field found by ``selector``.

        The difference to `Type Text` is that this keyword does not log the
        text to be written into the text field.

        ``selector`` <str> Selector of the text field. **Required**

        ``secret`` <str> Secret text for the text field. **Required**

        ``delay`` <str> Delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``.
        Example: ``50 ms``

        ``clear`` <bool> Set to false, if the field shall not be cleared before typing.
        Defaults to true.

        See `Type Text` for details.
        """
        self._type_text(selector, secret, delay, clear, log_response=False)

    @keyword(tags=["Setter", "PageContent"])
    def fill_secret(self, selector: str, secret: str):
        """Fills the given ``secret`` into the text field found by ``selector``.

        The difference to `Fill Text` is that this keyword does not log the
        text to be written into the text field.

        ``selector`` <str> Selector of the text field. **Required**

        ``secret`` <str> Secret text for the text field. **Required**

        See `Fill Text` for details.
        """
        self._fill_text(selector, secret, log_response=False)

    @keyword(tags=["Setter", "PageContent"])
    def press_keys(self, selector: str, *keys: str):
        """Types the given key combination into element found by ``selector``.

        ``selector`` <str> Selector of the text field. **Required**

        Supports values like "a, b" which will be automatically typed.
        .
        Also supports identifiers for keys like ``ArrowLeft`` or ``Backspace``.
        Using + to chain combine modifiers with a single keypress
        ``Control+Shift+T`` is supported.

        See playwright's documentation for a more comprehensive list of
        supported input keys.
        [https://github.com/microsoft/playwright/blob/master/docs/api.md#pagepressselector-key-options | Playwright docs for press.]

        Example: 

        | Keyword      | Selector                   | Keys | Keys | Keys | Keys | Keys        | Keys |
        | Press Keys   | //*[@id="username_field"]  |  h   |   e  |  l   |  o   |  ArrowLeft  |  l   |
        """  # noqa
        with self.playwright.grpc_channel() as stub:
            response = stub.Press(Request().PressKeys(selector=selector, key=keys))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def click(self, selector: str):
        """Clicks the element found by ``selector``.

        ``selector`` <str> Selector of the element to click. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Click(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def click_with_options(
        self,
        selector: str,
        button: MouseButton = MouseButton.left,
        click_count: int = 1,
        delay: Optional[str] = None,
        position_x: Optional[int] = None,
        position_y: Optional[int] = None,
        force: bool = False,
        *modifiers: KeyboardModifier,
    ):
        """Simulates mouse click with multiple options on the element found by ``selector``.

        ``selector`` <str> Selector element to click. **Required**

        ``button`` <left|right|middle> Defaults to ``left`` if invalid.

        ``click_count`` <int> Defaults to 1.

        ``delay`` <robot time> Time to wait between mousedown and mouseup in milliseconds.
        Defaults to 0.

        ``position_x`` & ``position_y`` <int> A point to click relative to the
        top-left corner of element padding box.
        If not specified, clicks to some visible point of the element.

        ``force`` <bool> Set to True to skip Playwright's [https://github.com/microsoft/playwright/blob/master/docs/actionability.md | Actionability checks].

        ``*modifiers`` ``<list<"Alt"|"Control"|"Meta"|"Shift">>``
        Modifier keys to press. Ensures that only these modifiers are pressed
        during the click, and then restores current modifiers back.
        If not specified, currently pressed modifiers are used.
        """
        with self.playwright.grpc_channel() as stub:
            options = {"button": button.name, "clickCount": click_count, "force": force}
            if delay:
                options["delay"] = timestr_to_millisecs(delay)
            if position_x and position_y:
                positions: Dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Click Options are: {options_json}")
            response = stub.Click(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json
                )
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def focus(self, selector: str):
        """Moves focus on to the element found by ``selector``.

        ``selector`` <str> Selector of the element. **Required**

        If there's no element matching selector, the method waits until a
        matching element appears in the DOM.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Focus(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def check_checkbox(self, selector: str):
        """Checks the checkbox or selects radio button found by ``selector``.

        ``selector`` <str> Selector of the checkbox. **Required**

        Does nothing if the element is already checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def uncheck_checkbox(self, selector: str):
        """Unchecks the checkbox found by ``selector``.

        ``selector`` <str> Selector of the checkbox. **Required**

        Does nothing if the element is not checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(
                Request().ElementSelector(selector=selector)
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def select_options_by(self, selector: str, attribute: SelectAttribute, *values):
        """Selects options from select element found by ``selector``.

        ``selector`` <str> Selector of the select tag. **Required**

        Matches based on the chosen attribute with list of ``values``.
        Possible attributes to match options by:
        ``attribute`` ``<"value"|"label"|"text"|"index">``

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
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def deselect_options(self, selector: str):
        """Deselects all options from select element found by ``selector``.

        ``selector`` <str> Selector of the select tag. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.DeselectOption(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    def _fill_text(self, selector: str, text: str, log_response: bool = True):
        with self.playwright.grpc_channel() as stub:
            response = stub.FillText(Request().FillText(selector=selector, text=text))
            if log_response:
                logger.debug(response.log)

    def _type_text(
        self,
        selector: str,
        text: str,
        delay: str = "0 ms",
        clear: bool = True,
        log_response: bool = True,
    ):
        with self.playwright.grpc_channel() as stub:
            delay_ms = timestr_to_millisecs(delay)
            response = stub.TypeText(
                Request().TypeText(
                    selector=selector, text=text, delay=int(delay_ms), clear=clear
                )
            )
            if log_response:
                logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent", "EventHandler"])
    def upload_file(self, path: str):
        """ Upload file from ``path`` into next file chooser dialog on page.

        ``path`` <str> Path to file to be uploaded.

        Example use:

            | Upload File |  ${CURDIR}/test_upload_file
            | Click       |  \\#file_chooser

        """
        p = Path(path)
        p.resolve(strict=True)
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFile(Request().FilePath(path=str(p)))
            logger.debug(response.log)

    @keyword(tags=["PageContent", "EventHandler"])
    def handle_alert(self, action: AlertAction, prompt_input: str = ""):
        """ Handle next dialog on page with ``action``. Dialog can be any of alert,
        beforeunload, confirm or prompt.

            ``action`` <accept|dismiss> How to handle the alert. **Required**

            ``prompt_input`` <str> The value to enter into prompt. Only valid if
            ``action`` equals accept. Defaults to empty string.
        """

        with self.playwright.grpc_channel() as stub:
            if prompt_input and action is not AlertAction.accept:
                raise ValueError("prompt_input is only valid if action is 'accept'")
            response = stub.HandleAlert(
                Request().AlertAction(alertAction=action.name, promptInput=prompt_input)
            )
            logger.debug(response.log)

    @keyword(tags=["VirtualMouse", "PageContent"])
    def mouse_button(
        self,
        action: MouseButtonAction,
        x: Optional[float] = None,
        y: Optional[float] = None,
        button: MouseButton = MouseButton.left,
        clickCount: int = 1,
        delay: int = 0,
    ):
        """ Click, hold a mouse button down or release it. Moving the mouse between holding down
        and releasing it for example is possible.

            ``action`` <click|up|down> Determines if it is a mouseclick, holding down a key or releasing it.

            ``x`` <int> and ``y`` <int> Coordinates for a click only. Defaults to None.
            **Required** if action is a click.

            ``button`` <left|right|middle> Defaults to ``left`` if invalid.

            ``clickCount`` <int> Deterine how often shall be clicked. Defaults to 1.

            ``delay`` <int> Delay in ms between the clicks. Can only be set if the action is click.
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {}
            if delay and action is not MouseButtonAction.click:
                raise ValueError("Delay is only valid on a mouse click")
            if action is MouseButtonAction.down or action is MouseButtonAction.up:
                if x or y:
                    raise ValueError(
                        "Coordinates are not valid on MouseAction.up or MouseAction.down"
                    )
                body = {
                    "options": {
                        "button": button.name,
                        "clickCount": clickCount,
                        "delay": delay,
                    }
                }
            else:
                body = {}
                if x:
                    body["x"] = float(x)
                if y:
                    body["y"] = float(y)
                body["options"] = {
                    "button": button.name,
                    "clickCount": clickCount,
                    "delay": delay,
                }

            response = stub.MouseButton(
                Request().MouseButtonOptions(action=action.name, json=json.dumps(body))
            )
            logger.debug(response.log)

    @keyword(tags=["VirtualMouse", "PageContent"])
    def mouse_move(self, x: float, y: float, steps: int = 1):
        """ Instead of selectors command mouse with coordinates.
            The Click commands will leave the virtual mouse on the specified coordinates.

            ``x`` <float> ``y`` <float> are absolute coordinates starting at the top left
            of the page.

            ``steps`` <int> Number of intermediate steps for the mouse event.
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {"x": x, "y": y, "options": {"steps": steps}}
            response = stub.MouseMove(Request().Json(body=json.dumps(body)))
            logger.debug(response.log)

    @keyword(tags=["VirtualKeyboard", "PageContent"])
    def keyboard_key(self, action: KeyAction, key: str):
        """ Press a keyboard key on the virtual keyboard or set a key up or down.

        ``action`` <up|down|press> Determine whether the key should be released,
        hold or pressed. ``down`` or ``up`` are useful for combinations i.e. with Shift.
        **Required**

        ``key`` <str> The key to be pressed. An example of valid keys are:

        ``F1`` - ``F12``, ``Digit0`` - ``Digit9``, ``KeyA``- ``KeyZ``, ``Backquote``, ``Minus``,
        ``Equal``, ``Backslash``, ``Backspace``, ``Tab``, ``Delete``, ``Escape``, ``ArrowDown``,
        ``End``, ``Enter``, ``Home``, ``Insert``, ``PageDown``, ``PageUp``, ``ArrowRight``, ``ArrowUp``
        , etc.

        Useful keys for ``down`` and ``up`` for example are:

        ``Shift``, ``Control``, ``Alt``, ``Meta``, ``ShiftLeft``

        Example excecution:
        | Keyboard Key | press | S         |
        | Keyboard Key | down  | Shift     |
        | Keyboard Key | press | ArrowLeft |
        | Keyboard Key | press | Delete    |
        | Keyboard Key | up    | Shift     |

        Note: Capital letters don't need to be written by the help of Shift. You can type them in directly.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.KeyboardKey(
                Request().KeyboardKeypress(action=action.name, key=key)
            )
            logger.debug(response.log)

    @keyword(tags=["VirtualKeyboard", "PageContent"])
    def keyboard_input(self, action: KeyboardInputAction, input: str, delay=0):
        """ Input text into page with virtual keyboard.

            ``action`` <insertText|type> **Required**

                - ``insertText`` Dispatches only input event, does not emit the keydown, keyup or keypress events.

                - ``type`` Sends a keydown, keypress/input, and keyup event for each character in the text.

            ``input`` <str> The inputstring to be typed. No special keys possible. **Required**

            Note: To press a special key, like Control or ArrowDown, use keyboard.press.
            Modifier keys DO NOT effect these methods. For testing modifier effects use single key
            presses with ``Keyboard Key  press``

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.KeyboardInput(
                Request().KeyboardInputOptions(
                    action=action.name, input=input, delay=delay
                )
            )
            logger.debug(response.log)
