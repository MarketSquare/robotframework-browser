from unittest.mock import MagicMock

import grpc  # type: ignore
import pytest

import Browser.playwright
from Browser import Browser as BrowserLibrary


class TimeoutRpcError(grpc.RpcError):
    def __init__(self, trailing_metadata):
        self._trailing_metadata = trailing_metadata

    def details(self):
        return "TimeoutError: page.goto: Timeout 1000ms exceeded."

    def trailing_metadata(self):
        return self._trailing_metadata


@pytest.fixture
def playwright():
    playwright = BrowserLibrary().playwright
    playwright.__dict__["_playwright_process"] = None
    playwright.__dict__["_channel"] = MagicMock()
    return playwright


@pytest.fixture
def info_log(monkeypatch) -> list:
    messages: list = []
    monkeypatch.setattr(Browser.playwright.logger, "info", messages.append)
    return messages


def fail_in_channel(playwright, error, original_error=False):
    with playwright.grpc_channel(original_error=original_error):
        raise error


def test_load_report_is_logged_and_the_timeout_is_raised(playwright, info_log):
    report = (
        "Load report of the page when the wait timed out:\nURL: http://localhost/ä.html"
    )
    error = TimeoutRpcError((("load-report-bin", report.encode("utf-8")),))

    with pytest.raises(AssertionError) as raised:
        fail_in_channel(playwright, error)

    assert info_log == [report]
    assert str(raised.value) == "TimeoutError: page.goto: Timeout 1000ms exceeded."


def test_load_report_is_logged_when_the_original_error_is_wanted(playwright, info_log):
    error = TimeoutRpcError((("load-report-bin", b"Load report"),))

    with pytest.raises(TimeoutRpcError):
        fail_in_channel(playwright, error, original_error=True)

    assert info_log == ["Load report"]


@pytest.mark.parametrize("trailing_metadata", [None, (), (("other-key", "value"),)])
def test_nothing_is_logged_without_a_load_report(
    playwright, info_log, trailing_metadata
):
    with pytest.raises(AssertionError):
        fail_in_channel(playwright, TimeoutRpcError(trailing_metadata))

    assert info_log == []


def test_an_rpc_error_without_trailing_metadata_is_raised_as_before(
    playwright, info_log
):
    class BareRpcError(grpc.RpcError):
        def details(self):
            return "Connection lost"

    with pytest.raises(AssertionError, match="Connection lost"):
        fail_in_channel(playwright, BareRpcError())

    assert info_log == []
