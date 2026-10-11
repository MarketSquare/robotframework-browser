from contextlib import contextmanager
from pathlib import Path

from Browser import Browser
from Browser.base.cache import ContextCache


class NoPlaywright:
    """Stands in for the Node process, which these tests do not need."""

    @contextmanager
    def grpc_channel(self):
        yield self


def library(tmpdir, monkeypatch) -> Browser:
    monkeypatch.setattr(Browser, "_output_dir", tmpdir)
    monkeypatch.setattr(Browser, "_context_cache", ContextCache())
    monkeypatch.delenv("ROBOT_FRAMEWORK_BROWSER_TRACING", raising=False)
    browser = Browser()
    browser._playwright = NoPlaywright()
    return browser


def test_no_tracing_and_no_video_by_default(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    assert browser.adopted_context_options() == {"tracing": ""}


def test_tracing_follows_new_context(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    assert browser.adopted_context_options(tracing=True)["tracing"] == str(
        browser.traces_output
    )
    assert browser.adopted_context_options(tracing=Path("trace.zip"))["tracing"] == str(
        Path(tmpdir, "trace.zip").resolve()
    )


def test_tracing_follows_the_global_setting(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    monkeypatch.setenv("ROBOT_FRAMEWORK_BROWSER_TRACING", "True")

    assert browser.adopted_context_options()["tracing"] == str(browser.traces_output)


def test_video_gets_browsers_folder_and_size(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(recordVideo={"showActions": {}})

    assert options["recordVideo"] == {
        "dir": str(browser.video_output.resolve()),
        "size": {"width": 1280, "height": 720},
        "showActions": {},
    }


def test_video_folder_and_size_follow_new_context(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    options = browser.adopted_context_options(
        recordVideo={"dir": "demo", "size": {"width": "800", "height": "600"}}
    )

    assert options["recordVideo"] == {
        "dir": str((browser.video_output / "demo").resolve()),
        "size": {"width": 800, "height": 600},
    }


def test_registering_without_tracing_and_video_changes_nothing(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)

    video_path = browser.register_adopted_context("context=1", {"tracing": ""})

    assert video_path == ""
    assert browser.tracing_contexts == []


def test_registered_context_gets_the_trace_groups(tmpdir, monkeypatch):
    browser = library(tmpdir, monkeypatch)
    options = browser.adopted_context_options(tracing=True)

    browser.register_adopted_context("context=1", options)

    assert browser.tracing_contexts == ["context=1"]


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
    assert browser._playwright_state.context_cache.get("context=1") is None


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

    params = browser._playwright_state._set_har_path(
        {"recordHar": {"path": "context.har"}}
    )

    assert params == {"recordHar": {"path": str(Path(tmpdir, "context.har").resolve())}}
