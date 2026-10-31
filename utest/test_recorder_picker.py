import pytest

from Browser.recorder.picker import SelectorPicker, run_picker

PICKED = {"selector": 'internal:role=button[name="Save"i]', "css": "#save"}


def picked(generator="playwright"):
    picker = SelectorPicker("Save button", generator)
    picker.handle_picked(PICKED)
    return picker


def test_a_new_picker_picks_and_shows_its_label():
    picker = SelectorPicker("Save button", "playwright")
    assert picker.request() == {"pick": True, "highlight": True}
    state = picker.toolbar_state()
    assert state["mode"] == "selector"
    assert state["label"] == "Save button"
    assert state["phase"] == "picking"
    assert state["generators"] == ["playwright", "css"]


def test_an_unknown_generator_is_refused():
    with pytest.raises(ValueError, match="Unknown selector generator"):
        SelectorPicker(None, "xpath")


def test_a_pick_shows_the_translated_playwright_selector_and_counts_it():
    picker = picked()
    assert picker.selector == 'role=button[name*="Save"i]'
    assert picker.toolbar_state()["phase"] == "picked"
    assert picker.request() == {
        "pick": False,
        "highlight": True,
        "count": 'role=button[name*="Save"i]',
    }
    assert picker.request() == {"pick": False, "highlight": True}


def test_a_pick_with_the_css_generator_shows_the_css_selector():
    assert picked("css").selector == "#save"


def test_switching_the_generator_shows_the_other_selector_of_the_same_element():
    picker = picked()
    version = picker.version
    picker.handle_command({"cmd": "generator", "name": "css", "id": "a-1"})
    assert picker.selector == "#save"
    assert picker.version == version + 1
    assert picker.answered == "a-1"
    assert picker.request()["count"] == "#save"


def test_a_generator_without_a_selector_is_unavailable():
    picker = SelectorPicker(None, "playwright")
    picker.handle_picked({"selector": "css=b", "error": "no css"})
    assert picker.toolbar_state()["unavailable"] == {"css": "no css"}


def test_an_internal_selector_comes_with_a_notice():
    picker = SelectorPicker(None, "playwright")
    picker.handle_picked({"selector": 'internal:attr=[alt=""i]', "css": ".map"})
    assert "internal:attr" in picker.toolbar_state()["notice"]


def test_a_failed_pick_is_an_error_and_keeps_picking():
    picker = SelectorPicker(None, "playwright")
    picker.handle_picked({"error": "Error: boom"})
    assert picker.toolbar_state()["error"] == "Picking failed: Error: boom"
    assert picker.request()["pick"] is True


def test_an_edit_is_counted_without_replacing_the_typed_text():
    picker = picked()
    picker.request()
    version = picker.version
    picker.handle_command({"cmd": "edit", "selector": "css=button"})
    assert picker.selector == "css=button"
    assert picker.version == version
    assert picker.request()["count"] == "css=button"


def test_a_blank_edit_is_not_counted():
    picker = picked()
    picker.request()
    picker.handle_command({"cmd": "edit", "selector": "  "})
    assert "count" not in picker.request()


def test_a_count_for_an_older_selector_is_dropped():
    picker = picked()
    picker.handle_command({"cmd": "edit", "selector": "css=b"})
    picker.handle_count({"selector": "css=a", "count": 2})
    assert picker.toolbar_state()["count"] is None
    picker.handle_count({"selector": "css=b", "count": 1})
    assert picker.toolbar_state()["count"] == {"selector": "css=b", "count": 1}


def test_an_oversized_edit_is_refused():
    picker = picked()
    picker.handle_command({"cmd": "edit", "selector": "x" * 10_001})
    assert picker.toolbar_state()["error"] == "The selector is too long."
    assert picker.selector == 'role=button[name*="Save"i]'


def test_reselect_picks_again():
    picker = picked()
    picker.handle_command({"cmd": "reselect"})
    assert picker.request()["pick"] is True
    assert picker.selector == ""
    assert picker.toolbar_state()["notice"] is None


def test_use_returns_the_trimmed_selector():
    picker = picked()
    picker.handle_command({"cmd": "edit", "selector": " css=b "})
    picker.handle_command({"cmd": "use"})
    assert picker.result == "css=b"


def test_use_before_a_pick_is_an_error():
    picker = SelectorPicker(None, "playwright")
    picker.handle_command({"cmd": "use"})
    assert picker.result is None
    assert (
        picker.toolbar_state()["error"] == "Pick an element first, or type a selector."
    )


def test_an_unknown_command_is_refused():
    with pytest.raises(ValueError, match="Unknown command"):
        picked().handle_command({"cmd": "format-disk"})


class FakeClient:
    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []
        self.stopped = False

    def poll(self, state, request, reset):
        self.requests.append((request, reset))
        return self.replies.pop(0) if self.replies else {"pages": 1}

    def stop(self):
        self.stopped = True


def test_run_picker_returns_the_used_selector_and_stops():
    client = FakeClient(
        [
            {"pages": 1},
            {"pages": 1, "picked": PICKED},
            {"pages": 1, "entries": [{"command": {"cmd": "use"}}]},
        ]
    )
    selector = run_picker(
        SelectorPicker(None, "css"), client, sleep=lambda _seconds: None
    )
    assert selector == "#save"
    assert client.requests[0] == ({"pick": True, "highlight": True}, True)
    assert client.stopped


def test_run_picker_fails_on_cancel():
    client = FakeClient([{"pages": 1, "entries": [{"command": {"cmd": "stop"}}]}])
    with pytest.raises(RuntimeError, match="cancelled"):
        run_picker(SelectorPicker(None, "css"), client, sleep=lambda _seconds: None)
    assert client.stopped


def test_run_picker_fails_when_the_page_closes():
    with pytest.raises(RuntimeError, match="page was closed"):
        run_picker(
            SelectorPicker(None, "css"),
            FakeClient([{"pages": 0}]),
            sleep=lambda _seconds: None,
        )


def test_run_picker_times_out_without_activity():
    now = [0.0]

    def clock():
        now[0] += 1
        return now[0]

    with pytest.raises(TimeoutError, match="timed out"):
        run_picker(
            SelectorPicker(None, "css"),
            FakeClient([]),
            idle_timeout=3,
            clock=clock,
            sleep=lambda _seconds: None,
        )


def test_run_picker_ignores_malformed_entries():
    client = FakeClient(
        [
            {
                "pages": 1,
                "entries": ["junk", {"command": "x"}, {"command": {"cmd": 1}}],
            },
            {"pages": 1, "picked": PICKED, "entries": [{"command": {"cmd": "use"}}]},
        ]
    )
    assert (
        run_picker(
            SelectorPicker(None, "playwright"), client, sleep=lambda _seconds: None
        )
        == 'role=button[name*="Save"i]'
    )


def test_highlight_is_on_by_default_and_can_be_switched_off():
    picker = picked()
    assert picker.toolbar_state()["highlight"] is True
    picker.request()
    picker.handle_command({"cmd": "highlight", "on": False})
    assert picker.request() == {"pick": False, "highlight": False}


def test_switching_highlight_on_again_highlights_the_shown_selector():
    picker = picked()
    picker.handle_command({"cmd": "highlight", "on": False})
    picker.request()
    picker.handle_command({"cmd": "highlight", "on": True})
    assert picker.request() == {
        "pick": False,
        "highlight": True,
        "count": picker.selector,
    }


def test_highlight_needs_a_boolean():
    picker = picked()
    picker.handle_command({"cmd": "highlight", "on": "yes"})
    assert picker.toolbar_state()["error"] == "'on' must be true or false."


def test_an_oversized_pick_is_refused():
    picker = SelectorPicker(None, "playwright")
    picker.handle_picked({"selector": "x" * 10_001, "css": "#a"})
    assert picker.toolbar_state()["error"] == "Picking failed."
    assert picker.request()["pick"] is True


def test_an_oversized_css_selector_is_unavailable():
    picker = SelectorPicker(None, "css")
    picker.handle_picked({"selector": "css=b", "css": "x" * 10_001})
    assert picker.selector == ""
    assert "css" in picker.toolbar_state()["unavailable"]


def test_a_long_command_id_is_not_echoed():
    picker = picked()
    picker.handle_command({"cmd": "reselect", "id": "x" * 65})
    assert picker.toolbar_state()["answered"] is None


def test_refused_commands_do_not_keep_the_pick_alive():
    now = [0.0]

    def clock():
        now[0] += 1
        return now[0]

    junk = {"pages": 1, "entries": [{"command": {"cmd": "format-disk"}}]}
    with pytest.raises(TimeoutError):
        run_picker(
            SelectorPicker(None, "css"),
            FakeClient([junk] * 10),
            idle_timeout=3,
            clock=clock,
            sleep=lambda _seconds: None,
        )


def test_a_refused_known_command_does_not_keep_the_pick_alive():
    now = [0.0]

    def clock():
        now[0] += 1
        return now[0]

    refused = {"pages": 1, "entries": [{"command": {"cmd": "highlight", "on": "yes"}}]}
    with pytest.raises(TimeoutError):
        run_picker(
            SelectorPicker(None, "css"),
            FakeClient([refused] * 10),
            idle_timeout=3,
            clock=clock,
            sleep=lambda _seconds: None,
        )
