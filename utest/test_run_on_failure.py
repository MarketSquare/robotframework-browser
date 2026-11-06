import json

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


@pytest.fixture
def translated_browser(monkeypatch, tmp_path):
    translation = tmp_path / "translation.json"
    translation.write_text(
        json.dumps({"take_screenshot": {"name": "ota_kuvakaappaus", "doc": ""}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        Browser.Browser, "_get_translation", staticmethod(lambda language: translation)
    )
    browser = Browser.Browser(language="fi")
    browser._playwright_log = tmp_path / "playwright-log.txt"
    return browser


def test_default_keyword_resolves_under_translation(
    translated_browser: Browser.Browser,
):
    keyword = translated_browser.run_on_failure_keyword
    assert keyword.name == "ota_kuvakaappaus"
    assert keyword.original_name == "Take Screenshot"
    assert keyword.args == ("fail-screenshot-{index}",)


@pytest.mark.parametrize("name", ["Take Screenshot", "Ota Kuvakaappaus"])
def test_english_and_translated_names_resolve_under_translation(
    translated_browser: Browser.Browser, name: str
):
    keyword = translated_browser._parse_run_on_failure_keyword(f"{name}  fullPage=True")
    assert keyword.name == "ota_kuvakaappaus"
    assert keyword.original_name == name
    assert keyword.args == ()
    assert keyword.kwargs == {"fullPage": True}


@pytest.mark.parametrize(
    ("registered", "expected_filename"),
    [
        (None, "fail-screenshot-{index}"),
        ("Ota Kuvakaappaus", "_FAILURE_SCREENSHOT_{index}"),
        ("Take Screenshot", "_FAILURE_SCREENSHOT_{index}"),
        ("Ota Kuvakaappaus  filename=custom-{index}", "custom-{index}"),
    ],
)
def test_screenshot_filename_on_failure_under_translation(
    translated_browser: Browser.Browser, monkeypatch, registered, expected_filename
):
    if registered is not None:
        translated_browser.scope_stack["run_on_failure"].set(
            translated_browser._parse_run_on_failure_keyword(registered)
        )
    filenames = []

    def record_filename(filename, file_type):
        filenames.append(filename)
        raise RuntimeError("stop before taking the screenshot")

    monkeypatch.setattr(
        translated_browser._browser_control, "_get_screenshot_path", record_filename
    )
    translated_browser.keyword_error(None)
    assert len(filenames) == 1
    assert filenames[0].endswith(expected_filename)
