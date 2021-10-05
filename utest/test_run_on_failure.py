import pytest

import Browser


@pytest.fixture(scope="module")
def browser():
    return Browser.Browser()


def test_external_keyword(browser: Browser.Browser):
    keyword = browser._parse("Tidii")
    assert keyword.name == "tidii"
    assert keyword.args == tuple()
    keyword = browser._parse("Tidii  arg1  arg2")
    assert keyword.name == "tidii"
    assert keyword.args == ("arg1", "arg2")


def test_no_keyword(browser: Browser.Browser):
    keyword = browser._parse("nOnE")
    assert keyword.name is None
    assert keyword.args is None
    keyword = browser._parse(None)
    assert keyword.name is None
    assert keyword.args is None


def test_library_keyword(browser: Browser.Browser):
    keyword = browser._parse("Take Screenshot")
    assert keyword.name == "take_screenshot"
    assert keyword.args is tuple()
    keyword = browser._parse("Take Screenshot  filename.png  //button  True")
    assert keyword.name == "take_screenshot"
    assert keyword.args == ("filename.png",  "//button",  True)