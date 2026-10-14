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

import json
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


# A text body: a JSON-quoted string with an optional flag, or a regex.
_QUOTED_TEXT_RE = re.compile(r'^("(?:[^"\\]|\\.)*")([is]?)$')
_REGEX_TEXT_RE = re.compile(r"^/(.+)/([a-z]*)$", re.DOTALL)
_REGEX_SPECIALS = re.compile(r"[\\^$.*+?()[\]{}|/]")


def _text_pattern(text: str) -> str:
    """A JS regex source for ``text`` that tolerates the whitespace Playwright
    normalizes away: Playwright compares ``text`` with the element's text after
    collapsing whitespace, a regex sees the text as it is."""
    escaped = _REGEX_SPECIALS.sub(lambda m: "\\" + m.group(), text)
    return r"\s+".join(escaped.split(" "))


def _exact_pattern(text: str) -> str:
    return r"^\s*" + _text_pattern(text) + r"\s*$"


@dataclass(frozen=True)
class _TextBody:
    """A parsed text selector body: a literal, exact or not, or a regex."""

    value: str
    exact: bool = False
    regex_flags: str | None = None


def _parse_text(body: str) -> _TextBody | None:
    if regex := _REGEX_TEXT_RE.match(body):
        return _TextBody(regex.group(1), regex_flags=regex.group(2))
    quoted = _QUOTED_TEXT_RE.match(body)
    if quoted is None:
        return None
    try:
        text = json.loads(quoted.group(1))
    except ValueError:
        return None
    if not isinstance(text, str) or not text or text != " ".join(text.split()):
        return None
    # Like Playwright: a quoted body without the `i` flag is exact.
    return _TextBody(text, exact=quoted.group(2) != "i")


def _translate_text(body: str) -> str | None:
    """Public `text=` equivalent of an `internal:text=` body, or None.

    Verified against Playwright 1.64 (`createTextMatcher`): the internal engine
    compares the element's whole normalized text - exactly with `s`, as a
    case-insensitive substring with `i` - and the public `text=X` does the
    latter too. The public `text="X"` compares only the element's own text
    nodes, so an exact text becomes an anchored regex, which matches the same
    elements or, if the text contains characters Playwright strips, fewer.
    """
    parsed = _parse_text(body)
    if parsed is None:
        return None
    if parsed.regex_flags is not None:
        return f"text=/{parsed.value}/{parsed.regex_flags}"
    if parsed.exact:
        return f"text=/{_exact_pattern(parsed.value)}/"
    # Unquoted, the public engine reads a leading quote or slash as syntax and
    # `>>` as the next part of the chain.
    if parsed.value[0] in "\"'/" or ">>" in parsed.value:
        return f"text=/{_text_pattern(parsed.value)}/i"
    return f"text={parsed.value}"


def _css_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _translate_has_text(body: str) -> str | None:
    """Public pseudo-class for an `internal:has-text=` filter, or None.

    The internal engine keeps the element whose whole text matches. The public
    `:has-text("X")` is the same for a substring; for an exact text or a regex,
    `:text-matches()` additionally requires that no child element matches on
    its own, so it finds the same element or none, never another.
    """
    parsed = _parse_text(body)
    if parsed is None:
        return None
    if parsed.regex_flags is not None:
        flags = f", {_css_string(parsed.regex_flags)}" if parsed.regex_flags else ""
        return f":text-matches({_css_string(parsed.value)}{flags})"
    if parsed.exact:
        return f":text-matches({_css_string(_exact_pattern(parsed.value))})"
    return f":has-text({_css_string(parsed.value)})"


# `internal:attr=[placeholder="Email"i]` - one attribute, a quoted value and a flag.
_ATTRIBUTE_RE = re.compile(r'^\[([A-Za-z_][\w-]*)=("(?:[^"\\]|\\.)*")\s*([isIS]?)\]$')


def _translate_attribute(body: str) -> str | None:
    """CSS equivalent of an `internal:attr` / `internal:testid` body, or None.

    Verified against Playwright 1.64 (`createAttributeMatcher`): the `s` flag,
    like no flag, is an exact, case-sensitive match, which plain CSS `[a="v"]`
    is; the `i` flag is a case-insensitive *substring* match, which is
    `[a*="v"i]`. CSS knows no `s` flag, so `[a="v"s]` would not even parse.
    """
    match = _ATTRIBUTE_RE.match(body)
    if match is None:
        return None
    name, value, flag = match.groups()
    if flag.lower() != "i":
        return f"[{name}={value}]"
    # An empty substring matches every element in Playwright, none in CSS.
    if value == '""':
        return None
    return f"[{name}*={value}i]"


# One `[attribute=value]` of a role body: a quoted value with an optional flag,
# a regular expression, or a bare word (`level=2`, `pressed=true`, `include-hidden`).
_ROLE_ATTRIBUTE_RE = re.compile(
    r'\[([a-z-]+)(?:=(?:("(?:[^"\\]|\\.)*")\s*([isIS]?)|(/(?:[^/\\]|\\.)+/[a-z]*)|([\w.-]+)))?\]'
)
_ROLE_NAME_RE = re.compile(r"[a-z]+")


def _translate_role(body: str) -> str | None:
    """Public `role=` equivalent of an `internal:role=` body, or None.

    Verified against Playwright 1.64 (`queryRole`): the engines differ in one
    point only - the internal one matches a `name` or `description` without
    the `s` flag as a substring (`*=`), the public one exactly. So
    `[name="Save"i]` becomes `[name*="Save"i]`; everything else is kept.
    """
    role = _ROLE_NAME_RE.match(body)
    if role is None:
        return None
    out = [role.group()]
    position = role.end()
    while position < len(body):
        attribute = _ROLE_ATTRIBUTE_RE.match(body, position)
        if attribute is None:
            return None
        name, quoted, flag = attribute.group(1, 2, 3)
        if (
            quoted is not None
            and name in ("name", "description")
            and flag.lower() == "i"
        ):
            out.append(f"[{name}*={quoted}i]")
        else:
            out.append(attribute.group())
        position = attribute.end()
    return "role=" + "".join(out)


def _translate_part(part: str) -> str:
    if part.startswith("internal:role="):
        return _translate_role(part[len("internal:role=") :]) or part
    if part.startswith("internal:text="):
        return _translate_text(part[len("internal:text=") :]) or part
    if part.startswith("internal:has-text="):
        return _translate_has_text(part[len("internal:has-text=") :]) or part
    for engine in ("internal:testid=", "internal:attr="):
        if part.startswith(engine):
            return _translate_attribute(part[len(engine) :]) or part
    # Everything else passes through: Playwright's locator parser accepts its
    # own internal engines verbatim, so this is always correct, just less readable.
    return part


def to_browser_selector(selector: str) -> str:
    """Convert a Playwright internal selector into a Browser selector."""
    if not selector:
        return selector
    parts = _split_parts(selector)
    translated = [_translate_part(p) for p in parts]
    # Rebuild, turning frame boundaries into Browser's ">>>" piercing separator
    # and attaching a text filter to the part it filters.
    out: list[str] = []
    for part in translated:
        if part == _ENTER_FRAME:
            if out:
                out[-1] = out[-1] + " >>>"
        elif not part.startswith(":"):
            out.append(part)
        elif out and _is_plain_css(out[-1]):
            out[-1] += part
        else:
            out.append(":scope" + part)
    return " >> ".join(out).replace(" >>> >> ", " >>> ")


# A css part a pseudo-class can be appended to: no engine prefix, no list.
_ENGINE_PREFIX_RE = re.compile(r"^[\w-]+=")


def _is_plain_css(part: str) -> bool:
    return (
        not part.endswith(">>>")
        and (part.startswith("css=") or not _ENGINE_PREFIX_RE.match(part))
        and "," not in part
        and not part.startswith(("//", ".."))
    )


def internal_engines(selector: str) -> list[str]:
    """The Playwright-internal engines a translated selector still uses."""
    return [
        part.split("=", 1)[0]
        for part in _split_parts(selector.replace(">>>", ">>"))
        if part.startswith("internal:")
    ]


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
    return Value.literal(to_browser_selector(action.get("selector", "")))


def _fixed(text: str) -> Value:
    return Value.literal(text, selectable=False)


def _named(text: str) -> Value:
    return Value([text], selectable=False, named=True)


def _data(text: object) -> Value:
    return Value.literal("" if text is None else str(text))


def internal_selector_notice(action: dict) -> str | None:
    """The toolbar notice for an Action whose selector stays Playwright-internal."""
    selector = action.get("selector")
    engines = (
        internal_engines(to_browser_selector(selector))
        if isinstance(selector, str)
        else []
    )
    if not engines:
        return None
    return (
        f"The selector uses Playwright-internal syntax ({', '.join(dict.fromkeys(engines))}), "
        "which has no public equivalent and may break with a Playwright upgrade."
    )


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
                [Call("Handle Future Dialogs", [_named("action=accept")])], []
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
            args.append(_named(f"clickCount={count}"))
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
