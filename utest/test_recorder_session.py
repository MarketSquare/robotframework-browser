import tempfile
from pathlib import Path

import pytest
from robot.running.arguments.embedded import EmbeddedArguments

from Browser.recorder.names import KnownKeywords
from Browser.recorder.session import RecorderSession

CLICK_A = {
    "name": "click",
    "selector": "css=.a",
    "button": "left",
    "modifiers": 0,
    "clickCount": 1,
}
CLICK_B = {**CLICK_A, "selector": "css=.b"}
FILL = {"name": "fill", "selector": "css=.i", "text": "a"}


@pytest.fixture
def target():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp) / "out.resource"


def test_starts_idle_and_drops_events(target):
    session = RecorderSession(target)
    assert session.state == "idle"
    session.handle_event("added", CLICK_A)
    assert session.toolbar_state()["steps"] == []
    assert not target.exists()


def test_new_keyword_starts_recording(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    assert session.state == "recording"
    session.handle_event("added", CLICK_A)
    assert session.toolbar_state()["steps"] == ["Click    css=.a"]


def test_updated_replaces_the_last_line(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", FILL)
    session.handle_event("updated", {**FILL, "text": "abc"})
    assert session.toolbar_state()["steps"] == ["Fill Text    css=.i    abc"]


def test_undo_removes_the_last_line_and_kills_later_updates(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    session.handle_event("added", FILL)
    session.handle_command({"cmd": "undo"})
    assert session.toolbar_state()["steps"] == ["Click    css=.a"]
    # The undone action keeps being refined by Playwright - it must stay dead.
    session.handle_event("updated", {**FILL, "text": "abc"})
    assert session.toolbar_state()["steps"] == ["Click    css=.a"]
    # A genuinely new action records again.
    session.handle_event("added", CLICK_B)
    assert session.toolbar_state()["steps"] == ["Click    css=.a", "Click    css=.b"]


def test_finish_records_the_keyword_and_returns_to_idle(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    assert session.state == "idle"
    assert session.keywords == ["Login"]
    assert "Login" in target.read_text()


def test_finish_with_no_steps_discards_the_keyword(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Empty"})
    session.handle_command({"cmd": "finish"})
    assert session.keywords == []
    assert session.state == "idle"
    # discard() saves, so the file exists and must not mention the keyword.
    assert "Empty" not in target.read_text()


def test_discard_removes_the_keyword_and_returns_to_idle(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Oops"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "discard"})
    assert session.state == "idle"
    assert session.keywords == []
    assert "Oops" not in target.read_text()


def test_several_keywords_in_one_session(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    session.handle_command({"cmd": "new", "name": "Search"})
    session.handle_event("added", CLICK_B)
    session.handle_command({"cmd": "finish"})

    assert session.keywords == ["Login", "Search"]
    content = target.read_text()
    assert "Login" in content
    assert "Search" in content
    assert "Click    css=.a" in content
    assert "Click    css=.b" in content


def test_duplicate_name_is_rejected(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    session.handle_command({"cmd": "new", "name": "Login"})
    assert session.state == "idle"
    assert "already exists" in session.toolbar_state()["error"]


def test_duplicate_of_a_name_already_in_the_file_is_rejected(target):
    target.write_text("*** Keywords ***\nExisting\n    Log    hi\n")
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Existing"})
    assert session.state == "idle"
    assert "already exists" in session.toolbar_state()["error"]


def test_empty_name_is_rejected(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "   "})
    assert session.state == "idle"
    assert session.toolbar_state()["error"]


#: Names that must never reach the file. The command channel is exposed to the
#: page under test (`context.exposeBinding('__rfbCommand', ...)`), so a keyword
#: name is untrusted input: written verbatim, a newline would end the row and
#: turn the rest into further Robot source, i.e. code injection into the user's
#: own repository.
_BAD_NAMES = [
    "",
    "   ",
    "Good\nEvil Keyword\n    Log    pwned",
    "Good\r\n    Log    pwned",
    "Tab\there",
    "Null\x00byte",
    "Bell\x07",
    " Leading",
    "Trailing ",
    "Two  Spaces",
    "#comment",
    "*** Keywords ***",
    # Robot's lexer is unicode aware where an ASCII-only check is not: it splits
    # cells on `\s{2,}` with `re.UNICODE` and splits lines with
    # `str.splitlines()`. So these reach an *executing* `Log    PWNED` just like
    # the `\n` above, one codepoint away from it.
    "Good\u3000\u3000Log\u3000\u3000PWNED",
    "Good\xa0\xa0Log\xa0\xa0PWNED",
    "Good \xa0Log \xa0PWNED",
    "Good\u2028Evil Keyword\u2028\u3000\u3000Log\u3000\u3000PWNED",
    "Good\u2028Evil Keyword \xa0Log \xa0PWNED",
    "Good\u2029Evil Keyword\u2029\u3000\u3000Log\u3000\u3000PWNED",
    "Good\x85Evil Keyword\x85\u3000\u3000Log\u3000\u3000PWNED",
    # A line starting with a pipe is a pipe-separated row: pure ASCII, no
    # control character, no double space, and still keyword `Good` + `Log`.
    "| Good | Log | PWNED",
    # Robot's continuation marker: no keyword is defined and the resource
    # becomes unimportable.
    "...",
]


@pytest.mark.parametrize("name", _BAD_NAMES)
def test_unusable_name_is_rejected_by_the_new_command(target, name):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": name})
    assert session.state == "idle"
    assert session.toolbar_state()["error"]
    assert not target.exists()


def test_injected_name_does_not_write_a_second_keyword(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Good"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    session.handle_command(
        {"cmd": "new", "name": "Good2\nEvil Keyword\n    Log    pwned"}
    )
    assert session.state == "idle"
    assert session.keywords == ["Good"]
    content = target.read_text()
    assert "Evil Keyword" not in content
    assert "pwned" not in content


@pytest.mark.parametrize("name", _BAD_NAMES)
def test_unusable_fixed_name_raises(target, name):
    # `fixed_name` comes from the suite author, so it must fail loudly.
    with pytest.raises(ValueError, match="Keyword name"):
        RecorderSession(target, fixed_name=name)
    assert not target.exists()


def test_new_while_recording_is_rejected(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_command({"cmd": "new", "name": "Search"})
    assert session.toolbar_state()["name"] == "Login"
    assert "Finish it first" in session.toolbar_state()["error"]


def test_finish_and_undo_while_idle_are_rejected(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "finish"})
    assert session.toolbar_state()["error"]
    session.handle_command({"cmd": "undo"})
    assert session.toolbar_state()["error"]


def test_unknown_command_is_logged_and_ignored(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "wat"})
    assert any("wat" in entry for entry in session.log)
    assert session.state == "idle"


def test_stop_marks_the_session_stopped(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "stop"})
    assert session.stopped is True


def test_signals_are_ignored(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("signal", {"name": "navigation", "url": "http://a"})
    assert session.toolbar_state()["steps"] == []


def test_unmappable_action_is_skipped_and_does_not_capture_updates(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    session.handle_event("added", {"name": "assertSnapshot", "selector": "css=.s"})
    session.handle_event("updated", {"name": "assertSnapshot", "selector": "css=.s"})
    assert session.toolbar_state()["steps"] == ["Click    css=.a"]


def test_close_finishes_an_in_progress_keyword(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    assert session.close() == ["Login"]
    assert "Click    css=.a" in target.read_text()


def test_fixed_name_session_starts_recording_immediately(target):
    session = RecorderSession(target, fixed_name="Only One")
    assert session.state == "recording"
    assert session.toolbar_state()["fixedName"] is True
    session.handle_event("added", CLICK_A)
    assert session.toolbar_state()["steps"] == ["Click    css=.a"]


def test_fixed_name_session_rejects_new_and_restarts_on_discard(target):
    session = RecorderSession(target, fixed_name="Only One")
    session.handle_command({"cmd": "new", "name": "Other"})
    assert session.toolbar_state()["name"] == "Only One"
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "discard"})
    # Discard starts the same keyword over rather than leaving nothing to record.
    assert session.state == "recording"
    assert session.toolbar_state()["name"] == "Only One"
    assert session.toolbar_state()["steps"] == []


def test_error_is_cleared_on_the_next_successful_command_but_shown_first(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_command({"cmd": "new", "name": "Search"})
    # The rejection must still be visible on the very next read.
    assert "Finish it first" in session.toolbar_state()["error"]
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    # A later successful command must not leave the stale error behind.
    assert session.toolbar_state()["error"] is None


def test_toolbar_state_shape(target):
    session = RecorderSession(target)
    state = session.toolbar_state()
    assert set(state) == {
        "state",
        "name",
        "steps",
        "keywords",
        "file",
        "error",
        "fixedName",
    }
    assert state["file"] == target.name


# --------------------------------------------------------------------------- #
# Collision with keywords the running suite already knows
# --------------------------------------------------------------------------- #

#: Names of real keywords a suite recording with this plugin always has in
#: scope. A recorded keyword lands in a resource, and resource keywords outrank
#: library keywords, so each of these would silently replace the real one - and
#: the recorded body can `Go To` an attacker URL or `Upload File By Selector`
#: an attacker-chosen local path.
_SUITE_KEYWORDS = ["Log", "No Operation", "Click", "New Page", "Open Browser"]


@pytest.mark.parametrize("name", _SUITE_KEYWORDS)
def test_new_rejects_a_name_that_shadows_a_keyword_of_the_running_suite(target, name):
    session = RecorderSession(
        target, known=KnownKeywords(names=frozenset(_SUITE_KEYWORDS))
    )
    session.handle_command({"cmd": "new", "name": name})
    assert session.state == "idle"
    error = session.toolbar_state()["error"]
    assert name in error
    assert "another name" in error
    assert not target.exists()


@pytest.mark.parametrize("name", _SUITE_KEYWORDS)
def test_fixed_name_that_shadows_a_keyword_of_the_running_suite_raises(target, name):
    with pytest.raises(ValueError, match="already exists in this suite"):
        RecorderSession(
            target,
            fixed_name=name,
            known=KnownKeywords(names=frozenset(_SUITE_KEYWORDS)),
        )
    assert not target.exists()


def test_collision_check_uses_robots_own_normalisation(target):
    # Robot resolves keyword names caseless and ignoring spaces/underscores, so
    # these are the *same* keyword to it.
    session = RecorderSession(
        target, known=KnownKeywords(names=frozenset({"Login As Admin"}))
    )
    session.handle_command({"cmd": "new", "name": "l_ogin as admin"})
    assert session.state == "idle"
    assert session.toolbar_state()["error"]


def test_duplicate_in_the_target_file_is_normalised_too(target):
    # Without normalisation Robot accepts the file, then errors on the duplicate
    # at run time - and the user's *pre-existing* keyword stops working.
    target.write_text("*** Keywords ***\nLogin As Admin\n    Log    hi\n")
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "l_ogin as admin"})
    assert session.state == "idle"
    assert "already exists" in session.toolbar_state()["error"]


def test_duplicate_recorded_this_session_is_normalised_too(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login As Admin"})
    session.handle_event("added", CLICK_A)
    session.handle_command({"cmd": "finish"})
    session.handle_command({"cmd": "new", "name": "LOGIN_asadmin"})
    assert session.state == "idle"
    assert "already exists" in session.toolbar_state()["error"]


def test_a_name_no_keyword_uses_is_still_accepted(target):
    session = RecorderSession(
        target, known=KnownKeywords(names=frozenset(_SUITE_KEYWORDS))
    )
    session.handle_command({"cmd": "new", "name": "Login As Büroleiter"})
    assert session.state == "recording"
    assert session.toolbar_state()["error"] is None


def test_no_known_keywords_keeps_the_session_usable(target):
    # `known_keywords` is empty when no suite is running; the recorder must
    # still work from plain Python.
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Log"})
    assert session.state == "recording"


# --------------------------------------------------------------------------- #
# Malformed input must not kill an in-progress recording
# --------------------------------------------------------------------------- #


def test_lone_surrogate_name_is_rejected_instead_of_crashing_the_save(target):
    # `model.save()` would raise UnicodeEncodeError, which used to abort the
    # whole recording session from the poll loop.
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "\ud800"})
    assert session.state == "idle"
    assert session.toolbar_state()["error"]
    assert not target.exists()


def test_a_malformed_command_does_not_abort_an_in_progress_recording(target):
    session = RecorderSession(target)
    session.handle_command({"cmd": "new", "name": "Login"})
    session.handle_event("added", CLICK_A)
    for bad in ({"cmd": "new", "name": "\ud800"}, {"cmd": 42}, {}):
        session.handle_command(bad)
    # Still recording, and the work done so far survived.
    assert session.state == "recording"
    session.handle_event("added", CLICK_B)
    session.handle_command({"cmd": "finish"})
    assert session.keywords == ["Login"]
    assert "Click    css=.b" in target.read_text()


# --------------------------------------------------------------------------- #
# Embedded-argument keywords and BDD prefixes
# --------------------------------------------------------------------------- #

#: Real Robot matchers, built the way the plugin builds them, so these tests
#: exercise the same matching Robot performs when it resolves a call.
_EMBEDDED = [
    (name, EmbeddedArguments.from_name(name).matches)
    for name in ("Open ${page} Page", "Zahle ${betrag} %")
]

_BDD_PREFIXES = ("Given", "When", "Then", "And", "But", "Angenommen", "Wenn", "Dann")


@pytest.mark.parametrize(
    "name",
    ["Open Login Page", "open the checkout page", "Zahle 50 %"],
)
def test_new_rejects_a_name_an_embedded_keyword_would_claim(target, name):
    # `Open ${page} Page` is *instantiated* by a literal call, so a recording
    # under that literal name silently replaces it - no name collision needed.
    session = RecorderSession(target, known=KnownKeywords(embedded=tuple(_EMBEDDED)))
    session.handle_command({"cmd": "new", "name": name})
    assert session.state == "idle"
    assert "another name" in session.toolbar_state()["error"]
    assert not target.exists()


def test_fixed_name_an_embedded_keyword_would_claim_raises(target):
    with pytest.raises(ValueError, match=r"Open \$\{page\} Page"):
        RecorderSession(
            target,
            fixed_name="Open Login Page",
            known=KnownKeywords(embedded=tuple(_EMBEDDED)),
        )
    assert not target.exists()


#: Every name the suite is documented to accept, plus the international set.
#: An over-strict collision check is its own defect, and embedded matching is
#: exactly where one creeps in.
_ACCEPTED_NAMES = [
    "Anmelden Als Büroleiter",
    "Öffne Übersicht",
    "登录系统",
    "تسجيل الدخول",
    "Café Größe 2m²",
    "A/B Test",
    "Søk Etter Produkt 3.0 (Raskt)",
    "Zahle 50 % {netto}",
    "E-Mail@Domain Prüfen",
    "Größe 100%",
    "Login As Admin",
    "Open Page",
    "Open The Login Page Again Now",
    "Whenever Possible",
    "Andere Seite Öffnen",
]


@pytest.mark.parametrize("name", _ACCEPTED_NAMES)
def test_embedded_and_bdd_checks_do_not_reject_ordinary_names(target, name):
    session = RecorderSession(
        target,
        known=KnownKeywords(
            names=frozenset(_SUITE_KEYWORDS),
            embedded=tuple(_EMBEDDED),
            bdd_prefixes=_BDD_PREFIXES,
        ),
    )
    session.handle_command({"cmd": "new", "name": name})
    assert session.toolbar_state()["error"] is None
    assert session.state == "recording"


def test_new_rejects_a_bdd_prefixed_name_because_it_would_be_unreachable(target):
    # NOT a hijack: `Namespace._get_bdd_style_runner` resolves the *stripped*
    # name first and only falls through when nothing matches it, so a recorded
    # `Given Log` never takes a `Given Log` call away from the real `Log` -
    # confirmed with a differential execution oracle. It can only be dead code
    # in the user's suite, so the recorder refuses it rather than writing a
    # keyword that can never run.
    session = RecorderSession(
        target,
        known=KnownKeywords(names=frozenset({"Log"}), bdd_prefixes=_BDD_PREFIXES),
    )
    session.handle_command({"cmd": "new", "name": "Given Log"})
    assert session.state == "idle"
    assert "another name" in session.toolbar_state()["error"]


def test_new_rejects_a_bdd_prefixed_name_that_takes_over_a_target_file_keyword(target):
    target.write_text("*** Keywords ***\nUser Is Logged In\n    Log    hi\n")
    session = RecorderSession(target, known=KnownKeywords(bdd_prefixes=_BDD_PREFIXES))
    session.handle_command({"cmd": "new", "name": "Wenn User Is Logged In"})
    assert session.state == "idle"
    assert "another name" in session.toolbar_state()["error"]


def test_a_bdd_prefixed_name_that_shadows_an_embedded_keyword_is_rejected(target):
    session = RecorderSession(
        target,
        known=KnownKeywords(embedded=tuple(_EMBEDDED), bdd_prefixes=_BDD_PREFIXES),
    )
    session.handle_command({"cmd": "new", "name": "Given Open Login Page"})
    assert session.state == "idle"
    assert "another name" in session.toolbar_state()["error"]


def test_fixed_name_is_checked_against_the_target_files_own_names_too(target):
    # `Record Keyword` ran a *weaker* check than the toolbar's `new`: it never
    # passed the target file's own keywords along, so a name the toolbar
    # refuses was accepted from the suite side.
    target.write_text("*** Keywords ***\nUser Is Logged In\n    Log    hi\n")
    with pytest.raises(ValueError, match="already exists in this suite"):
        RecorderSession(
            target,
            fixed_name="Wenn User Is Logged In",
            known=KnownKeywords(bdd_prefixes=_BDD_PREFIXES),
        )


def test_a_broken_embedded_matcher_does_not_kill_the_session(target):
    def boom(name):
        raise RuntimeError("no")

    session = RecorderSession(
        target, known=KnownKeywords(embedded=(("Broken ${x}", boom),))
    )
    session.handle_command({"cmd": "new", "name": "Login As Admin"})
    assert session.state == "recording"


def test_a_fixed_name_the_target_file_already_defines_is_rejected(target):
    # AC-37: a Keyword Recording never extends an existing keyword.
    target.write_text("*** Keywords ***\nSuite Local Keyword\n    Log    hi\n")
    with pytest.raises(ValueError, match="already exists"):
        RecorderSession(target, fixed_name="suite_local_keyword")
    assert target.read_text().count("Log    hi") == 1
