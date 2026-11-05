from __future__ import annotations

import pytest

from Browser.recorder.cells import tokens
from Browser.recorder.model import RecordedKeyword
from Browser.recorder.names import KnownKeywords
from Browser.recorder.picker import SelectorPicker
from Browser.recorder.session import (
    _STARTING,
    _UNREACHABLE_PAGE,
    MAX_RAW_LENGTH,
    MAX_RAW_TOTAL,
    SETTLE_SECONDS,
    TOOLBAR_TEXT_LIMIT,
    RecorderSession,
)


class FakeTarget:
    label = "fake.resource"

    def __init__(self, existing=(), fail=False):
        self.saved: list[str] = []
        self.finished: list[str] = []
        self.removed: list[str] = []
        self._existing = set(existing)
        self.fail = fail

    def existing_names(self):
        return set(self._existing)

    def save(self, keyword: RecordedKeyword):
        if self.fail:
            raise OSError("read-only")
        self.saved.append(keyword.block())

    def remove(self, name):
        self.removed.append(name)

    def finish(self, keyword):
        self.finished.append(keyword.block())


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


FILL = {"name": "fill", "selector": "#n", "text": "Alice"}
CLICK = {
    "name": "click",
    "selector": "#b",
    "button": "left",
    "clickCount": 1,
    "modifiers": 0,
}


def session(**kwargs):
    clock = kwargs.pop("clock", Clock())
    target = kwargs.pop("target", FakeTarget())
    return RecorderSession(target, clock=clock, **kwargs), target, clock


def settle(s, clock):
    clock.now += SETTLE_SECONDS
    s.tick()


def start(s, name):
    """Send New and let its settle time pass, as the poll loop does."""
    s.handle_command({"cmd": "new", "name": name})
    settle(s, s._clock)


def test_idle_actions_are_not_recorded():
    s, target, _ = session()
    s.handle_event("added", FILL)
    assert target.saved == []
    assert s.toolbar_state()["calls"] == []


def test_new_record_finish():
    s, target, clock = session()
    start(s, "Fill Name")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    assert s.toolbar_state()["pending"] == "finish"
    assert target.finished == []
    settle(s, clock)
    assert s.keywords == ["Fill Name"]
    assert "Fill Text" in target.finished[0]
    assert s.state == "idle"


def test_click_arriving_after_finish_lands_in_the_finished_keyword():
    s, target, clock = session()
    start(s, "K")
    s.handle_command({"cmd": "finish"})
    clock.now += 0.4
    s.handle_event("added", CLICK)
    settle(s, clock)
    assert "Click" in target.finished[0]


def test_commands_are_rejected_while_finishing():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "undo"})
    assert "finishing" in s.toolbar_state()["error"].lower()
    assert len(s.toolbar_state()["calls"]) == 1


def test_stop_overrides_a_pending_finish():
    s, target, clock = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "stop"})
    settle(s, clock)
    assert s.stopped
    assert s.close() == ["K"]
    assert target.finished


def test_finish_of_an_empty_keyword_saves_nothing():
    s, target, clock = session()
    start(s, "K")
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    assert target.finished == [] and s.keywords == []


def test_undo_ignores_later_updates_of_the_undone_action():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "undo"})
    s.handle_event("updated", {**FILL, "text": "Alicia"})
    assert s.toolbar_state()["calls"] == []


def test_update_after_a_skipped_action_appends():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", CLICK)
    s.handle_event("added", {"name": "somethingNew", "selector": "#x"})
    s.handle_event("updated", FILL)
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == ["Click", "Fill Text"]


def test_unsupported_action_shows_a_notice():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {"name": "somethingNew", "selector": "#x"})
    assert "somethingNew" in s.toolbar_state()["notice"]


def test_open_page_is_silent():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {"name": "openPage", "url": "about:blank"})
    assert s.toolbar_state()["notice"] is None
    assert s.toolbar_state()["calls"] == []


def test_toolbar_shows_the_assignment_of_a_download_promise():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", CLICK)
    s.handle_event("signal", {"name": "download"})
    calls = s.toolbar_state()["calls"]
    assert [(c["assign"], c["keyword"]) for c in calls] == [
        ("${download}=", "Promise To Wait For Download"),
        (None, "Click"),
        (None, "Wait For"),
    ]


def test_dialog_signal_and_undo_as_a_group():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", CLICK)
    s.handle_event("signal", {"name": "dialog"})
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == [
        "Handle Future Dialogs",
        "Click",
    ]
    s.handle_command({"cmd": "undo"})
    assert s.toolbar_state()["calls"] == []


def test_discard_removes_and_returns_to_idle():
    s, target, clock = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "discard"})
    settle(s, clock)
    assert target.removed == ["K"] and s.state == "idle"


def test_fixed_name_discard_restarts_the_same_keyword():
    s, _, clock = session(fixed_name="K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "discard"})
    settle(s, clock)
    assert s.state == "recording" and s.toolbar_state()["name"] == "K"


def test_fixed_name_rejects_new_and_finish():
    s, _, _ = session(fixed_name="K")
    start(s, "Other")
    assert s.toolbar_state()["error"]
    s.handle_command({"cmd": "finish"})
    assert s.toolbar_state()["error"]


def test_fixed_name_existing_in_target_raises():
    with pytest.raises(ValueError, match="already exists"):
        session(fixed_name="Existing", target=FakeTarget(existing={"Existing"}))


def test_new_rejects_shadowing_names():
    s, _, _ = session(known=KnownKeywords(names=frozenset({"Click"})))
    start(s, "click")
    assert "shadowed" in s.toolbar_state()["error"]
    assert s.state == "idle"


def test_new_rejects_a_name_recorded_earlier_in_the_session():
    s, _, clock = session()
    for _ in range(2):
        start(s, "K")
        s.handle_event("added", FILL)
        s.handle_command({"cmd": "finish"})
        settle(s, clock)
    assert s.keywords == ["K"]


def test_close_saves_a_running_keyword():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    assert s.close() == ["K"]
    assert target.finished


def test_text_of_all_finished_keywords():
    s, _, clock = session()
    for name in ("A", "B"):
        start(s, name)
        s.handle_event("added", FILL)
        s.handle_command({"cmd": "finish"})
        settle(s, clock)
    assert s.text().count("*** Keywords ***") == 1
    assert "\nA\n" in s.text() and "\nB\n" in s.text()


def test_argument_offer_and_replace():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Alice"})
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "who",
            "raw": "Alice",
        }
    )
    assert s.toolbar_state()["offer"] == {
        "argument": "who",
        "text": "Alice",
        "occurrences": [[1, 1]],
    }
    s.handle_command({"cmd": "replace", "argument": "who", "occurrences": [[1, 1]]})
    state = s.toolbar_state()
    assert state["offer"] is None
    assert [c["values"][1]["tokens"] for c in state["calls"]] == [
        [["variable", "${who}"]],
        [["variable", "${who}"]],
    ]


def test_argument_written_as_a_variable_gets_its_plain_name():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_event("added", {**FILL, "selector": "#m"})
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "${who}",
            "raw": "Alice",
        }
    )
    state = s.toolbar_state()
    assert state["error"] is None
    assert state["arguments"][0]["name"] == "who"
    assert state["offer"]["argument"] == "who"
    assert "[Arguments]    ${who}=Alice" in target.saved[-1]


def test_malformed_variable_argument_name_is_rejected():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "${who",
            "raw": "Alice",
        }
    )
    assert "${email}" in s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


def test_the_default_is_chosen_when_the_argument_is_made():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "who",
            "useDefault": False,
            "raw": "Alice",
        }
    )
    assert s.toolbar_state()["arguments"] == [
        {"name": "who", "default": "Alice", "useDefault": False}
    ]
    assert "[Arguments]    ${who}\n" in target.saved[-1]


@pytest.mark.parametrize("use_default", ["false", 0, None])
def test_use_default_must_be_a_boolean(use_default):
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command(arg(useDefault=use_default))
    assert "'useDefault'" in s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


def test_toolbar_shortens_long_texts_but_quotes_the_whole_value():
    s, _, _ = session()
    start(s, "K")
    text = "a" * (TOOLBAR_TEXT_LIMIT * 2)
    s.handle_event("added", {**FILL, "text": text})
    call = s.toolbar_state()["calls"][0]
    shown = "".join(text for _, text in call["values"][1]["tokens"])
    assert len(shown) == TOOLBAR_TEXT_LIMIT
    assert shown.endswith("\u2026")
    assert call["values"][1]["raw"] == text
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": len(text),
            "name": "long",
            "raw": text,
        }
    )
    state = s.toolbar_state()
    assert state["error"] is None
    assert len(state["arguments"][0]["default"]) == TOOLBAR_TEXT_LIMIT


def test_toolbar_offers_no_argument_for_a_value_too_long_to_quote():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {**FILL, "text": "a" * MAX_RAW_LENGTH})
    value = s.toolbar_state()["calls"][0]["values"][1]
    assert value["selectable"] is False
    assert value["raw"] is None


def test_toolbar_state_quotes_values_up_to_a_total_budget():
    s, _, _ = session()
    start(s, "K")
    text = "a" * (MAX_RAW_LENGTH - 10)
    count = MAX_RAW_TOTAL // MAX_RAW_LENGTH + 2
    for index in range(count):
        s.handle_event("added", {**FILL, "selector": f"#n{index}", "text": text})
    values = [c["values"][1] for c in s.toolbar_state()["calls"]]
    assert len(values) == count
    assert values[0]["raw"] == text
    assert values[-1] == {
        "tokens": values[-1]["tokens"],
        "selectable": False,
        "raw": None,
    }
    quoted = sum(len(v["raw"]) for v in values if v["raw"] is not None)
    assert quoted <= MAX_RAW_TOTAL


def test_toolbar_budget_counts_escaped_json():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {**FILL, "text": "\u6f22" * (MAX_RAW_LENGTH // 6 + 1)})
    assert s.toolbar_state()["calls"][0]["values"][1]["raw"] is None


@pytest.mark.parametrize(
    "command",
    [
        {
            "cmd": "argument",
            "call": "x",
            "value": 1,
            "start": 0,
            "end": 1,
            "name": "a",
            "raw": "Alice",
        },
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 1,
            "name": "${a.b}",
            "raw": "Alice",
        },
        {
            "cmd": "argument",
            "call": 0,
            "value": 0,
            "start": 0,
            "end": 99,
            "name": "a",
            "raw": "#n",
        },
        {"cmd": "replace", "argument": "nope", "occurrences": [[0, 1]]},
        {"cmd": "replace", "argument": "a", "occurrences": "bad"},
    ],
)
def test_bad_argument_commands_become_toolbar_errors(command):
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command(command)
    assert s.toolbar_state()["error"]


def test_save_failure_is_reported_and_recording_continues():
    s, target, _ = session(target=FakeTarget(fail=True))
    start(s, "K")
    s.handle_event("added", FILL)
    assert "read-only" in s.toolbar_state()["error"]
    target.fail = False
    s.handle_event("added", CLICK)
    assert len(s.toolbar_state()["calls"]) == 2
    assert s.toolbar_state()["error"] is None


def test_unknown_command_is_logged():
    s, _, _ = session()
    s.handle_command({"cmd": "explode"})
    assert any("explode" in entry for entry in s.log)


def test_toolbar_values_carry_their_raw_text():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    assert [v["raw"] for v in s.toolbar_state()["calls"][0]["values"]] == [
        "#n",
        "Alice",
    ]
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "who",
            "raw": "Alice",
        }
    )
    assert s.toolbar_state()["calls"][0]["values"][1]["raw"] is None


def test_argument_with_a_stale_raw_is_rejected():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Bob"})
    s.handle_command(
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 3,
            "name": "who",
            "raw": "Bob",
        }
    )
    assert "changed" in s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


class ValueErrorTarget(FakeTarget):
    def save(self, keyword):
        if self.fail:
            raise ValueError("foreign keyword")
        return super().save(keyword)

    def finish(self, keyword):
        if self.fail:
            raise ValueError("foreign keyword")
        super().finish(keyword)


def test_value_error_from_save_is_a_toolbar_error_and_clears_later():
    s, target, _ = session(target=ValueErrorTarget(fail=True))
    start(s, "K")
    s.handle_event("added", FILL)
    assert "foreign keyword" in s.toolbar_state()["error"]
    target.fail = False
    s.handle_event("added", CLICK)
    assert s.toolbar_state()["error"] is None
    assert len(s.toolbar_state()["calls"]) == 2


def test_value_error_from_finish_is_a_toolbar_error_and_keeps_the_keyword():
    s, _, clock = session(target=ValueErrorTarget(fail=True))
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    assert "foreign keyword" in s.toolbar_state()["error"]
    assert s.keywords == ["K"]


def arg(**fields):
    base = {
        "cmd": "argument",
        "call": 0,
        "value": 1,
        "start": 0,
        "end": 5,
        "name": "who",
    }
    return {**base, "raw": "Alice", **fields}


def recording(**kwargs):
    s, target, clock = session(**kwargs)
    start(s, "K")
    s.handle_event("added", FILL)
    return s, target, clock


def test_stop_after_a_pending_discard_still_discards():
    s, target, clock = recording()
    s.handle_command({"cmd": "discard"})
    s.handle_command({"cmd": "stop"})
    settle(s, clock)
    assert s.stopped
    assert target.removed == ["K"]
    assert s.close() == []
    assert target.finished == []


def test_close_with_a_pending_discard_discards():
    s, target, _ = recording()
    s.handle_command({"cmd": "discard"})
    assert s.close() == []
    assert target.removed == ["K"]
    assert target.finished == []


def test_close_with_a_pending_discard_does_not_restart_a_fixed_name():
    s, target, _ = recording(fixed_name="F")
    s.handle_command({"cmd": "discard"})
    s.close()
    assert target.finished == []
    assert s.state == "idle"


def test_stop_after_a_pending_finish_keeps_the_keyword():
    s, target, clock = recording()
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "stop"})
    settle(s, clock)
    assert s.stopped
    assert s.close() == ["K"]
    assert target.finished


def test_repeated_stop_does_not_extend_the_deadline():
    s, _, clock = recording()
    s.handle_command({"cmd": "stop"})
    clock.now += SETTLE_SECONDS - 0.1
    s.handle_command({"cmd": "stop"})
    clock.now += 0.1
    s.tick()
    assert s.stopped


@pytest.mark.parametrize(
    "fields", [{"call": -1, "value": -1}, {"start": -1}, {"end": -1}]
)
def test_negative_indexes_are_rejected(fields):
    s, _, _ = recording()
    s.handle_command(arg(**fields))
    assert s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


def test_negative_indexes_without_raw_are_rejected():
    s, _, _ = recording()
    command = arg(call=-1, value=-1)
    del command["raw"]
    s.handle_command(command)
    assert s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


def test_missing_raw_with_valid_indexes_is_rejected():
    s, _, _ = recording()
    command = arg()
    del command["raw"]
    s.handle_command(command)
    assert s.toolbar_state()["error"]
    assert s.toolbar_state()["arguments"] == []


def test_negative_occurrences_are_rejected():
    s, _, _ = recording()
    s.handle_command(arg())
    s.handle_command({"cmd": "replace", "argument": "who", "occurrences": [[-1, -1]]})
    assert s.toolbar_state()["error"]


class RemoveFailTarget(FakeTarget):
    def __init__(self, error):
        super().__init__()
        self.error = error

    def remove(self, name):
        raise self.error


@pytest.mark.parametrize("error", [OSError("disk"), ValueError("foreign")])
def test_failing_remove_on_discard_is_a_toolbar_error_and_the_keyword_is_gone(error):
    s, _, clock = recording(target=RemoveFailTarget(error))
    s.handle_command({"cmd": "discard"})
    settle(s, clock)
    state = s.toolbar_state()
    assert str(error) in state["error"]
    assert state["state"] == "idle"
    assert state["pending"] is None


def test_failing_remove_of_an_empty_keyword_on_finish_is_a_toolbar_error():
    s, _, clock = session(target=RemoveFailTarget(OSError("disk")))
    start(s, "K")
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    assert "disk" in s.toolbar_state()["error"]
    assert s.state == "idle"


@pytest.mark.parametrize(
    "command",
    [
        {"cmd": "new", "name": None},
        {"cmd": "new"},
        {"cmd": "new", "name": 5},
        {"cmd": "replace", "argument": None, "occurrences": []},
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": 7,
            "raw": "Alice",
        },
        {
            "cmd": "argument",
            "call": 0,
            "value": 1,
            "start": 0,
            "end": 5,
            "name": "w",
            "raw": 5,
        },
    ],
)
def test_non_conforming_command_fields_are_toolbar_errors(command):
    s, _, _ = session()
    start(s, "K") if command["cmd"] != "new" else None
    if command["cmd"] != "new":
        s.handle_event("added", FILL)
        s.handle_command(arg(name="who"))
    s.handle_command(command)
    assert s.toolbar_state()["error"]
    if command["cmd"] == "new":
        assert s.state == "idle"
    else:
        assert s.toolbar_state()["arguments"] == [
            {"name": "who", "default": "Alice", "useDefault": True}
        ]


def test_the_still_finishing_error_clears_when_the_command_runs():
    s, _, clock = recording()
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "undo"})
    assert s.toolbar_state()["error"]
    settle(s, clock)
    assert s.toolbar_state()["error"] is None


def test_the_offer_is_cleared_when_calls_change():
    s, _, _ = recording()
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Alice"})
    s.handle_command(arg())
    assert s.toolbar_state()["offer"]
    s.handle_event("added", CLICK)
    assert s.toolbar_state()["offer"] is None
    s.handle_command({"cmd": "undo"})
    s.handle_command(arg(call=1, name="again", raw="Alice"))
    assert s.toolbar_state()["offer"] is None


def test_the_offer_is_cleared_when_an_event_updates_or_attaches():
    s, _, _ = recording()
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Alice"})
    s.handle_command(arg())
    s.handle_event("updated", {"name": "fill", "selector": "#m", "text": "Alicex"})
    assert s.toolbar_state()["offer"] is None
    s.handle_command(arg(call=1, name="two", raw="Alicex", end=6))
    s.handle_event("signal", {"name": "dialog"})
    assert s.toolbar_state()["offer"] is None


def test_a_failed_argument_command_clears_the_offer():
    s, _, _ = recording()
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Alice"})
    s.handle_command(arg())
    assert s.toolbar_state()["offer"]
    s.handle_command(arg(name="bad name!", raw="Alice"))
    assert s.toolbar_state()["offer"] is None


def test_updated_event_on_an_empty_recording_is_added_as_a_call():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("updated", FILL)
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == ["Fill Text"]


def test_unsupported_action_name_is_text_and_truncated():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {"name": "x" * 500})
    assert len(s.toolbar_state()["notice"]) < 200
    s.handle_event("added", {"name": ["list"]})
    assert "?" in s.toolbar_state()["notice"]


def test_signal_after_undo_is_ignored():
    s, _, _ = recording()
    s.handle_command({"cmd": "undo"})
    s.handle_event("signal", {"name": "dialog"})
    assert s.toolbar_state()["calls"] == []


def test_signal_after_a_skipped_action_is_ignored():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", CLICK)
    s.handle_event("added", {"name": "somethingNew", "selector": "#x"})
    s.handle_event("signal", {"name": "dialog"})
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == ["Click"]


@pytest.mark.parametrize(
    "command", [{"cmd": "finish"}, {"cmd": "discard"}, {"cmd": "undo"}, arg()]
)
def test_commands_while_idle_are_toolbar_errors(command):
    s, _, _ = session()
    s.handle_command(command)
    assert s.toolbar_state()["error"]
    assert s.toolbar_state()["pending"] is None


def test_action_held_back_from_idle_time_does_not_land_in_the_new_keyword():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    state = s.toolbar_state()
    assert (state["state"], state["pending"], state["name"]) == ("idle", "new", "K")
    clock.now += 0.5
    s.handle_event("added", {"name": "navigate", "url": "http://idle"})
    settle(s, clock)
    assert s.state == "recording"
    assert s.toolbar_state()["calls"] == []
    assert target.saved == []


def test_stop_while_a_new_keyword_is_settling_never_starts_it():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_command({"cmd": "stop"})
    settle(s, clock)
    assert s.stopped
    assert s.state == "idle"
    assert s.toolbar_state()["name"] is None


def test_close_while_a_new_keyword_is_settling_records_nothing():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    assert s.close() == []
    assert s.state == "idle"


def test_picking_is_off_by_default_and_follows_set_picking():
    s = RecorderSession(FakeTarget(), clock=Clock())
    assert s.toolbar_state()["picking"] is False
    s.set_picking(True)
    assert s.toolbar_state()["picking"] is True
    s.set_picking(False)
    assert s.toolbar_state()["picking"] is False


# -- remaining branches of the state machine ------------------------------- #


def test_text_is_empty_before_any_keyword_is_finished():
    s, _, _ = session()
    assert s.text() == ""


def test_close_drops_a_running_keyword_without_calls():
    s, target, _ = session()
    start(s, "K")
    assert s.close() == []
    assert s.state == "idle"
    assert target.finished == []


def test_stop_after_a_pending_discard_with_the_keyword_gone_is_harmless():
    s, _, clock = recording()
    s.handle_command({"cmd": "discard"})
    s.handle_command({"cmd": "stop"})
    s._keyword = None
    settle(s, clock)
    assert s.stopped


def test_a_starting_command_without_a_name_does_nothing():
    s, _, clock = session()
    s._pending = (_STARTING, clock.now)
    s._starting = None
    s.tick()
    assert s.state == "idle"


def test_undo_with_nothing_to_undo_changes_nothing():
    s, target, _ = session()
    start(s, "K")
    s.handle_command({"cmd": "undo"})
    assert target.saved == []
    assert s.toolbar_state()["calls"] == []


def test_save_without_a_running_keyword_is_a_no_op():
    s, target, _ = session()
    s._save()
    assert target.saved == []


def test_a_notice_from_the_target_reaches_the_toolbar():
    class NoticeTarget(FakeTarget):
        def save(self, keyword):
            super().save(keyword)
            return "File changed on disk."

    s, _, _ = session(target=NoticeTarget())
    start(s, "K")
    s.handle_event("added", FILL)
    assert s.toolbar_state()["notice"] == "File changed on disk."


def test_new_while_a_keyword_is_recording_is_rejected():
    s, _, _ = recording()
    s.handle_command({"cmd": "new", "name": "Other"})
    assert "Still recording 'K'" in s.toolbar_state()["error"]


def test_unknown_command_log_entry_is_truncated():
    s, _, _ = session()
    s.handle_command({"cmd": "x" * 5000})
    assert max(len(entry) for entry in s.log) < 300


@pytest.mark.parametrize(
    "error",
    [
        OSError("gone"),
        ValueError("bad"),
        UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad"),
    ],
)
def test_unreadable_target_on_new_is_a_toolbar_error(error):
    class Unreadable(FakeTarget):
        def existing_names(self):
            raise error

    s, _, _ = session(target=Unreadable())
    s.handle_command({"cmd": "new", "name": "Fresh"})
    assert s.toolbar_state()["error"].startswith("Could not read fake.resource")
    assert s.state == "idle"


def test_the_state_names_the_last_answered_command():
    s, _, _ = session()
    assert s.toolbar_state()["answered"] is None
    s.handle_command({"cmd": "new", "name": "", "id": "t1-1"})
    state = s.toolbar_state()
    assert (state["answered"], bool(state["error"])) == ("t1-1", True)
    s.handle_command({"cmd": "new", "name": "K", "id": "t1-2"})
    state = s.toolbar_state()
    assert (state["answered"], state["error"]) == ("t1-2", None)


@pytest.mark.parametrize("command_id", [None, 7, "x" * 65])
def test_an_unusable_command_id_keeps_the_last_answer(command_id):
    s, _, _ = session()
    s.handle_command({"cmd": "undo", "id": "t1-1"})
    s.handle_command({"cmd": "undo", "id": command_id})
    assert s.toolbar_state()["answered"] == "t1-1"


def test_a_command_while_starting_says_so():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_command({"cmd": "undo"})
    assert s.toolbar_state()["error"] == "Still starting the keyword - please wait."


@pytest.mark.parametrize(
    ("quiet_ms", "wait"), [(0, 0.8), (300, 0.5), (800, 0.0), (5000, 0.0), (0.5, 0.7995)]
)
def test_finish_waits_only_until_the_page_was_quiet_long_enough(quiet_ms, wait):
    s, target, clock = recording()
    s.handle_command({"cmd": "finish", "quietMs": quiet_ms})
    clock.now += max(wait - 0.001, 0)
    s.tick()
    assert (s.state == "idle") is (wait == 0)
    clock.now += 0.002
    s.tick()
    assert s.state == "idle"
    assert target.finished


@pytest.mark.parametrize(
    "quiet_ms", [None, -1, True, "900", float("nan"), float("inf")]
)
def test_an_unusable_quiet_time_waits_the_whole_settle_time(quiet_ms):
    s, _, clock = session()
    s.handle_command({"cmd": "new", "name": "K", "quietMs": quiet_ms})
    clock.now += SETTLE_SECONDS - 0.001
    s.tick()
    assert s.state == "idle"
    clock.now += 0.001
    s.tick()
    assert s.state == "recording"


def test_a_selector_left_internal_is_recorded_with_a_notice():
    s, target, _ = session()
    start(s, "K")
    # An empty attribute value has no public form.
    s.handle_event(
        "added",
        {"name": "click", "selector": 'internal:attr=[alt=""i]', "button": "left"},
    )
    assert "internal:attr" in s.toolbar_state()["notice"]
    assert 'Click    internal:attr=[alt=""i]' in target.saved[-1]


def test_labels_and_deep_frames_are_recorded_in_browser_syntax():
    s, target, _ = session()
    start(s, "K")
    s.handle_event(
        "added",
        {
            "name": "click",
            "selector": 'internal:control=any-frame >> internal:label="Map"i',
            "button": "left",
        },
    )
    assert s.toolbar_state()["notice"] is None
    assert 'Click    >>> label="Map"i' in target.saved[-1]


UPLOAD_CLICK = {**CLICK, "selector": 'internal:role=button[name="Open Report"i]'}
CHOSEN = {
    "name": "fill",
    "selector": 'internal:attr=[type="file"s]',
    "text": "C:\\fakepath\\report.zip",
}


def test_a_file_chosen_after_a_click_wraps_the_click_in_an_upload_promise():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", UPLOAD_CLICK)
    s.handle_event("added", CHOSEN)
    assert target.saved[-1].splitlines()[2:] == [
        "    ${upload}=    Promise To Upload File    <define_path_to_file>/report.zip",
        '    Click    role=button[name*="Open Report"i]',
        "    Wait For    ${upload}",
    ]
    assert "<define_path_to_file>" in s.toolbar_state()["notice"]
    s.handle_command({"cmd": "undo"})
    assert "Promise To Upload File" not in target.saved[-1]
    assert "Click" not in target.saved[-1]


def test_setinputfiles_is_an_upload_too():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", UPLOAD_CLICK)
    s.handle_event(
        "added", {"name": "setInputFiles", "selector": "#f", "files": ["a.txt"]}
    )
    assert "Promise To Upload File    <define_path_to_file>/a.txt" in target.saved[-1]


@pytest.mark.parametrize(
    ("before", "upload"),
    [
        ([], CHOSEN),
        ([UPLOAD_CLICK, "undo"], CHOSEN),
        (
            [UPLOAD_CLICK],
            {"name": "setInputFiles", "selector": "#f", "files": ["a.txt", "b.txt"]},
        ),
    ],
    ids=["nothing_before", "after_undo", "several_files"],
)
def test_an_upload_without_an_action_to_wrap_sets_the_files_on_the_input(
    before, upload
):
    s, target, _ = session()
    start(s, "K")
    for step in before:
        if step == "undo":
            s.handle_command({"cmd": "undo"})
        else:
            s.handle_event("added", step)
    s.handle_event("added", upload)
    last = target.saved[-1].splitlines()[-1]
    assert last.startswith("    Upload File By Selector    ")
    assert "Promise To Upload File" not in target.saved[-1]


def test_a_cancelled_file_chooser_records_nothing():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", UPLOAD_CLICK)
    s.handle_event("added", {"name": "setInputFiles", "selector": "#f", "files": []})
    assert "Upload" not in target.saved[-1]


def pause(s, clock, cmd="pause"):
    s.handle_command({"cmd": cmd})
    settle(s, clock)


def test_actions_while_paused_are_not_recorded():
    s, target, clock = recording()
    pause(s, clock)
    assert s.toolbar_state()["paused"] is True
    s.handle_event("added", CLICK)
    s.handle_event("signal", {"name": "popup"})
    pause(s, clock, "resume")
    assert s.toolbar_state()["paused"] is False
    s.handle_event("added", {**FILL, "text": "Bob"})
    assert target.saved[-1].count("Fill Text") == 2
    assert "Click" not in target.saved[-1]


def test_an_action_right_before_pause_still_lands():
    s, target, clock = recording()
    s.handle_command({"cmd": "pause", "quietMs": 100})
    s.handle_event("added", CLICK)
    settle(s, clock)
    assert "Click" in target.saved[-1]
    assert s.toolbar_state()["paused"] is True


def test_a_signal_after_resume_does_not_attach_to_the_action_before_pause():
    s, target, clock = recording()
    pause(s, clock)
    pause(s, clock, "resume")
    s.handle_event("signal", {"name": "dialog"})
    assert "Handle Future Dialogs" not in target.saved[-1]


@pytest.mark.parametrize(
    ("first", "second", "error"),
    [("pause", "pause", "already paused"), ("resume", None, "not paused")],
)
def test_pause_and_resume_only_where_they_make_sense(first, second, error):
    s, _, clock = recording()
    pause(s, clock, first)
    if second:
        s.handle_command({"cmd": second})
    assert error in s.toolbar_state()["error"]


def test_pause_needs_a_keyword_and_ends_with_it():
    s, _, clock = session()
    s.handle_command({"cmd": "pause"})
    assert s.toolbar_state()["error"] == "No keyword is being recorded."
    start(s, "K")
    pause(s, clock)
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    start(s, "L")
    assert s.toolbar_state()["paused"] is False


def test_the_toolbar_shows_each_value_as_robot_reads_it():
    s, _, _ = session()
    start(s, "K")
    s.handle_event("added", {**FILL, "text": "id-42  ${HOME}"})
    s.handle_command(arg(start=3, end=5, name="number", raw="id-42  ${HOME}"))
    call = s.toolbar_state()["calls"][0]
    assert call["keyword"] == "Fill Text"
    assert call["values"][0]["tokens"] == [["argument", "\\#n"]]
    assert call["values"][1]["tokens"] == [
        ["argument", "id-"],
        ["variable", "${number}"],
        ["argument", " \\ \\${HOME}"],
    ]


def test_the_toolbar_shows_a_value_escaped_as_in_the_file():
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", {**FILL, "text": "txt=hello"})
    tokens = s.toolbar_state()["calls"][0]["values"][1]["tokens"]
    assert tokens == [["argument", "txt\\=hello"]]
    assert "txt\\=hello" in target.saved[-1]


@pytest.mark.parametrize("written", ["${part", "${a}[", "${{1+"])
def test_partial_variable_syntax_is_shown_uncoloured_rather_than_failing(written):
    assert tokens(written) == [("argument", written)]


class FlakyFinishTarget(FakeTarget):
    """Fails to finish until it is told the problem is gone."""

    def __init__(self):
        super().__init__()
        self.broken = True

    def finish(self, keyword):
        if self.broken:
            raise OSError("locked")
        super().finish(keyword)


def test_a_keyword_that_could_not_be_finished_is_written_on_close():
    s, _, clock = recording(target=FlakyFinishTarget())
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    assert [k.name for k in s.unsaved] == ["K"]
    s.target.broken = False
    s.close()
    assert s.unsaved == []
    assert s.target.finished


def test_a_keyword_still_not_written_on_close_stays_unsaved():
    s, _, clock = recording(target=FlakyFinishTarget())
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    s.close()
    assert [k.name for k in s.unsaved] == ["K"]
    assert "locked" in s.write_error


@pytest.mark.parametrize(
    "upload",
    [
        {**CHOSEN, "text": "C:\\fakepath\\../../.ssh/id_rsa"},
        {**CHOSEN, "text": "C:\\fakepath\\"},
        {"name": "setInputFiles", "selector": "#f", "files": ["a.txt", ".."]},
        {"name": "setInputFiles", "selector": "#f", "files": ["dir\\a.txt"]},
    ],
    ids=["traversal", "empty", "dot_dot", "backslash"],
)
def test_an_upload_without_a_plain_file_name_is_not_recorded(upload):
    s, target, _ = session()
    start(s, "K")
    s.handle_event("added", UPLOAD_CLICK)
    s.handle_event("added", upload)
    assert "Upload" not in target.saved[-1]
    assert "not a plain file name" in s.toolbar_state()["notice"]


# -- the toolbar's Pick button ------------------------------------------------ #

PICKED = {"selector": 'internal:role=button[name="Save"i]', "css": "#save"}


def picking(**kwargs):
    s, target, clock = session(fixed_name="K", **kwargs)
    s.handle_command({"cmd": "pick", "id": "p-1"})
    return s, target


def test_pick_opens_the_picker_while_recording():
    s, _ = picking()
    state = s.toolbar_state()
    assert state["picker"]["phase"] == "picking"
    assert state["answered"] == "p-1"
    assert s.request() == {"pick": True, "highlight": True}


def test_pick_while_idle_asks_for_a_keyword():
    s, _, _ = session()
    s.handle_command({"cmd": "pick"})
    assert s.toolbar_state()["picker"] is None
    assert "Start recording a keyword" in s.toolbar_state()["notice"]


def test_playwrights_pick_locator_opens_the_picker_and_then_picks_again():
    s, _, _ = session(fixed_name="K")
    s.request_pick()
    assert s.toolbar_state()["picker"]["phase"] == "picking"
    s.handle_picked(PICKED)
    s.request_pick()
    assert s.toolbar_state()["picker"]["phase"] == "picking"


def test_a_pick_reaches_the_picker_and_is_counted():
    s, _ = picking()
    s.handle_picked(PICKED)
    assert s.toolbar_state()["picker"]["selector"] == 'role=button[name*="Save"i]'
    assert s.request() == {
        "pick": False,
        "highlight": True,
        "count": 'role=button[name*="Save"i]',
    }
    s.handle_count({"selector": 'role=button[name*="Save"i]', "count": 1})
    assert s.toolbar_state()["picker"]["count"]["count"] == 1


def test_picker_commands_are_prefixed():
    s, _ = picking()
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-generator", "name": "css"})
    assert s.toolbar_state()["picker"]["selector"] == "#save"


def test_use_writes_the_selector_as_a_comment_row():
    s, target = picking()
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-use"})
    state = s.toolbar_state()
    assert state["picker"] is None
    assert state["calls"][0]["keyword"] == "# Picked Selector"
    assert state["calls"][0]["comment"] is True
    assert state["calls"][0]["values"][0]["selectable"] is False
    assert '    # Picked Selector    role=button[name*="Save"i]' in target.saved[-1]
    assert s.request() == {}


def test_cancel_closes_the_picker_without_a_row():
    s, target = picking()
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-cancel"})
    assert s.toolbar_state()["picker"] is None
    assert s.toolbar_state()["calls"] == []


def test_an_action_refined_after_a_pick_stays_the_same_keyword_call():
    s, target = picking()
    s.handle_command({"cmd": "pick-cancel"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "pick"})
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-use"})
    s.handle_event("updated", {**FILL, "text": "Alice B"})
    calls = s.toolbar_state()["calls"]
    assert [c["keyword"] for c in calls] == ["Fill Text", "# Picked Selector"]
    assert calls[0]["values"][1]["raw"] == "Alice B"


def test_undo_removes_a_picked_selector():
    s, _ = picking()
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-use"})
    s.handle_command({"cmd": "undo"})
    assert s.toolbar_state()["calls"] == []


def test_a_picker_command_without_a_picker_is_an_error():
    s, _, _ = session(fixed_name="K")
    s.handle_command({"cmd": "pick-use"})
    assert s.toolbar_state()["error"] == "No selector is being picked."


def test_stop_closes_the_picker():
    s, _ = picking()
    s.handle_command({"cmd": "stop"})
    assert s.toolbar_state()["picker"] is None


def test_the_next_pick_keeps_the_highlight_switch():
    s, _ = picking()
    s.handle_command({"cmd": "pick-highlight", "on": False})
    s.handle_command({"cmd": "pick-cancel"})
    s.handle_command({"cmd": "pick"})
    assert s.toolbar_state()["picker"]["highlight"] is False


@pytest.mark.parametrize("cmd", ["finish", "discard", "undo", "pause", "resume"])
def test_keyword_commands_wait_until_the_pick_is_used_or_cancelled(cmd):
    s, target = picking()
    s.handle_picked(PICKED)
    s.handle_command({"cmd": cmd})
    state = s.toolbar_state()
    assert state["error"] == "Use or cancel the picked selector first."
    assert state["picker"]["phase"] == "picked"
    assert state["pending"] is None


def test_a_pick_cannot_open_while_save_is_settling():
    s, _, clock = session()
    start(s, "K")
    s.handle_command({"cmd": "finish", "quietMs": 0})
    s.request_pick()
    assert s.toolbar_state()["picker"] is None
    settle(s, clock)
    assert s.state == "idle"
    assert s.request() == {}


@pytest.mark.parametrize("cmd", ["finish", "discard"])
def test_the_end_of_a_keyword_closes_a_picker_opened_meanwhile(cmd):
    s, _, clock = session()
    start(s, "K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": cmd, "quietMs": 0})
    # Opened through the page's command channel while the command settles.
    s._picker = SelectorPicker(None, "playwright")
    settle(s, clock)
    assert s.toolbar_state()["picker"] is None
    assert s.request() == {}


def test_actions_after_the_pick_are_not_recorded_until_use():
    s, target = picking()
    s.handle_event("added", FILL)
    s.handle_picked(PICKED)
    s.handle_event("added", {**FILL, "text": "tried out"})
    s.handle_event("signal", {"name": "popup", "popupPageGuid": "g"})
    s.handle_command({"cmd": "pick-use"})
    calls = s.toolbar_state()["calls"]
    assert [c["keyword"] for c in calls] == ["Fill Text", "# Picked Selector"]


def test_undoing_a_picked_selector_keeps_refining_the_action_before_it():
    s, _ = picking()
    s.handle_command({"cmd": "pick-cancel"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "pick"})
    s.handle_picked(PICKED)
    s.handle_command({"cmd": "pick-use"})
    s.handle_command({"cmd": "undo"})
    s.handle_event("updated", {**FILL, "text": "Alice B"})
    calls = s.toolbar_state()["calls"]
    assert [c["values"][1]["raw"] for c in calls] == ["Alice B"]


@pytest.mark.parametrize(
    ("selector", "written"),
    [
        ("#save", "\\#save"),
        ("text=${HOME}", "text=\\${HOME}"),
        ("text=a  b", "text=a \\ b"),
        ("text=a\nb", "text=a\\nb"),
    ],
)
def test_a_picked_selector_is_written_as_a_cell(selector, written):
    s, target = picking()
    s.handle_picked({"selector": selector, "css": "x"})
    s.handle_command({"cmd": "pick-use"})
    assert f"    # Picked Selector    {written}\n" in target.saved[-1]


FIRST = "page@first"
POPUP = "page@popup"


def recording_on_pages():
    s, _, _ = session()
    s.set_active_page(FIRST)
    start(s, "K")
    return s


def rows(s) -> list[str]:
    lines = s._keyword.lines()[1:]
    return [" | ".join(row.replace("\\#", "#").split("    ")) for row in lines]


def open_popup(s):
    s.handle_event("added", CLICK, FIRST)
    s.handle_event("signal", {"name": "popup", "popupPageGuid": POPUP}, FIRST)


def test_actions_on_the_active_page_switch_nothing():
    s = recording_on_pages()
    s.handle_event("added", CLICK, FIRST)
    s.handle_event("added", FILL, FIRST)
    assert rows(s) == ["Click | #b", "Fill Text | #n | Alice"]


def test_a_popup_keeps_its_page_without_a_variable_until_a_switch_back():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("added", FILL, POPUP)
    assert rows(s) == ["Click | #b", "Switch Page | NEW", "Fill Text | #n | Alice"]


def test_switching_back_assigns_the_id_the_popup_switch_returned():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("added", FILL, POPUP)
    s.handle_event("added", CLICK, FIRST)
    s.handle_event("added", FILL, POPUP)
    assert rows(s) == [
        "Click | #b",
        "${page}= | Switch Page | NEW",
        "Fill Text | #n | Alice",
        "${page_2}= | Switch Page | ${page}",
        "Click | #b",
        "Switch Page | ${page_2}",
        "Fill Text | #n | Alice",
    ]


def test_closing_the_active_page_needs_no_switch_to_the_one_browser_falls_back_to():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("closed", {"name": "closePage"}, POPUP)
    s.handle_event("added", FILL, FIRST)
    assert rows(s) == [
        "Click | #b",
        "${page}= | Switch Page | NEW",
        "Close Page",
        "Switch Page | ${page}",
        "Fill Text | #n | Alice",
    ]
    assert s.toolbar_state()["notice"] is None


def test_closing_another_page_closes_it_by_its_id():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("closed", {"name": "closePage"}, FIRST)
    assert rows(s) == [
        "Click | #b",
        "${page}= | Switch Page | NEW",
        "Close Page | ${page}",
    ]


def test_closing_a_page_the_keyword_has_no_id_of_is_not_recorded():
    s = recording_on_pages()
    s.handle_event("added", CLICK, FIRST)
    s.handle_event("closed", {"name": "closePage"}, "page@other")
    assert rows(s) == ["Click | #b"]


def test_an_action_on_a_page_without_an_id_gets_a_notice():
    s = recording_on_pages()
    s.handle_event("added", CLICK, FIRST)
    s.handle_event("added", FILL, "page@other")
    assert rows(s) == ["Click | #b", "Fill Text | #n | Alice"]
    assert s.toolbar_state()["notice"] == _UNREACHABLE_PAGE


def test_playwrights_own_close_page_is_silent():
    s = recording_on_pages()
    s.handle_event("added", {"name": "closePage"}, FIRST)
    assert rows(s) == []
    assert s.toolbar_state()["notice"] is None


def test_undoing_the_switch_back_drops_the_unused_assignment():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("added", CLICK, FIRST)
    s.handle_command({"cmd": "undo"})
    assert rows(s) == ["Click | #b", "Switch Page | NEW"]
    s.handle_event("added", FILL, POPUP)
    assert rows(s)[-1] == "Fill Text | #n | Alice"


def test_undoing_the_popup_returns_to_the_first_page():
    s = recording_on_pages()
    open_popup(s)
    s.handle_command({"cmd": "undo"})
    s.handle_event("added", FILL, FIRST)
    assert rows(s) == ["Fill Text | #n | Alice"]


def test_without_page_information_nothing_is_switched():
    s = recording_on_pages()
    s.handle_event("added", CLICK)
    s.handle_event("added", FILL)
    assert rows(s) == ["Click | #b", "Fill Text | #n | Alice"]


def test_undo_keeps_the_id_an_earlier_switch_returned():
    s = recording_on_pages()
    open_popup(s)
    s.handle_event("added", FILL, FIRST)
    s.handle_event("added", FILL, POPUP)
    s.handle_command({"cmd": "undo"})
    s.handle_command({"cmd": "undo"})
    assert rows(s) == ["Click | #b", "Switch Page | NEW"]
    s.handle_event("added", CLICK, FIRST)
    assert rows(s) == [
        "Click | #b",
        "${page}= | Switch Page | NEW",
        "Switch Page | ${page}",
        "Click | #b",
    ]
    assert s.toolbar_state()["notice"] is None
