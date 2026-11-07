from types import SimpleNamespace

import pytest

import Browser.playwright
from Browser.playwright import Playwright, PortTakenError


class Channel:
    def __init__(self, target, options=None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class Process:
    def __init__(self, pid, returncode=None):
        self.pid = pid
        self.returncode = returncode

    def poll(self):
        return self.returncode


def _stub_answering(body):
    class Stub:
        def __init__(self, channel):
            pass

        def Health(self, request):  # noqa: N802
            return SimpleNamespace(body=body)

    return Stub


@pytest.fixture
def grpc_fakes(monkeypatch):
    monkeypatch.setattr(Browser.playwright.grpc, "insecure_channel", Channel)

    def answer(body):
        monkeypatch.setattr(
            Browser.playwright.playwright_pb2_grpc,
            "PlaywrightStub",
            _stub_answering(body),
        )

    return answer


def _playwright():
    playwright = object.__new__(Playwright)
    playwright.host = "127.0.0.1"
    playwright.port = "12345"
    return playwright


def test_the_own_process_answering_is_up(grpc_fakes):
    grpc_fakes("OK 42")
    _playwright().wait_until_server_up(Process(42))


def test_another_process_answering_on_the_port_is_reported(grpc_fakes):
    grpc_fakes("OK 7")
    with pytest.raises(PortTakenError, match="12345 .* process 7, not by .* 42"):
        _playwright().wait_until_server_up(Process(42))


def test_a_wrapper_that_does_not_tell_its_pid_is_trusted(grpc_fakes):
    grpc_fakes("OK")
    _playwright().wait_until_server_up(Process(42))


def test_a_process_not_started_here_is_not_checked(grpc_fakes):
    grpc_fakes("OK 7")
    _playwright().wait_until_server_up()


def test_waiting_stops_when_the_own_process_has_exited(monkeypatch):
    def refuse(target, options=None):
        raise AssertionError("no server to connect to")

    monkeypatch.setattr(Browser.playwright.grpc, "insecure_channel", refuse)
    with pytest.raises(RuntimeError, match="exited with code 1"):
        _playwright().wait_until_server_up(Process(42, returncode=1))


def _starting_playwright(monkeypatch, outcomes):
    playwright = _playwright()
    playwright.port = None
    started = []

    def start():
        process = Process(len(started) + 1)
        started.append(process)
        return process

    def wait(process):
        outcome = outcomes[len(started) - 1]
        if outcome is not None:
            raise outcome

    monkeypatch.setattr(playwright, "start_playwright", start)
    monkeypatch.setattr(playwright, "wait_until_server_up", wait)
    monkeypatch.setattr(Browser.playwright, "close_process_tree", lambda process: None)
    monkeypatch.setattr(Browser.playwright.atexit, "register", lambda function: None)
    monkeypatch.setattr(Browser.playwright.platform, "system", lambda: "Linux")
    monkeypatch.setattr(Browser.playwright.time, "sleep", lambda seconds: None)
    return playwright, started


def test_a_taken_port_is_retried_on_a_fresh_port(monkeypatch):
    playwright, started = _starting_playwright(
        monkeypatch, [PortTakenError("taken"), None]
    )
    assert playwright._playwright_process is started[1]


def test_a_port_taken_three_times_in_a_row_fails(monkeypatch):
    taken = PortTakenError("taken")
    playwright, started = _starting_playwright(monkeypatch, [taken, taken, taken])
    with pytest.raises(PortTakenError):
        playwright._playwright_process
    assert len(started) == 3


def test_other_startup_failures_are_not_retried_on_linux(monkeypatch):
    playwright, started = _starting_playwright(
        monkeypatch, [RuntimeError("no node"), None]
    )
    with pytest.raises(RuntimeError, match="no node"):
        playwright._playwright_process
    assert len(started) == 1
