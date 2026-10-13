from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from Browser.keywords import recorder as module
from Browser.keywords.recorder import SUITE_SOURCE, Recorder
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
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
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
