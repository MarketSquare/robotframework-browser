import threading
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from Browser import Browser


@pytest.fixture
def browser() -> Browser:
    return Browser()


@pytest.fixture
def events() -> list:
    return []


def failing_keyword(browser: Browser, events: list, name: str):
    def keyword(*args):
        events.append(f"{name} fails")
        browser.run_after_failure_handling(lambda: events.append(f"{name} cleanup"))
        raise AssertionError(f"{name} failed")

    return keyword


def test_cleanup_runs_after_failure_handling(browser: Browser, monkeypatch, events):
    monkeypatch.setattr(
        browser, "keyword_error", lambda selector: events.append("keyword_error")
    )
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_keyword(browser, events, "new_page")
    )
    with pytest.raises(AssertionError, match="new_page failed"):
        browser.run_keyword("new_page", [], {})
    assert events == ["new_page fails", "keyword_error", "new_page cleanup"]


def test_cleanup_runs_after_pause_on_failure(browser: Browser, monkeypatch, events):
    browser.pause_on_failure.add("pause")
    monkeypatch.setattr("builtins.input", lambda: events.append("pause"))
    monkeypatch.setattr(browser, "keyword_error", lambda selector: None)
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_keyword(browser, events, "new_page")
    )
    with pytest.raises(AssertionError):
        browser.run_keyword("new_page", [], {})
    assert events == ["new_page fails", "pause", "new_page cleanup"]


def test_cleanup_runs_when_failure_handling_raises(
    browser: Browser, monkeypatch, events
):
    def broken_keyword_error(selector):
        raise RuntimeError("on-failure keyword broke")

    monkeypatch.setattr(browser, "keyword_error", broken_keyword_error)
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_keyword(browser, events, "new_page")
    )
    with pytest.raises(RuntimeError):
        browser.run_keyword("new_page", [], {})
    assert events == ["new_page fails", "new_page cleanup"]


def test_nested_keyword_runs_only_its_own_cleanup(
    browser: Browser, monkeypatch, events
):
    def on_failure(selector):
        if events[-1] == "inner fails":
            return
        with pytest.raises(AssertionError):
            browser.run_keyword("inner", [], {})
        events.append("outer keyword_error done")

    monkeypatch.setattr(browser, "keyword_error", on_failure)
    monkeypatch.setitem(
        browser.keywords, "outer", failing_keyword(browser, events, "outer")
    )
    monkeypatch.setitem(
        browser.keywords, "inner", failing_keyword(browser, events, "inner")
    )
    with pytest.raises(AssertionError, match="outer failed"):
        browser.run_keyword("outer", [], {})
    assert events == [
        "outer fails",
        "inner fails",
        "inner cleanup",
        "outer keyword_error done",
        "outer cleanup",
    ]


def test_cleanup_runs_immediately_on_python_path(browser: Browser, events):
    browser.run_after_failure_handling(lambda: events.append("cleanup"))
    assert events == ["cleanup"]


def test_cleanup_from_a_promise_thread_runs_immediately(
    browser: Browser, monkeypatch, events
):
    def keyword_running_while_a_promise_fails(*args):
        promise = threading.Thread(
            target=browser.run_after_failure_handling,
            args=(lambda: events.append("promise cleanup"),),
        )
        promise.start()
        promise.join()
        events.append("keyword done")

    monkeypatch.setitem(
        browser.keywords, "wait_for", keyword_running_while_a_promise_fails
    )
    browser.run_keyword("wait_for", [], {})
    assert events == ["promise cleanup", "keyword done"]


def test_failing_cleanup_is_logged_and_original_error_raised(
    browser: Browser, monkeypatch, events
):
    warnings = []
    monkeypatch.setattr("Browser.browser.logger.warn", warnings.append)
    monkeypatch.setattr(browser, "keyword_error", lambda selector: None)

    def keyword(*args):
        browser.run_after_failure_handling(lambda: events.append("first cleanup"))
        browser.run_after_failure_handling(_raise_connection_error)
        raise AssertionError("original")

    monkeypatch.setitem(browser.keywords, "new_page", keyword)
    with pytest.raises(AssertionError, match="original"):
        browser.run_keyword("new_page", [], {})
    assert events == ["first cleanup"]
    assert len(warnings) == 1
    assert "connection lost" in warnings[0]


def _raise_connection_error():
    raise ConnectionError("connection lost")


@contextmanager
def fake_channel(stub):
    yield stub


def test_failing_new_page_removes_the_failed_page_by_its_token(browser: Browser):
    stub = MagicMock()
    stub.NewPage.side_effect = AssertionError("page.goto: Timeout 5000ms exceeded")
    stub.RemoveFailedPage.return_value = MagicMock(log="")
    browser.playwright.grpc_channel = lambda *args, **kwargs: fake_channel(stub)

    with pytest.raises(AssertionError, match="Timeout"):
        browser.new_page("http://slow")

    token = stub.NewPage.call_args.args[0].failedPageToken
    assert token
    assert stub.RemoveFailedPage.call_args.args[0].token == token


def test_each_new_page_call_gets_its_own_failed_page_token(browser: Browser):
    stub = MagicMock()
    stub.NewPage.side_effect = AssertionError("page.goto: Timeout 5000ms exceeded")
    stub.RemoveFailedPage.return_value = MagicMock(log="")
    browser.playwright.grpc_channel = lambda *args, **kwargs: fake_channel(stub)

    for _ in range(2):
        with pytest.raises(AssertionError):
            browser.new_page("http://slow")

    first, second = (
        call.args[0].failedPageToken for call in stub.NewPage.call_args_list
    )
    assert first != second
