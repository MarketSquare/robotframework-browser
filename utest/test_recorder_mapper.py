import pytest

from Browser.recorder.action_mapper import (
    SILENT_ACTIONS,
    ActionMapper,
    to_browser_selector,
)
from Browser.recorder.model import RecordedKeyword


def rendered(action: dict) -> str | None:
    call = ActionMapper().map(action)
    return None if call is None else call.render()


@pytest.mark.parametrize(
    ("internal", "expected"),
    [
        ('internal:role=button[name="Submit"i]', 'role=button[name="Submit"i]'),
        # The public text engine has no `i` flag, so this is not a prefix swap.
        # Equivalences verified against a live Playwright 1.62 page.
        ('internal:text="Log in"i', "text=Log in"),
        ('internal:text="Log in"s', 'text="Log in"'),
        # Bodies that cannot be rewritten safely stay as the internal engine,
        # which `page.locator()` accepts verbatim.
        ('internal:text=" pad "i', 'internal:text=" pad "i'),
        ('internal:text="/re/"i', 'internal:text="/re/"i'),
        ('internal:text="say \\"hi\\""i', 'internal:text="say \\"hi\\""i'),
        ("internal:text=/^Log in$/i", "internal:text=/^Log in$/i"),
        ('internal:label="Email"i', 'internal:label="Email"i'),
        ('internal:testid=[data-testid="login"]', '[data-testid="login"]'),
        ('internal:attr=[placeholder="Email"i]', '[placeholder="Email"i]'),
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
    ],
)
def test_to_browser_selector(internal, expected):
    assert to_browser_selector(internal) == expected


def test_map_click_plain():
    action = {
        "name": "click",
        "selector": 'internal:role=button[name="OK"i]',
        "button": "left",
        "clickCount": 1,
        "modifiers": 0,
    }
    assert rendered(action) == 'Click    role=button[name="OK"i]'


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
    assert rendered(action) == 'Fill Text    [placeholder="Email"i]    a@b.c'


def test_map_navigate_is_always_go_to():
    # A recorded keyword must not create the page it runs in, so `navigate`
    # never becomes `New Page` - and the mapper stays stateless, which matters
    # because `actionUpdated` re-maps the same action repeatedly.
    assert rendered({"name": "navigate", "url": "http://a"}) == "Go To    http://a"
    assert rendered({"name": "navigate", "url": "http://b"}) == "Go To    http://b"


def test_map_hover():
    action = {"name": "hover", "selector": 'internal:role=link[name="Docs"i]'}
    assert rendered(action) == 'Hover    role=link[name="Docs"i]'


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


def test_unknown_action_returns_none():
    assert ActionMapper().map({"name": "assertSnapshot", "selector": "x"}) is None


def test_open_page_produces_nothing():
    assert ActionMapper().map({"name": "openPage", "url": "https://x"}) is None
    assert "openPage" in SILENT_ACTIONS


def test_selector_and_fixed_values_are_not_selectable():
    call = ActionMapper().map({"name": "select", "selector": "#s", "options": ["a"]})
    assert [v.selectable for v in call.args] == [False, False, True]


def test_fill_text_is_selectable():
    call = ActionMapper().map({"name": "fill", "selector": "#n", "text": "Al"})
    assert [v.selectable for v in call.args] == [False, True]


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
