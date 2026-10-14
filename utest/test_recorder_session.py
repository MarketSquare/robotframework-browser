from __future__ import annotations

import pytest

from Browser.recorder.model import RecordedKeyword
from Browser.recorder.names import KnownKeywords
from Browser.recorder.session import (
    _STARTING,
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
        return None

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
    assert [c["values"][1]["text"] for c in state["calls"]] == ["${who}", "${who}"]


def test_default_toggle():
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
            "name": "who",
            "raw": "Alice",
        }
    )
    s.handle_command({"cmd": "default", "argument": "who", "use": False})
    assert s.toolbar_state()["arguments"] == [
        {"name": "who", "default": "Alice", "useDefault": False}
    ]


def test_toolbar_shortens_long_texts_but_quotes_the_whole_value():
    s, _, _ = session()
    start(s, "K")
    text = "a" * (TOOLBAR_TEXT_LIMIT * 2)
    s.handle_event("added", {**FILL, "text": text})
    call = s.toolbar_state()["calls"][0]
    assert len(call["text"]) == TOOLBAR_TEXT_LIMIT
    assert call["text"].endswith("\u2026")
    assert len(call["values"][1]["text"]) == TOOLBAR_TEXT_LIMIT
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
    assert values[-1] == {"text": values[-1]["text"], "selectable": False, "raw": None}
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
            "name": "${a}",
            "raw": "Alice",
        },
        {
            "cmd": "argument",
            "call": 0,
            "value": 0,
            "start": 0,
            "end": 1,
            "name": "a",
            "raw": "#n",
        },
        {"cmd": "replace", "argument": "nope", "occurrences": [[0, 1]]},
        {"cmd": "replace", "argument": "a", "occurrences": "bad"},
        {"cmd": "default", "argument": "nope", "use": True},
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
        {"cmd": "default", "argument": 3, "use": True},
        {"cmd": "default", "argument": "who", "use": "false"},
        {"cmd": "default", "argument": "who", "use": 1},
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
