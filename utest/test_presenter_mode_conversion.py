from datetime import timedelta

import pytest
from approvaltests.approvals import verify  # type: ignore

from Browser.base.librarycomponent import LibraryComponent
from Browser.browser import Browser


@pytest.fixture
def browser():
    return Browser()


def test_presenter_mode_default(browser: Browser):
    browser.presenter_mode = {}
    verify(browser.presenter_mode)


def test_presenter_mode_duration_as_string(browser: Browser):
    browser.presenter_mode = {"color": "white", "duration": "4s"}
    verify(browser.presenter_mode)


def test_get_presenter_mode_duration_as_string(browser: Browser):
    browser.presenter_mode = {"color": "white", "duration": "4s"}
    ctx = LibraryComponent(browser)
    verify(ctx.get_presenter_mode)


def test_presenter_mode_duration_as_timedelta(browser: Browser):
    browser.presenter_mode = {"color": "black", "duration": timedelta(seconds=5)}
    verify(browser.presenter_mode)


def test_presenter_mode_with_boolean_true(browser: Browser):
    browser.presenter_mode = True
    verify(browser.presenter_mode)


def test_presenter_mode_with_boolean_false(browser: Browser):
    browser.presenter_mode = False
    ctx = LibraryComponent(browser)
    verify(ctx.get_presenter_mode)


def test_enable_presenter_mode_with_empty_dict():
    lib = Browser(enable_presenter_mode={})
    verify(lib.presenter_mode)


def test_enable_presenter_mode_with_partial_dict():
    lib = Browser(enable_presenter_mode={"color": "yellow", "duration": "30s"})
    verify(lib.presenter_mode)


def test_invalid_presenter_mode_type(browser: Browser):
    with pytest.raises(
        ValueError,
        match=r"'Presenter Mode' got value \"\{'color': 'white'\" \(str\) that cannot be converted to HighLightElement or boolean.",
    ):
        browser.presenter_mode = "{'color': 'white'"  # type: ignore
    with pytest.raises(
        ValueError,
        match=r"'Presenter Mode' got value 123 \(int\) that cannot be converted to HighLightElement or boolean.",
    ):
        browser.presenter_mode = 123  # type: ignore
