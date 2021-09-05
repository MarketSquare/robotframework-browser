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


def test_get_strict_mode_with_error(browser: Browser.Browser):
    browser.set_strict_mode(True)
    with pytest.raises(ValueError):
        browser.get_strict_mode("None")  # type: ignore
    with pytest.raises(ValueError):
        browser.get_strict_mode("True")  # type: ignore

