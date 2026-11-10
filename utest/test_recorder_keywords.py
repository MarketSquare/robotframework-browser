from __future__ import annotations

import json
import sys
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from robot.conf.languages import Languages

from Browser import Browser
from Browser.keywords import recorder as module
from Browser.keywords.interaction import Interaction
from Browser.keywords.recorder import SUITE_SOURCE, Recorder
from Browser.recorder import session as session_module
from Browser.recorder.model import Call, DisplayNames
from Browser.recorder.names import KnownKeywords, normalize_keyword_name
from Browser.recorder.parameters import KEYWORD_PARAMETERS
from Browser.recorder.target import FileTarget, LogTarget
from Browser.utils import keyword


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
    recorder = _recorder(monkeypatch)
    seen = {}

    def fake_run(session, client, idle_timeout=None):
        seen["idle"] = idle_timeout
        session.handle_command({"cmd": "new", "name": "K"})
        session.tick()
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
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
    recorder = _recorder(monkeypatch)
    seen = {}

    def fake_run(session, client, idle_timeout=None):
        seen["idle"] = idle_timeout
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
    recorder.record_keywords(str(tmp_path / "k.resource"), *given)
    assert seen["idle"] == expected


def test_record_keyword_rejects_a_shadowing_name(monkeypatch, tmp_path):
    recorder = _recorder(monkeypatch)
    monkeypatch.setattr(
        module,
        "collect_known_keywords",
        lambda: KnownKeywords(names=frozenset({"Click"})),
    )
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
def test_non_positive_idle_timeout_is_rejected(idle, tmp_path, monkeypatch):
    recorder = _recorder(monkeypatch)
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
    recorder = Recorder(
        SimpleNamespace(keywords={}, registered_keyword_names={}, keyword_call_stack=[])
    )
    recorder._client = lambda: object()
    return recorder


def test_record_keyword_happy_path(monkeypatch, tmp_path):
    recorder = _recorder(monkeypatch)

    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
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
    recorder = _recorder(monkeypatch)
    path = tmp_path / "k.resource"
    warnings = []
    monkeypatch.setattr(module.logger, "warn", warnings.append)

    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        path.chmod(0o444)
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    try:
        with pytest.raises(RuntimeError, match="'Fill Name' not saved"):
            recorder.record_keyword("Fill Name", str(path))
    finally:
        path.chmod(0o644)
    assert "Fill Name\n    [Tags]    recorded\n    Fill Text" in warnings[0]


TRANSLATED = ["Remplir Le Texte", "Tekst Eingeben", "Fill Text"]


def _translated_recorder(monkeypatch, translated):
    recorder = _recorder(monkeypatch)
    recorder.library = SimpleNamespace(
        keywords={}, registered_keyword_names={"fill_text": translated}
    )
    return recorder


@pytest.mark.parametrize("translated", TRANSLATED)
def test_returned_text_uses_registered_names(monkeypatch, tmp_path, translated):
    recorder = _translated_recorder(monkeypatch, translated)
    text = recorder.record_keywords(str(tmp_path / "translated.resource"))
    assert translated in text


@pytest.mark.parametrize("translated", TRANSLATED)
def test_file_gets_registered_names(monkeypatch, tmp_path, translated):
    recorder = _translated_recorder(monkeypatch, translated)
    path = tmp_path / "translated.resource"
    recorder.record_keywords(str(path))
    assert translated in path.read_text(encoding="utf-8")


@pytest.fixture(params=[None, "fr"], ids=["english", "french"])
def registered_library(monkeypatch, tmp_path, request):
    language = request.param

    translation = tmp_path / "translation.json"
    translation.write_text(
        json.dumps({"fill_text": {"name": "Remplir Le Texte", "doc": ""}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        Browser,
        "_get_translation",
        staticmethod(lambda lang: translation if lang else None),
    )
    library = Browser(language=language)
    return library, language


def _display_name(library, canonical):
    display_names = DisplayNames.from_registered(library.registered_keyword_names)
    return display_names.of(Call(canonical, []))


def test_registered_names_cover_all_recorded_keywords(registered_library):
    library, _ = registered_library
    registered = {normalize_keyword_name(m) for m in library.registered_keyword_names}
    assert {normalize_keyword_name(c) for c in KEYWORD_PARAMETERS} <= registered


def test_display_names_follow_registered_translation(registered_library):
    library, language = registered_library
    expected = "Remplir Le Texte" if language else "Fill Text"
    assert _display_name(library, "Fill Text") == expected


def test_untranslated_keyword_keeps_english_display_name(registered_library):
    library, _ = registered_library
    assert _display_name(library, "Click") == "Click"


@pytest.mark.parametrize("canonical", sorted(KEYWORD_PARAMETERS))
def test_display_names_exist_in_dynamic_core_registry(registered_library, canonical):
    library, _ = registered_library
    registered = {normalize_keyword_name(name) for name in library.keywords}
    assert normalize_keyword_name(_display_name(library, canonical)) in registered


def test_plugin_method_with_same_name_does_not_replace_browser_mapping(tmp_path):

    plugin = tmp_path / "AliasPlugin.py"
    plugin.write_text(
        """from Browser.base import LibraryComponent
from Browser.utils import keyword


class AliasPlugin(LibraryComponent):
    @keyword(name="Plugin Click")
    def click(self, selector: str): ...
""",
        encoding="utf-8",
    )
    library = Browser(plugins=str(plugin))
    assert _display_name(library, "Click") == "Click"


def test_inherited_plugin_method_does_not_replace_browser_mapping():

    class AliasPlugin(Interaction):
        pass

    library = Browser()
    library.keywords["Plugin Click"] = AliasPlugin(library).click
    assert _display_name(library, "Click") == "Click"


class _OverridingBrowser(Browser):
    @keyword
    def fill_text(self, selector: str, txt: str) -> None: ...


def test_library_subclass_override_keeps_translated_name(monkeypatch, tmp_path):
    translation = tmp_path / "translation.json"
    translation.write_text(
        json.dumps({"fill_text": {"name": "Remplir Le Texte", "doc": ""}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        Browser, "_get_translation", staticmethod(lambda lang: translation)
    )
    library = _OverridingBrowser(language="fr")
    assert _display_name(library, "Fill Text") == "Remplir Le Texte"


def test_file_target_gets_configured_languages(monkeypatch, tmp_path):
    monkeypatch.setattr(module, "configured_languages", lambda: tuple(Languages("fr")))
    target = Recorder._target(str(tmp_path / "k.resource"))
    assert target.settings.tags == "Étiquette"


def test_log_target_gets_configured_languages(monkeypatch):
    monkeypatch.setattr(module, "configured_languages", lambda: tuple(Languages("fr")))
    assert Recorder._target(None).settings.tags == "Étiquette"


def test_a_file_that_is_not_utf8_is_refused_before_recording(tmp_path):
    path = tmp_path / "k.resource"
    path.write_bytes(b"*** Keywords ***\nExisting\n    Log    caf\xe9\n")
    with pytest.raises(ValueError, match="Cannot record into .*not valid UTF-8"):
        Recorder._target(str(path))


def test_recording_writes_settings_in_file_language(monkeypatch, tmp_path):
    recorder = _recorder(monkeypatch)

    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    path = tmp_path / "k.resource"
    path.write_text("Language: fr\n", encoding="utf-8")
    recorder.record_keyword("Fill Name", str(path))
    assert "Fill Name\n    [Étiquette]    recorded\n" in path.read_text(
        encoding="utf-8"
    )


def test_browser_registers_builtin_keyword_names_by_method():
    assert Browser().registered_keyword_names["fill_text"] == "Fill Text"


def test_browser_registered_names_follow_translation(registered_library):
    library, language = registered_library
    expected = "Remplir Le Texte" if language else "Fill Text"
    assert library.registered_keyword_names["fill_text"] == expected


def test_browser_registered_names_follow_a_plugin_override(monkeypatch, tmp_path):
    translation = tmp_path / "translation.json"
    translation.write_text(
        json.dumps({"click": {"name": "Klikkaa", "doc": ""}}), encoding="utf-8"
    )
    monkeypatch.setattr(
        Browser, "_get_translation", staticmethod(lambda lang: translation)
    )
    plugin = tmp_path / "OverridePlugin.py"
    plugin.write_text(
        """from Browser.base import LibraryComponent
from Browser.utils import keyword


class OverridePlugin(LibraryComponent):
    @keyword
    def click(self, selector: str): ...
""",
        encoding="utf-8",
    )
    library = Browser(language="fi", plugins=str(plugin))
    assert library.registered_keyword_names["click"] == "Klikkaa"


def test_browser_registered_names_are_computed_once():
    library = Browser()
    assert library.registered_keyword_names is library.registered_keyword_names


def test_browser_registered_names_are_read_only():
    with pytest.raises(TypeError):
        Browser().registered_keyword_names["fill_text"] = "Changed"


@pytest.mark.skipif(
    sys.platform == "win32", reason="chmod does not make files unreadable"
)
def test_an_unreadable_file_is_refused_before_recording(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text("", encoding="utf-8")
    path.chmod(0o222)
    try:
        with pytest.raises(ValueError, match="Cannot record into .*Permission denied"):
            Recorder._target(str(path))
    finally:
        path.chmod(0o644)


def test_a_refused_file_reason_ends_with_one_period(monkeypatch, tmp_path):
    def refuse(path, languages):
        raise ValueError("No language with name 'MyLang.py' found.")

    monkeypatch.setattr(module, "FileTarget", refuse)
    with pytest.raises(ValueError, match=r"'MyLang\.py' found\.$"):
        Recorder._target(str(tmp_path / "k.resource"))


_DEBUG_SUITE = "*** Test Cases ***\nExplore\n    Debug\n"


def _in_test(monkeypatch, recorder, suite, line=3):
    monkeypatch.setattr(
        module, "_running_test", lambda: SimpleNamespace(source=str(suite))
    )
    monkeypatch.setattr(module, "_suite_source", lambda: str(suite))
    recorder.library.keyword_call_stack[:] = [{"file": str(suite), "line": line}]


def _record_one(monkeypatch, keyword_name="K", text="x"):
    def run(session, client, idle_timeout=None):
        session.handle_command({"cmd": "new", "name": keyword_name})
        session.tick()
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": text})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)


def test_insert_call_puts_the_calls_before_the_running_step(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(_DEBUG_SUITE)
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)
    _record_one(monkeypatch, "First")
    assert recorder.record_keywords(insert_call=True) is None
    _record_one(monkeypatch, "Second")
    assert recorder.record_keywords(insert_call=True) is None
    assert suite.read_text().startswith(
        "*** Test Cases ***\nExplore\n    First\n    Second\n    Debug\n"
    )
    assert "\nFirst\n    [Tags]    recorded\n" in suite.read_text()


def test_record_keyword_inserts_its_call(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(_DEBUG_SUITE)
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)

    def run(session, client, idle_timeout=None):
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    assert recorder.record_keyword("Fill Name", insert_call=True) is None
    assert "Explore\n    Fill Name\n    Debug\n" in suite.read_text()


def test_without_insert_call_the_test_is_left_alone(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(_DEBUG_SUITE)
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)
    recorder.record_keywords(str(suite))
    assert suite.read_text().startswith(_DEBUG_SUITE)


def test_insert_call_needs_a_file(monkeypatch, tmp_path):
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, tmp_path / "suite.robot")
    with pytest.raises(ValueError, match=r"file=\$\{None\}"):
        recorder.record_keywords(None, insert_call=True)


def test_insert_call_needs_a_running_test(monkeypatch, tmp_path):
    recorder = _recorder(monkeypatch)
    monkeypatch.setattr(module, "_running_test", lambda: None)
    with pytest.raises(ValueError, match="no test is running"):
        recorder.record_keywords(str(tmp_path / "k.resource"), insert_call=True)


def test_insert_call_needs_the_file_of_the_test(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(_DEBUG_SUITE)
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)
    other = tmp_path / "k.resource"
    with pytest.raises(ValueError, match="must be the file of that test"):
        recorder.record_keywords(str(other), insert_call=True)
    assert not other.exists()


def test_insert_call_is_refused_in_a_test_setup(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(
        "*** Test Cases ***\nExplore\n    [Setup]    Debug\n    Log    x\n"
    )
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)
    with pytest.raises(ValueError, match="setup or teardown"):
        recorder.record_keywords(insert_call=True)


def test_a_call_that_cannot_be_inserted_is_logged(monkeypatch, tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(_DEBUG_SUITE)
    recorder = _recorder(monkeypatch)
    _in_test(monkeypatch, recorder, suite)
    warnings = []
    monkeypatch.setattr(module.logger, "warn", warnings.append)

    def run(session, client, idle_timeout=None):
        _record_one_into(session)
        suite.write_text(suite.read_text().replace("Explore", "Renamed"))
        return "stop"

    monkeypatch.setattr(module, "run_session", run)
    recorder.record_keywords(insert_call=True)
    assert "The call of 'K' could not be inserted into test 'Explore'" in warnings[0]
    assert warnings[0].endswith("Add it by hand:\n    K")


def _record_one_into(session):
    session.handle_command({"cmd": "new", "name": "K"})
    session.tick()
    session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
    session.close()
