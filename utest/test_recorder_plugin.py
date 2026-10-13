import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder import plugin as recorder_plugin
from Browser.recorder.action_mapper import ActionMapper, to_browser_selector
from Browser.recorder.keyword_writer import (
    LiveKeywordWriter,
    existing_keyword_names,
    keyword_name_error,
    normalize_keyword_name,
)
from Browser.recorder.plugin import (
    KnownKeywords,
    _embedded_matcher,
    collect_known_keywords,
)

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
# Keyword name validation
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "name",
    [
        "Login As Admin",
        "Do It!",
        "Ünïcode Näme",
        "A",
        "keyword-with-dashes_and.dots",
        "Sum: 1 + 2 = 3",
        # Letters are never the problem - only whitespace and separators are.
        "Anmelden Als Büroleiter",
        "Öffne Übersicht",
        "Søk Etter Produkt 3.0 (Raskt)",
        "Search For Product",
        "Открыть Страницу",
        "ページを開く",
        "登录系统",
        "تسجيل الدخول",
        "Café Größe 2m²",
        "A/B Test",
        # `$`, `{` and `}` are only a problem as an *opening* variable marker -
        # Robot itself creates all of these keywords without complaint.
        "Cost Is 100$",
        "Set {brace} Style",
        "Closing } Only",
        "Discount Of 50%",
        "Send @ Sign",
    ],
)
def test_usable_keyword_names_are_accepted(name):
    assert keyword_name_error(name) is None


#: Names Robot's own lexer would read as more than one cell, more than one
#: line, or a pipe-separated row. The `new` command is callable by the page
#: under test, so each of these is a way for a hostile page to write extra
#: executable Robot source into the user's suite; the U+3000, U+00A0, U+2028
#: and leading-pipe entries were each confirmed to reach an *executing*
#: `Log    PWNED` through a real `robot` run while the validator still knew
#: only about ASCII spaces and C0/C1 control characters.
_INJECTING_NAMES = [
    # -- cell separators the ASCII-only check missed -------------------------- #
    # Robot splits cells on `\s{2,}` with *unicode* semantics, so each of these
    # defines a keyword `Good` whose first executed step is `Log    PWNED`.
    "Good\u3000\u3000Log\u3000\u3000PWNED",  # ideographic space
    "Good\xa0\xa0Log\xa0\xa0PWNED",  # non-breaking space
    # One ASCII space plus one NBSP is still two whitespace characters.
    "Good \xa0Log \xa0PWNED",
    "Good\t\tLog\t\tPWNED",
    "Good\x0b\x0bLog\x0b\x0bPWNED",
    # -- line breaks `str.splitlines()` honours ------------------------------- #
    # These write a whole second *executable* keyword.
    # The separators inside these are exotic too, so nothing but the line break
    # itself is doing the work - a run of four ASCII spaces would have been
    # caught by the old check for the wrong reason.
    "Good\u2028Evil Keyword\u2028\u3000\u3000Log\u3000\u3000PWNED",  # line separator
    "Good\u2028Evil Keyword \xa0Log \xa0PWNED",
    "Good\u2029Evil Keyword\u2029\u3000\u3000Log\u3000\u3000PWNED",  # paragraph sep.
    "Good\x85Evil Keyword\x85\u3000\u3000Log\u3000\u3000PWNED",  # NEL
    "Good\x0cEvil Keyword\x0c    Log    PWNED",
    "Good\x1cEvil Keyword\x1c    Log    PWNED",
    "Good\nEvil Keyword\n    Log    PWNED",
    "Good\rEvil Keyword\r    Log    PWNED",
    # -- pipe-separated format: pure ASCII, no control char, no double space -- #
    "| Good | Log | PWNED",
    "|Good",
    # Not an injection by itself (only a *leading* pipe switches the format),
    # but a cell-separator shape that has no business in a name.
    "Good | Log | PWNED",
    # -- the original, simpler shapes ---------------------------------------- #
    "",
    "  ",
    "\xa0",
    "a\x00b",
    " a",
    "a ",
    "\u3000a",
    "a\u3000",
    "a  b",
    "#a",
    "*a",
    "*** Keywords ***",
    # Found while attacking the fixed validator: `...` is Robot's continuation
    # marker, so the row folds into the section header and the recorded steps
    # become an unnamed keyword that makes the whole resource unimportable.
    "...",
    # -- variable syntax ------------------------------------------------------ #
    # `${a} ${b}` declares *embedded arguments*, so the recorded keyword matches
    # every two-word call in the suite. Verified against a real `robot` run:
    # a resource keyword `${a} ${b}` makes `No Operation` execute the recorded
    # body instead, with the suite still reporting rc=0.
    "${a} ${b}",
    "Fill In The ${VAR} Form",
    # Unclosed openers: Robot refuses to create the keyword ("Variable '${' was
    # not closed properly") and the recorded steps are silently lost.
    "${",
    "${a",
    "&{x",
    "@{y",
    "%{z",
    "Login As ${admin",
    # -- unencodable ---------------------------------------------------------- #
    # A lone surrogate passes every structural check and only fails inside
    # `model.save()` with a UnicodeEncodeError, aborting the whole recording.
    "\ud800",
    "Login\ud800As Admin",
]


@pytest.mark.parametrize("name", _INJECTING_NAMES)
def test_unusable_keyword_names_are_reported(name):
    assert keyword_name_error(name)


def test_non_string_keyword_name_is_reported_not_raised():
    assert keyword_name_error(None)
    assert keyword_name_error(42)


def test_normalize_keyword_name_matches_robots_own_comparison():
    assert normalize_keyword_name("l_ogin as admin") == normalize_keyword_name(
        "Login As Admin"
    )
    assert normalize_keyword_name("N o_Operation") == normalize_keyword_name(
        "No Operation"
    )
    assert normalize_keyword_name("Login") != normalize_keyword_name("Logout")


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


def test_recording_reuse_with_different_spelling_survives_a_real_robot_run(tmp_path):
    """The "defined multiple times" failure mode, genuinely excluded.

    A raw-name `_find_keyword` accepts the differently-spelled name (reuse is
    legitimate) but then fails to find the existing block, so it writes a
    *second* keyword under a name that only differs by case/underscores from
    the first. Both then fail identically at real `robot` run time with
    "Keyword with same name defined multiple times." - the reused-into
    keyword is broken by the mere act of recording into it.
    """
    target = tmp_path / "existing.resource"
    target.write_text("*** Keywords ***\nExisting In Target\n    Log    keep me\n")
    writer = LiveKeywordWriter(target, "existing_in_target")
    writer.append("Log", ["recorded step"])

    (tmp_path / "run.robot").write_text(
        "*** Settings ***\nResource    existing.resource\n\n"
        "*** Test Cases ***\nT\n    Existing In Target\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), "run.robot"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "defined multiple times" not in (result.stdout + result.stderr)
    assert existing_keyword_names(target) == {"Existing In Target"}


def test_existing_keyword_names():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "k.resource"
        assert existing_keyword_names(target) == set()
        target.write_text("*** Keywords ***\nOne\n    Log    a\n\nTwo\n    Log    b\n")
        assert existing_keyword_names(target) == {"One", "Two"}


# --------------------------------------------------------------------------- #
# Collecting the keyword names the running suite already knows
# --------------------------------------------------------------------------- #


def test_collect_known_keywords_is_empty_without_a_running_suite():
    # The recorder must stay usable from plain Python, so no suite means no
    # collision set rather than an exception.
    assert collect_known_keywords() == KnownKeywords()


def test_collect_known_keywords_warns_when_the_keyword_store_is_missing(monkeypatch):
    """`_kw_store` is a private Robot attribute; losing it must not fail silently.

    If a future RF version renames or removes it, the collision set silently
    shrinks to `namespace.libraries` only - resource and suite-file keywords
    stop being checked with no other signal. That must at least surface as a
    warning instead of vanishing without a trace.
    """
    namespace = SimpleNamespace(libraries=[], languages=None)
    context = SimpleNamespace(namespace=namespace)
    monkeypatch.setattr(BuiltIn, "_get_context", lambda self: context)

    warnings = []
    monkeypatch.setattr(recorder_plugin.logger, "warn", warnings.append)

    known = collect_known_keywords()

    assert known == KnownKeywords()
    assert len(warnings) == 1
    assert "_kw_store" in warnings[0]
    assert "resource and suite-file keywords" in warnings[0]


_PROBE_LIBRARY = '''\
import json
import pathlib

from Browser.recorder.plugin import RecorderPlugin, collect_known_keywords
from Browser.recorder.session import RecorderSession


def _target(file=None):
    if file:
        return pathlib.Path(file).resolve()
    # The default target is what `Record Keyword` itself uses.
    return RecorderPlugin._default_target()


def _report(payload):
    pathlib.Path(__file__).with_name("probe.json").write_text(json.dumps(payload))


def dump_known_keywords(file=None):
    known = collect_known_keywords(_target(file))
    _report(
        {
            "names": sorted(known.names),
            "embedded": sorted(name for name, _ in known.embedded),
            "prefixes": sorted(known.bdd_prefixes),
        }
    )


def try_to_record(name, file=None):
    """Build the session exactly as `Record Keyword` does, and report the outcome."""
    target = _target(file)
    known = collect_known_keywords(target)
    try:
        RecorderSession(
            target,
            fixed_name=name,
            known_keywords=known.names,
            embedded_keywords=known.embedded,
            bdd_prefixes=known.bdd_prefixes,
        )
    except ValueError as error:
        _report({"outcome": "rejected", "error": str(error)})
        return
    _report({"outcome": "accepted"})
'''


def _run_probe(tmp_path, call, via_symlink=False):
    """Run a real Robot suite and return what the probe saw inside it."""
    (tmp_path / "Probe.py").write_text(_PROBE_LIBRARY)
    (tmp_path / "helpers.resource").write_text(
        "*** Settings ***\nResource    nested.resource\n\n"
        "*** Keywords ***\nMy Helper\n    Log    x\n\n"
        # An embedded-argument keyword: a *literal* call instantiates it, so a
        # literal recorded name shadows it without ever repeating its name.
        "Open ${page} Page\n    Log    ${page}\n\n"
        # The same with a custom pattern, which the matcher must preserve.
        "Count ${n:\\d+} Items\n    Log    ${n}\n"
    )
    (tmp_path / "nested.resource").write_text(
        "*** Keywords ***\nNested Helper\n    Log    y\n"
    )
    (tmp_path / "run.robot").write_text(
        "*** Settings ***\n"
        "Library     Probe.py\n"
        "Library     Collections\n"
        # `WITH NAME` changes the owner name a qualified call must use.
        "Library     String    WITH NAME    Str\n"
        "Resource    helpers.resource\n\n"
        "*** Test Cases ***\n"
        "T\n"
        f"    {call}\n\n"
        "*** Keywords ***\n"
        "Suite Local Keyword\n"
        "    Log    z\n\n"
        "Given User Is Logged In\n"
        "    Log    z\n\n"
        "Open ${thing} From Suite\n"
        "    Log    ${thing}\n"
    )
    suite = "run.robot"
    if via_symlink:
        # `${SUITE_SOURCE}` is an abspath, not a realpath, so a suite reached
        # through a symlink only matches its own collected entry if the default
        # target is resolved.
        link = tmp_path / "link"
        link.symlink_to(tmp_path, target_is_directory=True)
        suite = str(link / "run.robot")
    repo_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), suite],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(repo_root)},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads((tmp_path / "probe.json").read_text())


def test_collect_known_keywords_sees_the_whole_running_suite(tmp_path):
    """The RF-API integration itself, inside a real `robot` run."""
    # An unrelated target excludes nothing, so this is the full picture.
    names = set(
        _run_probe(tmp_path, "Dump Known Keywords    file=unrelated.resource")["names"]
    )
    # BuiltIn, an explicitly imported library, an imported resource, a resource
    # imported by that resource, and the suite file's own keywords.
    assert "Log" in names
    assert "No Operation" in names
    assert "Append To List" in names
    assert "My Helper" in names
    assert "Nested Helper" in names
    assert "Suite Local Keyword" in names


def test_collect_known_keywords_excludes_the_recording_targets_own_names(tmp_path):
    # The target file's own keywords are the ones the writer may legitimately
    # reuse; they are checked against the file on disk instead.
    known = _run_probe(tmp_path, "Dump Known Keywords    file=helpers.resource")
    assert "My Helper" not in known["names"]
    assert "Nested Helper" in known["names"]
    assert "Log" in known["names"]


def test_collect_known_keywords_covers_bdd_prefix_stripping(tmp_path):
    """Robot strips `Given`/`When`/... *before* resolving a keyword.

    So a suite keyword `Given User Is Logged In` is actually reached by
    resolving `User Is Logged In`, and recording that bare name hijacks the BDD
    call while colliding with nothing. Verified against a real `robot` run: the
    resource keyword did run in place of the suite's own.
    """
    names = set(
        _run_probe(tmp_path, "Dump Known Keywords    file=unrelated.resource")["names"]
    )
    assert "Given User Is Logged In" in names
    assert "User Is Logged In" in names


def test_bdd_variants_of_the_target_file_survive_its_exclusion(tmp_path):
    """The target's *literal* names are droppable, its BDD variants are not.

    Dropping the whole owner took the variants with it, and the target is the
    suite file by default - so `Given User Is Logged In` in the suite could be
    hijacked by recording the bare `User Is Logged In` on the default path.
    """
    known = _run_probe(tmp_path, "Dump Known Keywords")
    assert "Suite Local Keyword" not in known["names"]
    assert "Given User Is Logged In" not in known["names"]
    assert "User Is Logged In" in known["names"]


def test_recording_rejects_the_bdd_variant_of_a_target_file_keyword(tmp_path):
    """End to end: the page's chosen name is refused inside a real `robot` run."""
    outcome = _run_probe(tmp_path, "Try To Record    User Is Logged In")
    assert outcome["outcome"] == "rejected"
    assert "already exists in this suite" in outcome["error"]


def test_recording_rejects_an_embedded_argument_instantiation(tmp_path):
    """`Open ${page} Page` is instantiated by the literal `Open Login Page`."""
    outcome = _run_probe(tmp_path, "Try To Record    Open Login Page")
    assert outcome["outcome"] == "rejected"
    assert "Open ${page} Page" in outcome["error"]


def test_recording_rejects_an_embedded_keyword_of_the_target_file(tmp_path):
    """An embedded keyword cannot be "reused" by a literal name, only shadowed."""
    outcome = _run_probe(
        tmp_path, "Try To Record    Open Login Page    file=helpers.resource"
    )
    assert outcome["outcome"] == "rejected"
    assert "Open ${page} Page" in outcome["error"]


def test_recording_rejects_an_embedded_keyword_of_the_default_target(tmp_path):
    # The suite file's own embedded keyword, on the default (excluded) path.
    outcome = _run_probe(tmp_path, "Try To Record    Open Coffee From Suite")
    assert outcome["outcome"] == "rejected"
    assert "Open ${thing} From Suite" in outcome["error"]


def test_recording_reuses_a_keyword_of_a_symlinked_suite_file(tmp_path):
    """`LiveKeywordWriter.reused` must keep working behind a symlink.

    `${SUITE_SOURCE}` is an abspath, so an unresolved default target never
    matched the suite's own entry and the suite's own keywords were reported as
    collisions with themselves.
    """
    outcome = _run_probe(
        tmp_path, "Try To Record    Suite Local Keyword", via_symlink=True
    )
    assert outcome["outcome"] == "accepted"


def test_an_ordinary_name_is_still_accepted_inside_a_real_run(tmp_path):
    # An over-strict validator is its own defect: embedded matching must not
    # start rejecting names nothing in the suite claims.
    assert _run_probe(tmp_path, "Try To Record    Café Größe 2m²") == {
        "outcome": "accepted"
    }


# --------------------------------------------------------------------------- #
# Embedded matching the way Robot *compares* names, not the way it spells them
# --------------------------------------------------------------------------- #

#: Each pair is a keyword that declares embedded arguments and a name that
#: Robot resolves to the recorded keyword instead, because a "normal" match -
#: caseless, spaceless and underscore-insensitive - beats an embedded one in
#: `KeywordStore._select_best_matches`. `EmbeddedArguments.matches` says *no*
#: to every one of them: its compiled pattern keeps the raw literal parts.
#: Each was confirmed to hijack the call with a differential execution oracle.
_NORMALISED_CLAIMS = [
    ("Open ${page} Page", "Open_Login_Page"),
    ("Open ${page} Page", "OpenLoginPage"),
    ("Open ${page} Page", "open_login_page"),
    ("Open ${page} Page", "Open Login_Page"),
    ("Zahle ${betrag} %", "Zahle_50_%"),
    ("Zahle ${betrag} %", "Zahle50%"),
    # A custom pattern must survive the rewrite, not be widened to `.*`.
    (r"Count ${n:\d+} Items", "Count_42_Items"),
    (r"Count ${n:\d+} Items", "Count42Items"),
    # The BDD variant of `Given ${who} Signs In`, which is how a `Given Alice
    # Signs In` call reaches it.
    ("${who} Signs In", "Alice_Signs_In"),
    ("Öffne ${seite} Übersicht", "ÖffneHauptÜbersicht"),
    # Owner-qualified declarations are matched the same way.
    ("helpers.Open ${page} Page", "helpers.Open_Login_Page"),
]


@pytest.mark.parametrize(("declared", "claimed"), _NORMALISED_CLAIMS)
def test_embedded_matcher_claims_robot_normalised_names(declared, claimed):
    assert _embedded_matcher(declared)(claimed) is True


#: Names no embedded keyword in `_NORMALISED_CLAIMS` claims. `Open Page` is the
#: interesting one: an embedded argument that swallowed *nothing* would make it
#: look like an instantiation of `Open ${page} Page`, but Robot does not resolve
#: it there - hence `(.+?)` rather than Robot's own `(.*?)`.
_UNCLAIMED_NAMES = [
    "Open Page",
    "Öffne Übersicht",
    "Café Größe 2m²",
    "A/B Test",
    "Zahle 50 % {netto}",
    "Größe 100%",
    "Count Items",
    "Signs In",
]


@pytest.mark.parametrize("declared", [pair[0] for pair in _NORMALISED_CLAIMS])
@pytest.mark.parametrize("name", _UNCLAIMED_NAMES)
def test_embedded_matcher_leaves_unclaimed_names_alone(declared, name):
    assert _embedded_matcher(declared)(name) is False


def test_embedded_matcher_is_none_for_a_literal_name():
    assert _embedded_matcher("Open Login Page") is None


@pytest.mark.parametrize(
    "name",
    [
        "Open_Login_Page",
        "OpenLoginPage",
        "Count_42_Items",
        "Open_Coffee_From_Suite",
    ],
)
def test_recording_rejects_a_normalised_embedded_instantiation(tmp_path, name):
    """The raw `EmbeddedArguments` check alone let each of these through.

    Robot's own matching is caseless, spaceless *and* underscore-insensitive and
    prefers such a normal match over the embedded owner, so writing any of these
    hijacks the existing call - rc=0, PASS, no warning.
    """
    outcome = _run_probe(tmp_path, f"Try To Record    {name}")
    assert outcome["outcome"] == "rejected"
    assert "already exists in this suite" in outcome["error"]


# --------------------------------------------------------------------------- #
# Owner-qualified names
# --------------------------------------------------------------------------- #


def test_collect_known_keywords_includes_owner_qualified_names(tmp_path):
    known = _run_probe(tmp_path, "Dump Known Keywords")
    names = set(known["names"])
    assert "BuiltIn.Log" in names
    # `WITH NAME` decides the owner name a call must use.
    assert "Str.Convert To Upper Case" in names
    assert "String.Convert To Upper Case" not in names
    assert "helpers.My Helper" in names
    assert "nested.Nested Helper" in names
    # An embedded keyword's qualified form is a pattern, not a plain name.
    assert "helpers.Open ${page} Page" in set(known["embedded"])
    # The suite file has no callable qualified form: `_get_explicit_runner`
    # searches libraries and resources only.
    assert not any(name.startswith("run.") for name in names)


@pytest.mark.parametrize(
    "name",
    [
        "BuiltIn.Log",
        "builtin.log",
        "BuiltIn._Log",
        "Str.Convert To Upper Case",
        "Str.Convert_To_Upper_Case",
        "helpers.My Helper",
        "nested.Nested Helper",
    ],
)
def test_recording_rejects_an_owner_qualified_name_on_the_default_target(
    tmp_path, name
):
    """`_get_runner_from_suite_file` runs *before* `_get_explicit_runner`.

    So a keyword literally named `BuiltIn.Log` in the suite file wins over the
    explicit `BuiltIn.Log` call - and the suite file is the default target. An
    alias from `WITH NAME` is just as exposed, since the alias is the owner name
    the call has to use.
    """
    outcome = _run_probe(tmp_path, f"Try To Record    {name}")
    assert outcome["outcome"] == "rejected"
    assert "already exists in this suite" in outcome["error"]


def test_a_name_an_embedded_owner_does_not_claim_stays_accepted(tmp_path):
    # `Open Page` is *not* an instantiation of `Open ${page} Page` - Robot does
    # not resolve it there, so refusing it would be a false positive.
    assert _run_probe(tmp_path, "Try To Record    Open Page") == {"outcome": "accepted"}
