import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder.keyword_writer import LiveKeywordWriter
from Browser.recorder.names import existing_keyword_names


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
