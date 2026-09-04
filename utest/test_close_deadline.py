from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

import Browser
from Browser.keywords.playwright_state import CLOSE_DEADLINE_FLOOR_SECS
from Browser.utils.data_types import Scope


@contextmanager
def grpc_deadline_spy(library):
    """Record the deadline of every closing call, without opening a browser."""
    deadlines = []
    stub = MagicMock()
    for rpc in ("CloseBrowser", "CloseAllBrowsers", "CloseContext"):

        def record(_request, timeout=None, _rpc=rpc, **_kwargs):
            deadlines.append((_rpc, timeout))
            response = MagicMock()
            response.log = ""
            response.body = "browser=1"
            return response

        getattr(stub, rpc).side_effect = record

    @contextmanager
    def channel(*_args, **_kwargs):
        yield stub

    library.playwright.grpc_channel = channel
    yield deadlines


def close_browser(library):
    library.close_browser()


def close_all_browsers(library):
    library.close_browser("ALL")


def close_context(library):
    state = library._playwright_state
    state.switch_context = lambda *args, **kwargs: None
    state.context_cache.remove = lambda *args, **kwargs: None
    state._close_pw_context([{"id": "context=1"}])


CLOSING_KEYWORDS = [close_browser, close_all_browsers, close_context]


@pytest.mark.parametrize("closing_keyword", CLOSING_KEYWORDS)
@pytest.mark.parametrize("browser_timeout", ["1ms", "1s", "10s"])
def test_closing_never_gets_less_than_the_floor(closing_keyword, browser_timeout):
    """A short Browser timeout must not shorten the deadline for closing.

    ``Set Browser Timeout    1ms`` used to leave the closing calls two seconds
    to finish, which a loaded Windows CI machine missed often enough to make
    the suite flaky. See issue #4124 for why the deadline is there at all.
    """
    library = Browser.Browser()
    library.set_browser_timeout(browser_timeout, Scope.Global)
    with grpc_deadline_spy(library) as deadlines:
        closing_keyword(library)
    assert deadlines, f"{closing_keyword.__name__} made no closing call"
    rpc, deadline = deadlines[-1]
    assert deadline == pytest.approx(CLOSE_DEADLINE_FLOOR_SECS), (
        f"{rpc} asked for a {deadline} second deadline with a "
        f"{browser_timeout} Browser timeout"
    )


@pytest.mark.parametrize("closing_keyword", CLOSING_KEYWORDS)
def test_closing_follows_a_long_timeout(closing_keyword):
    """Above the floor the deadline still follows the Browser timeout."""
    library = Browser.Browser()
    library.set_browser_timeout("5 minutes", Scope.Global)
    with grpc_deadline_spy(library) as deadlines:
        closing_keyword(library)
    rpc, deadline = deadlines[-1]
    assert deadline == pytest.approx(600), f"{rpc} asked for {deadline} seconds"
