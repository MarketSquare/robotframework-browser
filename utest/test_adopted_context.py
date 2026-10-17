import json
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

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


@pytest.fixture
def browser(tmpdir, monkeypatch) -> Browser:
    monkeypatch.setattr(Browser, "_output_dir", tmpdir)
    monkeypatch.setattr(Browser, "_context_cache", ContextCache())
    monkeypatch.delenv("ROBOT_FRAMEWORK_BROWSER_TRACING", raising=False)
    browser = Browser()
    browser._playwright = FakePlaywright()
    return browser


VIEWPORT = {"width": 800, "height": 600}
VIDEO_SIZES = [
    ({}, {"width": 800, "height": 600}),
    ({"size": {"width": 640, "height": 480}}, {"width": 640, "height": 480}),
]


def keyword_call(name: str) -> KeywordCallStackEntry:
    return {"name": name, "file": "", "line": 0, "kwname": name, "args": []}


def sent_request(stub_method):
    return stub_method.call_args.args[0]


def sent_options(stub_method) -> dict:
    return json.loads(sent_request(stub_method).rawOptions)


def test_no_tracing_and_no_recording_by_default(browser: Browser):
    options = browser.adopted_context_options()

    assert options["tracing"] is None
    assert options["recordVideo"] is None
    assert options["recordHar"] is None


def test_traces_dir_is_a_new_folder_in_browsers_temporary_trace_folder(
    browser: Browser,
):
    first = browser.adopted_context_options()["tracesDir"]
    second = browser.adopted_context_options()["tracesDir"]

    assert Path(first).parent == browser.traces_temp
    assert first != second


def test_tracing_follows_new_context(browser: Browser, tmpdir):
    assert browser.adopted_context_options(tracing=True)["tracing"] == str(
        browser.traces_output
    )
    assert browser.adopted_context_options(tracing=Path("trace.zip"))["tracing"] == str(
        Path(tmpdir, "trace.zip").resolve()
    )


def test_relative_trace_folder_is_in_browsers_trace_folder(browser: Browser):
    options = browser.adopted_context_options(tracing=Path("adopted"))

    assert options["tracing"] == str((browser.traces_output / "adopted").resolve())


def test_tracing_follows_the_global_setting(browser: Browser, monkeypatch):
    monkeypatch.setenv("ROBOT_FRAMEWORK_BROWSER_TRACING", "True")

    assert browser.adopted_context_options()["tracing"] == str(browser.traces_output)


def test_tracing_follows_the_robot_framework_variable(browser: Browser, monkeypatch):
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


def test_empty_video_options_record_with_the_defaults(browser: Browser):
    options = browser.adopted_context_options(recordVideo={})

    assert options["recordVideo"] == {
        "dir": str(browser.video_output.resolve()),
        "size": {"width": 1280, "height": 720},
    }


def test_video_keeps_its_other_keys(browser: Browser):
    options = browser.adopted_context_options(
        recordVideo={"showActions": {"duration": 500}}
    )

    assert options["recordVideo"]["showActions"] == {"duration": 500}


def test_video_options_are_converted_like_new_context(browser: Browser):
    options = browser.adopted_context_options(
        recordVideo={"fps": "10", "showActions": {"duration": "300"}}
    )

    assert options["recordVideo"]["fps"] == 10
    assert options["recordVideo"]["showActions"] == {"duration": 300}


def test_deprecated_font_size_fails_like_new_context(browser: Browser):
    with pytest.raises(ValueError, match="RecordVideo"):
        browser.adopted_context_options(recordVideo={"showActions": {"fontSize": 20}})


def test_video_folder_and_size_follow_new_context(browser: Browser):
    options = browser.adopted_context_options(
        recordVideo={"dir": "demo", "size": {"width": "800", "height": "600"}}
    )

    assert options["recordVideo"] == {
        "dir": str((browser.video_output / "demo").resolve()),
        "size": {"width": 800, "height": 600},
    }


def test_absolute_video_folder_is_kept(browser: Browser, tmpdir):
    videos = str(Path(tmpdir, "elsewhere", "videos").resolve())

    options = browser.adopted_context_options(recordVideo={"dir": videos})

    assert options["recordVideo"]["dir"] == videos


def test_video_without_size_has_the_size_of_the_viewport(browser: Browser):
    options = browser.adopted_context_options(
        recordVideo={}, viewport={"width": 1024, "height": 768}
    )

    assert options["recordVideo"]["size"] == {"width": 1024, "height": 768}


def test_registered_context_gets_the_keyword_calls_as_trace_groups(browser: Browser):
    browser.keyword_call_stack.append(keyword_call("Open Application"))
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    group = browser._playwright.stub.OpenTraceGroup.call_args.args[0]
    assert (group.name, group.contextId) == ("Open Application", "context=1")
    assert browser.tracing_contexts == ["context=1"]


def test_registered_context_without_tracing_gets_no_trace_groups(browser: Browser):
    browser.keyword_call_stack.append(keyword_call("Open Application"))

    browser.register_adopted_context("context=1", browser.adopted_context_options())

    assert not browser._playwright.stub.OpenTraceGroup.called
    assert browser.tracing_contexts == []


def test_playwright_tracing_group_mode_adds_no_trace_groups(browser: Browser):
    browser.tracing_group_mode = TracingGroupMode.Playwright
    browser.keyword_call_stack.append(keyword_call("Open Application"))
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    assert not browser._playwright.stub.OpenTraceGroup.called
    assert browser.tracing_contexts == []


def test_registered_context_outside_a_keyword_is_traced_without_trace_groups(
    browser: Browser,
):
    browser.tracing_group_mode = TracingGroupMode.Browser
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    assert not browser._playwright.stub.OpenTraceGroup.called
    assert browser.tracing_contexts == ["context=1"]


def test_registered_context_embeds_its_video(browser: Browser, caplog):
    caplog.set_level("INFO")
    options = browser.adopted_context_options(recordVideo={}, viewport=VIEWPORT)
    video = str(Path(options["recordVideo"]["dir"], "page.webm"))

    video_path = browser.register_adopted_context("context=1", options, video)

    assert video_path == video
    assert (
        '<video width="800" height="600" controls>'
        '<source src="browser/video/page.webm" type="video/webm"></video>'
    ) in caplog.text


def test_video_path_without_record_video_is_ignored(browser: Browser):
    options = browser.adopted_context_options()

    video_path = browser.register_adopted_context("context=1", options, "page.webm")

    assert video_path == ""


def test_relative_har_path_is_relative_to_the_output_directory(
    browser: Browser, tmpdir
):
    options = browser.adopted_context_options(
        recordHar={"path": "har/app.har", "omitContent": True}
    )

    assert options["recordHar"] == {
        "path": str(Path(tmpdir, "har", "app.har").resolve()),
        "omitContent": True,
    }


def test_absolute_har_path_is_kept(browser: Browser, tmpdir):
    har = str(Path(tmpdir, "elsewhere", "app.har").resolve())

    options = browser.adopted_context_options(recordHar={"path": har})

    assert options["recordHar"] == {"path": har}


def test_new_context_resolves_a_relative_har_path(browser: Browser, tmpdir):
    browser.new_context(recordHar={"path": "context.har"})

    options = sent_options(browser._playwright.stub.NewContext)
    assert options["recordHar"] == {"path": str(Path(tmpdir, "context.har").resolve())}


def test_new_persistent_context_resolves_a_relative_har_path(browser: Browser, tmpdir):
    browser.new_persistent_context(recordHar={"path": "persistent.har"})

    options = sent_options(browser._playwright.stub.NewPersistentContext)
    assert options["recordHar"] == {
        "path": str(Path(tmpdir, "persistent.har").resolve())
    }


def test_new_context_sends_frame_rate_and_action_annotations(browser: Browser):
    show_actions = {
        "duration": 300,
        "position": "bottom-left",
        "cursor": "none",
        "style": {"title": "font-size: 32px"},
    }

    browser.new_context(recordVideo={"fps": 10, "showActions": show_actions})

    options = sent_options(browser._playwright.stub.NewContext)
    assert options["recordVideo"]["fps"] == 10
    assert options["recordVideo"]["showActions"] == show_actions


def test_new_persistent_context_sends_action_annotations(browser: Browser):
    browser.new_persistent_context(recordVideo={"showActions": {"position": "top"}})

    options = sent_options(browser._playwright.stub.NewPersistentContext)
    assert options["recordVideo"]["showActions"] == {"position": "top"}


def persistent_context_with_video(browser: Browser) -> MagicMock:
    stub = browser._playwright.stub
    stub.NewPersistentContext.return_value = MagicMock(
        id="context=1",
        browserId="browser=1",
        contextOptions="{}",
        video=json.dumps({"video_path": "page.webm", "contextUuid": "context=1"}),
    )
    return stub


def test_new_persistent_context_caches_and_embeds_its_video_once_its_url_opened(
    browser: Browser, caplog
):
    caplog.set_level("INFO")
    persistent_context_with_video(browser)

    browser.new_persistent_context(url="http://localhost:1", recordVideo={})

    assert browser._playwright_state.context_cache.get("context=1") == {
        "width": 1280,
        "height": 720,
    }
    assert "<video" in caplog.text


def test_new_persistent_context_is_traced_before_its_url_opens(browser: Browser):
    browser.keyword_call_stack.append(keyword_call("New Persistent Context"))
    stub = persistent_context_with_video(browser)
    stub.GoTo.side_effect = RuntimeError("net::ERR_CONNECTION_REFUSED")

    with pytest.raises(RuntimeError):
        browser.new_persistent_context(url="http://localhost:1", tracing=True)

    assert stub.OpenTraceGroup.call_args.args[0].contextId == "context=1"


def test_new_persistent_context_is_not_cached_when_its_url_fails_to_open(
    browser: Browser, caplog
):
    caplog.set_level("INFO")
    stub = persistent_context_with_video(browser)
    stub.GoTo.side_effect = RuntimeError("net::ERR_CONNECTION_REFUSED")

    with pytest.raises(RuntimeError, match="ERR_CONNECTION_REFUSED"):
        browser.new_persistent_context(url="http://localhost:1", recordVideo={})

    assert browser._playwright_state.context_cache.get("context=1") is None
    assert "<video" not in caplog.text


def test_new_context_with_empty_video_options_records_into_the_video_folder(
    browser: Browser,
):
    browser.new_context(recordVideo={})

    options = sent_options(browser._playwright.stub.NewContext)
    assert options["recordVideo"] == {
        "dir": str(browser.video_output.resolve()),
        "size": {"width": 1280, "height": 720},
    }


def test_adopted_recording_options_match_what_new_context_sends(browser: Browser):
    record_video = {"dir": "clips", "fps": 10}
    record_har = {"path": "app.har"}
    viewport = {"width": 800, "height": 600}

    adopted = browser.adopted_context_options(
        recordVideo=record_video, recordHar=record_har, viewport=viewport
    )
    browser.new_context(
        recordVideo=record_video, recordHar=record_har, viewport=viewport
    )

    sent = sent_options(browser._playwright.stub.NewContext)
    assert adopted["recordVideo"] == sent["recordVideo"]
    assert adopted["recordHar"] == sent["recordHar"]


def test_adopted_trace_file_matches_what_new_context_sends(browser: Browser):
    adopted = browser.adopted_context_options(tracing=Path("app.zip"))
    browser.new_context(tracing=Path("app.zip"))

    assert (
        adopted["tracing"]
        == sent_request(browser._playwright.stub.NewContext).traceFile
    )


@pytest.mark.parametrize(
    ("record_video", "video_size"), VIDEO_SIZES, ids=["viewport", "size"]
)
def test_new_context_caches_its_video_size(
    browser: Browser, record_video: dict, video_size: dict
):
    browser._playwright.stub.NewContext.return_value = MagicMock(
        id="context=1", contextOptions="{}"
    )

    browser.new_context(recordVideo=record_video, viewport=VIEWPORT)

    assert browser._playwright_state.context_cache.get("context=1") == video_size


@pytest.mark.parametrize(
    ("record_video", "video_size"), VIDEO_SIZES, ids=["viewport", "size"]
)
def test_new_persistent_context_caches_its_video_size(
    browser: Browser, record_video: dict, video_size: dict
):
    persistent_context_with_video(browser)

    browser.new_persistent_context(recordVideo=record_video, viewport=VIEWPORT)

    assert browser._playwright_state.context_cache.get("context=1") == video_size


@pytest.mark.parametrize(
    ("record_video", "video_size"), VIDEO_SIZES, ids=["viewport", "size"]
)
def test_registered_context_caches_its_video_size(
    browser: Browser, record_video: dict, video_size: dict
):
    options = browser.adopted_context_options(
        recordVideo=record_video, viewport=VIEWPORT
    )

    browser.register_adopted_context("context=1", options, "page.webm")

    assert browser._playwright_state.context_cache.get("context=1") == video_size


def test_context_without_video_caches_no_video_size(browser: Browser):
    stub = browser._playwright.stub
    stub.NewContext.return_value = MagicMock(id="context=1", contextOptions="{}")
    stub.NewPersistentContext.return_value.id = "context=2"

    browser.new_context(viewport=VIEWPORT)
    browser.new_persistent_context(viewport=VIEWPORT)
    browser.register_adopted_context("context=3", browser.adopted_context_options())

    cache = browser._playwright_state.context_cache
    assert [cache.get(f"context={n}") for n in (1, 2, 3)] == [None, None, None]
