import pytest

import Browser.playwright
from Browser.playwright import Playwright, grpc_channel_options, is_local_host

NO_PROXY = (("grpc.enable_http_proxy", 0),)


@pytest.mark.parametrize(
    "host",
    [
        None,
        "",
        "localhost",
        "LocalHost",
        "test.localhost",
        "127.0.0.1",
        "127.0.1.2",
        "::1",
        "[::1]",
        "0.0.0.0",
    ],
)
def test_local_host_disables_the_http_proxy(host):
    assert is_local_host(host) is True
    assert grpc_channel_options(host) == NO_PROXY


@pytest.mark.parametrize(
    "host",
    [
        "playwright.example.com",
        "10.0.0.5",
        "192.168.1.10",
        "2001:db8::1",
        "[2001:db8::1]",
    ],
)
def test_remote_host_keeps_the_default_options(host):
    assert is_local_host(host) is False
    assert grpc_channel_options(host) == ()


class ChannelSpy:
    def __init__(self):
        self.calls = []

    def __call__(self, target, options=None):
        self.calls.append((target, options))
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class HealthyStub:
    def __init__(self, channel):
        pass

    def Health(self, request):  # noqa: N802
        return "healthy"


@pytest.fixture
def channel_spy(monkeypatch):
    spy = ChannelSpy()
    monkeypatch.setattr(Browser.playwright.grpc, "insecure_channel", spy)
    return spy


def _playwright(host, port="12345"):
    playwright = object.__new__(Playwright)
    playwright.host = host
    playwright.port = port
    return playwright


def test_channel_disables_the_proxy_for_the_local_process(channel_spy):
    _playwright("127.0.0.1")._channel
    assert channel_spy.calls == [("127.0.0.1:12345", NO_PROXY)]


def test_channel_keeps_the_default_options_for_a_remote_process(channel_spy):
    _playwright("playwright.example.com")._channel
    assert channel_spy.calls == [("playwright.example.com:12345", ())]


def test_wait_until_server_up_disables_the_proxy_for_the_local_process(
    channel_spy, monkeypatch
):
    monkeypatch.setattr(
        Browser.playwright.playwright_pb2_grpc, "PlaywrightStub", HealthyStub
    )
    _playwright("localhost").wait_until_server_up()
    assert channel_spy.calls == [("localhost:12345", NO_PROXY)]
