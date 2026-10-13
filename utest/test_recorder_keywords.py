from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from Browser.keywords import recorder as module
from Browser.keywords.recorder import SUITE_SOURCE, Recorder
from Browser.recorder import session as session_module
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
    monkeypatch.setattr(
        module, "collect_known_keywords", lambda: module.KnownKeywords()
    )
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    text = recorder.record_keywords(str(tmp_path / "k.resource"), timedelta(seconds=3))
    assert seen["idle"] == 3.0
    assert text.startswith("*** Keywords ***\nK\n")
    assert Path(tmp_path / "k.resource").exists()


def test_record_keyword_rejects_a_shadowing_name(monkeypatch, tmp_path):
    monkeypatch.setattr(
        module,
        "collect_known_keywords",
        lambda: module.KnownKeywords(names=frozenset({"Click"})),
    )
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    with pytest.raises(ValueError, match="shadowed"):
        recorder.record_keyword("Click", str(tmp_path / "k.resource"))


class _FakeStub:
    def __init__(self, reply_json=""):
        self.reply_json = reply_json
        self.bodies = []
        self.stopped = False

    def RecorderPoll(self, request):  # noqa: N802
        self.bodies.append(request.body)
        return type("R", (), {"json": self.reply_json})()

    def RecorderStop(self, request):  # noqa: N802
        self.stopped = True


def _client(stub):
    from contextlib import contextmanager

    @contextmanager
    def channel():
        yield stub

    library = type(
        "L",
        (),
        {"playwright": type("P", (), {"grpc_channel": staticmethod(channel)})()},
    )()
    return module._GrpcRecorderClient(library)


def test_poll_parses_valid_json():
    stub = _FakeStub('{"events": []}')
    assert _client(stub).poll({"a": 1}, True) == {"events": []}
    assert '"reset": true' in stub.bodies[0]


@pytest.mark.parametrize("raw", ["", "not json", "[1]"])
def test_poll_tolerates_empty_and_malformed_replies(raw):
    assert _client(_FakeStub(raw)).poll({}, False) == {}


def test_stop_calls_recorder_stop():
    stub = _FakeStub()
    _client(stub).stop()
    assert stub.stopped


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
    monkeypatch.setattr(
        module, "collect_known_keywords", lambda: module.KnownKeywords()
    )
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    return recorder


def test_record_keyword_happy_path(monkeypatch, tmp_path):
    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    monkeypatch.setattr(
        module, "collect_known_keywords", lambda: module.KnownKeywords()
    )
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
