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
from datetime import timedelta
from time import sleep
from typing import Any, Dict, Optional

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    exec_scroll_function,
    get_abs_scroll_coordinates,
    get_rel_scroll_coordinates,
    keyword,
    locals_to_params,
    logger,
)
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
    ScrollBehavior,
    SelectAttribute,
)


class Interaction(LibraryComponent):
    @keyword(tags=("Setter", "PageContent"))
    def type_text(
        self,
        selector: str,
        txt: str,
        delay: timedelta = timedelta(seconds=0),
        clear: bool = True,
    ):
        """Types the given ``txt`` into the text field found by ``selector``.

        Sends a ``keydown``, ``keypress/input``, and ``keyup`` event for each
        character in the text.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        ``txt`` Text for the text field.

        ``delay`` Delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``.
        Example: ``50 ms``

        ``clear`` Set to false, if the field shall not be cleared before typing.
        Defaults to true.

        See `Fill Text` for direct filling of the full text at once.
        """
        logger.info(f"Types the text '{txt}' in the given field.")
        self._type_text(selector, txt, delay, clear)

    @keyword(tags=("Setter", "PageContent"))
    def fill_text(self, selector: str, txt: str):
        """Clears and fills the given ``text`` into the text field found by ``selector``.

        This method waits for an element matching the ``selector`` to appear,
        waits for actionability checks, focuses the element, fills it and
        triggers an input event after filling.

        If the element matching selector is not an <input>, <textarea> or
        [contenteditable] element, this method throws an error. Note that
        you can pass an empty string as ``text`` to clear the input field.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        ``txt`` Text for the text field.

        See `Type Text` for emulating typing text character by character.
        """
        logger.info(f"Fills the text '{txt}' in the given field.")
        self._fill_text(selector, txt)

    @keyword(tags=("Setter", "PageContent"))
    def clear_text(self, selector: str):
        """Clears the text field found by ``selector``.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        See `Type Text` for emulating typing text character by character.
        See `Fill Text` for direct filling of the full text at once.

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearText(Request().ClearText(selector=selector))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def type_secret(
        self,
        selector: str,
        secret: str,
        delay: timedelta = timedelta(seconds=0),
        clear: bool = True,
    ):
        """Types the given secret from ``variable_name`` into the text field
        found by ``selector``.

        This keyword does not log secret in Robot Framework logs.
        If ``enable_playwright_debug`` is enabled in the library
        import, secret will be always visible as plain text in the playwright debug
        logs, regardless of the Robot Framework log level.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        ``secret`` Environment variable name with % prefix or a local
        variable with $ prefix that has the secret text value.
        Variable names can be used with and without curly braces.

        Example:
        ``$Password`` and ``${Password}`` resolve the robot framework variable.
        ``%ENV_PWD`` and ``%{ENV_PWD}`` resolve to the environment variable ``ENV_PWD``.

        ``delay`` Delay between the single key strokes. It may be either a
        number or a Robot Framework time string. Time strings are fully
        explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``.
        Example: ``50 ms``

        ``clear`` Set to false, if the field shall not be cleared before typing.
        Defaults to true.

        See `Type Text` for details.
        """
        originals = self._get_original_values(locals())
        secret = self.resolve_secret(
            secret, originals.get("secret") or secret, "secret"
        )
        self._type_text(selector, secret, delay, clear, log_response=False)

    def _get_original_values(self, local_args: Dict[str, Any]) -> Dict[str, Any]:
        originals = locals_to_params(local_args)
        if not self.library.current_arguments:
            return originals
        named_args = False
        for idx, val in enumerate(self.library.current_arguments):
            if idx > len(originals):
                break
            if "=" in val and not named_args:
                named_args = val.split("=", 1)[0] in originals
            if named_args:
                arg_name, arg_value = val.split("=", 1)
                originals[arg_name] = arg_value
            else:
                originals[list(originals.keys())[idx]] = val
        return originals

    @keyword(tags=("Setter", "PageContent"))
    def fill_secret(self, selector: str, secret: str):
        """Fills the given secret from ``variable_name`` into the
        text field found by ``selector``.

        This keyword does not log secret in Robot Framework logs, when
        keywords resolves the ``secret`` variable internally. When
        ``secret`` variable is prefixed with `$`, without the curly braces,
         library will resolve the corresponding Robot Framework variable.
         If ``secret`` variable is prefixed with `%`, library will resolve
         corresponding environment variable. Example `$Password`` will
         resolve to ``${Password}`` Robot Framework variable. Also
         ``%ENV_PWD``will resolve to ``%{ENV_PWD}`` environment variable.
         Using normal Robt Framework variables or plain text will also work,
         but then library can not prevent Robot Framework leaking the secrets
         in the output files. Also library will log a warning if library
         can not resolve the secret internally.

        If ``enable_playwright_debug`` is enabled in the library import,
        secret will be always visible as plain text in the playwright debug
        logs, regardless of the Robot Framework log level.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        See `Fill Text` for other details.
        """
        originals = self._get_original_values(locals())
        secret = self.resolve_secret(
            secret, originals.get("secret") or secret, "secret"
        )
        self._fill_text(selector, secret, log_response=False)

    @keyword(tags=("Setter", "PageContent"))
    def press_keys(self, selector: str, *keys: str):
        """Types the given key combination into element found by ``selector``.

        ``selector`` Selector of the text field.
        See the `Finding elements` section for details about the selectors.

        Supports values like "a, b" which will be automatically typed.
        .
        Also supports identifiers for keys like ``ArrowLeft`` or ``Backspace``.
        Using + to chain combine modifiers with a single keypress
        ``Control+Shift+T`` is supported.

        See playwright's documentation for a more comprehensive list of
        supported input keys.
        [https://playwright.dev/docs/api/class-page#pagepressselector-key-options | Playwright docs for press.]

        Example:

        | # Keyword       Selector                    *Keys
        | Press Keys      //*[@id="username_field"]    h    e   l   o   ArrowLeft   l
        """  # noqa
        with self.playwright.grpc_channel() as stub:
            response = stub.Press(Request().PressKeys(selector=selector, key=keys))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def click(
        self,
        selector: str,
        button: MouseButton = MouseButton.left,
        clickCount: int = 1,
        delay: Optional[timedelta] = None,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        force: bool = False,
        noWaitAfter: bool = False,
        *modifiers: KeyboardModifier,
    ):
        """Simulates mouse click on the element found by ``selector``.

        This keyword clicks an element matching ``selector`` by performing the following steps:
        - Find an element matches selector. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set. If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Button` to click in the center of the element, or the specified position.
        - Wait for initiated navigation to either succeed or fail, unless ``noWaitAfter`` option is set.

        ``selector`` Selector element to click.
        See the `Finding elements` section for details about the selectors.

        ``button`` Defaults to ``left`` if invalid.

        ``clickCount`` Defaults to 1.

        ``delay`` Time to wait between mouse-down and mouse-up.
        Defaults to 0.

        ``position_x`` & ``position_y`` A point to click relative to the
        top-left corner of element bounding-box. Only positive values within the bounding-box are allowed.
        If not specified, clicks to some visible point of the element.

        ``force`` Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks].

        ``noWaitAfter`` Actions that initiate navigation, are waiting for
        these navigation to happen and for pages to start loading.
        You can opt out of waiting via setting this flag.
        You would only need this option in the exceptional cases such as navigating
        to inaccessible pages. Defaults to ``False``.

        ``*modifiers``
        Modifier keys to press. Ensures that only these modifiers are pressed
        during the click, and then restores current modifiers back.
        If not specified, currently pressed modifiers are used.
        """
        if self.library.presenter_mode:
            self.hover(selector)
            self.library.highlight_elements(selector, duration=timedelta(seconds=2))
            sleep(2)
        with self.playwright.grpc_channel() as stub:
            options = {
                "button": button.name,
                "clickCount": clickCount,
                "force": force,
                "noWaitAfter": noWaitAfter,
            }
            if delay:
                options["delay"] = self.get_timeout(delay)
            # Without the != None 0 being falsy causes issues
            if position_x is not None and position_y is not None:
                positions: Dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Click options are: {options_json}")
            response = stub.Click(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json
                )
            )
            logger.debug(response.log)

    @keyword(tags=("PageContent",))
    def record_selector(self):
        """
        Record the selector that is under mouse.
        Focus on the page and move mouse over the element you want to select.
        Press 's' to store the elements selector.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.RecordSelector(Request.Empty())
            selector_repr = response.result.replace("#", "\\#")
            logger.info(f"Selector: {selector_repr}")
            return json.loads(response.result)

    @keyword(tags=("Setter", "PageContent"))
    def hover(
        self,
        selector: str,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        force: bool = False,
        *modifiers: KeyboardModifier,
    ):
        """Moves the virtual mouse and scrolls to the element found by ``selector``.

        This method hovers over an element matching ``selector`` by performing the following steps:
        - Find an element match matching ``selector``. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set. If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Move` to hover over the center of the element, or the specified ``position``.

        ``selector`` Selector element to hover.
        See the `Finding elements` section for details about the selectors.

        ``position_x`` & ``position_y`` A point to hover relative to the top-left corner of element bounding box.
        If not specified, hovers over some visible point of the element.
        Only positive values within the bounding-box are allowed.

        ``force`` Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks].

        ``*modifiers`` Modifier keys to press. Ensures that only these modifiers are
        pressed during the hover, and then restores current modifiers back.
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

    @keyword(tags=("Setter", "PageContent"))
    def focus(self, selector: str):
        """Moves focus on to the element found by ``selector``.

        ``selector`` Selector of the element.
        See the `Finding elements` section for details about the selectors.

        If there's no element matching selector, the method waits until a
        matching element appears in the DOM. Timeouts after 10 seconds.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Focus(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def scroll_to(
        self,
        selector: Optional[str] = None,
        vertical: str = "top",
        horizontal: str = "left",
        behavior: ScrollBehavior = ScrollBehavior.auto,
    ):
        """Scrolls an element or the page to an absolute position based on given coordinates.

        ``selector`` Selector of the element. If the selector is ``${None}`` or ``${Empty}``
        the page itself is scrolled. To ensure an element is in view use `Hover` instead.
        See the `Finding elements` section for details about the selectors.

        ``vertical`` defines where to scroll vertically.
        It can be a positive number, like ``300``.
        It can be a percentage value of the absolute scrollable size, like ``50%``.
        It can be a string defining that top or the bottom of the scroll area. < ``top`` | ``bottom`` >
        _Be aware that some pages do lazy loading and load more content once you scroll down._
        Bottom defines the current known bottom coordinate.

        ``horizontal`` defines where to scroll horizontally.
        Works same as vertical but defines < ``left`` | ``right`` > as start and end.

        ``behavior`` defines whether the scroll happens directly or it scrolls smoothly.
        """
        scroll_size = self.library.get_scroll_size(selector)
        scroll_width = scroll_size["width"]
        scroll_height = scroll_size["height"]
        client_size = self.library.get_client_size(selector)
        client_width = client_size["width"]
        client_height = client_size["height"]
        vertical_px = get_abs_scroll_coordinates(
            vertical, scroll_height - client_height, "top", "bottom"
        )
        horizontal_px = get_abs_scroll_coordinates(
            horizontal, scroll_width - client_width, "left", "right"
        )
        exec_scroll_function(
            self,
            f'scrollTo({{"left": {horizontal_px}, "top": {vertical_px}, "behavior": "{behavior.name}"}})',
            selector,
        )

    @keyword(tags=("Setter", "PageContent"))
    def scroll_by(
        self,
        selector: Optional[str] = None,
        vertical: str = "height",
        horizontal: str = "0",
        behavior: ScrollBehavior = ScrollBehavior.auto,
    ):
        """Scrolls an element or the page relative from current position by the given values.

        ``selector`` Selector of the element. If the selector is ``${None}`` or ``${Empty}``
        the page itself is scrolled. To ensure an element is in view use `Hover` instead.
        See the `Finding elements` section for details about the selectors.

        ``vertical`` defines how far and in which direction to scroll vertically.
        It can be a positive or negative number. Positive scrolls down, like ``50``, negative scrolls up, like ``-50``.
        It can be a percentage value of the absolute scrollable size, like ``9.95%`` or negative like ``-10%``.
        It can be the string ``height`` to defining to scroll exactly one visible height down or up with ``-height``.
        _Be aware that some pages do lazy loading and load more content once you scroll down._
        The percentage of the current scrollable height is used and may change.

        ``horizontal`` defines where to scroll horizontally.
        Works same as vertical but defines positive values for right and negative values for left.
        ``width`` defines to scroll exactly one visible range to the right.

        ``behavior`` defines whether the scroll happens directly or it scrolls smoothly.
        """
        scroll_size = self.library.get_scroll_size(selector)
        scroll_width = scroll_size["width"]
        scroll_height = scroll_size["height"]
        client_size = self.library.get_client_size(selector)
        client_width = client_size["width"]
        client_height = client_size["height"]
        vertical_px = get_rel_scroll_coordinates(
            vertical, scroll_height - client_height, client_height, "height"
        )
        horizontal_px = get_rel_scroll_coordinates(
            horizontal, scroll_width - client_width, client_width, "width"
        )
        exec_scroll_function(
            self,
            f'scrollBy({{"left": {horizontal_px}, "top": {vertical_px}, "behavior": "{behavior.name}"}})',
            selector,
        )

    @keyword(tags=("Setter", "PageContent"))
    def check_checkbox(self, selector: str):
        """Checks the checkbox or selects radio button found by ``selector``.

        ``selector`` Selector of the checkbox.
        See the `Finding elements` section for details about the selectors.

        Does nothing if the element is already checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def uncheck_checkbox(self, selector: str):
        """Unchecks the checkbox found by ``selector``.

        ``selector`` Selector of the checkbox.
        See the `Finding elements` section for details about the selectors.

        Does nothing if the element is not checked/selected.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(
                Request().ElementSelector(selector=selector)
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def select_options_by(self, selector: str, attribute: SelectAttribute, *values):
        """Selects options from select element found by ``selector``.

        ``selector`` Selector of the select tag.
        See the `Finding elements` section for details about the selectors.

        Matches based on the chosen attribute with list of ``values``.
        Possible attributes to match options by:
        ``attribute``

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

    @keyword(tags=("Setter", "PageContent"))
    def deselect_options(self, selector: str):
        """Deselects all options from select element found by ``selector``.

        ``selector`` Selector of the select tag.
        See the `Finding elements` section for details about the selectors.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.DeselectOption(Request().ElementSelector(selector=selector))
            logger.debug(response.log)

    def _fill_text(self, selector: str, txt: str, log_response: bool = True):
        if self.library.presenter_mode:
            self.hover(selector)
            self.library.highlight_elements(selector, duration=timedelta(seconds=2))
            sleep(2)
        with self.playwright.grpc_channel() as stub:
            response = stub.FillText(Request().FillText(selector=selector, text=txt))
            if log_response:
                logger.debug(response.log)

    def _type_text(
        self,
        selector: str,
        txt: str,
        delay: timedelta = timedelta(microseconds=0),
        clear: bool = True,
        log_response: bool = True,
    ):
        if self.library.presenter_mode:
            self.hover(selector)
            self.library.highlight_elements(selector, duration=timedelta(seconds=2))
            sleep(2)
        with self.playwright.grpc_channel() as stub:
            delay_ms = self.get_timeout(delay)
            response = stub.TypeText(
                Request().TypeText(
                    selector=selector, text=txt, delay=int(delay_ms), clear=clear
                )
            )
            if log_response:
                logger.debug(response.log)

    @keyword(tags=("PageContent",))
    def handle_future_dialogs(self, action: DialogAction, prompt_input: str = ""):
        """Handle next dialog on page with ``action``.

        Dialog can be any of alert, beforeunload, confirm or prompt. Handling dialogue
        must be called before the action, like example click, that triggers the
        dialogue.

        If a handler is not set dialogs are dismissed by default.

            ``action`` How to handle the alert.

            ``prompt_input`` The value to enter into prompt. Only valid if
            ``action`` equals accept. Defaults to empty string.

        Example:

        | Handle Future Dialogs    action=accept
        | Click                    \\#alerts
        """

        with self.playwright.grpc_channel() as stub:
            if prompt_input and action is not DialogAction.accept:
                raise ValueError("prompt_input is only valid if action is 'accept'")
            response = stub.HandleAlert(
                Request().AlertAction(alertAction=action.name, promptInput=prompt_input)
            )
            logger.debug(response.log)

    @keyword(tags=("Wait", "PageContent"))
    def wait_for_alert(
        self, action: DialogAction, prompt_input: str = "", text: Optional[str] = None
    ):
        """Handle next dialog on page with ``action`` as promise.

        See `Handle Future Dialogs` for more details about ``action`` and what
        types of dialogues are supported.

        The main difference between this keyword and `Handle Future Dialogs`
        is that `Handle Future Dialogs` keyword is automatically set as promise.
        But this keyword must be called as argument to `Promise To` keyword. Also this
        keyword can optionally verify the dialogue text and return it. If ``text`` is
        argument ``None`` or is not set, dialogue text is not verified.

        Example with returning text:

        | ${promise} =       Promise To    Wait For Alert    action=accept
        | Click              id=alerts
        | ${text} =          Wait For      ${promise}
        | Should Be Equal    ${text}       Am an alert

        Example with text verify:

        | ${promise} =       Promise To    Wait For Alert    action=accept    text=Am an alert
        | Click              id=alerts
        | ${text} =          Wait For      ${promise}
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.WaitForAlert(
                Request().AlertAction(alertAction=action.name, promptInput=prompt_input)
            )
        logger.debug(response.log)
        if text is not None:
            assert (
                text == response.body
            ), f'Alert text was: "{response.body}" but it should have been: "{text}"'
        else:
            logger.debug("Not verifying alter text.")
        return response.body

    @keyword(tags=("Setter", "PageContent"))
    def mouse_button(
        self,
        action: MouseButtonAction,
        x: Optional[float] = None,
        y: Optional[float] = None,
        button: MouseButton = MouseButton.left,
        clickCount: int = 1,
        delay: int = 0,
    ):
        """Clicks, presses or releases a mouse button.


        ``action`` Determines if it is a mouseclick, holding down a key or releasing it.

        ``x`` and ``y`` Coordinates to move before.

        ``button`` Defaults to ``left``.

        ``clickCount`` Determine how often shall be clicked. Defaults to 1.

        ``delay`` Delay in ms between the mousedown and mouseup event.
        Can only be set if the action is click.

        Moving the mouse between holding down and releasing it, is possible with `Mouse Move`.
        """
        with self.playwright.grpc_channel() as stub:
            if x and y:
                self.mouse_move(x, y)
            else:
                logger.info(
                    "No coordinates where set. Action appears at current position."
                )
            if action == MouseButtonAction.click:
                for _ in range(clickCount):
                    self.mouse_button(MouseButtonAction.down, button=button)
                    sleep(delay / 1000)
                    self.mouse_button(MouseButtonAction.up, button=button)
                return
            else:
                if delay:
                    raise ValueError("Delay is only valid on 'click' action.")
                body = {"options": {"button": button.name, "clickCount": clickCount}}
            response = stub.MouseButton(
                Request().MouseButtonOptions(action=action.name, json=json.dumps(body))
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def drag_and_drop(self, selector_from: str, selector_to: str, steps: int = 1):
        """Executes a Drag&Drop operation from the element selected by ``selector_from``
        to the element selected by ``selector_to``.
        See the `Finding elements` section for details about the selectors.

        First it moves the mouse to the start-point,
        then presses the left mouse button,
        then moves to the end-point in specified number of steps,
        then releases the mouse button.

        Start- and end-point are defined by the center of the elements boundingbox.

        ``selector_from`` identifies the element, which center is the start-point.

        ``selector_to`` identifies the element, which center is the end-point.

        ``steps`` defines how many intermediate mouse move events are sent.
        """
        from_bbox = self.library.get_boundingbox(selector_from)
        from_xy = self._center_of_boundingbox(from_bbox)
        to_bbox = self.library.get_boundingbox(selector_to)
        to_xy = self._center_of_boundingbox(to_bbox)
        self.mouse_button(MouseButtonAction.down, **from_xy)
        self.mouse_move(**to_xy, steps=steps)
        self.mouse_button(MouseButtonAction.up)

    @keyword(tags=("Setter", "PageContent"))
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

        ``from_x`` & ``from_y`` identify the the start-point.

        ``to_x`` & ``to_y`` identify the the end-point.

        ``steps`` defines how many intermediate mouse move events are sent.
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

    @keyword(tags=("Setter", "PageContent"))
    def mouse_move_relative_to(
        self, selector: str, x: float = 0.0, y: float = 0.0, steps: int = 1
    ):
        """Moves the mouse cursor relative to the selected element.

        ``x`` ``y`` are relative coordinates to the center of the elements bounding box.

        ``steps`` Number of intermediate steps for the mouse event.
        This is sometime needed for websites to recognize the movement.
        """
        with self.playwright.grpc_channel() as stub:
            bbox = self.library.get_boundingbox(selector)
            center = self._center_of_boundingbox(bbox)
            body: MouseOptionsDict = {
                "x": center["x"] + x,
                "y": center["y"] + y,
                "options": {"steps": steps},
            }
            logger.info(
                f"Moving mouse relative to element center by x: {x}, y: {y} coordinates."
            )
            logger.debug(f"Element Center is: {center}")
            logger.debug(
                f"Mouse Position is: {{'x': {center['x'] + x}, 'y': {center['y'] + y}}}"
            )
            response = stub.MouseMove(Request().Json(body=json.dumps(body)))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def mouse_move(self, x: float, y: float, steps: int = 1):
        """Instead of selectors command mouse with coordinates.
        The Click commands will leave the virtual mouse on the specified coordinates.

        ``x`` ``y`` are absolute coordinates starting at the top left
        of the page.

        ``steps`` Number of intermediate steps for the mouse event.
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {"x": x, "y": y, "options": {"steps": steps}}
            logger.info(f"Moving mouse to x: {x}, y: {y} coordinates.")
            response = stub.MouseMove(Request().Json(body=json.dumps(body)))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def keyboard_key(self, action: KeyAction, key: str):
        """Press a keyboard key on the virtual keyboard or set a key up or down.

        ``action`` Determine whether the key should be released,
        hold or pressed. ``down`` or ``up`` are useful for combinations i.e. with Shift.


        ``key`` The key to be pressed. An example of valid keys are:

        ``F1`` - ``F12``, ``Digit0`` - ``Digit9``, ``KeyA`` - ``KeyZ``, ``Backquote``, ``Minus``,
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

    @keyword(tags=("Setter", "PageContent"))
    def keyboard_input(self, action: KeyboardInputAction, input: str, delay=0):
        """Input text into page with virtual keyboard.

        ``action``

            - ``insertText`` Dispatches only input event, does not emit the keydown, keyup or keypress events.

            - ``type`` Sends a keydown, keypress/input, and keyup event for each character in the text.

        ``input`` The inputstring to be typed. No special keys possible.

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
