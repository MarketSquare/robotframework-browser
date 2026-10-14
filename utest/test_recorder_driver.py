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
from __future__ import annotations

import pytest

from Browser.recorder.driver import run_session
from Browser.recorder.session import RecorderSession

from .test_recorder_session import FILL, Clock, FakeTarget

FAIL_ON_POLL = 2
DRAIN_POLLS = 3
BAD_REPLY_POLLS = 2
IDLE_POLL_LIMIT = 6
#: Polls (0.2 s each) until a New has settled and the keyword is recording.
SETTLE_POLLS = 3


class Client:
    def __init__(self, replies, clock=None, step=0.2):
        self.replies = list(replies)
        self.polls: list[tuple[dict, bool]] = []
        self.stopped = False
        self.clock = clock
        self.step = step

    def poll(self, state, reset):
        self.polls.append((state, reset))
        if self.clock is not None:
            self.clock.now += self.step
        if self.replies:
            return self.replies.pop(0)
        return {"mode": "recording", "pages": 1, "events": [], "commands": []}

    def stop(self):
        self.stopped = True


def reply(events=(), commands=(), mode="recording", pages=1):
    return {
        "mode": mode,
        "pages": pages,
        "events": list(events),
        "commands": list(commands),
    }


def settling():
    return [reply() for _ in range(SETTLE_POLLS)]


def make(clock=None, **kwargs):
    clock = clock or Clock()
    return RecorderSession(FakeTarget(), clock=clock, **kwargs), clock


def test_first_poll_resets_later_ones_do_not():
    s, clock = make()
    client = Client([reply(commands=[{"cmd": "stop"}])], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "stop"
    assert [reset for _, reset in client.polls][:2] == [True, False]
    assert client.stopped


def test_playwright_stop_drains_once_more_then_ends():
    s, clock = make()
    client = Client(
        [
            reply(commands=[{"cmd": "new", "name": "K"}]),
            *settling(),
            reply(mode="stopped"),
            reply(events=[{"event": "added", "action": FILL}]),
        ],
        clock,
    )
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "playwright"
    assert s.keywords == ["K"]
    assert "Fill Text" in s.text()
    assert len(client.polls) == DRAIN_POLLS + SETTLE_POLLS


def test_failing_drain_poll_after_playwright_stop_is_ignored():
    s, clock = make()

    class DrainBoom(Client):
        def poll(self, state, reset):
            if len(self.polls) == FAIL_ON_POLL + SETTLE_POLLS:
                raise RuntimeError("late")
            return super().poll(state, reset)

    client = DrainBoom(
        [reply(commands=[{"cmd": "new", "name": "K"}]), *settling()], clock
    )
    client.replies.append(
        reply(mode="stopped", events=[{"event": "added", "action": FILL}])
    )
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "playwright"
    assert s.keywords == ["K"]
    assert client.stopped


def test_all_pages_closed_ends_the_session():
    s, clock = make()
    client = Client([reply(pages=0)], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "pages"


def test_idle_timeout_is_reset_by_activity():
    s, clock = make()
    activity = [reply(commands=[{"cmd": "new", "name": "K"}])] + [
        reply(events=[{"event": "added", "action": FILL}]) for _ in range(10)
    ]
    client = Client(activity, clock, step=0.2)
    reason = run_session(s, client, idle_timeout=1.0, clock=clock, sleep=lambda _: None)
    assert reason == "idle"
    assert len(client.polls) >= 11 + 5


def test_idle_timeout_also_counts_idle_actions():
    s, clock = make()
    client = Client(
        [reply(events=[{"event": "added", "action": FILL}])] * 8, clock, step=0.2
    )
    run_session(s, client, idle_timeout=1.0, clock=clock, sleep=lambda _: None)
    assert len(client.polls) >= 8 + 5


def test_exception_still_saves_and_stops():
    s, clock = make()

    class Boom(Client):
        def poll(self, state, reset):
            if len(self.polls) == FAIL_ON_POLL + SETTLE_POLLS:
                raise RuntimeError("grpc down")
            return super().poll(state, reset)

    client = Boom(
        [
            reply(commands=[{"cmd": "new", "name": "K"}]),
            *settling(),
            reply(events=[{"event": "added", "action": FILL}]),
        ],
        clock,
    )
    with pytest.raises(RuntimeError, match="grpc down"):
        run_session(s, client, clock=clock, sleep=lambda _: None)
    assert s.keywords == ["K"]
    assert client.stopped


def test_malformed_events_and_commands_are_ignored():
    s, clock = make()
    client = Client(
        [
            reply(
                events=[None, {"event": "added", "action": "nope"}], commands=[None, 42]
            ),
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "stop"


def test_stop_failure_does_not_mask_the_real_error():
    s, clock = make()

    class Both(Client):
        def poll(self, state, reset):
            raise RuntimeError("real")

        def stop(self):
            raise RuntimeError("cleanup")

    with pytest.raises(RuntimeError, match="real"):
        run_session(s, Both([], clock), clock=clock, sleep=lambda _: None)


@pytest.mark.parametrize(
    "bad",
    [
        None,
        [],
        "text",
        {"mode": "recording", "pages": 1, "events": 5, "commands": "abc"},
        {"mode": "recording", "pages": 1, "events": "abc", "commands": 5},
    ],
)
def test_malformed_reply_shapes_do_not_kill_the_loop(bad):
    s, clock = make()
    client = Client([bad, reply(commands=[{"cmd": "stop"}])], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "stop"
    assert len(client.polls) >= BAD_REPLY_POLLS


def test_close_failure_still_stops_client_and_keeps_loop_error(monkeypatch):
    s, clock = make()

    def broken_close():
        raise RuntimeError("close broke")

    monkeypatch.setattr(s, "close", broken_close)

    class Boom(Client):
        def poll(self, state, reset):
            raise RuntimeError("loop error")

    client = Boom([], clock)
    with pytest.raises(RuntimeError, match="loop error"):
        run_session(s, client, clock=clock, sleep=lambda _: None)
    assert client.stopped


def test_close_failure_without_loop_error_still_returns(monkeypatch):
    s, clock = make()

    def broken_close():
        raise RuntimeError("close broke")

    monkeypatch.setattr(s, "close", broken_close)
    client = Client([reply(pages=0)], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "pages"
    assert client.stopped


def test_close_base_exception_still_stops_client(monkeypatch):
    s, clock = make()

    def interrupted():
        raise KeyboardInterrupt

    monkeypatch.setattr(s, "close", interrupted)
    client = Client([reply(pages=0)], clock)
    with pytest.raises(KeyboardInterrupt):
        run_session(s, client, clock=clock, sleep=lambda _: None)
    assert client.stopped


def test_junk_entries_do_not_count_as_activity():
    s, clock = make()
    junk = reply(events=[None, "x", 7], commands=[None, 42])
    client = Client([junk] * 10, clock, step=0.2)
    assert (
        run_session(s, client, idle_timeout=1.0, clock=clock, sleep=lambda _: None)
        == "idle"
    )
    assert len(client.polls) <= IDLE_POLL_LIMIT


def test_events_are_applied_before_commands_within_one_reply():
    s, clock = make()
    client = Client(
        [
            reply(commands=[{"cmd": "new", "name": "K"}]),
            *settling(),
            reply(
                events=[{"event": "added", "action": FILL}],
                commands=[{"cmd": "new", "name": "L"}],
            ),
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    run_session(s, client, clock=clock, sleep=lambda _: None)
    assert s.keywords == ["K"]
    assert "Fill Text" in s.text()


def test_picking_flag_of_the_reply_reaches_the_toolbar_state():
    s, clock = make()
    client = Client(
        [
            {**reply(), "picking": True},
            reply(),
            {**reply(), "picking": True},
            {**reply(), "picking": False},
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    run_session(s, client, clock=clock, sleep=lambda _: None)
    assert [state["picking"] for state, _ in client.polls][:5] == [
        False,
        True,
        False,
        True,
        False,
    ]


@pytest.mark.parametrize("bad", ["yes", 1, None, [True]])
def test_a_non_bool_picking_field_counts_as_off(bad):
    s, clock = make()
    client = Client(
        [
            {**reply(), "picking": True},
            {**reply(), "picking": bad},
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    run_session(s, client, clock=clock, sleep=lambda _: None)
    assert client.polls[2][0]["picking"] is False


def test_ignored_entries_are_logged_truncated(monkeypatch):
    from Browser.recorder import driver

    warnings: list[str] = []
    monkeypatch.setattr(driver.logger, "warn", warnings.append)
    s, clock = make()
    client = Client(
        [
            reply(events=[{"event": "added", "action": "x" * 5000}]),
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    run_session(s, client, clock=clock, sleep=lambda _: None)
    assert warnings
    assert max(len(w) for w in warnings) < 600
