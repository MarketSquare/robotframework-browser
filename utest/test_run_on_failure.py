import pytest

import Browser


@pytest.fixture(scope="module")
def browser():
    return Browser.Browser()


def test_external_keyword(browser: Browser.Browser):
    keyword = browser._parse_run_on_failure_keyword("Kala")
    assert keyword.name == "Kala"
    assert keyword.original_name == "Kala"
    assert keyword.args == tuple()
    keyword = browser._parse_run_on_failure_keyword("Kala  arg1  arg2")
    assert keyword.name == "Kala"
    assert keyword.original_name == "Kala"
    assert keyword.args == ("arg1", "arg2")
    assert keyword.kwargs == {}


def test_no_keyword(browser: Browser.Browser):
    keyword = browser._parse_run_on_failure_keyword("nOnE")
    assert keyword.name is None
    assert keyword.args == tuple()
    keyword = browser._parse_run_on_failure_keyword(None)
    assert keyword.name is None
    assert keyword.args == tuple()
    assert keyword.kwargs == {}


def test_library_keyword(browser: Browser.Browser):
    keyword = browser._parse_run_on_failure_keyword("Take Screenshot")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args is tuple()
    assert keyword.kwargs == {}
    keyword = browser._parse_run_on_failure_keyword("tAke sCreenshot  filename.png  //button  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "tAke sCreenshot"
    assert keyword.args == ("filename.png", "//button")
    assert keyword.kwargs == {'fullPage': True}
    keyword = browser._parse_run_on_failure_keyword("tAke sCreenshot  filename.png  //button  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "tAke sCreenshot"
    assert keyword.args == ("filename.png", "//button")
    assert keyword.kwargs == {'fullPage': True}


def test_library_keyword_with_named_args(browser: Browser.Browser):
    keyword = browser._parse_run_on_failure_keyword("Take Screenshot  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == tuple()
    assert keyword.kwargs == {"fullPage": True}
    keyword = browser._parse_run_on_failure_keyword("Take Screenshot  filename=image  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == tuple()
    assert keyword.kwargs == {"filename": "image", "fullPage": True}
    keyword = browser._parse_run_on_failure_keyword("Take Screenshot  image-{index}  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == ("image-{index}", )
    assert keyword.kwargs == {"fullPage": True}
