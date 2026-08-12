import pkgutil
import sys
import zipfile
from pathlib import Path

import pytest

from Browser import Browser


@pytest.fixture
def browser() -> Browser:
    sys.path.append(str(Path(__file__).parent.absolute()))
    return Browser(language="ENG")


class UnlistableImporter:
    """Importer that cannot enumerate its modules, like a stale zip importer."""

    def __init__(self, path: str):
        self.path = path

    def find_spec(self, fullname, target=None):
        return None

    def iter_modules(self, prefix=""):
        raise KeyError(self.path)


@pytest.fixture
def unlistable_path_entry(tmp_path):
    """Put an importer that raises when listed first on ``sys.path``."""
    entry = str(tmp_path / "unlistable")

    def hook(path):
        if path == entry:
            return UnlistableImporter(path)
        raise ImportError(path)

    sys.path_hooks.insert(0, hook)
    sys.path.insert(0, entry)
    try:
        yield entry
    finally:
        sys.path.remove(entry)
        sys.path_hooks.remove(hook)
        sys.path_importer_cache.pop(entry, None)


def test_no_translation(browser: Browser):
    assert browser._get_translation(None) is None
    assert browser._get_translation(False) is None


def test_provide_translation_as_not_list(browser: Browser):
    received_path = browser._get_translation("fi")
    assert received_path is None, received_path


def test_provide_translation_as_list(browser: Browser):
    lang_plugin = "robotframework_browser_translation_as_list"
    file_path = Path(__file__).parent / lang_plugin / "translate_2.json"
    received_path = browser._get_translation("swe")
    assert received_path == file_path, received_path
    assert browser._get_translation("wrong") is None
    received_path = browser._get_translation("Eng")
    file_path = Path(__file__).parent / lang_plugin / "translate_1.json"
    assert received_path == file_path, received_path


def test_translated_kw_and_docs(browser: Browser):
    spec = browser.keywords_spec["__init__"]
    assert spec.argument_specification
    doc: str = spec.documentation
    assert doc.startswith("1 Browser library can be taken into")

    doc = browser.get_keyword_documentation("__intro__")
    assert doc.startswith("1 Browser library is a browser automation library")

    spec = browser.keywords_spec["1_session_storage_set_item"]
    assert spec.argument_specification
    doc: str = spec.documentation
    assert doc.startswith("1 Save data to session storage")

    spec = browser.keywords_spec["1_cancel_download"]
    assert spec.argument_specification
    doc: str = spec.documentation
    assert doc.startswith("1 Cancels an active download.")


def test_an_importer_that_cannot_be_listed_does_not_hide_translations(
    browser: Browser, unlistable_path_entry
):
    assert pkgutil.get_importer(unlistable_path_entry) is not None
    with pytest.raises(KeyError):
        list(pkgutil.iter_modules())
    lang_plugin = "robotframework_browser_translation_as_list"
    file_path = Path(__file__).parent / lang_plugin / "translate_2.json"
    assert browser._get_translation("swe") == file_path


def test_a_stale_zip_importer_does_not_hide_translations(browser: Browser, tmp_path):
    """A Windows console script such as ``robot.exe`` is a zip archive on sys.path.

    ``pkgutil`` reads ``zipimport``'s private directory cache, so on Python 3.13 and
    newer an invalidated entry makes ``pkgutil.iter_modules()`` raise ``KeyError``.
    """
    archive = tmp_path / "console_script.exe"
    with zipfile.ZipFile(archive, "w") as zip_file:
        zip_file.writestr("__main__.py", "")
    sys.path.insert(0, str(archive))
    try:
        pkgutil.get_importer(str(archive)).invalidate_caches()
        lang_plugin = "robotframework_browser_translation_as_list"
        file_path = Path(__file__).parent / lang_plugin / "translate_2.json"
        assert browser._get_translation("swe") == file_path
    finally:
        sys.path.remove(str(archive))
        sys.path_importer_cache.pop(str(archive), None)


def test_no_translation():
    browser = Browser(language=None)
    spec = browser.keywords_spec["cancel_download"]
    assert spec.argument_specification
    doc: str = spec.documentation
    assert doc.startswith("Cancels an active download.")
