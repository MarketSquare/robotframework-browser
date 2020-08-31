# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from pathlib import Path
from typing import Any, Dict, Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import (
    BoundingBox,
    Coordinates,
    DialogAction,
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

        | # Keyword       Selector                    *Keys
        | Press Keys      //*[@id="username_field"]    h    e   l   o   ArrowLeft   l
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
        clickCount: int = 1,
        delay: Optional[str] = None,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        force: bool = False,
        noWaitAfter: bool = False,
        *modifiers: KeyboardModifier,
    ):
        """Moves the virtual mouse with multiple options on the element found by ``selector``.

        This method hovers over an element matching ``selector`` by performing the following steps:
        - Find an element match matching ``selector``. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set. If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Move` to hover over the center of the element, or the specified ``position``.

        ``selector`` <str> Selector element to click. **Required**

        ``button`` < ``left`` | ``middle`` |  ``right``> The button that shall be used for clicking.

        ``clickCount`` <int> How many time shall be clicked.

        ``delay`` <robot time str> Time to wait between mousedown and mouseup and next click.

        *Caution: be aware that if the delal leats to a total time that exceets the timeout, the keyword fails*

        ``position_x`` & ``position_y`` <float> A point to click relative to the
        top-left corner of element boundingbox. Only positive values within the boundingbox are allowed.
        If not specified, clicks to some visible point of the element.

        *Caution: even with 0, 0 might click a few pixels off from the corner of the boundingbox. Click uses detection to find the first clickable point.*

        ``force`` <bool> Set to True to skip Playwright's [https://github.com/microsoft/playwright/blob/master/docs/actionability.md | Actionability checks].

        ``*modifiers`` < ``Alt`` | ``Control`` | ``Meta`` | ``Shift`` >
        Modifier keys to press. Ensures that only these modifiers are pressed
        during the click, and then restores current modifiers back.
        If not specified, currently pressed modifiers are used.
        """
        with self.playwright.grpc_channel() as stub:
            options = {
                "button": button.name,
                "clickCount": clickCount,
                "force": force,
                "noWaitAfter": noWaitAfter,
            }
            if delay:
                options["delay"] = timestr_to_millisecs(delay)
            # Without the != None 0 being falsy causes issues
            if position_x is not None and position_y is not None:
                positions: Dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Click Options are: {options_json}")
            response = stub.ClickWithOptions(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json
                )
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def hover(
        self,
        selector: str,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        force: bool = False,
        *modifiers: KeyboardModifier,
    ):
        """Simulates mouse click with multiple options on the element found by ``selector``.

        This keyword clicks an element matching ``selector`` by performing the following steps:
        - Find an element matches selector. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set. If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Button` to click in the center of the element, or the specified position.
        - Wait for initiated navigations to either succeed or fail, unless ``noWaitAfter`` option is set.

        ``selector`` <str> Selector element to click. **Required**

        ``button`` < ``left`` | ``right`` | ``middle`` > Defaults to ``left`` if invalid.

        ``click_count`` <int> Defaults to 1.

        ``delay`` <robot time str> Time to wait between mousedown and mouseup.
        Defaults to 0.

        ``position_x`` & ``position_y`` <int> A point to click relative to the
        top-left corner of element boundingbox. Only positive values within the boundingbox are allowed.
        If not specified, clicks to some visible point of the element.

        ``force`` <bool> Set to True to skip Playwright's [https://github.com/microsoft/playwright/blob/master/docs/actionability.md | Actionability checks].

        ``noWaitAfter`` <bool> Actions that initiate navigations are waiting for
        these navigations to happen and for pages to start loading.
        You can opt out of waiting via setting this flag.
        You would only need this option in the exceptional cases such as navigating
        to inaccessible pages. Defaults to ``False``.

        ``*modifiers`` < ``Alt`` | ``Control`` | ``Meta`` | ``Shift`` >
        Modifier keys to press. Ensures that only these modifiers are pressed
        during the click, and then restores current modifiers back.
        If not specified, currently pressed modifiers are used.
        """
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, Any] = {"force": force}
            if position_x and position_y:
                positions: Dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Hover Options are: {options_json}")
            response = stub.Hover(
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
        matching element appears in the DOM. Timeouts after 10 seconds.
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
        ``attribute`` < ``value`` | ``label `` | ``text`` | ``index`` >

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

    @keyword(tags=["Setter", "PageContent"])
    def upload_file(self, path: str):
        """Upload file from ``path`` into next file chooser dialog on page.

        ``path`` <str> Path to file to be uploaded.

        Example use:

        | Upload File    ${CURDIR}/test_upload_file
        | Click          \\#file_chooser

        """
        p = Path(path)
        p.resolve(strict=True)
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFile(Request().FilePath(path=str(p)))
            logger.debug(response.log)

    @keyword(tags=["PageContent"])
    def handle_future_dialogs(self, action: DialogAction, prompt_input: str = ""):
        """Handle next dialog on page with ``action``. Dialog can be any of alert,
        beforeunload, confirm or prompt.

            ``action`` < ``acceppt`` | ``dismiss`` > How to handle the alert. **Required**

            ``prompt_input`` <str> The value to enter into prompt. Only valid if
            ``action`` equals accept. Defaults to empty string.
        """

        with self.playwright.grpc_channel() as stub:
            if prompt_input and action is not DialogAction.accept:
                raise ValueError("prompt_input is only valid if action is 'accept'")
            response = stub.HandleAlert(
                Request().AlertAction(alertAction=action.name, promptInput=prompt_input)
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def mouse_button(
        self,
        action: MouseButtonAction,
        x: Optional[float] = None,
        y: Optional[float] = None,
        button: MouseButton = MouseButton.left,
        clickCount: int = 1,
        delay: int = 0,
    ):
        """Click, hold a mouse button down or release it.

        Moving the mouse between holding down and releasing it for example is possible with `Mouse Move`.

        ``action`` < ``click`` | ``up`` | ``down`` > Determines if it is a mouseclick, holding down a key or releasing it.

        ``x`` <int> and ``y`` <int> Coordinates for a click only. Defaults to None.
        **Required** if action is a click.

        ``button`` < ``left``| ``right`` | ``middle`` > Defaults to ``left`` if invalid.

        ``clickCount`` <int> Deterine how often shall be clicked. Defaults to 1.

        ``delay`` <int> Delay in ms between the mousedown and mouseup event. Can only be set if the action is click.
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {}
            if delay and action is not MouseButtonAction.click:
                raise ValueError("Delay is only valid on 'click' action.")
            if action == MouseButtonAction.click:
                body = {}
                if x and y:
                    body["x"] = float(x)
                    body["y"] = float(y)
                else:
                    raise ValueError(
                        f"`Mouse Button    Click` requires that x and y are set! x: {x}, y: {y}"
                    )
                body["options"] = {
                    "button": button.name,
                    "clickCount": clickCount,
                    "delay": delay,
                }
            else:
                if x and y:
                    self.mouse_move(x, y)
                else:
                    logger.info(
                        f"No coordinates where set. Action will appear at current position. x: {x}, y {y}"
                    )
                body = {
                    "options": {
                        "button": button.name,
                        "clickCount": clickCount,
                        "delay": delay,
                    }
                }

            response = stub.MouseButton(
                Request().MouseButtonOptions(action=action.name, json=json.dumps(body))
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def drag_and_drop(self, selector_from: str, selector_to: str, steps: int = 1):
        """Executes a Drag&Drop operation from the element selected by ``selector_from``
        to the element selected by ``selector_to``.

        First it moves the mouse to the start-point,
        then presses the left mouse button,
        then moves to the end-point in specified number of steps,
        then releases the mouse button.

        Start- and end-point are defined by the center of the elements boundingbox.

        ``selector_from``: <float> identifies the element, which center is the start-point. **Required**

        ``selector_to``: <float> identifies the element, which center is the end-point. **Required**

        ``steps``: <int> defines how many intermediate mouse move events are sent.
        """
        from_bbox = self.library.get_boundingbox(selector_from)
        from_xy = self._center_of_boundingbox(from_bbox)
        to_bbox = self.library.get_boundingbox(selector_to)
        to_xy = self._center_of_boundingbox(to_bbox)
        self.mouse_button(MouseButtonAction.down, **from_xy)
        self.mouse_move(**to_xy, steps=steps)
        self.mouse_button(MouseButtonAction.up)

    @keyword(tags=["Setter", "PageContent"])
    def drag_and_drop_by_coordinates(
        self, from_x: float, from_y: float, to_x: float, to_y: float, steps: int = 1
    ):
        """Executes a Drag&Drop operation from a coordinate to another coordinate.

        First it moves the mouse to the start-point,
        then presses the left mouse button,
        then moves to the end-point in specified number of steps,
        then releases the mouse button.

        Start- and end-point are defined by ``x`` and ``y`` coordinates relative to
        the top left corner of the pages viewport.

        ``from_x`` & ``from_y``: <float> identify the the start-point. **Required**

        ``to_x`` & ``to_y``: <float> identify the the end-point. **Required**

        ``steps``: <int> defines how many intermediate mouse move events are sent.
        """
        self.mouse_button(MouseButtonAction.down, x=from_x, y=from_y)
        self.mouse_move(x=to_x, y=to_y, steps=steps)
        self.mouse_button(MouseButtonAction.up)

    @staticmethod
    def _center_of_boundingbox(boundingbox: BoundingBox) -> Coordinates:
        center = Coordinates()
        center["x"] = boundingbox["x"] + (boundingbox["width"] / 2)
        center["y"] = boundingbox["y"] + (boundingbox["height"] / 2)
        return center

    @keyword(tags=["Setter", "PageContent"])
    def mouse_move(self, x: float, y: float, steps: int = 1):
        """Instead of selectors command mouse with coordinates.
        The Click commands will leave the virtual mouse on the specified coordinates.

        ``x`` <float> ``y`` <float> are absolute coordinates starting at the top left
        of the page.

        ``steps`` <int> Number of intermediate steps for the mouse event.
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {"x": x, "y": y, "options": {"steps": steps}}
            logger.info(f"Moving mouse to x: {x}, y: {y} coordinates.")
            response = stub.MouseMove(Request().Json(body=json.dumps(body)))
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def keyboard_key(self, action: KeyAction, key: str):
        """Press a keyboard key on the virtual keyboard or set a key up or down.

        ``action`` < ``up`` | ``down`` | ``press`` > Determine whether the key should be released,
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
        | Keyboard Key    press    S
        | Keyboard Key    down     Shift
        | Keyboard Key    press    ArrowLeft
        | Keyboard Key    press    Delete
        | Keyboard Key    up       Shift

        Note: Capital letters don't need to be written by the help of Shift. You can type them in directly.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.KeyboardKey(
                Request().KeyboardKeypress(action=action.name, key=key)
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent"])
    def keyboard_input(self, action: KeyboardInputAction, input: str, delay=0):
        """Input text into page with virtual keyboard.

        ``action`` < ``insertText`` | ``type`` > **Required**

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
