import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, PropertyMock

import pytest


@pytest.fixture()
def browser():
    import Browser
    return Browser.Browser()


@pytest.mark.skipif(sys.platform == "win32", reason="Cleanup does not work in Windows")
def test_cleanup_browser_folder_no_folder(browser):
    with tempfile.TemporaryDirectory() as tmp_dir:
        browser_folder = Path(tmp_dir) / "browser"
        assert not browser_folder.is_dir()
        browser_folder.mkdir()
        with patch("Browser.Browser.outputdir", new_callable=PropertyMock) as mock_property:
            mock_property.return_value = tmp_dir
            browser._start_suite(None, None)
            assert not browser_folder.is_dir()


@pytest.mark.skipif(sys.platform == "win32", reason="Cleanup does not work in Windows")
def test_cleanup_browser_folder_folder(browser):
    with tempfile.TemporaryDirectory() as tmp_dir:
        browser_folder = Path(tmp_dir) / "browser"
        assert not browser_folder.is_dir()
        with patch("Browser.Browser.outputdir", new_callable=PropertyMock) as mock_property:
            mock_property.return_value = tmp_dir
            browser._start_suite(None, None)
            assert not browser_folder.is_dir()
            browser_folder.mkdir()
            browser._start_suite(None, None)
            assert browser_folder.is_dir()
