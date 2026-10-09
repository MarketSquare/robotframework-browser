from unittest.mock import MagicMock

import pytest

from Browser.keywords.playwright_state import PlaywrightState


@pytest.fixture
def library():
    lib = MagicMock()
    lib._playwright = None
    return lib


@pytest.fixture
def state(library):
    return PlaywrightState(library)


def test_set_rf_context_skips_grpc_when_playwright_not_initialized(state, library):
    library._playwright = None

    state.set_rf_context(test_id="s1-t1", test_name="My Test")

    library.playwright.grpc_channel.assert_not_called()


def test_set_rf_context_calls_grpc_when_playwright_is_initialized(state, library):
    library._playwright = MagicMock()
    stub = MagicMock()
    library.playwright.grpc_channel.return_value.__enter__ = MagicMock(
        return_value=stub
    )
    library.playwright.grpc_channel.return_value.__exit__ = MagicMock(
        return_value=False
    )

    state.set_rf_context(
        test_id="s1-t1", test_name="My Test", suite_id="s1", suite_name="My Suite"
    )

    stub.SetRFContext.assert_called_once()


def test_set_rf_context_passes_empty_strings_for_clear(state, library):
    library._playwright = MagicMock()
    stub = MagicMock()
    library.playwright.grpc_channel.return_value.__enter__ = MagicMock(
        return_value=stub
    )
    library.playwright.grpc_channel.return_value.__exit__ = MagicMock(
        return_value=False
    )

    state.set_rf_context(test_id="", test_name="")

    stub.SetRFContext.assert_called_once()
