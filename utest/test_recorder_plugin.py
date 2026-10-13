import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder.action_mapper import ActionMapper, to_browser_selector
from Browser.recorder.keyword_writer import LiveKeywordWriter
from Browser.recorder.names import existing_keyword_names

# --------------------------------------------------------------------------- #
# Selector translation
# --------------------------------------------------------------------------- #


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


# --------------------------------------------------------------------------- #
# Action mapping
# --------------------------------------------------------------------------- #


def test_map_click_plain():
    mapper = ActionMapper()
    action = {
        "name": "click",
        "selector": 'internal:role=button[name="OK"i]',
        "button": "left",
        "clickCount": 1,
        "modifiers": 0,
    }
    assert mapper.map(action) == ("Click", ['role=button[name="OK"i]'])


def test_map_double_click():
    mapper = ActionMapper()
    action = {
        "name": "click",
        "selector": "css=.x",
        "button": "left",
        "clickCount": 2,
        "modifiers": 0,
    }
    assert mapper.map(action) == ("Click With Options", ["css=.x", "clickCount=2"])


def test_map_right_click_with_modifier():
    mapper = ActionMapper()
    action = {
        "name": "click",
        "selector": "css=.x",
        "button": "right",
        "clickCount": 1,
        "modifiers": 8,
    }  # Shift
    assert mapper.map(action) == ("Click With Options", ["css=.x", "right", "Shift"])


def test_map_fill():
    mapper = ActionMapper()
    action = {
        "name": "fill",
        "selector": 'internal:attr=[placeholder="Email"i]',
        "text": "a@b.c",
    }
    assert mapper.map(action) == ("Fill Text", ['[placeholder="Email"i]', "a@b.c"])


def test_map_navigate_is_always_go_to():
    # A recorded keyword must not create the page it runs in, so `navigate`
    # never becomes `New Page` - and the mapper stays stateless, which matters
    # because `actionUpdated` re-maps the same action repeatedly.
    mapper = ActionMapper()
    assert mapper.map({"name": "navigate", "url": "http://a"}) == (
        "Go To",
        ["http://a"],
    )
    assert mapper.map({"name": "navigate", "url": "http://b"}) == (
        "Go To",
        ["http://b"],
    )


def test_map_open_page():
    assert ActionMapper().map({"name": "openPage", "url": "http://a"}) == (
        "New Page",
        ["http://a"],
    )


def test_map_hover():
    action = {"name": "hover", "selector": 'internal:role=link[name="Docs"i]'}
    assert ActionMapper().map(action) == ("Hover", ['role=link[name="Docs"i]'])


def test_map_press_plain():
    action = {"name": "press", "selector": "css=.x", "key": "Enter", "modifiers": 0}
    assert ActionMapper().map(action) == ("Press Keys", ["css=.x", "Enter"])


def test_map_press_with_modifiers():
    # `Press Keys` chains modifiers with "+".
    action = {"name": "press", "selector": "css=.x", "key": "A", "modifiers": 2 | 8}
    assert ActionMapper().map(action) == ("Press Keys", ["css=.x", "Control+Shift+A"])


def test_map_select():
    mapper = ActionMapper()
    action = {"name": "select", "selector": "css=select", "options": ["1", "2"]}
    assert mapper.map(action) == (
        "Select Options By",
        ["css=select", "value", "1", "2"],
    )


def test_map_assert_text_substring():
    mapper = ActionMapper()
    action = {
        "name": "assertText",
        "selector": "css=.msg",
        "text": "Hi",
        "substring": True,
    }
    assert mapper.map(action) == ("Get Text", ["css=.msg", "contains", "Hi"])


def test_map_assert_checked():
    mapper = ActionMapper()
    action = {"name": "assertChecked", "selector": "css=.c", "checked": False}
    assert mapper.map(action) == ("Get Checkbox State", ["css=.c", "==", "unchecked"])


def test_unknown_action_returns_none():
    assert ActionMapper().map({"name": "assertSnapshot", "selector": "x"}) is None


# --------------------------------------------------------------------------- #
# Live keyword writer (Robot Framework AST)
# --------------------------------------------------------------------------- #


def test_writer_creates_file_and_appends_live():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "out.resource"
        writer = LiveKeywordWriter(target, "Login As Admin")
        writer.append("New Page", ["http://localhost"])
        # file is written after the first action already (live)
        assert target.exists()
        writer.append("Fill Text", ['role=textbox[name="User"i]', "admin"])
        writer.append("Click", ['role=button[name="Login"i]'])

        content = target.read_text()
        assert "*** Keywords ***" in content
        assert "Login As Admin" in content
        assert "New Page    http://localhost" in content
        assert 'Fill Text    role=textbox[name="User"i]    admin' in content
        assert 'Click    role=button[name="Login"i]' in content


def test_writer_appends_to_existing_file_preserving_content():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.robot"
        target.write_text(
            "*** Settings ***\nLibrary    Browser\n\n"
            "*** Test Cases ***\nMy Test\n    Log    hello\n"
        )
        writer = LiveKeywordWriter(target, "Recorded")
        writer.append("Click", ["css=.btn"])
        content = target.read_text()
        # original content preserved
        assert "Library    Browser" in content
        assert "My Test" in content
        assert "Log    hello" in content
        # new keyword added
        assert "*** Keywords ***" in content
        assert "Recorded" in content
        assert "Click    css=.btn" in content


def test_writer_empty_argument_uses_empty_marker():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "out.resource"
        writer = LiveKeywordWriter(target, "KW")
        writer.append("Fill Text", ["css=.x", ""])
        assert "Fill Text    css=.x    ${EMPTY}" in target.read_text()


#: Values a recording can realistically produce that also mean something to
#: the Robot parser. Each is written by the writer, then read back by actually
#: *running* Robot - escapes are resolved at run time, not at parse time, so
#: anything less than a real run would not prove the round trip.
_TWO = 2

_ROUNDTRIP_VALUES = [
    # A leading "#" starts a Robot comment - Playwright's recorder emits plenty
    # of `#id` selectors, and unescaped they vanish entirely.
    ["#pw"],
    ["css=.x", "a${b}"],
    ["css=.x", "@{a} &{b} %{c}"],
    # Two or more spaces are a cell separator, edge spaces are stripped.
    ["css=.x", "two    spaces"],
    ["css=.x", " padded "],
    ["css=.x", ""],
    ["css=.x", "   "],
    ["css=.x", "back\\slash"],
    ["css=.x", "\\${not a var}"],
    ["css=.x", "tab\tand\nnewline"],
    ['role=button[name="Save & exit"i]'],
    # -- hostile payloads ---------------------------------------------------- #
    # Selectors and typed text come from the page under test, so they are
    # attacker controlled. Robot's tokenizer splits cells on `\s{2,}` with
    # unicode semantics and its reader splits lines with `str.splitlines()`, so
    # an unescaped U+00A0 or U+2028 in an *argument* writes a second executable
    # keyword just as surely as one in a name. These must survive as data.
    ["css=.x", "x Evil Keyword  \xa0Log \xa0PWNED-ARG"],
    ["css=.x", "a\u2028Evil Keyword \xa0Log \xa0PWNED-ARG"],
    ["css=.x", "a\u2029Evil Keyword \xa0Log \xa0PWNED-ARG"],
    ["css=.x", "a\x85Evil Keyword\x85\xa0\xa0Log\xa0\xa0PWNED-ARG"],
    ["css=.x", "a\x1cEvil Keyword\x1c\u3000\u3000Log\u3000\u3000PWNED-ARG"],
    ["css=.x", "nbsp\xa0\xa0pair"],
    ["css=.x", "ideographic\u3000\u3000pair"],
    ["css=.x", "vertical\x0btab\x0cform"],
    ["css=.x", "| piped | row"],
    ["\xa0\xa0leading and trailing\xa0\xa0"],
]


def test_writer_roundtrips_values_through_a_real_robot_run(tmp_path):
    """Whatever was recorded must reach the keyword as exactly that value."""
    (tmp_path / "ArgSpy.py").write_text(
        "import json, pathlib\n"
        "CALLS = []\n"
        "def spy(*args):\n"
        "    CALLS.append(list(args))\n"
        "    pathlib.Path(__file__).with_name('calls.json').write_text(json.dumps(CALLS))\n"
    )
    resource = tmp_path / "recorded.resource"
    writer = LiveKeywordWriter(resource, "Recorded")
    for value in _ROUNDTRIP_VALUES:
        writer.append("Spy", value)

    (tmp_path / "run.robot").write_text(
        "*** Settings ***\n"
        "Library     ArgSpy.py\n"
        "Resource    recorded.resource\n\n"
        "*** Test Cases ***\n"
        "T\n"
        "    Recorded\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), "run.robot"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / "calls.json").read_text()) == _ROUNDTRIP_VALUES
    # A payload that smuggled a second keyword into the resource would still
    # let the arguments above round-trip, so check the *structure* too: Robot
    # must see exactly the one keyword the recorder meant to write.
    assert existing_keyword_names(resource) == {"Recorded"}


def test_writer_replace_last_overwrites_only_the_last_call():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "out.resource"
        writer = LiveKeywordWriter(target, "KW")
        writer.append("Click", ["css=.x"])
        writer.append("Fill Text", ["css=.i", "a"])
        writer.replace_last("Fill Text", ["css=.i", "abc"])

        content = target.read_text()
        assert "Click    css=.x" in content
        assert "Fill Text    css=.i    abc" in content
        assert "Fill Text    css=.i    a\n" not in content
        assert len(writer) == _TWO


def test_writer_replace_last_never_touches_pre_existing_content():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.resource"
        target.write_text("*** Keywords ***\nKW\n    Log    keep me\n")
        writer = LiveKeywordWriter(target, "KW")
        assert writer.reused
        # Nothing recorded yet -> must append instead of clobbering `Log`.
        writer.replace_last("Click", ["css=.x"])
        content = target.read_text()
        assert "Log    keep me" in content
        assert "Click    css=.x" in content


# --------------------------------------------------------------------------- #
# Undo, discard, lines()
# --------------------------------------------------------------------------- #


def test_writer_lines_returns_escaped_robot_cells():
    with tempfile.TemporaryDirectory() as tmp:
        writer = LiveKeywordWriter(Path(tmp) / "out.resource", "KW")
        writer.append("Click", ["#pw"])
        writer.append("Fill Text", ["css=.x", "a b"])
        assert writer.lines() == ["Click    \\#pw", "Fill Text    css=.x    a b"]


def test_writer_undo_last_removes_only_the_last_call():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "out.resource"
        writer = LiveKeywordWriter(target, "KW")
        writer.append("Click", ["css=.a"])
        writer.append("Click", ["css=.b"])
        assert writer.undo_last() is True
        assert len(writer) == 1
        content = target.read_text()
        assert "Click    css=.a" in content
        assert "Click    css=.b" not in content


def test_writer_undo_last_is_false_when_nothing_was_recorded():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.resource"
        target.write_text("*** Keywords ***\nKW\n    Log    keep me\n")
        writer = LiveKeywordWriter(target, "KW")
        assert writer.undo_last() is False
        assert "Log    keep me" in target.read_text()


def test_writer_discard_removes_the_whole_created_keyword_and_section():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.robot"
        target.write_text("*** Test Cases ***\nMy Test\n    Log    hello\n")
        writer = LiveKeywordWriter(target, "Recorded")
        writer.append("Click", ["css=.a"])
        writer.discard()

        content = target.read_text()
        assert "Log    hello" in content
        assert "Recorded" not in content
        assert "*** Keywords ***" not in content
        assert target.exists()


def test_writer_discard_keeps_pre_existing_keyword_body():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.resource"
        target.write_text("*** Keywords ***\nKW\n    Log    keep me\n")
        writer = LiveKeywordWriter(target, "KW")
        writer.append("Click", ["css=.a"])
        writer.discard()

        content = target.read_text()
        assert "Log    keep me" in content
        assert "Click    css=.a" not in content
        assert "*** Keywords ***" in content


def test_writer_discard_keeps_a_section_it_did_not_create():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.resource"
        target.write_text("*** Keywords ***\nOther\n    Log    hi\n")
        writer = LiveKeywordWriter(target, "Recorded")
        writer.append("Click", ["css=.a"])
        writer.discard()

        content = target.read_text()
        assert "*** Keywords ***" in content
        assert "Other" in content
        assert "Recorded" not in content


def test_writer_reuses_a_keyword_from_a_second_keyword_section():
    # A file may legally hold several `*** Keywords ***` sections. Looking only
    # in the first one writes a duplicate definition, which Robot rejects at
    # run time with "Multiple keywords with name ... found".
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "two_sections.robot"
        target.write_text(
            "*** Keywords ***\nFirst\n    Log    a\n\n"
            "*** Keywords ***\nSecond\n    Log    b\n"
        )
        writer = LiveKeywordWriter(target, "Second")
        assert writer.reused is True
        writer.append("Click", ["css=.x"])

        content = target.read_text()
        assert content.count("Second") == 1
        assert "Log    b" in content
        assert "Click    css=.x" in content
        # The call landed inside the existing keyword, not in a new block.
        assert content.index("Click    css=.x") > content.index("Log    b")


def test_writer_finds_an_existing_keyword_by_normalized_name():
    # `_shadow_error` deliberately allows a recorded name to *reuse* an
    # existing keyword when it only differs by case/spaces/underscores - the
    # exact case `Record Keyword` supports. `_find_keyword` must recognise the
    # same reuse, or a second, duplicate keyword block gets written instead of
    # appending to the first one.
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "existing.resource"
        target.write_text("*** Keywords ***\nExisting In Target\n    Log    keep me\n")
        writer = LiveKeywordWriter(target, "existing_in_target")
        assert writer.reused is True
        writer.append("Click", ["css=.x"])

        content = target.read_text()
        assert content.count("Existing In Target") == 1
        assert "Log    keep me" in content
        assert "Click    css=.x" in content
        assert existing_keyword_names(target) == {"Existing In Target"}
