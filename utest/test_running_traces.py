import pytest

from Browser.utils.data_types import TracingGroupMode
from Browser.utils.running_traces import RunningTraces


def test_no_trace_running_sends_no_groups():
    traces = RunningTraces(TracingGroupMode.Full)

    assert not traces.sends_groups
    assert "context=1" not in traces


@pytest.mark.parametrize("mode", [TracingGroupMode.Full, TracingGroupMode.Browser])
def test_a_running_trace_sends_groups(mode):
    traces = RunningTraces(mode)

    traces.started("context=1")

    assert traces.sends_groups
    assert "context=1" in traces


def test_playwright_group_mode_sends_no_groups_while_a_trace_runs():
    traces = RunningTraces(TracingGroupMode.Playwright)

    traces.started("context=1")

    assert not traces.sends_groups
    assert "context=1" in traces


def test_a_stopped_trace_no_longer_runs():
    traces = RunningTraces(TracingGroupMode.Full)
    traces.started("context=1")

    traces.stopped("context=1")

    assert "context=1" not in traces
    assert not traces.sends_groups


def test_stopping_a_context_without_a_recorded_trace_is_harmless():
    traces = RunningTraces(TracingGroupMode.Full)
    traces.started("context=1")

    traces.stopped("context=2")

    assert "context=1" in traces


def test_traces_of_closed_contexts_are_forgotten():
    traces = RunningTraces(TracingGroupMode.Full)
    traces.started("context=1")
    traces.started("context=2")

    traces.keep_only(["context=2", "context=3"])

    assert "context=1" not in traces
    assert "context=2" in traces
    assert "context=3" not in traces


def test_ending_a_scope_hands_over_and_forgets_only_its_traces():
    traces = RunningTraces(TracingGroupMode.Full)
    traces.started("context=1", scope_id="s1-t1")
    traces.started("context=2", scope_id="s1")
    traces.started("context=3", scope_id="s1-t1")

    assert traces.end_scope("s1-t1") == ["context=1", "context=3"]
    assert "context=1" not in traces
    assert "context=2" in traces
    assert "context=3" not in traces


def test_a_trace_without_a_scope_does_not_end_with_any_scope():
    traces = RunningTraces(TracingGroupMode.Full)
    traces.started("context=1")

    assert traces.end_scope("s1") == []
    assert "context=1" in traces


def test_any_running_tells_if_a_trace_runs_in_every_group_mode():
    traces = RunningTraces(TracingGroupMode.Playwright)
    assert not traces.any_running

    traces.started("context=1")
    assert traces.any_running


def test_the_group_mode_can_not_be_changed_after_creation():
    traces = RunningTraces(TracingGroupMode.Playwright)

    with pytest.raises(AttributeError):
        traces.group_mode = TracingGroupMode.Full  # type: ignore[misc]
