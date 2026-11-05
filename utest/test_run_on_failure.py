import sys
from pathlib import Path

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
    keyword = browser._parse_run_on_failure_keyword(
        "tAke sCreenshot  filename.png  //button  fullPage=True"
    )
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "tAke sCreenshot"
    assert keyword.args == ("filename.png", "//button")
    assert keyword.kwargs == {"fullPage": True}
    keyword = browser._parse_run_on_failure_keyword(
        "tAke sCreenshot  filename.png  //button  fullPage=True"
    )
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "tAke sCreenshot"
    assert keyword.args == ("filename.png", "//button")
    assert keyword.kwargs == {"fullPage": True}


def test_library_keyword_with_named_args(browser: Browser.Browser):
    keyword = browser._parse_run_on_failure_keyword("Take Screenshot  fullPage=True")
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == tuple()
    assert keyword.kwargs == {"fullPage": True}
    keyword = browser._parse_run_on_failure_keyword(
        "Take Screenshot  filename=image  fullPage=True"
    )
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == tuple()
    assert keyword.kwargs == {"filename": "image", "fullPage": True}
    keyword = browser._parse_run_on_failure_keyword(
        "Take Screenshot  image-{index}  fullPage=True"
    )
    assert keyword.name == "take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == ("image-{index}",)
    assert keyword.kwargs == {"fullPage": True}


@pytest.fixture(scope="module")
def translated_browser():
    sys.path.append(str(Path(__file__).parent.absolute()))
    return Browser.Browser(language="ENG")


def test_english_library_keyword_with_translation(translated_browser: Browser.Browser):
    keyword = translated_browser._parse_run_on_failure_keyword(
        "Take Screenshot  fail-screenshot-{index}"
    )
    assert keyword.name == "1_take_screenshot"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == ("fail-screenshot-{index}",)


def test_translated_library_keyword(translated_browser: Browser.Browser):
    keyword = translated_browser._parse_run_on_failure_keyword("1 Take Screenshot")
    assert keyword.name == "1_take_screenshot"
    assert keyword.args == ()


def test_translated_screenshot_gets_failure_filename(
    translated_browser: Browser.Browser, monkeypatch
):
    calls = []

    def take_screenshot(*args, **kwargs):
        calls.append(args)

    monkeypatch.setitem(
        translated_browser.keywords, "1_take_screenshot", take_screenshot
    )
    monkeypatch.setattr(
        translated_browser, "_failure_screenshot_path", lambda: "failure.png"
    )
    monkeypatch.setattr(translated_browser, "_playwright_log", None)
    translated_browser.scope_stack["run_on_failure"].set(
        translated_browser._parse_run_on_failure_keyword("1 Take Screenshot")
    )
    translated_browser.keyword_error(None)
    assert calls == [("failure.png",)]
