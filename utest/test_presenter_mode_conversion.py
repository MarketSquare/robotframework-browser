from datetime import timedelta
from unittest.mock import PropertyMock

import pytest
from approvaltests.approvals import verify  # type: ignore

from Browser.base.librarycomponent import LibraryComponent
from Browser.browser import Browser


@pytest.fixture
def browser():
    return Browser.Browser()


def test_presenter_mode_default():
    lib = Browser()
    lib.presenter_mode = {}
    verify(lib.presenter_mode)


def test_presenter_mode_duration_as_string():
    lib = Browser()
    lib.presenter_mode = {"color": "white", "duration": "4s"}
    verify(lib.presenter_mode)


def test_get_presenter_mode_duration_as_string():
    lib = Browser()
    lib.presenter_mode = {"color": "white", "duration": "4s"}
    ctx = LibraryComponent(lib)
    verify(ctx.get_presenter_mode)


def test_presenter_mode_duration_as_timedelta():
    lib = Browser()
    duration = timedelta(seconds=5)
    lib.presenter_mode = {"color": "black", "duration": duration}
    verify(lib.presenter_mode)


def test_presenter_mode_with_boolean_true():
    lib = Browser()
    lib.presenter_mode = True
    verify(lib.presenter_mode)


def test_presenter_mode_with_boolean_false():
    lib = Browser()
    lib.presenter_mode = False
    ctx = LibraryComponent(lib)
    verify(ctx.get_presenter_mode)


def test_enable_presenter_mode_with_empty_dict():
    lib = Browser(enable_presenter_mode={})
    verify(lib.presenter_mode)


def test_invalid_presenter_mode_type():
    lib = Browser()
    with pytest.raises(
        ValueError,
        match="Invalid mode! Expected a boolean or HighLightElement dictionary",
    ):
        lib.presenter_mode = "{'color': 'white'"  # type: ignore
    with pytest.raises(
        ValueError,
        match="Invalid mode! Expected a boolean or HighLightElement dictionary",
    ):
        lib.presenter_mode = 123  # type: ignore
