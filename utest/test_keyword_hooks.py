import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import Browser.browser as browser_module
from Browser import Browser


TRANSLATION = {
    "fill_secret": {"name": "taeytae_salaisuus", "doc": ""},
    "take_screenshot": {"name": "ota_kuvakaappaus", "doc": ""},
    "get_page_source": {"name": "hae_sivun_laehdekoodi", "doc": ""},
    "get_title": {"name": "hae_otsikko", "doc": ""},
}


@pytest.fixture
def browser() -> Browser:
    return Browser()


@pytest.fixture
def translated_browser(monkeypatch, tmp_path) -> Browser:
    translation_file = tmp_path / "translation.json"
    translation_file.write_text(json.dumps(TRANSLATION), encoding="utf-8")
    monkeypatch.setattr(
        Browser, "_get_translation", staticmethod(lambda language: translation_file)
    )
    return Browser(language="fi")


def test_translated_browser_really_renames_keywords(translated_browser: Browser):
    assert "taeytae_salaisuus" in translated_browser.keywords
    assert "fill_secret" not in translated_browser.keywords


def test_resolve_keyword_function(browser: Browser):
    assert browser._resolve_keyword_function("fill_secret").__name__ == "fill_secret"
    assert browser._resolve_keyword_function("Get BoundingBox").__name__ == (
        "get_boundingbox"
    )
    assert browser._resolve_keyword_function("Log") is None


def test_resolve_keyword_function_with_translation(translated_browser: Browser):
    resolve = translated_browser._resolve_keyword_function
    assert resolve("taeytae_salaisuus").__name__ == "fill_secret"
    assert resolve("ota_kuvakaappaus").__name__ == "take_screenshot"
    assert resolve("fill_secret") is None


@pytest.mark.parametrize(
    ("keyword", "expected"),
    [
        ("fill_secret", True),
        ("type_secret", True),
        ("fill_text", False),
        ("get_title", False),
    ],
)
def test_is_secret_keyword(browser: Browser, keyword: str, expected: bool):
    assert browser._is_secret_keyword(keyword) is expected


def test_is_secret_keyword_with_translation(translated_browser: Browser):
    assert translated_browser._is_secret_keyword("taeytae_salaisuus") is True
    assert translated_browser._is_secret_keyword("hae_otsikko") is False


@pytest.mark.parametrize(
    ("keyword", "expected"),
    [
        ("take_screenshot", True),
        ("get_page_source", True),
        ("get_title", False),
        ("fill_secret", False),
    ],
)
def test_is_banner_muted_keyword(browser: Browser, keyword: str, expected: bool):
    assert browser._is_banner_muted_keyword(keyword) is expected


def test_is_banner_muted_keyword_with_translation(translated_browser: Browser):
    muted = translated_browser._is_banner_muted_keyword
    assert muted("ota_kuvakaappaus") is True
    assert muted("hae_sivun_laehdekoodi") is True
    assert muted("hae_otsikko") is False


def test_banner_content_without_arguments(browser: Browser):
    assert browser._keyword_call_banner_content("get_title", "Get Title", []) == (
        "Get Title"
    )


def test_banner_content_joins_arguments_with_four_spaces(browser: Browser):
    content = browser._keyword_call_banner_content(
        "fill_text", "Fill Text", ["id=name", "Hyvä päivä"]
    )
    assert content == "Fill Text    id=name    Hyvä päivä"


def test_banner_content_keeps_variables_unresolved(browser: Browser):
    content = browser._keyword_call_banner_content(
        "fill_text", "Fill Text", ["id=name", "${GREETING}"]
    )
    assert content == "Fill Text    id=name    ${GREETING}", (
        "resolving variables is the callers job, the pure part must stay testable"
    )


def test_banner_content_masks_positional_secret(browser: Browser):
    content = browser._keyword_call_banner_content(
        "fill_secret", "Fill Secret", ["id=password", "${PASSWORD}"]
    )
    assert content == "Fill Secret    id=password    ***"


def test_banner_content_masks_named_secret(browser: Browser):
    content = browser._keyword_call_banner_content(
        "type_secret",
        "Type Secret",
        ["id=password", "secret=${PASSWORD}", "clear=False"],
    )
    assert content == "Type Secret    id=password    secret=***    clear=False"


def test_banner_content_masks_secret_of_translated_keyword(
    translated_browser: Browser,
):
    content = translated_browser._keyword_call_banner_content(
        "taeytae_salaisuus", "Taeytae Salaisuus", ["id=password", "${PASSWORD}"]
    )
    assert content == "Taeytae Salaisuus    id=password    ***"


def test_banner_content_does_not_mask_a_selector_called_secret(browser: Browser):
    content = browser._keyword_call_banner_content(
        "fill_text", "Fill Text", ["id=secret", "${PASSWORD}"]
    )
    assert content == "Fill Text    id=secret    ${PASSWORD}"


def test_banner_content_masks_secret_given_as_embedded_variable(browser: Browser):
    content = browser._keyword_call_banner_content(
        "fill_secret", "Fill Secret", ["id=password", "prefix-${PASSWORD}-suffix"]
    )
    assert content == "Fill Secret    id=password    ***"


def test_run_keyword_suppresses_logging_around_secret_keywords(
    browser: Browser, monkeypatch
):
    events = []
    monkeypatch.setattr(
        browser, "_set_logging", lambda status: events.append(f"logging={status}")
    )
    monkeypatch.setitem(
        browser.keywords, "fill_secret", lambda *args: events.append("keyword")
    )
    browser.run_keyword("fill_secret", ["id=password", "$PASSWORD"], {})
    assert events == ["logging=False", "keyword", "logging=True"]


def test_run_keyword_restores_logging_when_secret_keyword_fails(
    browser: Browser, monkeypatch
):
    def failing(*args):
        events.append("keyword")
        raise AssertionError("boom")

    events = []
    monkeypatch.setattr(
        browser, "_set_logging", lambda status: events.append(f"logging={status}")
    )
    monkeypatch.setattr(browser, "keyword_error", lambda selector: None)
    monkeypatch.setitem(browser.keywords, "fill_secret", failing)
    with pytest.raises(AssertionError):
        browser.run_keyword("fill_secret", ["id=password", "$PASSWORD"], {})
    assert events == ["logging=False", "keyword", "logging=True"]


def test_run_keyword_does_not_touch_logging_for_other_keywords(
    browser: Browser, monkeypatch
):
    events = []
    monkeypatch.setattr(
        browser, "_set_logging", lambda status: events.append(f"logging={status}")
    )
    monkeypatch.setitem(
        browser.keywords, "get_title", lambda *args: events.append("keyword")
    )
    browser.run_keyword("get_title", [], {})
    assert events == ["keyword"]


def test_nested_secret_keywords_restore_the_original_log_level(
    browser: Browser, monkeypatch
):
    class FakeOutput:
        def __init__(self):
            self.level = "TRACE"

        def set_log_level(self, level):
            previous = self.level
            self.level = level
            return previous

    output = FakeOutput()
    monkeypatch.setattr(
        browser_module,
        "BuiltIn",
        lambda: SimpleNamespace(_context=SimpleNamespace(output=output)),
    )
    browser._set_logging(False)
    assert output.level == "NONE"
    browser._set_logging(False)
    browser._set_logging(True)
    assert output.level == "NONE", "the outer secret keyword is still running"
    browser._set_logging(True)
    assert output.level == "TRACE"


@pytest.fixture
def browser_with_plugin() -> Browser:
    plugin = str(Path(__file__).parent / "KeywordHooksPlugin.py")
    return Browser(plugins=plugin)


def test_plugin_keyword_resolves_to_the_plugin_function(browser_with_plugin: Browser):
    resolve = browser_with_plugin._resolve_keyword_function
    assert resolve("Plugin Login With Credentials").__name__ == (
        "plugin_login_with_credentials"
    )
    assert resolve("plugin_without_secret").__name__ == "plugin_without_secret"


def test_plugin_keyword_with_a_secret_argument_is_detected(
    browser_with_plugin: Browser,
):
    assert browser_with_plugin._is_secret_keyword("Plugin Login With Credentials")
    assert not browser_with_plugin._is_secret_keyword("plugin_without_secret"), (
        "the name carries no hint either way, only the argument specification does"
    )


def test_banner_content_masks_the_secret_of_a_plugin_keyword(
    browser_with_plugin: Browser,
):
    content = browser_with_plugin._keyword_call_banner_content(
        "Plugin Login With Credentials",
        "Plugin Login With Credentials",
        ["css=input#username", "${PASSWORD}"],
    )
    assert content == "Plugin Login With Credentials    css=input#username    ***"


def test_run_keyword_suppresses_logging_around_a_plugin_secret_keyword(
    browser_with_plugin: Browser, monkeypatch
):
    events = []
    monkeypatch.setattr(
        browser_with_plugin,
        "_set_logging",
        lambda status: events.append(f"logging={status}"),
    )
    monkeypatch.setitem(
        browser_with_plugin.keywords,
        "Plugin Login With Credentials",
        lambda *args: events.append("keyword"),
    )
    browser_with_plugin.run_keyword(
        "Plugin Login With Credentials", ["css=input#username", "$PASSWORD"], {}
    )
    assert events == ["logging=False", "keyword", "logging=True"]


def test_secret_arguments_are_found_by_name_and_by_annotation(browser: Browser):
    assert browser._secret_argument_names("fill_secret") == {"secret"}
    assert browser._secret_argument_names("type_secret") == {"secret"}
    assert browser._secret_argument_names("create_credential") == {
        "privateKey",
        "publicKey",
    }
    assert browser._secret_argument_names("fill_text") == set()


def test_create_credential_counts_as_a_secret_keyword(browser: Browser):
    assert browser._is_secret_keyword("create_credential") is True


def test_banner_content_masks_a_secret_typed_argument(browser: Browser):
    content = browser._keyword_call_banner_content(
        "create_credential",
        "Create Credential",
        ["rpId=example.com", "privateKey=${PRIVATE_KEY}"],
    )
    assert content == "Create Credential    rpId=example.com    privateKey=***"


def test_banner_content_masks_every_secret_typed_argument(browser: Browser):
    content = browser._keyword_call_banner_content(
        "create_credential",
        "Create Credential",
        ["example.com", "id", "${PRIVATE_KEY}", "${PUBLIC_KEY}", "handle"],
    )
    assert content == "Create Credential    example.com    id    ***    ***    handle"


def test_plugin_secret_without_a_secret_annotation_is_still_found_by_name(
    browser_with_plugin: Browser,
):
    assert browser_with_plugin._secret_argument_names(
        "Plugin Login With Credentials"
    ) == {"secret"}
