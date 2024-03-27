import importlib
from pathlib import Path
import pkgutil
import sys
import pytest

from Browser import Browser


@pytest.fixture()
def browser() -> Browser:
    sys.path.append(str(Path(__file__).parent.absolute()))
    return Browser(language="FI")


def test_no_translation(browser: Browser):
    assert browser._get_translation(None) is None
    assert browser._get_translation(False) is None

def test_prodide_translation(browser: Browser):
    lang_plugin = "robotframework_browser_translation_fi"
    file_path = Path(__file__).parent / lang_plugin / "translate.json"
    assert browser._get_translation("fi") == file_path
    assert browser._get_translation("wrong") is None

def test_translated_kw_and_docs(browser: Browser):
    spec = browser.keywords_spec["__init__"]
    assert spec.argument_specification
    doc: str =  spec.documentation
    assert doc.startswith("1 Browser library can be taken into")

    doc = browser.get_keyword_documentation("__intro__")
    assert doc.startswith("1 Browser library is a browser automation library")

    spec = browser.keywords_spec["1_session_storage_set_item"]
    assert spec.argument_specification
    doc: str =  spec.documentation
    assert doc.startswith("1 Save data to session storage")

    spec = browser.keywords_spec["1_cancel_download"]
    assert spec.argument_specification
    doc: str =  spec.documentation
    assert doc.startswith("1 Cancels an active download.")


def test_no_translation():
    browser = Browser(language=None)
    spec = browser.keywords_spec["cancel_download"]
    assert spec.argument_specification
    doc: str =  spec.documentation
    assert doc.startswith("Cancels an active download.")
