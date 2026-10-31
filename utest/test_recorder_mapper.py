import json
import subprocess
import sys

import pytest

from Browser.recorder.action_mapper import (
    SILENT_ACTIONS,
    ActionMapper,
    internal_selector_notice,
    to_browser_selector,
)
from Browser.recorder.model import RecordedKeyword


def rendered(action: dict) -> str | None:
    call = ActionMapper().map(action)
    return None if call is None else call.render()


@pytest.mark.parametrize(
    ("internal", "expected"),
    [
        # The internal role engine matches a name without `s` as a substring;
        # the public one needs `*=` for that. Verified against Playwright 1.64.
        ('internal:role=button[name="Submit"i]', 'role=button[name*="Submit"i]'),
        ('internal:role=button[name="Submit"s]', 'role=button[name="Submit"s]'),
        ('internal:role=button[name="Submit"]', 'role=button[name="Submit"]'),
        ("internal:role=button[name=/^Sub/i]", "role=button[name=/^Sub/i]"),
        (
            'internal:role=heading[name="A ] \\" b"i][level=2]',
            'role=heading[name*="A ] \\" b"i][level=2]',
        ),
        (
            'internal:role=checkbox[checked=true][include-hidden][description="d"I]',
            'role=checkbox[checked=true][include-hidden][description*="d"i]',
        ),
        ("internal:role=button[name=unclosed", "internal:role=button[name=unclosed"),
        # `i` is a case-insensitive substring of the whole text, which public
        # `text=X` is too; an exact text becomes an anchored regex, because the
        # public `text="X"` looks at the element's own text nodes only.
        # Verified against Playwright 1.64 by the "Translated Selectors Match
        # Like Playwright" acceptance test.
        ('internal:text="Log in"i', "text=Log in"),
        ('internal:text="Log in"s', r"text=/^\s*Log\s+in\s*$/"),
        ('internal:text="Log in"', r"text=/^\s*Log\s+in\s*$/"),
        ('internal:text="/re/"i', r"text=/\/re\//i"),
        ('internal:text="a >> b"i', r"text=/a\s+>>\s+b/i"),
        ('internal:text="say \\"hi\\" (1.5)"i', 'text=say "hi" (1.5)'),
        ('internal:text="\\"quoted\\""i', r'text=/"quoted"/i'),
        ("internal:text=/^Log in$/i", "text=/^Log in$/i"),
        ('internal:text=" pad "i', 'internal:text=" pad "i'),
        # A text filter is attached to the css part it filters.
        ('div >> internal:has-text="Twin"i', 'div:has-text("Twin")'),
        ("div >> internal:has-text=/^Twin$/", 'div:text-matches("^Twin$")'),
        ("div >> internal:has-text=/^a\\/b$/i", 'div:text-matches("^a\\\\/b$", "i")'),
        ('div >> internal:has-text="Twin"s', r'div:text-matches("^\\s*Twin\\s*$")'),
        (
            'internal:role=paragraph >> internal:has-text="Card one"i >> i',
            'role=paragraph >> :scope:has-text("Card one") >> i',
        ),
        # Browser's label engine takes Playwright's values as they are.
        ('internal:label="Email"i', 'label="Email"i'),
        ('internal:label="Email"s', 'label="Email"s'),
        ("internal:label=/e-?mail/i", "label=/e-?mail/i"),
        # `s` is exact and case-sensitive (CSS has no `s` flag), `i` is a
        # case-insensitive substring. Verified against Playwright 1.64.
        ('internal:testid=[data-testid="login"s]', '[data-testid="login"]'),
        ('internal:attr=[placeholder="Email"s]', '[placeholder="Email"]'),
        ('internal:attr=[placeholder="Email"i]', '[placeholder*="Email"i]'),
        ('internal:attr=[title="say \\"hi\\""i]', '[title*="say \\"hi\\""i]'),
        ('internal:attr=[alt=""i]', 'internal:attr=[alt=""i]'),
        ("internal:attr=[alt=/re/]", "internal:attr=[alt=/re/]"),
        (
            'internal:testid=[data-testid="main"s] >> internal:role=button[name="Open Report"i]',
            '[data-testid="main"] >> role=button[name*="Open Report"i]',
        ),
        ("css=.foo", "css=.foo"),
        ("//button", "//button"),
        # chaining is preserved
        (
            'internal:role=listitem >> internal:text="Item"i',
            "role=listitem >> text=Item",
        ),
        # frame boundary becomes Browser's ">>>" piercing separator
        (
            'internal:attr=[id="frame"] >> internal:control=enter-frame >> internal:role=textbox',
            '[id="frame"] >>> role=textbox',
        ),
        # a shortened path to a deep frame becomes a leading ">>>"
        (
            'internal:control=any-frame >> internal:attr=[name="b"s]'
            ' >> internal:control=enter-frame >> internal:label="Pin"i',
            '>>> [name="b"] >>> label="Pin"i',
        ),
        ("internal:control=any-frame >> internal:role=button", ">>> role=button"),
        # a frame separator inside a quoted value is text
        (
            'internal:role=button[name="a >>> >> b"i]',
            'role=button[name*="a >>> >> b"i]',
        ),
        (
            'internal:attr=[id="f"s] >> internal:control=enter-frame >> div'
            ' >> internal:has-text="x"i',
            '[id="f"] >>> div:has-text("x")',
        ),
        # a line break in an attribute value is no valid CSS string: kept internal
        ('internal:attr=[title="a\nb"s]', 'internal:attr=[title="a\nb"s]'),
    ],
)
def test_to_browser_selector(internal, expected):
    assert to_browser_selector(internal) == expected


@pytest.mark.parametrize(
    ("selector", "engines"),
    [
        ('internal:label="Map"i', []),
        ('internal:text="Map"i', []),
        ("internal:control=any-frame >> internal:role=button", []),
        ('internal:attr=[alt=""i] >> internal:attr=[alt=/x/]', ["internal:attr"]),
    ],
)
def test_internal_selector_notice_names_the_engines_left(selector, engines):
    notice = internal_selector_notice({"name": "click", "selector": selector})
    if not engines:
        assert notice is None
    else:
        assert f"({', '.join(engines)})" in notice
    assert internal_selector_notice({"name": "navigate", "url": "x"}) is None


def test_map_click_plain():
    action = {
        "name": "click",
        "selector": 'internal:role=button[name="OK"i]',
        "button": "left",
        "clickCount": 1,
        "modifiers": 0,
    }
    assert rendered(action) == 'Click    role=button[name*="OK"i]'


def test_map_double_click():
    action = {
        "name": "click",
        "selector": "css=.x",
        "button": "left",
        "clickCount": 2,
        "modifiers": 0,
    }
    assert rendered(action) == "Click With Options    css=.x    clickCount=2"


def test_map_right_click_with_modifier():
    action = {
        "name": "click",
        "selector": "css=.x",
        "button": "right",
        "clickCount": 1,
        "modifiers": 8,
    }  # Shift
    assert rendered(action) == "Click With Options    css=.x    right    Shift"


def test_map_fill():
    action = {
        "name": "fill",
        "selector": 'internal:attr=[placeholder="Email"i]',
        "text": "a@b.c",
    }
    assert rendered(action) == 'Fill Text    [placeholder*="Email"i]    a@b.c'


@pytest.mark.parametrize(
    "selector",
    [
        'internal:attr=[type="password"i]',
        'internal:label="Password"i',
        "input[type=password]",
    ],
)
def test_fill_on_a_password_field_keeps_the_typed_value_verbatim(selector):
    # Password fields get no special treatment - no Fill Secret, no masking.
    line = rendered({"name": "fill", "selector": selector, "text": "hunter2"})
    assert line.startswith("Fill Text    ")
    assert line.endswith("    hunter2")
    assert "Secret" not in line


def test_map_navigate_is_always_go_to():
    # A recorded keyword must not create the page it runs in, so `navigate`
    # never becomes `New Page` - and the mapper stays stateless, which matters
    # because `actionUpdated` re-maps the same action repeatedly.
    assert rendered({"name": "navigate", "url": "http://a"}) == "Go To    http://a"
    assert rendered({"name": "navigate", "url": "http://b"}) == "Go To    http://b"


def test_map_press_plain():
    action = {"name": "press", "selector": "css=.x", "key": "Enter", "modifiers": 0}
    assert rendered(action) == "Press Keys    css=.x    Enter"


def test_map_press_with_modifiers():
    # `Press Keys` chains modifiers with "+".
    action = {"name": "press", "selector": "css=.x", "key": "A", "modifiers": 2 | 8}
    assert rendered(action) == "Press Keys    css=.x    Control+Shift+A"


def test_map_select():
    action = {"name": "select", "selector": "css=select", "options": ["1", "2"]}
    assert rendered(action) == "Select Options By    css=select    value    1    2"


def test_map_assert_text_substring():
    action = {
        "name": "assertText",
        "selector": "css=.msg",
        "text": "Hi",
        "substring": True,
    }
    assert rendered(action) == "Get Text    css=.msg    contains    Hi"


def test_map_assert_checked():
    action = {"name": "assertChecked", "selector": "css=.c", "checked": False}
    assert rendered(action) == "Get Checkbox State    css=.c    ==    unchecked"


def test_map_assert_visible_is_get_element_states_contains_visible():
    call = ActionMapper().map({"name": "assertVisible", "selector": "css=#a"})
    assert call is not None
    assert call.render() == "Get Element States    css=#a    *=    visible"
    assert [v.selectable for v in call.args] == [True, False, False]


def test_unknown_action_returns_none():
    assert ActionMapper().map({"name": "somethingNew", "selector": "x"}) is None


SNAPSHOT = '- heading "Hi" [level=1]\n- button "Save  now"'


def test_map_assert_snapshot_is_get_aria_snapshot_with_exact_yaml():
    action = {"name": "assertSnapshot", "selector": "css=#a", "ariaSnapshot": SNAPSHOT}
    call = ActionMapper().map(action)
    assert call is not None
    assert call.keyword == "Get Aria Snapshot"
    assert [(v.text, v.selectable) for v in call.args] == [
        ("css=#a", True),
        ("yaml", False),
        ("==", False),
        (SNAPSHOT, True),
    ]


def test_assert_snapshot_renders_as_one_cell_and_roundtrips_through_robot(tmp_path):
    call = ActionMapper().map(
        {"name": "assertSnapshot", "selector": "css=#a", "ariaSnapshot": SNAPSHOT}
    )
    line = call.render()
    assert "\n" not in line
    (tmp_path / "Spy.py").write_text(
        "import json, pathlib\n"
        "def get_aria_snapshot(*args):\n"
        "    pathlib.Path(__file__).with_name('args.json').write_text(json.dumps(args))\n"
    )
    (tmp_path / "run.robot").write_text(
        "*** Settings ***\nLibrary    Spy.py\n\n*** Keywords ***\n"
        + "Recorded\n    "
        + line
        + "\n\n*** Test Cases ***\nT\n    Recorded\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), "run.robot"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / "args.json").read_text()) == [
        "css=#a",
        "yaml",
        "==",
        SNAPSHOT,
    ]


def test_open_page_produces_nothing():
    assert ActionMapper().map({"name": "openPage", "url": "https://x"}) is None
    assert "openPage" in SILENT_ACTIONS


def test_selectors_are_selectable_fixed_values_are_not():
    call = ActionMapper().map({"name": "select", "selector": "#s", "options": ["a"]})
    assert [v.selectable for v in call.args] == [True, False, True]
    click = ActionMapper().map(
        {"name": "click", "selector": "#b", "button": "right", "clickCount": 2}
    )
    assert [v.selectable for v in click.args] == [True, False, False]


def test_pressed_keys_and_expected_checkbox_state_are_selectable():
    press = ActionMapper().map(
        {"name": "press", "selector": "#n", "key": "Enter", "modifiers": 0}
    )
    assert [v.selectable for v in press.args] == [True, True]
    checked = ActionMapper().map(
        {"name": "assertChecked", "selector": "#c", "checked": True}
    )
    assert [v.selectable for v in checked.args] == [True, False, True]


def test_fill_text_is_selectable():
    call = ActionMapper().map({"name": "fill", "selector": "#n", "text": "Al"})
    assert [v.selectable for v in call.args] == [True, True]


def test_popup_signal_switches_to_the_new_page():
    effect = ActionMapper().map_signal({"name": "popup"}, lambda b: b)
    assert [c.render() for c in effect.after] == ["Switch Page    NEW"]
    assert effect.before == []


def test_dialog_signal_accepts_before_the_action():
    effect = ActionMapper().map_signal({"name": "dialog"}, lambda b: b)
    assert [c.render() for c in effect.before] == [
        "Handle Future Dialogs    action=accept"
    ]


def test_download_signal_wraps_the_action():
    kw = RecordedKeyword("K")
    effect = ActionMapper().map_signal({"name": "download"}, kw.unique_variable)
    assert [c.render() for c in effect.before] == [
        "${download}=    Promise To Wait For Download"
    ]
    assert [c.render() for c in effect.after] == ["Wait For    ${download}"]


@pytest.mark.parametrize("name", ["expect", "navigation", "unknown"])
def test_other_signals_produce_nothing(name):
    assert ActionMapper().map_signal({"name": name}, lambda b: b) is None
