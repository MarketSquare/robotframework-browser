from __future__ import annotations

import json
import subprocess
import sys
from types import SimpleNamespace

import pytest
from robot.api import get_model
from robot.conf.languages import Language, Languages
from robot.libraries.BuiltIn import BuiltIn
from robot.parsing.model.blocks import KeywordSection

from Browser.recorder.cells import tokens
from Browser.recorder.model import (
    Call,
    DisplayNames,
    RecordedKeyword,
    SettingNames,
    Value,
)
from Browser.recorder.names import configured_languages
from Browser.recorder import target as target_module
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
    path = tmp_path / "k.resource"
    kw = RecordedKeyword("Echo")
    tricky = "#a  b ${x} \u00a0\n"
    kw.add(Call("Should Be Equal", [Value.literal(tricky), Value.literal(tricky)]))
    FileTarget(path).finish(kw)
    suite = tmp_path / "s.robot"
    suite.write_text(
        "*** Settings ***\nResource    ${CURDIR}/k.resource\n*** Test Cases ***\nT\n    Echo\n"
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
    # `*{` is syntax Robot reserves; unclosed it fails the keyword at run time.
    ["css=.x", "*{abc"],
    ["css=.x", "a *{b} c"],
    # Two or more spaces are a cell separator, edge spaces are stripped.
    ["css=.x", "two    spaces"],
    ["css=.x", " padded "],
    ["css=.x", "trailing  "],
    ["css=.x", "  leading"],
    ["css=.x", " "],
    ["css=.x", "back\\  "],
    ["css=.x", ""],
    ["css=.x", "   "],
    ["css=.x", "back\\slash"],
    ["css=.x", "\\${not a var}"],
    ["css=.x", "tab\tand\nnewline"],
    # `[` after escaped spaces must stay a literal bracket.
    ["css=.x", "[\n  [1, 2],\n  [3]\n]"],
    ["css=.x", " [lead"],
    ["css=.x", "a  [0]"],
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


def _save_and_remove(tmp_path, data: bytes):
    path = tmp_path / "k.resource"
    path.write_bytes(data)
    target = FileTarget(path)
    target.save(keyword())
    saved = path.read_bytes()
    target.remove("Fill Name")
    return saved, path.read_bytes()


def test_crlf_file_stays_crlf_and_is_restored(tmp_path):
    data = ORIGINAL.replace("\n", "\r\n").encode()
    saved, restored = _save_and_remove(tmp_path, data)
    assert saved.startswith(data)
    assert saved.count(b"\n") == saved.count(b"\r\n")
    assert restored == data


@pytest.mark.parametrize(
    "data",
    [
        b"*** Settings ***\nLibrary    Browser\n\n\n",
        b"*** Settings ***\nLibrary    Browser\n   \n",
        b"*** Keywords ***\nExisting\n    Log    hi",
        b"*** Settings ***\nLibrary    Browser",
        b"\xef\xbb\xbf*** Keywords ***\nExisting\n    Log    hi\n",
    ],
    ids=["trailing_blank", "whitespace_line", "no_eol", "no_eol_settings", "bom"],
)
def test_save_then_remove_restores_unusual_files(tmp_path, data):
    saved, restored = _save_and_remove(tmp_path, data)
    assert saved.startswith(data[:-1] if not data.endswith(b"\n") else data)
    assert saved.startswith(b"\xef\xbb\xbf") == data.startswith(b"\xef\xbb\xbf")
    assert restored == data


def test_failed_remove_keeps_ownership_for_a_retry(tmp_path, monkeypatch):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    target.save(keyword())
    write = FileTarget._write

    def broken(self, model, restore_final_newline=False):
        raise OSError("disk full")

    monkeypatch.setattr(FileTarget, "_write", broken)
    with pytest.raises(OSError):
        target.remove("Fill Name")
    monkeypatch.setattr(FileTarget, "_write", write)
    target.remove("Fill Name")
    assert "Fill Name" not in path.read_text()


def test_named_argument_shaped_values_roundtrip_through_a_real_robot_run(tmp_path):
    (tmp_path / "NamedSpy.py").write_text(
        "import json, pathlib\n"
        "def fill(selector, txt, clear=None):\n"
        "    out = pathlib.Path(__file__).with_name('named.json')\n"
        "    calls = json.loads(out.read_text()) if out.exists() else []\n"
        "    calls.append([selector, txt, clear])\n"
        "    out.write_text(json.dumps(calls))\n"
    )
    resource = tmp_path / "recorded.resource"
    kw = RecordedKeyword("Recorded")
    values = ["txt=hello", "clear=yes", "selector=x", "a b=c", "=lead"]
    for text in values:
        kw.add(Call("Fill", [Value.literal("css=.x", False), Value.literal(text)]))
    # An unknown keyword may take any name, so a selector is escaped too.
    kw.add(Call("Fill", [Value.literal("text=hello", False), Value.literal("x")]))
    FileTarget(resource).finish(kw)
    assert "txt\\=hello" in resource.read_text()
    (tmp_path / "run.robot").write_text(
        "*** Settings ***\n"
        "Library     NamedSpy.py\n"
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
    assert json.loads((tmp_path / "named.json").read_text()) == [
        *(["css=.x", text, None] for text in values),
        ["text=hello", "x", None],
    ]


def test_fixed_named_argument_stays_named(tmp_path):
    kw = RecordedKeyword("Dialog")
    kw.add(
        Call(
            "Handle Future Dialogs",
            [Value(["action=accept"], selectable=False, named=True)],
        )
    )
    assert "Handle Future Dialogs    action=accept" in kw.block()


def test_a_value_shaped_like_a_parameter_of_the_called_keyword_is_escaped():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("text=Log in", False)]))
    kw.add(Call("Fill Text", [Value.literal("id=name", False), Value.literal("txt=a")]))
    kw.add(
        Call("Fill Text", [Value.literal("css=.x", False), Value.literal("force=1")])
    )
    assert kw.lines()[1:] == [
        "Click    text=Log in",
        "Fill Text    id=name    txt\\=a",
        "Fill Text    css=.x    force\\=1",
    ]


def test_a_bracket_after_an_argument_is_not_item_access(tmp_path):
    (tmp_path / "BracketSpy.py").write_text(
        "import json, pathlib\n"
        "def spy(value):\n"
        "    out = pathlib.Path(__file__).with_name('bracket.json')\n"
        "    calls = json.loads(out.read_text()) if out.exists() else []\n"
        "    out.write_text(json.dumps(calls + [value]))\n"
    )
    resource = tmp_path / "recorded.resource"
    kw = RecordedKeyword("Recorded")
    kw.add(Call("Spy", [Value.literal("id[0]")]))
    kw.make_argument(0, 0, 0, 2, "id")
    FileTarget(resource).finish(kw)
    assert "${id}\\[0]" in resource.read_text()
    (tmp_path / "run.robot").write_text(
        "*** Settings ***\n"
        "Library     BracketSpy.py\n"
        "Resource    recorded.resource\n\n"
        "*** Test Cases ***\n"
        "T\n"
        "    Recorded\n"
        "    Recorded    abc\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), "run.robot"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / "bracket.json").read_text()) == ["id[0]", "abc[0]"]


@pytest.mark.parametrize("bom", [b"", b"\xef\xbb\xbf"])
def test_a_file_that_is_not_utf8_is_refused_and_left_alone(tmp_path, bom):
    path = tmp_path / "k.resource"
    data = bom + b"*** Keywords ***\nExisting\n    Log    caf\xe9\n"
    path.write_bytes(data)
    with pytest.raises(ValueError, match=f"not valid UTF-8 \\(byte {len(bom) + 40}\\)"):
        FileTarget(path).save(keyword())
    assert path.read_bytes() == data


#: Typed text, and the part of it that becomes the argument ``${who}``: the
#: argument borders on partial variable syntax or on spaces, which Robot is picky about.
_NEXT_TO_PARTIAL_SYNTAX = [
    ("${who}", 2, 5),
    ("a$who", 2, 5),
    ("@who", 1, 4),
    ("x\\who", 2, 5),
    ("who{", 0, 3),
    ("who}", 0, 3),
    ("{who}", 1, 4),
    ("%{who}", 2, 5),
    ("who[0]", 0, 3),
    ("${part", 2, 6),
    # Escaped spaces on either side of the argument.
    ("a  who  b", 3, 6),
    ("  who  ", 2, 5),
    ("x  who", 3, 6),
]


def test_an_argument_next_to_partial_variable_syntax_roundtrips(tmp_path):
    (tmp_path / "PartSpy.py").write_text(
        "import json, pathlib\n"
        "OUT = []\n"
        "def spy(value):\n"
        "    OUT.append(value)\n"
        "    pathlib.Path(__file__).with_name('part.json').write_text(json.dumps(OUT))\n"
    )
    resource = tmp_path / "recorded.resource"
    kw = RecordedKeyword("Recorded")
    for index, (text, start, end) in enumerate(_NEXT_TO_PARTIAL_SYNTAX):
        kw.add(Call("Spy", [Value.literal(text)]))
        kw.make_argument(index, 0, start, end, f"who{index}")
    FileTarget(resource).finish(kw)
    (tmp_path / "run.robot").write_text(
        "*** Settings ***\n"
        "Library     PartSpy.py\n"
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
    assert json.loads((tmp_path / "part.json").read_text()) == [
        text for text, _, _ in _NEXT_TO_PARTIAL_SYNTAX
    ]
    for index, call in enumerate(kw.calls()):
        variables = [
            t for kind, t in tokens(call.rendered_args()[0]) if kind == "variable"
        ]
        assert variables == [f"${{who{index}}}"]


@pytest.mark.skipif(
    sys.platform == "win32", reason="chmod does not make files read-only"
)
def test_a_read_only_file_is_not_overwritten(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    path.chmod(0o444)
    try:
        with pytest.raises(PermissionError, match="is read-only"):
            FileTarget(path).save(keyword())
        assert path.read_text() == ORIGINAL
    finally:
        path.chmod(0o644)


@pytest.mark.skipif(sys.platform == "win32", reason="no POSIX permissions")
def test_a_new_file_gets_the_permissions_of_any_new_file(tmp_path):
    reference = tmp_path / "reference.txt"
    reference.write_text("")
    path = tmp_path / "k.resource"
    FileTarget(path).save(keyword())
    assert path.stat().st_mode & 0o777 == reference.stat().st_mode & 0o777


def test_a_missing_folder_is_named_in_the_error(tmp_path):
    with pytest.raises(PermissionError, match="does not exist"):
        FileTarget(tmp_path / "missing" / "k.resource").save(keyword())


def test_a_failed_first_write_does_not_claim_a_keyword_added_meanwhile(tmp_path):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    write = target._write

    def fail_once(*args, **kwargs):
        target._write = write
        raise OSError("disk full")

    target._write = fail_once
    kw = RecordedKeyword("Shared")
    kw.add(Call("Log", [Value.literal("ours")]))
    with pytest.raises(OSError):
        target.save(kw)
    path.write_text("*** Keywords ***\nShared\n    Log    theirs\n", encoding="utf-8")
    with pytest.raises(ValueError, match="already exists"):
        target.save(kw)
    assert "theirs" in path.read_text(encoding="utf-8")


@pytest.fixture(
    params=[
        ("fr", "Mots-clés"),
        ("de", "Schlüsselwörter"),
        ("en", "Keywords"),
        ("fr\nLanguage: en", "Mots-clés"),
    ]
)
def localized_target(tmp_path, request):
    declaration, header = request.param
    original = f"Language: {declaration}\n"
    path = tmp_path / "localized.robot"
    path.write_text(original, encoding="utf-8")
    target = FileTarget(path)
    target.save(keyword())
    return target, original, header


def test_new_section_uses_declared_language(localized_target):
    target, _, header = localized_target
    assert f"*** {header} ***" in target.path.read_text(encoding="utf-8")


def test_localized_section_is_parsed_as_one_keyword_section(localized_target):

    target, _, _ = localized_target
    sections = [
        section
        for section in get_model(target.path).sections
        if isinstance(section, KeywordSection)
    ]
    assert len(sections) == 1


def test_localized_section_contains_recorded_keyword(localized_target):

    target, _, _ = localized_target
    section = next(
        section
        for section in get_model(target.path).sections
        if isinstance(section, KeywordSection)
    )
    assert section.body[0].name == "Fill Name"


def test_removing_localized_recording_restores_original_file(localized_target):
    target, original, _ = localized_target
    target.remove("Fill Name")
    assert target.path.read_text(encoding="utf-8") == original


def test_existing_section_keeps_its_header_in_localized_file(tmp_path):
    path = tmp_path / "localized.robot"
    original = "Language: fr\n*** Keywords ***\nExisting\n    No Operation\n"
    path.write_text(original, encoding="utf-8")
    FileTarget(path).save(keyword())
    assert path.read_text(encoding="utf-8").startswith(original)
    assert "*** Mots-clés ***" not in path.read_text(encoding="utf-8")


@pytest.fixture
def translated_keyword():
    kw = RecordedKeyword("Remplir", DisplayNames({"Fill Text": "Remplir Le Texte"}))
    kw.add(Call("Fill Text", [Value.literal("#n"), Value.literal("txt=bonjour")]))
    return kw


def test_translated_call_is_written_to_file(tmp_path, translated_keyword):

    path = tmp_path / "localized.robot"
    path.write_text("Language: fr\n", encoding="utf-8")
    FileTarget(path).finish(translated_keyword)
    section = next(s for s in get_model(path).sections if isinstance(s, KeywordSection))
    assert section.body[0].body[1].keyword == "Remplir Le Texte"


@pytest.mark.parametrize("output", ["console", "info"])
def test_translated_call_is_logged(translated_keyword, output):
    messages = {"console": [], "info": []}
    LogTarget(messages["console"].append, messages["info"].append).finish(
        translated_keyword
    )
    assert "Remplir Le Texte" in messages[output][0]


def test_translated_call_is_in_returned_text(translated_keyword):
    assert "Remplir Le Texte" in translated_keyword.text()


class _NoKeywordsHeader(Language):
    code = "test-no-keywords-header"
    keywords_header = ""


def test_custom_language_without_keyword_header_falls_back_to_english(tmp_path):
    path = tmp_path / "custom.robot"
    path.write_text("", encoding="utf-8")
    FileTarget(path, [_NoKeywordsHeader()]).save(keyword())
    assert path.read_text(encoding="utf-8").startswith("*** Keywords ***")


FRENCH = tuple(Languages("fr"))
FRENCH_SECTION = "*** Mots-clés ***\nExisting\n    No Operation\n"


def test_configured_language_finds_existing_localized_section(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text(FRENCH_SECTION, encoding="utf-8")
    FileTarget(path, FRENCH).save(keyword())
    assert path.read_text(encoding="utf-8").count("***") == 2


def test_configured_language_writes_into_existing_localized_section(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text(FRENCH_SECTION, encoding="utf-8")
    FileTarget(path, FRENCH).save(keyword())
    section = get_model(path, lang=FRENCH).sections[0]
    assert [item.name for item in section.body if item.name] == [
        "Existing",
        "Fill Name",
    ]


def test_configured_language_reports_existing_names(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text(FRENCH_SECTION, encoding="utf-8")
    assert FileTarget(path, FRENCH).existing_names() == {"Existing"}


def test_new_section_uses_configured_language(tmp_path):
    path = tmp_path / "configured.robot"
    FileTarget(path, FRENCH).save(keyword())
    assert path.read_text(encoding="utf-8").startswith("*** Mots-clés ***\n")


def test_declared_language_wins_over_configured_language(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    FileTarget(path, FRENCH).save(keyword())
    assert "*** Schlüsselwörter ***" in path.read_text(encoding="utf-8")


def test_existing_english_section_is_used_with_configured_language(tmp_path):
    path = tmp_path / "configured.robot"
    original = "*** Keywords ***\nExisting\n    No Operation\n"
    path.write_text(original, encoding="utf-8")
    FileTarget(path, FRENCH).save(keyword())
    text = path.read_text(encoding="utf-8")
    assert text.startswith(original)
    assert "Mots-clés" not in text


@pytest.mark.parametrize(
    ("content", "languages", "tags"),
    [
        ("", (), "Tags"),
        ("", FRENCH, "Étiquette"),
        ("Language: de\n", (), "Marker"),
        ("Language: de\n", FRENCH, "Marker"),
    ],
    ids=["english", "configured", "declared", "declared-over-configured"],
)
def test_file_setting_names_follow_file_language(tmp_path, content, languages, tags):
    path = tmp_path / "settings.robot"
    path.write_text(content, encoding="utf-8")
    assert FileTarget(path, languages or ()).settings.tags == tags


def test_missing_file_setting_names_follow_configured_language(tmp_path):
    target = FileTarget(tmp_path / "missing.robot", FRENCH)
    assert target.settings == SettingNames("Étiquette", "Arguments")


def test_log_setting_names_follow_configured_language():
    assert LogTarget(languages=FRENCH).settings.tags == "Étiquette"


def test_log_setting_names_default_to_english():
    assert LogTarget().settings == SettingNames()


def test_localized_settings_are_written_and_parsed(tmp_path):
    path = tmp_path / "configured.robot"
    kw = RecordedKeyword("Fill Name", settings=SettingNames("Étiquette", "Arguments"))
    kw.add(Call("Fill Text", [Value.literal("#n", False), Value.literal("Alice")]))
    FileTarget(path, FRENCH).save(kw)
    body = get_model(path, lang=FRENCH).sections[0].body[0]
    assert body.body[0].type == "TAGS"


def test_resaving_localized_settings_is_not_reported_as_outside_change(tmp_path):
    path = tmp_path / "configured.robot"
    target = FileTarget(path, FRENCH)
    kw = RecordedKeyword("Fill Name", settings=SettingNames("Étiquette", "Arguments"))
    kw.add(Call("Fill Text", [Value.literal("#n", False), Value.literal("Alice")]))
    target.save(kw)
    kw.add(Call("Click", [Value.literal("#b", False)]))
    assert target.save(kw) is None


def test_section_language_is_determined_when_the_target_is_created(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    target = FileTarget(path)
    path.write_text("Language: fr\nLanguage: de\n", encoding="utf-8")
    target.save(keyword())
    assert "*** Schlüsselwörter ***" in path.read_text(encoding="utf-8")


def test_saving_fails_when_the_file_no_longer_enables_its_language(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    target = FileTarget(path)
    path.write_text("Language: fr\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no longer enables German"):
        target.save(keyword())


def test_a_refused_save_leaves_the_file_alone(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    target = FileTarget(path)
    path.write_text("Language: fr\n", encoding="utf-8")
    with pytest.raises(ValueError):
        target.save(keyword())
    assert path.read_text(encoding="utf-8") == "Language: fr\n"


def test_a_configured_language_stays_enabled_without_a_declaration(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: fr\n", encoding="utf-8")
    target = FileTarget(path, FRENCH)
    path.write_text("", encoding="utf-8")
    target.save(keyword())
    assert "*** Mots-clés ***" in path.read_text(encoding="utf-8")


def test_recorded_settings_are_parsed_in_the_declared_language(tmp_path, monkeypatch):
    parsed = []
    original = target_module._parse_block
    monkeypatch.setattr(
        target_module,
        "_parse_block",
        lambda text, languages: parsed.append(original(text, languages)) or parsed[-1],
    )
    path = tmp_path / "declared.robot"
    path.write_text("Language: fi\n", encoding="utf-8")
    target = FileTarget(path)
    kw = RecordedKeyword("Fill Name", settings=target.settings)
    kw.add(Call("Fill Text", [Value.literal("#n", False), Value.literal("Alice")]))
    target.save(kw)
    assert parsed[0].body[0].type == "TAGS"


def test_settings_are_determined_when_the_target_is_created(tmp_path):
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    target = FileTarget(path)
    path.write_text("Language: fr\n", encoding="utf-8")
    assert target.settings.tags == "Marker"


def test_reading_a_localized_file_leaves_the_suite_languages_unchanged(
    tmp_path, monkeypatch
):
    suite_languages = Languages("fr")
    context = SimpleNamespace(namespace=SimpleNamespace(languages=suite_languages))
    monkeypatch.setattr(BuiltIn, "_get_context", lambda self: context)
    path = tmp_path / "configured.robot"
    path.write_text("Language: de\n", encoding="utf-8")
    FileTarget(path, configured_languages()).save(keyword())
    assert [language.code for language in suite_languages] == ["fr", "en"]
