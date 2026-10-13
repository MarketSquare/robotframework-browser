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
"""Tests for the ``RecorderPlugin`` poll-loop driver itself (`_run_session`,
`_call`), as opposed to `RecorderSession`'s collaborator logic, which is
covered separately in ``test_recorder_session.py``.

The plugin is constructed without going through ``LibraryComponent.__init__``
(no live `Browser` instance is needed) and the network-facing bits
(`_poll`/`_call`/gRPC) are stubbed, so the whole driver loop runs in
milliseconds.
"""

from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace

import pytest

from Browser.recorder import plugin as recorder_plugin
from Browser.recorder.plugin import RecorderPlugin
from Browser.recorder.session import RecorderSession


def _make_plugin() -> RecorderPlugin:
    plugin = RecorderPlugin.__new__(RecorderPlugin)
    registered: list = []
    plugin.registered_js = registered
    plugin.initialize_js_extension = registered.append
    return plugin


class _ScriptedPoll:
    """A `_poll` stand-in that returns pre-scripted replies and records calls."""

    def __init__(self, replies: list[dict]) -> None:
        self._replies = list(replies)
        self.calls: list[dict] = []

    def __call__(self, state: dict, reset: bool) -> dict:
        self.calls.append({"state": state, "reset": reset})
        return self._replies.pop(0)


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """None of these tests should wait on the real poll interval."""
    monkeypatch.setattr(recorder_plugin, "_POLL_INTERVAL", 0)


# --------------------------------------------------------------------------- #
# reset flag
# --------------------------------------------------------------------------- #


def test_reset_is_true_on_first_poll_and_false_afterwards(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    poll = _ScriptedPoll(
        [
            {"mode": "recording", "pages": [1], "events": [], "commands": []},
            {"mode": "recording", "pages": [1], "events": [], "commands": []},
            {"mode": "stopped", "pages": [1], "events": [], "commands": []},
        ]
    )
    plugin._poll = poll

    plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    assert [call["reset"] for call in poll.calls] == [True, False, False]


# --------------------------------------------------------------------------- #
# JS extension registration
# --------------------------------------------------------------------------- #


def test_js_extension_is_registered_for_every_session(tmp_path):
    # Node's extension list lives on a per-peer state that can be re-created
    # between sessions (a new browser/peer), so caching "already registered" on
    # the plugin makes the second session fail with an unknown keyword.
    # Registering again is cheap - node's `require` is cached.
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    for _ in range(2):
        plugin._poll = _ScriptedPoll(
            [{"mode": "stopped", "pages": [1], "events": [], "commands": []}]
        )
        plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    assert plugin.registered_js == [recorder_plugin._JS_EXTENSION] * 2


# --------------------------------------------------------------------------- #
# The four independent exit conditions
# --------------------------------------------------------------------------- #


def test_stop_command_ends_the_loop(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    poll = _ScriptedPoll(
        [
            {
                "mode": "recording",
                "pages": [1],
                "events": [],
                "commands": [{"cmd": "stop"}],
            }
        ]
    )
    plugin._poll = poll

    session = plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    assert session.stopped is True
    assert len(poll.calls) == 1


def test_mode_stopped_ends_the_loop(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    poll = _ScriptedPoll(
        [{"mode": "stopped", "pages": [1], "events": [], "commands": []}]
    )
    plugin._poll = poll

    session = plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    assert session.stopped is False
    assert len(poll.calls) == 1


def test_no_pages_left_ends_the_loop(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    poll = _ScriptedPoll(
        [{"mode": "recording", "pages": [], "events": [], "commands": []}]
    )
    plugin._poll = poll

    plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    assert len(poll.calls) == 1


def test_timeout_expiry_ends_the_loop(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    # A deadline already in the past guarantees expiry is seen after the very
    # first poll, without relying on real wall-clock waiting.
    poll = _ScriptedPoll(
        [{"mode": "recording", "pages": [1], "events": [], "commands": []}]
    )
    plugin._poll = poll

    plugin._run_session(
        tmp_path / "out.resource", timedelta(seconds=-1), fixed_name="KW"
    )

    assert len(poll.calls) == 1


# --------------------------------------------------------------------------- #
# Ordering: events land before commands within one poll batch
# --------------------------------------------------------------------------- #


def test_events_are_applied_before_commands_in_the_same_batch(tmp_path):
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    click = {
        "name": "click",
        "selector": "css=.x",
        "button": "left",
        "modifiers": 0,
        "clickCount": 1,
    }
    poll = _ScriptedPoll(
        [
            {
                "mode": "recording",
                "pages": [1],
                "events": [{"event": "added", "action": click}],
                "commands": [{"cmd": "finish"}],
            },
            {"mode": "stopped", "pages": [1], "events": [], "commands": []},
        ]
    )
    plugin._poll = poll

    session = plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    # If commands ran first, "finish" would see zero recorded steps and
    # discard the keyword before the click ever got a chance to land in it.
    assert session.keywords == ["KW"]
    assert "Click    css=.x" in session.text()


# --------------------------------------------------------------------------- #
# FIX 1 regression: session.close() failing in `finally` must not skip the
# stop call, and must not replace an exception already propagating.
# --------------------------------------------------------------------------- #


def test_close_failure_does_not_skip_stop_or_mask_the_loop_exception(
    tmp_path, monkeypatch
):
    plugin = _make_plugin()
    calls: list[str] = []

    def fake_call(name: str, _arguments: dict) -> dict:
        calls.append(name)
        return {}

    plugin._call = fake_call

    def failing_poll(_state: dict, reset: bool) -> dict:
        raise RuntimeError("poll boom")

    plugin._poll = failing_poll

    def failing_close(_self) -> list[str]:
        raise RuntimeError("close boom")

    monkeypatch.setattr(RecorderSession, "close", failing_close)

    with pytest.raises(RuntimeError, match="poll boom"):
        plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    # The stop keyword must still have been called even though close() blew up.
    assert recorder_plugin._STOP_KEYWORD in calls


# --------------------------------------------------------------------------- #
# _call: gRPC body accumulation
# --------------------------------------------------------------------------- #


class _FakeResponse:
    def __init__(self, body_part: str = "", json_body: str = "") -> None:
        self.bodyPart = body_part
        self.json = json_body


class _FakeStub:
    def __init__(self, responses: list[_FakeResponse]) -> None:
        self._responses = responses

    def CallExtensionKeyword(self, _request):  # noqa: N802 - gRPC stub API
        return iter(self._responses)


class _FakeChannel:
    def __init__(self, stub: _FakeStub) -> None:
        self._stub = stub

    def __enter__(self) -> _FakeStub:
        return self._stub

    def __exit__(self, *_exc) -> bool:
        return False


def _plugin_with_stub(responses: list[_FakeResponse]) -> RecorderPlugin:
    plugin = _make_plugin()
    stub = _FakeStub(responses)
    fake_playwright = SimpleNamespace(grpc_channel=lambda: _FakeChannel(stub))
    plugin.library = SimpleNamespace(playwright=fake_playwright)
    return plugin


def test_call_accumulates_multiple_body_part_chunks_into_one_json_document():
    plugin = _plugin_with_stub(
        [
            _FakeResponse(body_part='{"a": 1,'),
            _FakeResponse(body_part=' "b": 2}'),
        ]
    )

    result = plugin._call("someKeyword", {"x": 1})

    assert result == {"a": 1, "b": 2}


def test_call_uses_the_final_json_field_when_present():
    plugin = _plugin_with_stub([_FakeResponse(json_body='{"ok": true}')])

    result = plugin._call("someKeyword", {})

    assert result == {"ok": True}


def test_call_returns_empty_dict_for_an_empty_body():
    plugin = _plugin_with_stub([_FakeResponse()])

    result = plugin._call("someKeyword", {})

    assert result == {}


# --------------------------------------------------------------------------- #
# A malformed event or command must not tear down the whole recording.
# --------------------------------------------------------------------------- #

_CLICK = {
    "name": "click",
    "selector": "css=.x",
    "button": "left",
    "modifiers": 0,
    "clickCount": 1,
}


def test_a_malformed_command_does_not_abort_the_recording(tmp_path):
    # Commands arrive over `context.exposeBinding('__rfbCommand', ...)`, which
    # the page under test can call with anything at all. A payload that is not
    # even a dict used to raise straight out of the poll loop and abort a
    # recording the user had been building for minutes.
    plugin = _make_plugin()
    plugin._call = lambda *_a, **_kw: {}
    poll = _ScriptedPoll(
        [
            {
                "mode": "recording",
                "pages": [1],
                "events": [{"event": "added", "action": _CLICK}],
                "commands": ["not a dict"],
            },
            {
                "mode": "recording",
                "pages": [1],
                "events": ["also not a dict"],
                "commands": [],
            },
            {
                "mode": "recording",
                "pages": [1],
                "events": [{"event": "added", "action": {**_CLICK, "selector": ".y"}}],
                "commands": [],
            },
            {"mode": "stopped", "pages": [1], "events": [], "commands": []},
        ]
    )
    plugin._poll = poll

    session = plugin._run_session(tmp_path / "out.resource", None, fixed_name="KW")

    # The loop ran to the end and both good actions were recorded.
    assert poll.calls[-1]["reset"] is False
    assert len(poll.calls) == 4  # noqa: PLR2004
    assert session.keywords == ["KW"]
    assert "Click    css=.x" in session.text()
    assert "Click    .y" in session.text()
