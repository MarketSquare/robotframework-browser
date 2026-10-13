from __future__ import annotations

import json
import subprocess
import sys

import pytest

from Browser.recorder.model import Call, RecordedKeyword, Value
from Browser.recorder.target import FileTarget, LogTarget

ORIGINAL = (
    "*** Settings ***\nLibrary    Browser\n\n"
    "*** Keywords ***\nExisting\n    Log    hi\n"
)


def keyword(name: str = "Fill Name", *texts: str) -> RecordedKeyword:
    kw = RecordedKeyword(name)
    for text in texts or ("Alice",):
        kw.add(Call("Fill Text", [Value.literal("#n", False), Value.literal(text)]))
    return kw


def test_save_creates_file_and_section(tmp_path):
    path = tmp_path / "new.resource"
    FileTarget(path).save(keyword())
    assert path.read_text() == (
        "*** Keywords ***\nFill Name\n    [Tags]    recorded\n    Fill Text    \\#n    Alice\n"
    )


def test_save_appends_after_existing_content(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    FileTarget(path).save(keyword())
    assert path.read_text() == ORIGINAL + (
        "\nFill Name\n    [Tags]    recorded\n    Fill Text    \\#n    Alice\n"
    )


def test_external_edit_outside_the_block_is_kept(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(path.read_text().replace("Log    hi", "Log    changed"))
    kw.add(Call("Click", [Value.literal("#b", False)]))
    assert target.save(kw) is None
    text = path.read_text()
    assert "Log    changed" in text
    assert text.endswith("    Click    \\#b\n")


def test_external_edit_inside_the_block_is_overwritten_with_notice(tmp_path):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(path.read_text().replace("Alice", "Bob"))
    notice = target.save(kw)
    assert "changed outside the recorder" in notice
    assert "Alice" in path.read_text()


def test_deleted_block_is_written_again_with_notice(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(ORIGINAL)
    assert "written again" in target.save(kw)
    assert "Fill Name" in path.read_text()


def test_remove_restores_the_file_byte_for_byte(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.read_text() == ORIGINAL


def test_remove_drops_a_section_it_created(tmp_path):
    path = tmp_path / "k.robot"
    original = "*** Settings ***\nLibrary    Browser\n"
    path.write_text(original)
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.read_text() == original


def test_remove_never_deletes_the_file(tmp_path):
    path = tmp_path / "new.resource"
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.exists()


def test_remove_of_an_unsaved_keyword_is_a_no_op(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    FileTarget(path).remove("Never Saved")
    assert path.read_text() == ORIGINAL


def test_saving_an_empty_keyword_removes_its_block(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    kw.undo()
    target.save(kw)
    assert path.read_text() == ORIGINAL


def test_formatting_of_existing_content_is_preserved(tmp_path):
    path = tmp_path / "k.resource"
    odd = "*** Keywords ***\nExisting\n  Log  two  spaces    # comment\n"
    path.write_text(odd)
    FileTarget(path).save(keyword())
    assert path.read_text().startswith(odd)


def test_two_keywords_are_separated_by_one_blank_line(tmp_path):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    target.finish(keyword("One"))
    target.finish(keyword("Two"))
    assert "Alice\n\nTwo\n" in path.read_text()


def test_existing_names(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    assert FileTarget(path).existing_names() == {"Existing"}


def test_log_target_writes_block_to_console_and_log():
    seen: list[tuple[str, str]] = []
    target = LogTarget(
        console=lambda t: seen.append(("console", t)),
        info=lambda t: seen.append(("info", t)),
    )
    kw = keyword()
    assert target.save(kw) is None
    target.finish(kw)
    assert seen == [("console", kw.text()), ("info", kw.text())]
    assert target.existing_names() == set()


def test_written_keyword_runs_in_a_real_robot_run(tmp_path):
    """Escaped values come back as the exact recorded strings."""
    path = tmp_path / "k.resource"
    kw = RecordedKeyword("Echo")
    tricky = "#a  b ${x} \u00a0\n"
    kw.add(Call("Should Be Equal", [Value.literal(tricky), Value.literal(tricky)]))
    FileTarget(path).finish(kw)
    suite = tmp_path / "s.robot"
    suite.write_text(
        f"*** Settings ***\nResource    {path}\n*** Test Cases ***\nT\n    Echo\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), str(suite)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout


def test_empty_argument_is_written_as_empty_marker(tmp_path):
    path = tmp_path / "k.resource"
    kw = RecordedKeyword("KW")
    kw.add(Call("Fill Text", [Value.literal("css=.x", False), Value.literal("")]))
    FileTarget(path).finish(kw)
    assert "Fill Text    css=.x    ${EMPTY}" in path.read_text()


#: Values a recording can realistically produce that also mean something to
#: the Robot parser (or are hostile: selectors and typed text come from the page
#: under test). Each is written by the target, then read back by actually
#: *running* Robot, because escapes are resolved at run time, not at parse time.
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


def test_values_roundtrip_through_a_real_robot_run(tmp_path):
    """Whatever was recorded must reach the keyword as exactly that value."""
    (tmp_path / "ArgSpy.py").write_text(
        "import json, pathlib\n"
        "CALLS = []\n"
        "def spy(*args):\n"
        "    CALLS.append(list(args))\n"
        "    pathlib.Path(__file__).with_name('calls.json').write_text(json.dumps(CALLS))\n"
    )
    resource = tmp_path / "recorded.resource"
    kw = RecordedKeyword("Recorded")
    for row in _ROUNDTRIP_VALUES:
        kw.add(Call("Spy", [Value.literal(item, False) for item in row]))
    FileTarget(resource).finish(kw)
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
    # round-trip its arguments, so check the structure too.
    assert FileTarget(resource).existing_names() == {"Recorded"}


def test_saving_over_a_foreign_keyword_of_the_same_name_is_refused(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    with pytest.raises(ValueError, match="already exists"):
        FileTarget(path).save(keyword("Existing"))
    assert path.read_text() == ORIGINAL
