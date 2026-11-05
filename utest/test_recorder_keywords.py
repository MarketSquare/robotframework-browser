from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

import pytest

from Browser.keywords import recorder as module
from Browser.keywords.recorder import SUITE_SOURCE, Recorder
from Browser.recorder import session as session_module
from Browser.recorder.names import KnownKeywords
from Browser.recorder.target import FileTarget, LogTarget


def test_none_means_log_only():
    assert isinstance(Recorder._target(None), LogTarget)


def test_explicit_file_is_resolved(tmp_path):
    target = Recorder._target(str(tmp_path / "k.resource"))
    assert isinstance(target, FileTarget)
    assert target.path == (tmp_path / "k.resource").resolve()


def test_default_resolves_suite_source(monkeypatch, tmp_path):
    suite = tmp_path / "s.robot"
    monkeypatch.setattr(module, "_suite_source", lambda: str(suite))
    assert Recorder._target(SUITE_SOURCE).path == suite.resolve()


def test_default_without_running_suite_fails_clearly(monkeypatch):
    monkeypatch.setattr(module, "_suite_source", lambda: None)
    with pytest.raises(ValueError, match="file"):
        Recorder._target(SUITE_SOURCE)


def test_record_keywords_runs_a_session_and_returns_text(monkeypatch, tmp_path):
    seen = {}

    def fake_run(session, client, idle_timeout=None):
        seen["idle"] = idle_timeout
        session.handle_command({"cmd": "new", "name": "K"})
        session.tick()
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
    monkeypatch.setattr(session_module, "SETTLE_SECONDS", 0)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    text = recorder.record_keywords(str(tmp_path / "k.resource"), timedelta(seconds=3))
    assert seen["idle"] == 3.0
    assert text.startswith("*** Keywords ***\nK\n")
    assert Path(tmp_path / "k.resource").exists()


@pytest.mark.parametrize(
    ("given", "expected"),
    [((), 300.0), ((None,), None)],
    ids=["default 5 minutes", "None waits without limit"],
)
def test_idle_timeout_default_and_none(monkeypatch, tmp_path, given, expected):
    seen = {}

    def fake_run(session, client, idle_timeout=None):
        seen["idle"] = idle_timeout
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    recorder.record_keywords(str(tmp_path / "k.resource"), *given)
    assert seen["idle"] == expected


def test_record_keyword_rejects_a_shadowing_name(monkeypatch, tmp_path):
    monkeypatch.setattr(
        module,
        "collect_known_keywords",
        lambda: KnownKeywords(names=frozenset({"Click"})),
    )
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    with pytest.raises(ValueError, match="shadowed"):
        recorder.record_keyword("Click", str(tmp_path / "k.resource"))


class _FakeStub:
    def __init__(self, reply_json="{}"):
        self.reply_json = reply_json
        self.bodies = []
        self.stopped = False

    def RecorderPoll(self, request):  # noqa: N802
        self.bodies.append(request.body)
        return type("R", (), {"json": self.reply_json})()

    def RecorderStop(self, request):  # noqa: N802
        self.stopped = True


def _client(stub, allows_headless=False):
    from contextlib import contextmanager

    @contextmanager
    def channel():
        yield stub

    library = type(
        "L",
        (),
        {
            "playwright": type("P", (), {"grpc_channel": staticmethod(channel)})(),
            "recorder_allows_headless": allows_headless,
        },
    )()
    return module._GrpcRecorderClient(library)


def test_poll_parses_valid_json():
    stub = _FakeStub('{"events": []}')
    assert _client(stub).poll({"a": 1}, True) == {"events": []}
    assert '"reset": true' in stub.bodies[0]
    assert '"allowHeadless": false' in stub.bodies[0]


def test_poll_passes_the_headless_test_switch():
    stub = _FakeStub()
    _client(stub, allows_headless=True).poll({}, True)
    assert '"allowHeadless": true' in stub.bodies[0]


@pytest.mark.parametrize("raw", ["", "not json", "[1]"])
def test_an_unreadable_reply_is_a_protocol_error(raw):
    with pytest.raises(RuntimeError, match="unreadable reply"):
        _client(_FakeStub(raw)).poll({}, False)


def test_stop_calls_recorder_stop_after_a_started_session():
    stub = _FakeStub()
    client = _client(stub)
    client.poll({}, True)
    client.stop()
    assert stub.stopped


def test_stop_leaves_a_session_alone_whose_start_was_refused():
    stub = _FakeStub()
    _client(stub).stop()
    assert not stub.stopped


@pytest.mark.parametrize("idle", [timedelta(0), timedelta(seconds=-1)])
def test_non_positive_idle_timeout_is_rejected(idle, tmp_path):
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    with pytest.raises(ValueError, match="idle_timeout"):
        recorder.record_keywords(str(tmp_path / "k.resource"), idle)


def _fake_run(session, client, idle_timeout=None):
    session.handle_command({"cmd": "new", "name": "K"})
    session.tick()
    session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
    session.close()
    return "stop"


def _recorder(monkeypatch):
    monkeypatch.setattr(module, "run_session", _fake_run)
    monkeypatch.setattr(session_module, "SETTLE_SECONDS", 0)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    return recorder


def test_record_keyword_happy_path(monkeypatch, tmp_path):
    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    path = tmp_path / "k.resource"
    text = recorder.record_keyword("Fill Name", str(path))
    assert text.startswith("*** Keywords ***\nFill Name\n")
    assert "Fill Name" in path.read_text()


def test_log_only_returns_text_without_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    text = _recorder(monkeypatch).record_keywords(None)
    assert text.startswith("*** Keywords ***\nK\n")
    assert list(tmp_path.iterdir()) == []


def test_symlinked_path_resolves_to_real_file(tmp_path):
    real = tmp_path / "real.resource"
    link = tmp_path / "link.resource"
    link.symlink_to(real)
    assert Recorder._target(str(link)).path == real.resolve()


def test_directory_target_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="is a directory"):
        Recorder._target(str(tmp_path))


def test_a_directory_suite_records_into_its_init_file(monkeypatch, tmp_path):
    (tmp_path / "__init__.robot").write_text("*** Settings ***\n")
    monkeypatch.setattr(module, "_suite_source", lambda: str(tmp_path))
    assert (
        Recorder._target(SUITE_SOURCE).path == (tmp_path / "__init__.robot").resolve()
    )


@pytest.mark.parametrize("init", [None, "__init__.rst"])
def test_a_directory_suite_without_init_robot_is_refused(monkeypatch, tmp_path, init):
    if init:
        (tmp_path / init).write_text("")
    monkeypatch.setattr(module, "_suite_source", lambda: str(tmp_path))
    with pytest.raises(ValueError, match="has no __init__.robot"):
        Recorder._target(SUITE_SOURCE)


def test_a_file_in_a_missing_folder_is_refused_before_recording(tmp_path):
    with pytest.raises(ValueError, match="does not exist"):
        Recorder._target(str(tmp_path / "missing" / "k.resource"))


@pytest.mark.skipif(
    sys.platform == "win32", reason="chmod does not make files read-only"
)
def test_a_read_only_file_is_refused_before_recording(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text("*** Keywords ***\n")
    path.chmod(0o444)
    try:
        with pytest.raises(ValueError, match="is read-only"):
            Recorder._target(str(path))
    finally:
        path.chmod(0o644)


@pytest.mark.skipif(
    sys.platform == "win32", reason="chmod does not make files read-only"
)
def test_a_keyword_that_could_not_be_written_fails_the_call_and_is_logged(
    monkeypatch, tmp_path
):
    path = tmp_path / "k.resource"
    warnings = []
    monkeypatch.setattr(module.logger, "warn", warnings.append)

    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        path.chmod(0o444)
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    try:
        with pytest.raises(RuntimeError, match="'Fill Name' not saved"):
            recorder.record_keyword("Fill Name", str(path))
    finally:
        path.chmod(0o644)
    assert "Fill Name\n    [Tags]    recorded\n    Fill Text" in warnings[0]
