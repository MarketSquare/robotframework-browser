import threading
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from Browser import Browser


@pytest.fixture
def browser() -> Browser:
    return Browser()


@pytest.fixture
def events(browser: Browser, monkeypatch) -> list:
    events: list = []
    monkeypatch.setattr(
        browser._playwright_state,
        "_remove_failed_page",
        lambda token: events.append(f"remove {token}"),
    )
    return events


def failing_new_page(browser: Browser, events: list, token: str):
    def keyword(*args):
        events.append(f"{token} fails")
        browser._remove_failed_page_after_failure_handling(token)
        raise AssertionError(f"{token} failed")

    return keyword


def test_failed_page_is_removed_after_failure_handling(
    browser: Browser, monkeypatch, events
):
    monkeypatch.setattr(
        browser, "keyword_error", lambda selector: events.append("keyword_error")
    )
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_new_page(browser, events, "page")
    )
    with pytest.raises(AssertionError, match="page failed"):
        browser.run_keyword("new_page", [], {})
    assert events == ["page fails", "keyword_error", "remove page"]


def test_failed_page_is_removed_after_pause_on_failure(
    browser: Browser, monkeypatch, events
):
    browser.pause_on_failure.add("pause")
    monkeypatch.setattr("builtins.input", lambda: events.append("pause"))
    monkeypatch.setattr(browser, "keyword_error", lambda selector: None)
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_new_page(browser, events, "page")
    )
    with pytest.raises(AssertionError):
        browser.run_keyword("new_page", [], {})
    assert events == ["page fails", "pause", "remove page"]


def test_failed_page_is_removed_when_failure_handling_raises(
    browser: Browser, monkeypatch, events
):
    def broken_keyword_error(selector):
        raise RuntimeError("on-failure keyword broke")

    monkeypatch.setattr(browser, "keyword_error", broken_keyword_error)
    monkeypatch.setitem(
        browser.keywords, "new_page", failing_new_page(browser, events, "page")
    )
    with pytest.raises(RuntimeError):
        browser.run_keyword("new_page", [], {})
    assert events == ["page fails", "remove page"]


def test_nested_keyword_removes_only_its_own_failed_page(
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
        browser.keywords, "outer", failing_new_page(browser, events, "outer")
    )
    monkeypatch.setitem(
        browser.keywords, "inner", failing_new_page(browser, events, "inner")
    )
    with pytest.raises(AssertionError, match="outer failed"):
        browser.run_keyword("outer", [], {})
    assert events == [
        "outer fails",
        "inner fails",
        "remove inner",
        "outer keyword_error done",
        "remove outer",
    ]


def test_failed_page_is_removed_immediately_on_python_path(browser: Browser, events):
    browser._remove_failed_page_after_failure_handling("page")
    assert events == ["remove page"]


def test_failed_page_from_a_promise_thread_is_removed_immediately(
    browser: Browser, monkeypatch, events
):
    def keyword_running_while_a_promise_fails(*args):
        promise = threading.Thread(
            target=browser._remove_failed_page_after_failure_handling,
            args=("promised page",),
        )
        promise.start()
        promise.join()
        events.append("keyword done")

    monkeypatch.setitem(
        browser.keywords, "wait_for", keyword_running_while_a_promise_fails
    )
    browser.run_keyword("wait_for", [], {})
    assert events == ["remove promised page", "keyword done"]


def test_failing_removal_is_logged_and_original_error_raised(
    browser: Browser, monkeypatch
):
    removed = []

    def remove_failed_page(token):
        if token == "unreachable":
            raise ConnectionError("connection lost")
        removed.append(token)

    warnings = []
    monkeypatch.setattr("Browser.browser.logger.warn", warnings.append)
    monkeypatch.setattr(browser, "keyword_error", lambda selector: None)
    monkeypatch.setattr(
        browser._playwright_state, "_remove_failed_page", remove_failed_page
    )

    def keyword(*args):
        browser._remove_failed_page_after_failure_handling("page")
        browser._remove_failed_page_after_failure_handling("unreachable")
        raise AssertionError("original")

    monkeypatch.setitem(browser.keywords, "new_page", keyword)
    with pytest.raises(AssertionError, match="original"):
        browser.run_keyword("new_page", [], {})
    assert removed == ["page"]
    assert len(warnings) == 1
    assert "connection lost" in warnings[0]


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
