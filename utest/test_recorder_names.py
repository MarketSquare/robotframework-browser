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
"""Tests for the naming and escaping rules of recorded keywords."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder import names
from Browser.recorder.cells import cell
from Browser.recorder.names import (
    NAME_LIMIT,
    KnownKeywords,
    NameGuard,
    _embedded_matcher,
    argument_name_error,
    collect_known_keywords,
    existing_keyword_names,
    keyword_name_error,
    normalize_keyword_name,
    plain_argument_name,
)

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


def test_existing_keyword_names():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "k.resource"
        assert existing_keyword_names(target) == set()
        target.write_text("*** Keywords ***\nOne\n    Log    a\n\nTwo\n    Log    b\n")
        assert existing_keyword_names(target) == {"One", "Two"}
        target.write_text("*** Keywords ***\n# only a comment\nOne\n    Log    a\n")
        assert existing_keyword_names(target) == {"One"}
        target.write_text(
            "*** Settings ***\nLibrary    Browser\n\n*** Variables ***\n${X}    1\n\n"
            "*** Test Cases ***\nA Test\n    Log    x\n\n"
            "*** Keywords ***\nOne\n    Log    a\n"
        )
        assert existing_keyword_names(target) == {"One"}


# --------------------------------------------------------------------------- #
# Collecting the keyword names the running suite already knows
# --------------------------------------------------------------------------- #


def test_collect_known_keywords_is_empty_without_a_running_suite():
    # The recorder must stay usable from plain Python, so no suite means no
    # collision set rather than an exception.
    assert collect_known_keywords() == KnownKeywords()


def test_collect_known_keywords_warns_when_the_keyword_store_is_missing(monkeypatch):
    namespace = SimpleNamespace(libraries=[], languages=None)
    context = SimpleNamespace(namespace=namespace)
    monkeypatch.setattr(BuiltIn, "_get_context", lambda self: context)

    warnings = []
    monkeypatch.setattr(names.logger, "warn", warnings.append)

    known = collect_known_keywords()

    assert known == KnownKeywords()
    assert len(warnings) == 1
    assert "_kw_store" in warnings[0]
    assert "resource and suite-file keywords" in warnings[0]


_PROBE_LIBRARY = '''\
import json
import pathlib

from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder.names import NameGuard, collect_known_keywords, existing_keyword_names


def _target(file=None):
    if file:
        return pathlib.Path(file).resolve()
    return pathlib.Path(BuiltIn().get_variable_value("${SUITE_SOURCE}")).resolve()


def _report(payload):
    pathlib.Path(__file__).with_name("probe.json").write_text(json.dumps(payload))


def dump_known_keywords(file=None):
    known = collect_known_keywords()
    _report(
        {
            "names": sorted(known.names),
            "embedded": sorted(name for name, _ in known.embedded),
            "prefixes": sorted(known.bdd_prefixes),
        }
    )


def try_to_record(name, file=None):
    """Check a name exactly as `Record Keyword` does, and report the outcome."""
    guard = NameGuard(collect_known_keywords())
    error = guard.error(name, taken=existing_keyword_names(_target(file)))
    _report({"outcome": "rejected", "error": error} if error else {"outcome": "accepted"})
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
    # A file the suite does not import, so its keywords reach the guard only as
    # `taken` names, never as known ones.
    (tmp_path / "target.resource").write_text(
        "*** Keywords ***\nTarget Only Keyword\n    Log    t\n"
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
        "    Log    ${thing}\n",
        # The call may hold non-ASCII names; Robot reads UTF-8 on every platform.
        encoding="utf-8",
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
    names = set(_run_probe(tmp_path, "Dump Known Keywords")["names"])
    # BuiltIn, an explicitly imported library, an imported resource, a resource
    # imported by that resource, and the suite file's own keywords.
    assert "Log" in names
    assert "No Operation" in names
    assert "Append To List" in names
    assert "My Helper" in names
    assert "Nested Helper" in names
    assert "Suite Local Keyword" in names


def test_collect_known_keywords_covers_bdd_prefix_stripping(tmp_path):
    names = set(_run_probe(tmp_path, "Dump Known Keywords")["names"])
    assert "Given User Is Logged In" in names
    assert "User Is Logged In" in names


def test_recording_rejects_the_bdd_variant_of_a_target_file_keyword(tmp_path):
    outcome = _run_probe(tmp_path, "Try To Record    User Is Logged In")
    assert outcome["outcome"] == "rejected"
    assert "already exists in this suite" in outcome["error"]


def test_recording_rejects_an_embedded_argument_instantiation(tmp_path):
    outcome = _run_probe(tmp_path, "Try To Record    Open Login Page")
    assert outcome["outcome"] == "rejected"
    assert "Open ${page} Page" in outcome["error"]


def test_recording_rejects_an_embedded_keyword_of_the_target_file(tmp_path):
    outcome = _run_probe(
        tmp_path, "Try To Record    Open Login Page    file=helpers.resource"
    )
    assert outcome["outcome"] == "rejected"
    assert "Open ${page} Page" in outcome["error"]


def test_recording_rejects_an_embedded_keyword_of_the_default_target(tmp_path):
    # The suite file's own embedded keyword, on the default path.
    outcome = _run_probe(tmp_path, "Try To Record    Open Coffee From Suite")
    assert outcome["outcome"] == "rejected"
    assert "Open ${thing} From Suite" in outcome["error"]


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
    outcome = _run_probe(tmp_path, f"Try To Record    {name}")
    assert outcome["outcome"] == "rejected"
    assert "already exists in this suite" in outcome["error"]


def test_a_name_an_embedded_owner_does_not_claim_stays_accepted(tmp_path):
    # `Open Page` is *not* an instantiation of `Open ${page} Page` - Robot does
    # not resolve it there, so refusing it would be a false positive.
    assert _run_probe(tmp_path, "Try To Record    Open Page") == {"outcome": "accepted"}


def test_recording_rejects_a_target_keyword_behind_a_symlink(tmp_path):
    outcome = _run_probe(
        tmp_path,
        "Try To Record    Target Only Keyword    file=link/target.resource",
        via_symlink=True,
    )
    assert outcome["outcome"] == "rejected"
    assert "already exists" in outcome["error"]


def test_recording_rejects_a_keyword_of_the_target_file(tmp_path):
    outcome = _run_probe(
        tmp_path, "Try To Record    target_only_keyword    file=target.resource"
    )
    assert outcome["outcome"] == "rejected"
    assert "already exists" in outcome["error"]


@pytest.mark.parametrize(
    "name", ["email", "item_id", "_x", "Password2", "${email}", "${_x}"]
)
def test_usable_argument_names_are_accepted(name):
    assert argument_name_error(name) is None


@pytest.mark.parametrize(
    "name",
    [
        "",
        "2fa",
        "e mail",
        "a-b",
        "x}",
        "a\nb",
        "ä",
        None,
        42,
        "${",
        "${}",
        "${email",
        "${e mail}",
        "${a}b}",
        "${${a}}",
        "${a.b}",
        "@{list}",
    ],
)
def test_unusable_argument_names_are_reported(name):
    assert argument_name_error(name)


@pytest.mark.parametrize(
    "name", ["SPACE", "s_pace", "empty", "True", "test_name", "OUTPUT_DIR"]
)
def test_argument_names_shadowing_robot_variables_are_reported(name):
    assert "built-in variable" in argument_name_error(name)
    assert "built-in variable" in argument_name_error(f"${{{name}}}")


@pytest.mark.parametrize(
    ("given", "plain"), [("${email}", "email"), ("email", "email"), ("${a", "${a")]
)
def test_plain_argument_name(given, plain):
    assert plain_argument_name(given) == plain


def test_name_guard_rejects_a_taken_name_in_any_spelling():
    guard = NameGuard(KnownKeywords())
    assert guard.error("l_ogin as ADMIN", taken=["Login As Admin"])


def test_name_guard_reports_an_invalid_name_before_collisions():
    guard = NameGuard(KnownKeywords(names=frozenset({"Log"})))
    assert "must not be empty" in guard.error("")


def test_name_guard_rejects_a_known_library_keyword():
    guard = NameGuard(KnownKeywords(names=frozenset({"Click"})))
    assert "Click" in guard.error("click")


def test_inner_part_keeps_edge_spaces_and_hash():
    assert cell("price ", at_end=False) == "price "
    assert cell(" #x", at_start=False) == " #x"
    assert cell(" x ") == "\\ x \\"
    assert cell("#x") == "\\#x"


@pytest.mark.parametrize(
    ("value", "written"),
    [
        ("test  ", "test \\ \\"),
        ("test ", "test \\"),
        ("  lead", "\\ \\ lead"),
        ("a b", "a b"),
        ("a  b", "a \\ b"),
        ("a     b", "a \\ \\ \\ \\ b"),
        (" ", "\\ \\"),
        ("  ", "\\ \\ \\"),
        ("x  [0]", "x \\ [0]"),
        ("#  x", "\\# \\ x"),
    ],
)
def test_spaces_are_escaped_with_backslashes(value, written):
    assert cell(value) == written


def test_spaces_at_the_edge_of_an_inner_part_stay_plain():
    assert cell("  b", at_start=False) == " \\ b"
    assert cell("a  ", at_end=False) == "a \\ "


# --------------------------------------------------------------------------- #
# In-process coverage of the namespace walk, the matcher fallbacks and NameGuard
# --------------------------------------------------------------------------- #


def _fake_context(
    monkeypatch, *, libraries, resources=None, suite_file=None, prefixes=()
):
    store = SimpleNamespace(resources=resources or {}, suite_file=suite_file)
    namespace = SimpleNamespace(
        libraries=libraries,
        _kw_store=store,
        languages=SimpleNamespace(bdd_prefixes=prefixes),
    )
    context = SimpleNamespace(namespace=namespace)
    monkeypatch.setattr(BuiltIn, "_get_context", lambda self: context)


def _owner(name, *keyword_names):
    return SimpleNamespace(
        name=name, keywords=[SimpleNamespace(name=kw) for kw in keyword_names]
    )


def test_collect_known_keywords_reads_libraries_resources_and_suite_file(monkeypatch):
    _fake_context(
        monkeypatch,
        libraries=[_owner("lib", "Plain Lib Kw", "")],
        resources={"res": _owner("res", "Resource Kw", "Open ${page} Page")},
        suite_file=_owner("suite", "Suite Kw"),
        prefixes=("Given",),
    )

    known = collect_known_keywords()

    assert known.bdd_prefixes == ("Given",)
    assert {"Plain Lib Kw", "lib.Plain Lib Kw", "Resource Kw", "res.Resource Kw"} <= (
        known.names
    )
    # The suite file's own keywords have no callable qualified form.
    assert "Suite Kw" in known.names
    assert "suite.Suite Kw" not in known.names
    assert "" not in known.names
    declared = [d for d, _ in known.embedded]
    assert "Open ${page} Page" in declared
    assert "res.Open ${page} Page" in declared


def test_collect_known_keywords_without_a_suite_file(monkeypatch):
    _fake_context(monkeypatch, libraries=[_owner("lib", "Kw")], suite_file=None)
    assert "Kw" in collect_known_keywords().names


def test_collect_known_keywords_handles_namespace_without_languages(monkeypatch):
    namespace = SimpleNamespace(
        libraries=[_owner("lib", "Kw")],
        _kw_store=SimpleNamespace(resources={}, suite_file=None),
    )
    context = SimpleNamespace(namespace=namespace)
    monkeypatch.setattr(BuiltIn, "_get_context", lambda self: context)
    assert collect_known_keywords().bdd_prefixes == ()


def test_bdd_variants_strip_a_prefix_only_when_something_remains():
    assert names._bdd_variants("Given Alice Signs In", ("Given", "When")) == {
        "Alice Signs In"
    }
    assert names._bdd_variants("Given", ("Given",)) == set()
    assert names._bdd_variants("Other Name", ("Given",)) == set()


def test_embedded_matcher_survives_a_name_robot_cannot_parse(monkeypatch):
    def broken(name):
        raise ValueError("bad pattern")

    monkeypatch.setattr(names.EmbeddedArguments, "from_name", broken)
    assert _embedded_matcher("Open ${page:[} Page") is None


def test_embedded_matcher_falls_back_to_roberts_own_matcher(monkeypatch):
    monkeypatch.setattr(names, "_normalized_embedded_pattern", lambda name: None)
    matcher = _embedded_matcher("Open ${page} Page")
    assert matcher("Open Login Page") is True
    assert matcher("Close Login Page") is False


def test_normalized_pattern_is_none_when_the_parser_fails(monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("no parser")

    monkeypatch.setattr(names, "_custom_pattern", broken)
    assert names._normalized_embedded_pattern("Open ${page} Page") is None


class _OldParser:
    """Robot 7.1/7.2: the split is called `_get_name_and_pattern`."""

    def _get_name_and_pattern(self, name):
        if ":" in name:
            arg, pattern = name.split(":", 1)
            return arg, pattern, True
        return name, ".*?", False


def test_custom_pattern_reads_the_older_parser_too():
    assert names._custom_pattern(_OldParser(), "n:\\d+") == "\\d+"
    assert names._custom_pattern(_OldParser(), "page") is None


def test_a_parser_without_either_method_warns_once_and_keeps_the_literal_check(
    monkeypatch,
):
    warnings = []
    monkeypatch.setattr(names.logger, "warn", warnings.append)
    monkeypatch.setattr(names, "_warned_without_normalized_check", False)
    monkeypatch.setattr(names, "EmbeddedArgumentParser", object)
    assert names._normalized_embedded_pattern("Open ${page} Page") is None
    assert names._normalized_embedded_pattern("Close ${page} Page") is None
    assert len(warnings) == 1
    matches = _embedded_matcher("Open ${page} Page")
    assert matches("Open Login Page")
    assert not matches("Open_Login_Page")


def test_the_literal_matcher_falls_back_to_match():
    class OldEmbedded:
        def match(self, name):
            return name if name == "Open Login Page" else None

    matches = names._literal_matcher(OldEmbedded())
    assert matches("Open Login Page")
    assert not matches("Close Login Page")


def test_normalized_pattern_is_none_for_a_literal_name():
    assert names._normalized_embedded_pattern("Open Login Page") is None


def test_name_guard_rejects_what_an_embedded_keyword_would_claim():
    known = KnownKeywords(
        embedded=(("Open ${page} Page", _embedded_matcher("Open ${page} Page")),)
    )
    message = NameGuard(known).error("open_login_page")
    assert "Open ${page} Page" in message


def test_name_guard_ignores_an_embedded_matcher_that_raises():
    def explode(name):
        raise RuntimeError("boom")

    known = KnownKeywords(embedded=(("Broken ${x}", explode),))
    assert NameGuard(known).error("Something Fresh") is None


def test_name_guard_skips_a_non_matching_embedded_keyword():
    known = KnownKeywords(
        embedded=(("Open ${page} Page", _embedded_matcher("Open ${page} Page")),)
    )
    assert NameGuard(known).error("Close It") is None


def test_names_up_to_the_limit_are_accepted_and_longer_ones_reported():
    assert keyword_name_error("K" * NAME_LIMIT) is None
    assert "200 characters" in keyword_name_error("K" * (NAME_LIMIT + 1))
    assert argument_name_error("a" * NAME_LIMIT) is None
    assert "200 characters" in argument_name_error("a" * (NAME_LIMIT + 1))
    assert "200 characters" in argument_name_error("${" + "a" * (NAME_LIMIT + 1) + "}")
