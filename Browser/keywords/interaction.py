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
import sys
from collections.abc import Generator
from datetime import timedelta
from os import PathLike
from pathlib import Path
from time import sleep
from typing import Any, Optional, Union

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    get_abs_scroll_coordinates,
    get_rel_scroll_coordinates,
    keyword,
    logger,
)
from ..utils.data_types import (
    BoundingBox,
    Coordinates,
    DialogAction,
    FileUploadBuffer,
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

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |
        | ``txt`` | Text for the text field. |
        | ``delay`` | Delay between the single key strokes. It may be either a number or a Robot Framework time string. Time strings are fully explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``. Example: ``50 ms`` |
        | ``clear`` | Set to false, if the field shall not be cleared before typing. Defaults to true. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        See `Fill Text` for direct filling of the full text at once.

        Example
        | `Type Text`    input#username_field    user
        | `Type Text`    input#username_field    user    delay=10 ms    clear=No

        [https://forum.robotframework.org/t//4339|Comment >>]
        """
        logger.info(f"Types the text '{txt}' in the given field.")
        self._type_text(
            selector,
            txt,
            delay,
            clear,
            strict=self.strict_mode,
        )

    @keyword(tags=("Setter", "PageContent"))
    def fill_text(self, selector: str, txt: str, force: bool = False):
        """Clears and fills the given ``txt`` into the text field found by ``selector``.

        This method waits for an element matching the ``selector`` to appear,
        waits for actionability checks, focuses the element, fills it and
        triggers an input event after filling.

        If the element matching selector is not an <input>, <textarea> or
        [contenteditable] element, this method throws an error. Note that
        you can pass an empty string as ``txt`` to clear the input field.


        | =Arguments= | =Description= |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |
        | ``txt`` | Text for the text field. |
        | ``force`` | Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks]. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        See `Type Text` for emulating typing text character by character.

        Example:
        | `Fill Text`    css=input#username_field    username

        [https://forum.robotframework.org/t//4254|Comment >>]
        """
        logger.info(f"Fills the text '{txt}' in the given field.")
        self._fill_text(selector, txt, strict=self.strict_mode, force=force)

    @keyword(tags=("Setter", "PageContent"))
    def clear_text(self, selector: str):
        """Clears the text field found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        [https://forum.robotframework.org/t//4237|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearText(
                Request().ClearText(selector=selector, strict=self.strict_mode)
            )
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

        This keyword does not log secret in Robot Framework logs, if keyword resolves
        the variable value internally. If ``enable_playwright_debug`` is enabled in
        the library import, secret will be always visible as plain text in the playwright
        debug logs, regardless of the Robot Framework log level.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |
        | ``secret`` | Environment variable name with % prefix or a local variable with $ prefix that has the secret text value. Variable names can be used with and without curly braces. |
        | ``delay`` | Delay between the single key strokes. It may be either a number or a Robot Framework time string. Time strings are fully explained in an appendix of Robot Framework User Guide. Defaults to ``0 ms``. Example: ``50 ms`` |
        | ``clear`` | Set to false, if the field shall not be cleared before typing. Defaults to true. |

        This keyword does not log secret in Robot Framework logs, when
        keyword resolves the ``secret`` variable internally.
        When ``secret`` variable is prefixed with `$`, without the curly braces,
        library will resolve the corresponding Robot Framework variable.

        If ``secret`` variable is prefixed with `%`, library will resolve
        corresponding environment variable. Example `$Password`` will
        resolve to ``${Password}`` Robot Framework variable.
        Also ``%ENV_PWD`` will resolve to ``%{ENV_PWD}`` environment variable.

        *Using normal Robot Framework variables like ``${password}`` will not work!*

        *Normal plain text will not work.*
        If you want to use plain text, use `Type Text` keyword instead.

        This keyword will also work with a give cryptographic cipher text, that has been
        encrypted by Crypto library.
        See [https://github.com/Snooz82/robotframework-crypto | Crypto Library] for more details.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        See `Type Text` for details.

        Example
        | `Type Secret`    input#username_field    $username      # Keyword resolves ${username} variable value from Robot Framework variables
        | `Type Secret`    input#username_field    %username      # Keyword resolves $USERNAME/%USERNAME% variable value from environment variables
        | `Type Secret`    input#username_field    ${username}    # Robot Framework resolves the variable value, but secrect can leak to Robot framework output files.

        [https://forum.robotframework.org/t//4338|Comment >>]
        """
        secret = self.resolve_secret(secret, "secret")
        try:
            self._type_text(
                selector,
                secret,
                delay,
                clear,
                log_response=False,
                strict=self.strict_mode,
            )
        except Exception as e:
            raise Exception(str(e).replace(secret, "***"))

    @keyword(tags=("Setter", "PageContent"))
    def fill_secret(self, selector: str, secret: str, force: bool = False):
        """Fills the given secret from ``variable_name`` into the
        text field found by ``selector``.


        | =Arguments= | =Description= |
        | ``secret`` | The secret string that should be filled into the text field. |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |
        | ``force`` | Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks]. |


        This keyword does not log secret in Robot Framework logs, when
        keyword resolves the ``secret`` variable internally.
        When ``secret`` variable is prefixed with `$`, without the curly braces,
        library will resolve the corresponding Robot Framework variable.

        If ``secret`` variable is prefixed with `%`, library will resolve
        corresponding environment variable. Example `$Password`` will
        resolve to ``${Password}`` Robot Framework variable.
        Also ``%ENV_PWD`` will resolve to ``%{ENV_PWD}`` environment variable.

        *Using normal Robot Framework variables like ``${password}`` will not work!*

        *Normal plain text will not work.*
        If you want to use plain text, use `Fill Text` keyword instead.

        This keyword will also work with a give cryptographic cipher text, that has been
        encrypted by Crypto library.
        See [https://github.com/Snooz82/robotframework-crypto | Crypto Library] for more details.

        If ``enable_playwright_debug`` is enabled in the library import,
        secret will be always visible as plain text in the playwright debug
        logs, regardless of the Robot Framework log level.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        See `Fill Text` for other details.

        Example:
        | `Fill Secret`    input#username_field    $username    # Keyword resolves variable value from Robot Framework variables
        | `Fill Secret`    input#username_field    %username    # Keyword resolves variable value from environment variables

        [https://forum.robotframework.org/t//4253|Comment >>]
        """
        secret = self.resolve_secret(secret, "secret")
        try:
            self._fill_text(
                selector,
                secret,
                log_response=False,
                strict=self.strict_mode,
                force=force,
            )
        except Exception as e:
            raise Exception(str(e).replace(secret, "***"))

    @keyword(tags=("Setter", "PageContent"))
    def press_keys(self, selector: str, *keys: str):
        """Types the given key combination into element found by ``selector``.


        | =Arguments= | =Description= |
        | ``selector`` | Selector of the text field. See the `Finding elements` section for details about the selectors. |
        | ``*keys`` | Keys to be press after each other. Using + to chain combine modifiers with a single keypress ``Control+Shift+T`` is supported. |


        Supports values like "a, b" which will be automatically typed.

        Also supports identifiers for keys like ``ArrowLeft`` or ``Backspace``.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        See playwright's documentation for a more comprehensive list of
        supported input keys.
        [https://playwright.dev/docs/api/class-page#page-press | Playwright docs for press.]

        Example:
        | # Keyword         Selector                    *Keys
        | `Press Keys`      //*[@id="username_field"]    h    e   l   o   ArrowLeft   l

        [https://forum.robotframework.org/t//4311|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.Press(
                Request().PressKeys(
                    selector=selector, strict=self.strict_mode, key=keys
                )
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def click(self, selector: str, button: MouseButton = MouseButton.left):
        """Simulates mouse click on the element found by ``selector``.

        This keyword clicks an element matching ``selector`` by performing the following steps:
        - Find an element matches selector. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set.
          If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Button` to click in the center of the element, or the specified position.
        - Wait for initiated navigation to either succeed or fail.


        | =Arguments= | =Description= |
        | ``selector`` | Selector element to click. See the `Finding elements` section for details about the selectors. |
        | ``button`` | Defaults to ``left`` if invalid. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Click`    id=button_location
        | `Click`    id=button_location    left
        | `Click`    id=button_location    right

        [https://forum.robotframework.org/t//4238|Comment >>]
        """
        self.click_with_options(selector, button)

    @keyword(tags=("Setter", "PageContent"))
    def click_with_options(
        self,
        selector: str,
        button: MouseButton = MouseButton.left,
        *modifiers: KeyboardModifier,
        clickCount: int = 1,
        delay: Optional[timedelta] = None,
        force: bool = False,
        noWaitAfter: bool = False,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        trial: bool = False,
    ):
        """Simulates mouse click on the element found by ``selector``.

        This keyword clicks an element matching ``selector`` by performing the following steps:
        - Find an element matches selector. If there is none, wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set.
          If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Button` to click in the center of the element, or the specified position.
        - Wait for initiated navigation to either succeed or fail, unless ``noWaitAfter`` option is set.


        | =Arguments= | =Description= |
        | ``selector`` | Selector element to click. See the `Finding elements` section for details about the selectors. |
        | ``button`` | Defaults to ``left`` if invalid. |
        | ``*modifiers`` | Modifier keys to press. Ensures that only these modifiers are pressed during the click, and then restores current modifiers back. If not specified, currently pressed modifiers are used. Modifiers can be specified in any order, and multiple modifiers can be specified. Valid modifier keys are ``Control``, ``Alt``, ``Shift`` and ``Meta``. Due to the fact that the argument `*modifiers` is a positional only argument, all preceding keyword arguments have to be specified as positional arguments before `*modifiers`. |
        | ``clickCount`` | Defaults to 1. |
        | ``delay`` | Time to wait between mouse-down and mouse-up. Defaults to 0. |
        | ``position_x`` ``position_y`` | A point to click relative to the top-left corner of element bounding-box. Only positive values within the bounding-box are allowed. If not specified, clicks to some visible point of the element. |
        | ``force`` | Set to True to skip Playwright's Actionability checks (https://playwright.dev/docs/actionability). |
        | ``noWaitAfter`` | Deprecated. This option will default to true in the future. Actions that initiate navigation, are waiting for these navigation to happen and for pages to start loading. You can opt out of waiting via setting this flag. You would only need this option in the exceptional cases such as navigating to inaccessible pages. Defaults to ``False``. |
        | ``trial`` | When set, this method only performs the actionability checks and skips the action. Defaults to false. Useful to wait until the element is ready for the action without performing it. |

        Arguments ``clickCount``, ``delay``, ``position_x``, ``position_y``, ``force``, ``noWaitAfter`` and ``trial`` are named-only arguments and must be specified using their names..

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Click With Options`    id=button_location
        | `Click With Options`    id=button_location    trial=True
        | `Click With Options`    \\#clickWithOptions    delay=100ms    clickCount=2
        | `Click With Options`    id=clickWithModifiers    left     Alt    Meta    Shift    clickCount=1    force=True
        | `Click With Options`    id=clickWithOptions    right    clickCount=2    force=True

        [https://forum.robotframework.org/t//5936|Comment >>]
        """
        logger.info(f"Clicks the element '{selector}'.")
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            options = {
                "button": button.name,
                "clickCount": clickCount,
                "force": force,
                "noWaitAfter": noWaitAfter,
                "trial": trial,
            }
            if delay:
                options["delay"] = self.get_timeout(delay)
            # Without the != None 0 being falsy causes issues
            if position_x is not None and position_y is not None:
                positions: dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Click options are: {options_json}")
            response = stub.Click(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json, strict=self.strict_mode
                )
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def tap(
        self,
        selector: str,
        *modifiers: KeyboardModifier,
        force: bool = False,
        noWaitAfter: bool = False,
        position_x: Optional[int] = None,
        position_y: Optional[int] = None,
        trial: bool = False,
    ):
        """Simulates tap on the element found by ``selector``.

        Requires that the ``hasTouch`` option of the `New Context` be set to true.
        This method taps the element by performing the following steps:
        - Wait for actionability checks on the element, unless force option is set.
        - Scroll the element into view if needed.
        - Use page.touchscreen to tap the center of the element, or the specified position.
        - Wait for initiated navigations to either succeed or fail, unless noWaitAfter option is set.

        | =Arguments= | =Description= |
        | ``selector`` | Selector element to click. See the `Finding elements` section for details about the selectors. |
        | ``*modifiers`` | Modifier keys to press. Ensures that only these modifiers are pressed during the click, and then restores current modifiers back. If not specified, currently pressed modifiers are used. Modifiers can be specified in any order, and multiple modifiers can be specified. Valid modifier keys are ``Control``, ``Alt``, ``Shift`` and ``Meta``. |
        | ``force`` | Whether to bypass the actionability checks. Defaults to false. |
        | ``noWaitAfter`` | Deprecated. This option has no effect. Actions that initiate navigations are waiting for these navigations to happen and for pages to start loading. You can opt out of waiting via setting this flag. You would only need this option in the exceptional cases such as navigating to inaccessible pages. Defaults to ``False``. |
        | ``position_x`` ``position_y`` | A point to click relative to the top-left corner of element bounding-box. Only positive values within the bounding-box are allowed. If not specified, clicks to some visible point of the element. |
        | ``trial`` | When set, this method only performs the actionability checks and skips the action. Defaults to ``False``.  |

        Example:
        | New Context    hasTouch=${False}
        | New Page    ${URL}
        | Tap    css=input#login_button

        [https://forum.robotframework.org/t//5939|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        options: dict[str, object] = {
            "force": force,
            "noWaitAfter": noWaitAfter,
            "trial": trial,
        }
        if position_x is not None and position_y is not None:
            positions: dict[str, int] = {"x": position_x, "y": position_y}
            options["position"] = positions
        if modifiers:
            options["modifiers"] = [modifier.name for modifier in modifiers]
        options_json = json.dumps(options)
        with self.playwright.grpc_channel() as stub:
            logger.debug(f"Tap options are: {options_json}")
            response = stub.Tap(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json, strict=self.strict_mode
                )
            )
            logger.debug(response.log)

    @keyword(tags=("PageContent",))
    def record_selector(
        self,
        label: Optional[str] = None,
    ):
        """Record the selector that is under mouse.


        | =Arguments= | =Description= |
        | ``label`` | text to show when on the box in the page while recording. |

        Focus on the page and move mouse over the element you want to select.

        Example:
        | ${selector} =    `Record Selector`   Button
        | `Click`  ${selector}
        | ${selector2} =    `Record Selector`  Page header
        | `Get Text`  ${selector2}  ==  Expected text

        [https://forum.robotframework.org/t//4315|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.RecordSelector(Request.Label(label=label or ""))
            selector_repr = response.result.replace("#", "\\#")
            logger.console(
                f"\nSelector{' for ' + label if label else ''}: {selector_repr}"
            )
            logger.info(f"Selector{' for ' + label if label else ''}: {selector_repr}")
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
        - Find an element match matching ``selector``. If there is none,
          wait until a matching element is attached to the DOM.
        - Wait for actionability checks on the matched element, unless ``force`` option is set.
          If the element is detached during the checks, the whole action is retried.
        - Scroll the element into view if needed.
        - Use `Mouse Move` to hover over the center of the element, or the specified ``position``.


        | =Arguments= | =Description= |
        | ``selector`` | Selector element to hover. See the `Finding elements` section for details about the selectors. |
        | ``position_x`` & ``position_y`` | A point to hover relative to the top-left corner of element bounding box. If not specified, hovers over some visible point of the element. Only positive values within the bounding-box are allowed. |
        | ``force`` | Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks]. |
        | ``*modifiers`` | Modifier keys to press. Ensures that only these modifiers are pressed during the hover, and then restores current modifiers back. If not specified, currently pressed modifiers are used. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Hover`    h1
        | `Hover`    h1    10   20    Alt

        [https://forum.robotframework.org/t//4295|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            options: dict[str, Any] = {"force": force}
            if position_x and position_y:
                positions: dict[str, object] = {"x": position_x, "y": position_y}
                options["position"] = positions
            if modifiers:
                options["modifiers"] = [m.name for m in modifiers]
            options_json = json.dumps(options)
            logger.debug(f"Hover Options are: {options_json}")
            response = stub.Hover(
                Request().ElementSelectorWithOptions(
                    selector=selector, options=options_json, strict=self.strict_mode
                )
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def focus(self, selector: str):
        """Moves focus on to the element found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the element. See the `Finding elements` section for details about the selectors. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        If there's no element matching selector, the method waits until a
        matching element appears in the DOM. Timeouts after 10 seconds.

        [https://forum.robotframework.org/t//4255|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.Focus(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
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

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the element. If the selector is ``${None}`` or ``${Empty}`` the page itself is scrolled. To ensure an element is in view use `Hover` instead. See the `Finding elements` section for details about the selectors. |
        | ``vertical`` | defines where to scroll vertically. It can be a positive number, like ``300``. It can be a percentage value of the absolute scrollable size, like ``50%``. It can be a string defining that top or the bottom of the scroll area. < ``top`` | ``bottom`` > _Be aware that some pages do lazy loading and load more content once you scroll down._ Bottom defines the current known bottom coordinate. |
        | ``horizontal`` | defines where to scroll horizontally. Works same as vertical but defines < ``left`` | ``right`` > as start and end. |
        | ``behavior`` | defines whether the scroll happens directly or it scrolls smoothly. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        [https://forum.robotframework.org/t//4320|Comment >>]
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
        self.exec_scroll_function(
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

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the element. If the selector is ``${None}`` or ``${Empty}`` the page itself is scrolled. To ensure an element is in view use `Hover` instead. See the `Finding elements` section for details about the selectors. |
        | ``vertical`` | defines how far and in which direction to scroll vertically. It can be a positive or negative number. Positive scrolls down, like ``50``, negative scrolls up, like ``-50``. It can be a percentage value of the absolute scrollable size, like ``9.95%`` or negative like ``-10%``. It can be the string ``height`` to defining to scroll exactly one visible height down or up with ``-height``. _Be aware that some pages do lazy loading and load more content once you scroll down._ The percentage of the current scrollable height is used and may change. |
        | ``horizontal`` | defines where to scroll horizontally. Works same as vertical but defines positive values for right and negative values for left. ``width`` defines to scroll exactly one visible range to the right. |
        | ``behavior`` | defines whether the scroll happens directly or it scrolls smoothly. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        [https://forum.robotframework.org/t//4319|Comment >>]
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
        self.exec_scroll_function(
            f'scrollBy({{"left": {horizontal_px}, "top": {vertical_px}, "behavior": "{behavior.name}"}})',
            selector,
        )

    @keyword(tags=("Setter", "PageContent"))
    def scroll_to_element(self, selector: str):
        """This method waits for actionability checks, then tries to scroll element into view,
        unless it is completely visible.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the checkbox. See the `Finding elements` section for details about the selectors. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Does nothing if the element is already visible.

        [https://forum.robotframework.org/t//4321|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.ScrollToElement(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def check_checkbox(self, selector: str, force: bool = False):
        """Checks the checkbox or selects radio button found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the checkbox. See the `Finding elements` section for details about the selectors. |
        | ``force`` | Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks]. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Does nothing if the element is already checked/selected.

        [https://forum.robotframework.org/t//4235|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.CheckCheckbox(
                Request().ElementSelector(
                    selector=selector, strict=self.strict_mode, force=force
                )
            )
        logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def uncheck_checkbox(self, selector: str, force: bool = False):
        """Unchecks the checkbox found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the checkbox. See the `Finding elements` section for details about the selectors. |
        | ``force`` | Set to True to skip Playwright's [https://playwright.dev/docs/actionability | Actionability checks]. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Does nothing if the element is not checked/selected.

        [https://forum.robotframework.org/t//4340|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.UncheckCheckbox(
                Request().ElementSelector(
                    selector=selector, strict=self.strict_mode, force=force
                )
            )
        logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def select_options_by(
        self,
        selector: str,
        attribute: SelectAttribute,
        *values,
    ) -> list[Any]:
        """Selects options from select element found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the ``<select>`` tag. See the `Finding elements` section for details about the selectors. |
        | ``attribute`` | Attribute to select options by. Can be ``value``, ``label``, ``text`` or ``index``. Where ``label`` and ``text`` are same. |
        | ``*values`` | Values to select. |


        Returns list of options which keyword was able to select. The type of
        list item matches to ``attribute`` definition. Example if ``attribute``
        equals to `label` returned list contains label values. Or in case of
        `index` it contains list of selected indexes.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        If no values to select are passed will deselect options in element.

        Example:
        | ${selected} =    `Select Options By`    select[name=preferred_channel]    label    Direct mail
        | List Should Contain Value    ${selected}    Direct mail
        | ${selected} =    `Select Options By`    select[name=interests]    value    males    females    others
        | List Should Contain Value    ${selected}    males
        | List Should Contain Value    ${selected}    females
        | List Should Contain Value    ${selected}    others
        | Length Should Be    ${selected}    3
        | ${selected} =    `Select Options By`    select[name=possible_channels]    index    0    2
        | List Should Contain Value    ${selected}    0
        | List Should Contain Value    ${selected}    2
        | ${selected} =    `Select Options By`    select[name=interests]    text     Males    Females
        | List Should Contain Value    ${selected}    Males
        | List Should Contain Value    ${selected}    Females

        [https://forum.robotframework.org/t//4322|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        matchers = ""
        if not values or (len(values) == 1 and not values[0]):
            self.deselect_options(selector)
            return []

        logger.info(
            f"Selects the option(s) {', '.join([str(value) for value in values])} by attribute {attribute} from element {selector}."
        )
        if attribute is SelectAttribute.value:
            matchers = json.dumps([{"value": s} for s in values])
        elif attribute is SelectAttribute.label:
            matchers = json.dumps([{"label": s} for s in values])
        elif attribute is SelectAttribute.index:
            matchers = json.dumps([{"index": int(s)} for s in values])
        else:
            raise TypeError(
                'Invalid type for `attribute`. Please specify SelectAttribute["value"], "label" or "index"'
            )

        with self.playwright.grpc_channel() as stub:
            response = stub.SelectOption(
                Request().SelectElementSelector(
                    selector=selector, matcherJson=matchers, strict=self.strict_mode
                )
            )
        logger.debug(response)
        return [getattr(sel, attribute.name) for sel in response.entry if sel.selected]

    @keyword(tags=("Setter", "PageContent"))
    def deselect_options(self, selector: str):
        """Deselects all options from select element found by ``selector``.

        | =Arguments= | =Description= |
        | ``selector`` | Selector of the select tag. See the `Finding elements` section for details about the selectors. |

        If you just want to select one or more specific options and
        currently more options are selected, use `Select Options By`
        keyword with the options to be selected in the end.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        [https://forum.robotframework.org/t//4245|Comment >>]
        """
        selector = self.presenter_mode(selector, self.strict_mode)
        with self.playwright.grpc_channel() as stub:
            response = stub.DeselectOption(
                Request().ElementSelector(selector=selector, strict=self.strict_mode)
            )
        logger.debug(response.log)

    def _fill_text(
        self,
        selector: str,
        txt: str,
        log_response: bool = True,
        strict: bool = True,
        force: bool = False,
    ):
        selector = self.presenter_mode(selector, strict)
        with self.playwright.grpc_channel() as stub:
            response = stub.FillText(
                Request().FillText(
                    selector=selector, text=txt, strict=strict, force=force
                )
            )
            if log_response:
                logger.debug(response.log)

    def _type_text(
        self,
        selector: str,
        txt: str,
        delay: timedelta = timedelta(microseconds=0),
        clear: bool = True,
        log_response: bool = True,
        strict: bool = True,
    ):
        selector = self.presenter_mode(selector, strict)
        with self.playwright.grpc_channel() as stub:
            delay_ms = self.get_timeout(delay)
            response = stub.TypeText(
                Request().TypeText(
                    selector=selector,
                    text=txt,
                    delay=int(delay_ms),
                    clear=clear,
                    strict=strict,
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

        | =Arguments= | =Description= |
        | ``action`` | How to handle the alert. Can be ``accept`` or ``dismiss``. |
        | ``prompt_input`` | The value to enter into prompt. Only valid if ``action`` argument equals ``accept``. Defaults to empty string. |

        Example:
        | `Handle Future Dialogs`    action=accept
        | `Click`                    \\#alerts

        [https://forum.robotframework.org/t//4293|Comment >>]
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
        self,
        action: DialogAction,
        prompt_input: str = "",
        text: Optional[str] = None,
        timeout: Optional[timedelta] = None,
    ):
        """Returns a promise to wait for next dialog on page, handles it with ``action`` and optionally verifies the dialogs text.

        Dialog/alert can be any of alert, beforeunload, confirm or prompt.

        | =Arguments= | =Description= |
        | ``action`` | How to handle the alert. Can be ``accept`` or ``dismiss``. |
        | ``prompt_input`` | The value to enter into prompt. Only valid if ``action`` argument equals ``accept``. Defaults to empty string. |
        | ``text`` | Optional text to verify the dialogs text. |
        | ``timeout`` | Optional timeout in Robot Framework time format. |


        The main difference between this keyword and `Handle Future Dialogs`
        is that `Handle Future Dialogs` keyword is automatically set as promise.
        But this keyword must be called as argument to `Promise To` keyword. Also this
        keyword can optionally verify the dialogue text and return it. If ``text`` is
        argument ``None`` or is not set, dialogue text is not verified.

        Example with returning text:

        | ${promise} =         `Promise To`    `Wait For Alert`    action=accept
        | `Click`               id=alerts
        | ${text} =            `Wait For`      ${promise}
        | Should Be Equal      ${text}         Am an alert

        Example with text verify:

        | ${promise} =       `Promise To`    Wait For Alert    action=accept    text=Am an alert
        | Click              id=alerts
        | ${text} =          `Wait For`      ${promise}

        [https://forum.robotframework.org/t//4343|Comment >>]
        """
        received_text = self.wait_for_alerts([action], [prompt_input], [None], timeout)
        received_text = received_text[0] if received_text else ""
        if text is not None:
            assert text == received_text, (
                f'Alert text was: "{received_text}" but it should have been: "{text}"'
            )
        else:
            logger.debug("Not verifying alter text.")
        return received_text

    @keyword(tags=("Wait", "PageContent"))
    def wait_for_alerts(
        self,
        actions: list[DialogAction],
        prompt_inputs: list[Union[None, str]],
        texts: list[Union[None, str]],
        timeout: Optional[timedelta] = None,
    ) -> list[str]:
        """Returns a promise to wait for multiple dialog on a page.

        Handles each alert/dialog with ``actions`` and optionally verifies the dialogs texts.
        Dialog/alert can be any of alert, beforeunload, confirm or prompt.

        | =Arguments= | =Description= |
        | ``actions`` | List of how to handle the alerts. Can be ``accept`` or ``dismiss``. |
        | ``prompt_inputs`` | List of the values to enter into prompt. Only valid if ``action`` argument equals ``accept``. Defaults to empty string. IF input not preset, use None |
        | ``texts`` | List of optional text to verify the dialogs text. Use None if text verification should be disabled. |
        | ``timeout`` | Optional timeout in Robot Framework time format. |

        There must be equal amount of items in ``actions``, ``prompt_inputs`` and ``texts``  lists.
        Use None if texts and/or prompt_inputs are not needed.

        This keyword works in same way as `Wait For Alert` but can handle multiple alerts
        with one promise. Lie `Wait For Alert` keyword, this keyword must be called as
        argument to `Promise To` keyword.

        Example to handle two alerts, first one is accepted and second one is dismissed:

        | ${promise} =    Promise To
        | ...    Wait For Alerts
        | ...    ["accept", "dismiss"]
        | ...    [None, None]
        | ...    [None, None]
        | Click    id=alerts
        | ${texts} =    Wait For    ${promise}

        Example to handle confirm and prompt alert. Example assumes that the first is a
        confirm and second one is prompt:

        | ${promise} =    Promise To
        | ...    Wait For Alerts
        | ...    ["dismiss", "accept"]
        | ...    [None, "I am a prompt"]
        | ...    ["First alert accepted?", None]
        | Click    id=confirmAndPrompt
        | ${texts} =    Wait For    ${promise}

        [https://forum.robotframework.org/t/7887|Comment >>]
        """
        if not len(actions) == len(prompt_inputs) == len(texts):
            raise ValueError(
                "There was not equal amount of items in actions, prompt_inputs and texts lists. "
                f"actions: {len(actions)}, prompt_inputs: {len(prompt_inputs)}, texts: {len(texts)}"
            )
        lib_default_or_timeout = self.get_timeout(timeout)
        alert_actions = Request().AlertActions()
        for action, prompt_input in zip(actions, prompt_inputs):
            alert_action = Request().AlertAction()
            alert_action.alertAction = action.name
            alert_action.promptInput = prompt_input or ""
            alert_action.timeout = lib_default_or_timeout
            alert_actions.items.append(alert_action)
        with self.playwright.grpc_channel() as stub:
            response = stub.WaitForAlerts(alert_actions)
            logger.debug(response.items)
        index = 1
        for expected_text, received_text in zip(texts, response.items):
            if expected_text is None:
                index += 1
                continue
            assert expected_text == received_text, (
                f'Alert index {index} text was: "{received_text}" but it should have been: "{expected_text}"'
            )
            index += 1
        return response.items

    @keyword(tags=("Setter", "PageContent"))
    def mouse_button(
        self,
        action: MouseButtonAction,
        x: Optional[float] = None,
        y: Optional[float] = None,
        button: MouseButton = MouseButton.left,
        clickCount: int = 1,
        delay: Union[int, timedelta] = timedelta(seconds=0),
        # TODO: remove int special handling. Was only here since 09.2022 for removing delay ms to timedelta
    ):
        """Clicks, presses or releases a mouse button.

        | =Arguments= | =Description= |
        | ``action`` | Defines if it is a mouseclick (``click``), holding down a button (``down``) or releasing it (``up``). |
        | ``x``, ``y`` | Coordinates to move before action is executed. |
        | ``button`` | One of ``left``, ``middle`` or ``up``. Defaults to ``left``. |
        | ``clickCount`` | Determine how often the button shall be clicked if action is equal to ``click``. Defaults to 1. |
        | ``delay`` | Delay in Robot Framework time format between the mousedown and mouseup event. Can only be set if the action is ``click``. |

        *Attention:*
        Argument type `int` for 'delay' in milliseconds has been changed to `timedelta` in Browser 14.0.0. Use Robot Framework time format instead.
        For refactoring just add 'ms' after the delay number.

        Delay Example:
        | `Mouse Button`    click    100 ms
        | `Mouse Button`    click    ${dyn_delay} ms

        Moving the mouse between holding down and releasing it, is possible with `Mouse Move`.

        Example:
        | `Hover`                     "Obstacle"           # Move mouse over the element
        | `Mouse Button`              down                 # Press mouse button down
        | `Mouse Move Relative To`    "Obstacle"    500    # Drag mouse
        | `Mouse Button`              up                   # Release mouse button

        [https://forum.robotframework.org/t//4303|Comment >>]
        """
        if isinstance(delay, int):
            logger.warn(
                "Keyword 'Mouse Button' will not support int in ms for 'delay' in the future. "
                "Use timedelta with units ('ms' or 's') instead."
            )
            delay = timedelta(milliseconds=delay)
            # ToDo: add in 15.0.0
            # raise ValueError(
            #     "Argument type `int` for 'delay' in milliseconds has been changed to `timedelta` in Browser 14.0.0. Use Robot Framework time format instead."
            # )
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
                    sleep(delay.total_seconds())
                    self.mouse_button(MouseButtonAction.up, button=button)
                return
            if delay:
                raise ValueError("Delay is only valid on 'click' action.")
            body = {"options": {"button": button.name, "clickCount": clickCount}}
            response = stub.MouseButton(
                Request().MouseButtonOptions(action=action.name, json=json.dumps(body))
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def drag_and_drop(
        self,
        selector_from: str,
        selector_to: str,
        steps: int = 1,
    ):
        """Executes a Drag&Drop operation from the element selected by ``selector_from``
        to the element selected by ``selector_to``.

        | =Arguments= | =Description= |
        | ``selector_from`` | Identifies the element, which center is the start-point. |
        | ``selector_to`` | Identifies the element, which center is the end-point. |
        | ``steps`` | Defines how many intermediate mouse move events are sent. Often it is necessary to send more than one intermediate event to get the desired result. Defaults to 1. |

        See the `Finding elements` section for details about the selectors.

        First it moves the mouse to the start-point,
        then presses the left mouse button,
        then moves to the end-point in specified number of steps,
        then releases the mouse button.

        Start- and end-point are defined by the center of the elements boundingbox.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example
        | `Drag And Drop`    "Circle"    "Goal"

        [https://forum.robotframework.org/t//4247|Comment >>]
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
        self,
        from_x: float,
        from_y: float,
        to_x: float,
        to_y: float,
        steps: int = 1,
    ):
        """Executes a Drag&Drop operation from a coordinate to another coordinate.

        First it moves the mouse to the start-point,
        then presses the left mouse button,
        then moves to the end-point in specified number of steps,
        then releases the mouse button.

        Start- and end-point are defined by ``x`` and ``y`` coordinates relative to
        the top left corner of the pages viewport.

        | ``from_x`` & ``from_y`` | Identify the start-point on page. |
        | ``to_x`` & ``to_y`` | Identify the end-point. |
        | ``steps`` | Defines how many intermediate mouse move events are sent. Often it is necessary to send more than one intermediate event to get the desired result. Defaults to 1. |

        Example:
        | `Drag And Drop By Coordinates`
        | ...    from_x=30    from_y=30
        | ...    to_x=10    to_y=10    steps=20

        [https://forum.robotframework.org/t//4248|Comment >>]
        """
        self.mouse_button(MouseButtonAction.down, x=from_x, y=from_y)
        self.mouse_move(x=to_x, y=to_y, steps=steps)
        self.mouse_button(MouseButtonAction.up)

    @keyword(tags=("Setter", "PageContent"))
    def drag_and_drop_relative_to(
        self,
        selector_from: str,
        x: float = 0.0,
        y: float = 0.0,
        steps: int = 1,
    ):
        """Executes a Drag&Drop operation from the element selected by ``selector_from``
        to coordinates relative to the center of that element.

        This keyword can be handy to simulate swipe actions.

        | =Arguments= | =Description= |
        | ``selector_from`` | identifies the element, which center is the start-point. |
        | ``x`` & ``y`` | identifies the end-point which is relative to the start-point. |
        | ``steps`` | defines how many intermediate mouse move events are sent. Often it is necessary to send more than one intermediate event to get the desired result. Defaults to 1. |

        See the `Finding elements` section for details about the selectors.

        First it moves the mouse to the start-point (center of boundingbox),
        then presses the left mouse button,
        then moves to the relative position with the given intermediate steps,
        then releases the mouse button.

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example
        | `Drag And Drop Relative to`    "Circle"    -20    0     # Slides the element 20 pixel to the left

        [https://forum.robotframework.org/t//4249|Comment >>]
        """
        from_bbox = self.library.get_boundingbox(selector_from)
        from_xy = self._center_of_boundingbox(from_bbox)
        to_x = from_xy["x"] + x
        to_y = from_xy["y"] + y
        self.mouse_button(MouseButtonAction.down, **from_xy)
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
        self,
        selector: str,
        x: float = 0.0,
        y: float = 0.0,
        steps: int = 1,
    ):
        """Moves the mouse cursor relative to the selected element.

        | =Arguments= | =Description= |
        | ``selector`` | Identifies the element, which center is the start-point. |
        | ``x`` & ``y`` | Are relative coordinates to the center of the elements bounding box. |
        | ``steps`` | Number of intermediate steps for the mouse event. Often it is necessary to send more than one intermediate event to get the desired result. Defaults to 1. |

        Keyword uses strict mode, see `Finding elements` for more details about strict mode.

        Example:
        | `Mouse Move Relative To`    id=indicator    -100

        [https://forum.robotframework.org/t//4305|Comment >>]
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

        | =Arguments= | =Description= |
        | ``x`` & ``y`` | Are absolute coordinates starting at the top left of the page. |
        | ``steps`` | Number of intermediate steps for the mouse event. Often it is necessary to send more than one intermediate event to get the desired result. Defaults to 1. |

        Example:
        | `Mouse Move`    400    400

        [https://forum.robotframework.org/t//4304|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            body: MouseOptionsDict = {"x": x, "y": y, "options": {"steps": steps}}
            logger.info(f"Moving mouse to x: {x}, y: {y} coordinates.")
            response = stub.MouseMove(Request().Json(body=json.dumps(body)))
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def mouse_wheel(self, deltaX: int, deltaY: int):
        """Simulates the user rotation of a mouse wheel.

        | =Arguments= | =Description= |
        | ``deltaX`` & ``deltaY`` | Pixels that are scrolled horizontally & vertically. |

        Example:
        | # Before doing a mouse wheel interaction. A mouse needs to be positioned on the browser window.
        | `Hover`    body
        | `Mouse Wheel`    0    250

        [https://forum.robotframework.org/t//5186|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.MouseWheel(
                Request().MouseWheel(deltaX=deltaX, deltaY=deltaY)
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def keyboard_key(self, action: KeyAction, key: str):
        """Press a keyboard key on the virtual keyboard or set a key up or down.

        | =Arguments= | =Description= |
        | ``action`` | Determine whether the key should be released (``up``), hold (``down``) or pressed once (``press``). ``down`` or ``up`` are useful for combinations i.e. with Shift. |
        | ``key`` | The key to be pressed. An example of valid keys are: ``F1`` - ``F12``, ``Digit0`` - ``Digit9``, ``KeyA`` - ``KeyZ``, ``Backquote``, ``Minus``, ``Equal``, ``Backslash``, ``Backspace``, ``Tab``, ``Delete``, ``Escape``, ``ArrowDown``, ``End``, ``Enter``, ``Home``, ``Insert``, ``PageDown``, ``PageUp``, ``ArrowRight``, ``ArrowUp`` , etc. |


        Useful keys for ``down`` and ``up`` for example are:
        ``Shift``, ``Control``, ``Alt``, ``Meta``, ``ShiftLeft``

        Example execution:
        | `Keyboard Key`    press    S
        | `Keyboard Key`    down     Shift
        | `Keyboard Key`    press    ArrowLeft
        | `Keyboard Key`    press    Delete
        | `Keyboard Key`    up       Shift

        Note: Capital letters don't need to be written by the help of Shift. You can type them in directly.

        [https://forum.robotframework.org/t//4298|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.KeyboardKey(
                Request().KeyboardKeypress(action=action.name, key=key)
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def keyboard_input(
        self,
        action: KeyboardInputAction,
        input: str,  # noqa: A002
        delay: Union[int, timedelta] = timedelta(milliseconds=0),
        # TODO: remove int special handling. Was only here since 09.2022 for removing delay ms to timedelta
    ):
        """Input text into page with virtual keyboard.

        | =Arguments= | =Description= |
        | ``action`` | ``insertText``: Dispatches only input event, does not emit the keydown, keyup or keypress events. ``type``: Sends a keydown, keypress/input, and keyup event for each character in the text. |
        | ``input`` | The inputstring to be typed. _No special keys possible._ |
        | ``delay`` | Time to wait between key presses in Robot Framework's time format. Defaults to 0. |

        *Attention:*
        Argument type `int` for 'delay' in milliseconds has been changed to `timedelta` in Browser 14.0.0. Use Robot Framework time format with units instead.


        Note: To press a special key, like Control or ArrowDown, use keyboard.press.
        Modifier keys DO NOT effect these methods. For testing modifier effects use single key
        presses with ``Keyboard Key  press``

        Example:
        | `Keyboard Input`    insertText    0123456789

        [https://forum.robotframework.org/t//4297|Comment >>]
        """
        if isinstance(delay, int):
            logger.warn(
                "Keyword 'Keyboard Input' will not support int in ms for 'delay' in the future. "
                "Use timedelta with units ('ms' or 's') instead."
            )
            delay = timedelta(milliseconds=delay)
            # TODO: add in 15.0.0
            # raise ValueError(
            #     "Argument type `int` for 'delay' in milliseconds has been changed to `timedelta` in Browser 14.0.0. Use Robot Framework time format instead."
            # )
        with self.playwright.grpc_channel() as stub:
            response = stub.KeyboardInput(
                Request().KeyboardInputOptions(
                    action=action.name,
                    input=input,
                    delay=int(delay.total_seconds() * 1000),
                )
            )
            logger.debug(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def upload_file_by_selector(
        self,
        selector: str,
        path: Union[PathLike, FileUploadBuffer],
        *extra_paths: PathLike,
    ):
        """Uploads file from ``path`` to file input element matched by selector.

        Fails if upload is not done before library timeout.
        Therefor it may be necessary to increase the timeout with `Set Browser Timeout`.
        It is possible to upload multiple files or folder by defining additional paths
        or folders. in `extra_paths`.

        If path is a directory, it will be uploaded all files from the directory.
        Subdirectories are not included. It is possible to upload files and directories
        with the same keyword.

        | =Arguments= | =Description= |
        | ``selector`` | Identifies the file input element. |
        | ``path`` | Path to the file or folder to be uploaded. Path can  FileUploadBuffer dictionary |
        | ``extra_paths`` | Additional paths to files or folders to be uploaded. |

        if ``path`` is  `FileUploadBuffer` dictionary, then structure should be:
        | {
        |   'name': `str`,
        |   'mimeType': `str`,
        |   'buffer': `str`
        | }

        If ``path`` argument is `FileUploadBuffer`, then ``extra_paths`` argument is not supported and
        using it will raise an error.

        Upload single file example:
        | `Upload File By Selector`    //input[@type='file']    big_file.zip

        Upload many files example:
        | `Upload File By Selector`    //input[@type='file']    file1.zip    file2.zip    file3.zip

        Upload folder example:
        | `Upload File By Selector`    //input[@type='file']    /path/to/folder

        Upload as buffer example:
        | ${text} =    Get File    /path/to/file    # Read file from disk
        | VAR    &{buffer}    name=not_here.txt    mimeType=text/plain    buffer=${text}    # Create buffer dictionary
        | `Upload File By Selector`    id=file_chooser    ${buffer}    # Upload buffer

        [https://forum.robotframework.org/t//4341|Comment >>]
        """
        selector = self.resolve_selector(selector)
        if isinstance(path, PathLike):
            files = self._get_files(path, *extra_paths)
            name = ""
            mimeType = ""
            buffer = ""
        else:
            if extra_paths:
                raise ValueError(
                    "Extra paths are not supported when using FileUploadBuffer as path."
                )
            files = []
            name = path["name"]
            mimeType = path["mimeType"]
            buffer = path["buffer"]
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFileBySelector(
                _get_file_by_selectors(
                    files, selector, self.strict_mode, name, mimeType, buffer
                ),
            )
            logger.debug(response.log)

    def _get_files(
        self,
        path: PathLike,
        *extra_paths: PathLike,
    ) -> list:
        result_paths = []
        all_paths = [path, *list(extra_paths)]
        for item in all_paths:
            path_object = Path(item).resolve()
            if path_object.is_file():
                result_paths.extend([str(path_object)])
            elif path_object.is_dir():
                files = [
                    str(file.resolve())
                    for file in path_object.iterdir()
                    if file.is_file()
                ]
                result_paths.extend(files)
            else:
                raise ValueError(f"Nonexistent input file path '{path_object}'")
        logger.debug(f"Uploading files: {result_paths}")
        return result_paths


def _get_file_by_selectors(
    path: list, selector: str, strict: bool, name: str, mimeType: str, buffer: str
) -> Generator[Request.FileBySelector, None, None]:
    grpc_max_zize = 4000000
    if sys.getsizeof(buffer) > grpc_max_zize:
        for index in range(0, len(buffer), grpc_max_zize):
            yield Request().FileBySelector(
                selector=selector,
                strict=strict,
                path=path,
                name=name,
                mimeType=mimeType,
                buffer=buffer[index : index + grpc_max_zize],
            )
    else:
        yield Request().FileBySelector(
            selector=selector,
            strict=strict,
            path=path,
            name=name,
            mimeType=mimeType,
            buffer=buffer,
        )
