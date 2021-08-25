import pytest

import Browser


@pytest.fixture(scope="module")
def browser():
    return Browser.Browser()


def test_get_strict_mode(browser: Browser.Browser):
    browser.set_strict_mode(True)
    assert browser.get_strict_mode(None) is True
    assert browser.get_strict_mode(True) is True
    assert browser.get_strict_mode(False) is False
    browser.set_strict_mode(False)
    assert browser.get_strict_mode(True) is True
