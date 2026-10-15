import json
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from Browser import Browser
from Browser.base.cache import ContextCache
from Browser.utils.data_types import KeywordCallStackEntry, TracingGroupMode


class FakePlaywright:
    def __init__(self):
        self.stub = MagicMock()
        self.stub.NewContext.return_value = MagicMock(contextOptions="{}")
        self.stub.NewPersistentContext.return_value = MagicMock(
            contextOptions="{}", video="{}"
        )
        self.stub.GetBrowserCatalog.return_value = MagicMock(json="[]")

    @contextmanager
    def grpc_channel(self):
        yield self.stub


def library(tmpdir, monkeypatch) -> Browser:
    monkeypatch.setattr(Browser, "_output_dir", tmpdir)
    monkeypatch.setattr(Browser, "_context_cache", ContextCache())
    monkeypatch.delenv("ROBOT_FRAMEWORK_BROWSER_TRACING", raising=False)
    browser = Browser()
    browser._playwright = FakePlaywright()
    return browser


def keyword_call(name: str) -> KeywordCallStackEntry:
    return {"name": name, "file": "", "line": 0, "kwname": name, "args": []}


def sent_options(request) -> dict:
    return json.loads(request.call_args.args[0].rawOptions)


def test_no_tracing_and_no_recording_by_default(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options()

    assert options["tracing"] is None
    assert options["recordVideo"] is None
    assert options["recordHar"] is None


def test_traces_dir_is_a_new_folder_in_browsers_temporary_trace_folder(
    tmpdir, monkeypatch
):
    browser = library(tmpdir, monkeypatch)

    first = browser.adopted_context_options()["tracesDir"]
    second = browser.adopted_context_options()["tracesDir"]

    assert Path(first).parent == browser.traces_temp
    assert first != second


def test_tracing_follows_new_context(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    assert browser.adopted_context_options(tracing=True)["tracing"] == str(
        browser.traces_output
    )
    assert browser.adopted_context_options(tracing=Path("trace.zip"))["tracing"] == str(
        Path(tmpdir, "trace.zip").resolve()
    )


def test_relative_trace_folder_is_in_browsers_trace_folder(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(tracing=Path("adopted"))

    assert options["tracing"] == str((browser.traces_output / "adopted").resolve())


def test_tracing_follows_the_global_setting(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    monkeypatch.setenv("ROBOT_FRAMEWORK_BROWSER_TRACING", "True")

    assert browser.adopted_context_options()["tracing"] == str(browser.traces_output)


def test_tracing_follows_the_robot_framework_variable(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    variables = {"${ROBOT_FRAMEWORK_BROWSER_TRACING}": "True"}
    monkeypatch.setattr(
        "Browser.keywords.playwright_state.EXECUTION_CONTEXTS",
        SimpleNamespace(current=True),
    )
    monkeypatch.setattr(
        "Browser.keywords.playwright_state.BuiltIn",
        lambda: SimpleNamespace(get_variable_value=variables.get),
    )

    assert browser.adopted_context_options()["tracing"] == str(browser.traces_output)


def test_empty_video_options_record_with_the_defaults(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(recordVideo={})

    assert options["recordVideo"] == {
        "dir": str(browser.video_output.resolve()),
        "size": {"width": 1280, "height": 720},
    }


def test_video_keeps_its_other_keys(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(
        recordVideo={"showActions": {"duration": 500}}
    )

    assert options["recordVideo"]["showActions"] == {"duration": 500}


def test_video_folder_and_size_follow_new_context(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(
        recordVideo={"dir": "demo", "size": {"width": "800", "height": "600"}}
    )

    assert options["recordVideo"] == {
        "dir": str((browser.video_output / "demo").resolve()),
        "size": {"width": 800, "height": 600},
    }


def test_absolute_video_folder_is_kept(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    videos = str(Path(tmpdir, "elsewhere", "videos").resolve())

    options = browser.adopted_context_options(recordVideo={"dir": videos})

    assert options["recordVideo"]["dir"] == videos


def test_video_without_size_has_the_size_of_the_viewport(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(
        recordVideo={}, viewport={"width": 1024, "height": 768}
    )

    assert options["recordVideo"]["size"] == {"width": 1024, "height": 768}


def test_registered_context_gets_the_keyword_calls_as_trace_groups(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    browser.keyword_call_stack.append(keyword_call("Open Application"))
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    group = browser._playwright.stub.OpenTraceGroup.call_args.args[0]
    assert (group.name, group.contextId) == ("Open Application", "context=1")
    assert browser.tracing_contexts == ["context=1"]


def test_registered_context_without_tracing_gets_no_trace_groups(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    browser.keyword_call_stack.append(keyword_call("Open Application"))

    browser.register_adopted_context("context=1", browser.adopted_context_options())

    assert not browser._playwright.stub.OpenTraceGroup.called
    assert browser.tracing_contexts == []


def test_playwright_tracing_group_mode_adds_no_trace_groups(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    browser.tracing_group_mode = TracingGroupMode.Playwright
    browser.keyword_call_stack.append(keyword_call("Open Application"))
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    assert not browser._playwright.stub.OpenTraceGroup.called
    assert browser.tracing_contexts == []


def test_registered_context_embeds_its_video(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    options = browser.adopted_context_options(recordVideo={})
    video = str(Path(options["recordVideo"]["dir"], "page.webm"))

    video_path = browser.register_adopted_context("context=1", options, video)

    assert video_path == video
    assert browser._playwright_state.context_cache.get("context=1") == {
        "width": 1280,
        "height": 720,
    }


def test_video_path_without_record_video_is_ignored(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    options = browser.adopted_context_options()

    video_path = browser.register_adopted_context("context=1", options, "page.webm")

    assert video_path == ""


def test_relative_har_path_is_relative_to_the_output_directory(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(
        recordHar={"path": "har/app.har", "omitContent": True}
    )

    assert options["recordHar"] == {
        "path": str(Path(tmpdir, "har", "app.har").resolve()),
        "omitContent": True,
    }


def test_absolute_har_path_is_kept(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    har = str(Path(tmpdir, "elsewhere", "app.har").resolve())

    options = browser.adopted_context_options(recordHar={"path": har})

    assert options["recordHar"] == {"path": har}


def test_new_context_resolves_a_relative_har_path(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    browser.new_context(recordHar={"path": "context.har"})

    options = sent_options(browser._playwright.stub.NewContext)
    assert options["recordHar"] == {"path": str(Path(tmpdir, "context.har").resolve())}


def test_new_persistent_context_resolves_a_relative_har_path(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    browser.new_persistent_context(recordHar={"path": "persistent.har"})

    options = sent_options(browser._playwright.stub.NewPersistentContext)
    assert options["recordHar"] == {
        "path": str(Path(tmpdir, "persistent.har").resolve())
    }
