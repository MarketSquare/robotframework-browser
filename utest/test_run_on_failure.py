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


@pytest.fixture(params=["Prendre Une Capture", "Ota Kuvakaappaus"])
def translated_browser(request, monkeypatch, tmp_path):
    import json

    translation = tmp_path / "translation.json"
    translation.write_text(
        json.dumps(
            {
                "take_screenshot": {
                    "name": request.param.lower().replace(" ", "_"),
                    "doc": "",
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        Browser.Browser, "_get_translation", staticmethod(lambda language: translation)
    )
    browser = Browser.Browser(language="translated")
    browser._playwright_log = None
    return browser, request.param


def test_translated_default_failure_keyword(translated_browser):
    browser, translated = translated_browser
    keyword = browser.run_on_failure_keyword
    assert keyword.name in browser.keywords
    assert browser.keywords[keyword.name].__name__ == "take_screenshot"
    assert keyword.args == ("fail-screenshot-{index}",)


@pytest.mark.parametrize("canonical", [True, False])
def test_translated_failure_keyword_parses_named_arguments(
    translated_browser, canonical
):
    browser, translated = translated_browser
    name = "Take Screenshot" if canonical else translated
    keyword = browser._parse_run_on_failure_keyword(f"{name}  fullPage=True")
    assert keyword.name in browser.keywords
    assert browser.keywords[keyword.name].__name__ == "take_screenshot"
    assert keyword.original_name == name
    assert keyword.args == ()
    assert keyword.kwargs == {"fullPage": True}


@pytest.mark.parametrize(
    ("setting", "expected_args", "expected_kwargs"),
    [
        (None, ("fail-screenshot-{index}",), {}),
        ("", ("failure-path",), {}),
        ("  fullPage=True", ("failure-path",), {"fullPage": True}),
        ("  filename=custom", (), {"filename": "custom"}),
    ],
)
def test_translated_screenshot_runs_on_failure(
    translated_browser, monkeypatch, setting, expected_args, expected_kwargs
):
    from functools import wraps

    browser, translated = translated_browser
    if setting is not None:
        browser.scope_stack["run_on_failure"].set(
            browser._parse_run_on_failure_keyword(translated + setting)
        )
    name = browser.run_on_failure_keyword.name
    calls = []

    @wraps(
        next(m for m in browser.keywords.values() if m.__name__ == "take_screenshot")
    )
    def capture(*args, **kwargs):
        calls.append((args, kwargs))

    browser.keywords[name] = capture
    monkeypatch.setattr(browser, "_failure_screenshot_path", lambda: "failure-path")
    browser.keyword_error(None)
    assert calls == [(expected_args, expected_kwargs)]
    assert not browser._running_on_failure_keyword


def test_translated_external_and_disabled_failure_keywords(translated_browser):
    browser, _ = translated_browser
    keyword = browser._parse_run_on_failure_keyword("Custom Failure  value")
    assert keyword.name == "Custom Failure"
    assert keyword.args == ("value",)
    assert browser._parse_run_on_failure_keyword("NONE").name is None


def test_translated_external_failure_keyword_is_delegated(
    translated_browser, monkeypatch
):
    from importlib import import_module
    from unittest.mock import Mock

    browser, _ = translated_browser
    builtin = Mock()
    monkeypatch.setattr(import_module("Browser.browser"), "BuiltIn", lambda: builtin)
    browser.scope_stack["run_on_failure"].set(
        browser._parse_run_on_failure_keyword("Custom Failure  value")
    )
    browser.keyword_error(None)
    builtin.run_keyword.assert_called_once_with("Custom Failure", "value")


def test_translated_disabled_failure_keyword_does_nothing(
    translated_browser, monkeypatch
):
    from importlib import import_module
    from unittest.mock import Mock

    browser, _ = translated_browser
    builtin = Mock()
    monkeypatch.setattr(import_module("Browser.browser"), "BuiltIn", builtin)
    browser.scope_stack["run_on_failure"].set(
        browser._parse_run_on_failure_keyword("NONE")
    )
    browser.keyword_error(None)
    builtin.assert_not_called()
