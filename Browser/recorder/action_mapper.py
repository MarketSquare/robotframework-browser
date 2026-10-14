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
"""Translate Playwright recorder actions into Browser keyword calls.

Two pure, side-effect-free pieces (unit tested without a browser):

* :func:`to_browser_selector` - turn a Playwright *internal* selector string
  (``internal:role=button[name="Submit"i] >> ...``) into a selector that
  Browser understands. Browser resolves selectors via ``page.locator(selector)``
  (``node/playwright-wrapper/playwright-invoke.ts``), so Playwright's public
  engine prefixes (``role=``, ``text=``, css attribute selectors, ...) work as
  is, and frame boundaries map to Browser's ``>>>`` piercing separator.

* :class:`ActionMapper` - map a single recorded action (a ``dict`` matching
  Playwright's ``actions.d.ts``) to a :class:`~Browser.recorder.model.Call`, or
  ``None`` when the action has no sensible keyword representation.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar

from .model import ArgRef, Call, Value

# --------------------------------------------------------------------------- #
# Selector translation
# --------------------------------------------------------------------------- #

_ENTER_FRAME = "internal:control=enter-frame"


def _split_parts(selector: str) -> list[str]:
    """Split on the top-level `` >> `` combinator, never inside quotes or brackets."""
    parts: list[str] = []
    depth = 0
    quote = ""
    buf = ""
    i = 0
    while i < len(selector):
        ch = selector[i]
        ahead = selector[i : i + 4]
        if quote:
            buf += ch
            if ch == quote:
                quote = ""
        elif ch in ('"', "'"):
            quote = ch
            buf += ch
        elif ch == "[":
            depth += 1
            buf += ch
        elif ch == "]":
            depth = max(0, depth - 1)
            buf += ch
        elif depth == 0 and ahead == " >> ":
            parts.append(buf)
            buf = ""
            i += 4
            continue
        else:
            buf += ch
        i += 1
    if buf:
        parts.append(buf)
    return [p.strip() for p in parts if p.strip()]


# `internal:text="Log in"i` - the quoted body plus a case-sensitivity flag.
# Only a body without quotes, backslashes or edge whitespace can be rewritten
# to the public `text=` engine without changing what it matches.
_TEXT_RE = re.compile(r'^internal:text="([^"\\]*)"([is])$')


def _translate_text(body: str, flag: str) -> str | None:
    """Public `text=` equivalent of an `internal:text=` body, or None.

    Verified against Playwright 1.63 (identical match sets):
    `internal:text="X"i` == `text=X` (substring, case-insensitive) and
    `internal:text="X"s` == `text="X"` (exact, case-sensitive).

    Note that `text="X"i` is *not* valid - the public text engine has no `i`
    flag - which is why this cannot be a plain prefix swap.
    """
    if not body or body != body.strip():
        return None
    if flag == "s":
        return f'text="{body}"'
    # An unquoted body starting with "/" would be parsed as a regex.
    if body.startswith("/"):
        return None
    return f"text={body}"


def _translate_part(part: str) -> str:
    # `role` has a public engine with identical body syntax.
    if part.startswith("internal:role="):
        return "role=" + part[len("internal:role=") :]
    if match := _TEXT_RE.match(part):
        return _translate_text(*match.groups()) or part
    # testid / attr bodies are already `[attr="value"]` css selectors.
    if part.startswith("internal:testid="):
        return part[len("internal:testid=") :]
    if part.startswith("internal:attr="):
        return part[len("internal:attr=") :]
    # Everything else passes through: Playwright's locator parser accepts its
    # own internal engines verbatim, so this is always correct, just less readable.
    return part


def to_browser_selector(selector: str) -> str:
    """Convert a Playwright internal selector into a Browser selector."""
    if not selector:
        return selector
    parts = _split_parts(selector)
    translated = [_translate_part(p) for p in parts]
    # Rebuild, turning frame boundaries into Browser's ">>>" piercing separator.
    out: list[str] = []
    for part in translated:
        if part == _ENTER_FRAME:
            if out:
                out[-1] = out[-1] + " >>>"
            continue
        out.append(part)
    return " >> ".join(out).replace(" >>> >> ", " >>> ")


# --------------------------------------------------------------------------- #
# Keyboard modifier bitmask (see Playwright toKeyboardModifiers)
# --------------------------------------------------------------------------- #

_MODIFIERS = [(1, "Alt"), (2, "Control"), (4, "Meta"), (8, "Shift")]


def _modifier_names(mask: int) -> list[str]:
    return [name for bit, name in _MODIFIERS if mask & bit]


# --------------------------------------------------------------------------- #
# Action -> keyword mapping
# --------------------------------------------------------------------------- #


#: Actions that never produce a Keyword Call and need no notice: Playwright
#: reports `openPage` for pages that already exist and for tabs opened by hand,
#: and a page opened by an Action arrives as a `popup` signal on that Action.
SILENT_ACTIONS = frozenset({"openPage"})


@dataclass
class SignalEffect:
    before: list[Call]
    after: list[Call]


def _selector(action: dict) -> Value:
    return Value.literal(
        to_browser_selector(action.get("selector", "")), selectable=False
    )


def _fixed(text: str) -> Value:
    return Value.literal(text, selectable=False)


def _data(text: object) -> Value:
    return Value.literal("" if text is None else str(text))


class ActionMapper:
    """Map recorded Playwright actions to Browser Keyword Calls.

    Stateless: Playwright's recorder refines an action *in place* (see
    ``actionUpdated``), so a mapper that remembered previous actions would give
    a different answer for the same action depending on how often it was
    re-mapped.
    """

    def map(self, action: dict) -> Call | None:
        handler = self._HANDLERS.get(action.get("name", ""))
        return None if handler is None else handler(self, action)

    def map_signal(
        self, signal: dict, unique: Callable[[str], str]
    ) -> SignalEffect | None:
        """The Keyword Calls a signal adds around the Action that raised it.

        Playwright reports dialogs, downloads and popups *after* the Action, but
        Browser needs dialog handling and the download promise *before* it.
        """
        name = signal.get("name")
        if name == "popup":
            return SignalEffect([], [Call("Switch Page", [_fixed("NEW")])])
        if name == "dialog":
            return SignalEffect(
                [Call("Handle Future Dialogs", [_fixed("action=accept")])], []
            )
        if name == "download":
            variable = unique("download")
            return SignalEffect(
                [Call("Promise To Wait For Download", [], assign=variable)],
                [Call("Wait For", [Value([ArgRef(variable)], selectable=False)])],
            )
        return None

    # -- navigation -------------------------------------------------------- #

    def _map_navigate(self, action: dict) -> Call:
        # A recorded keyword is reusable only if it does not create the page it
        # runs in - browser/page setup stays the caller's job, so an in-page
        # navigation is always `Go To`.
        return Call("Go To", [_data(action.get("url", ""))])

    def _map_close_page(self, action: dict) -> Call:
        return Call("Close Page", [])

    # -- interaction ------------------------------------------------------- #

    def _map_click(self, action: dict) -> Call:
        selector = _selector(action)
        button = action.get("button", "left")
        count = action.get("clickCount", 1)
        modifiers = _modifier_names(action.get("modifiers", 0))
        if button == "left" and count == 1 and not modifiers:
            return Call("Click", [selector])
        args = [selector]
        # `button` is positional before *modifiers, so it must be present
        # whenever a modifier follows it, even if it is the default "left".
        if button != "left" or modifiers:
            args.append(_fixed(button))
        args.extend(_fixed(m) for m in modifiers)
        if count > 1:
            args.append(_fixed(f"clickCount={count}"))
        return Call("Click With Options", args)

    def _map_fill(self, action: dict) -> Call:
        return Call("Fill Text", [_selector(action), _data(action.get("text", ""))])

    def _map_press(self, action: dict) -> Call:
        # `Press Keys` chains modifiers with "+", e.g. `Control+Shift+T`.
        keys = [*_modifier_names(action.get("modifiers", 0)), action.get("key", "")]
        return Call(
            "Press Keys", [_selector(action), _data("+".join(k for k in keys if k))]
        )

    def _map_check(self, action: dict) -> Call:
        return Call("Check Checkbox", [_selector(action)])

    def _map_uncheck(self, action: dict) -> Call:
        return Call("Uncheck Checkbox", [_selector(action)])

    def _map_select(self, action: dict) -> Call:
        return Call(
            "Select Options By",
            [
                _selector(action),
                _fixed("value"),
                *(_data(o) for o in action.get("options", [])),
            ],
        )

    # -- assertions -------------------------------------------------------- #

    def _map_assert_text(self, action: dict) -> Call:
        operator = "contains" if action.get("substring") else "=="
        return Call(
            "Get Text",
            [_selector(action), _fixed(operator), _data(action.get("text", ""))],
        )

    def _map_assert_value(self, action: dict) -> Call:
        return Call(
            "Get Property",
            [
                _selector(action),
                _fixed("value"),
                _fixed("=="),
                _data(action.get("value", "")),
            ],
        )

    def _map_assert_checked(self, action: dict) -> Call:
        state = "checked" if action.get("checked") else "unchecked"
        return Call(
            "Get Checkbox State", [_selector(action), _fixed("=="), _data(state)]
        )

    def _map_assert_visible(self, action: dict) -> Call:
        return Call(
            "Get Element States", [_selector(action), _fixed("*="), _fixed("visible")]
        )

    def _map_assert_snapshot(self, action: dict) -> Call:
        # Playwright's snapshot is a multi-line YAML string; `yaml` + `==` is an
        # exact comparison of it.
        return Call(
            "Get Aria Snapshot",
            [
                _selector(action),
                _fixed("yaml"),
                _fixed("=="),
                _data(action.get("ariaSnapshot", "")),
            ],
        )

    # Maps a Playwright action name (see actions.d.ts) to its handler.
    _HANDLERS: ClassVar[dict[str, Callable[[ActionMapper, dict], Call]]] = {
        "navigate": _map_navigate,
        "closePage": _map_close_page,
        "click": _map_click,
        "fill": _map_fill,
        "press": _map_press,
        "check": _map_check,
        "uncheck": _map_uncheck,
        "select": _map_select,
        "assertText": _map_assert_text,
        "assertValue": _map_assert_value,
        "assertChecked": _map_assert_checked,
        "assertVisible": _map_assert_visible,
        "assertSnapshot": _map_assert_snapshot,
    }
