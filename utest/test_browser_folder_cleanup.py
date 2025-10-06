import sys
import tempfile
from pathlib import Path
from unittest.mock import PropertyMock, patch

import pytest

import Browser


@pytest.fixture
def browser():
    return Browser.Browser()


@pytest.mark.skipif(sys.platform == "win32", reason="Cleanup does not work in Windows")
def test_cleanup_browser_folder_no_folder(browser):
    Browser._suite_cleanup_done = False
    with tempfile.TemporaryDirectory() as tmp_dir:
        browser_folder = Path(tmp_dir) / "browser"
        assert not browser_folder.is_dir()
        browser_folder.mkdir()
        screenshot = browser_folder / "screenshot"
        screenshot.mkdir()
        video = browser_folder / "video"
        video.mkdir()
        traces = browser_folder / "traces"
        traces.mkdir()
        state = browser_folder / "state"
        state.mkdir()
        foobar = browser_folder / "foobar"
        foobar.mkdir()
        with patch(
            "Browser.Browser.outputdir", new_callable=PropertyMock
        ) as mock_property:
            mock_property.return_value = tmp_dir
            browser._start_suite(None, {"id": "s1"})
            assert browser_folder.is_dir()
            assert not screenshot.is_dir()
            assert not video.is_dir()
            assert not traces.is_dir()
            assert not state.is_dir()
            assert foobar.is_dir()


@pytest.mark.skipif(sys.platform == "win32", reason="Cleanup does not work in Windows")
def test_cleanup_browser_folder_folder(browser):
    with tempfile.TemporaryDirectory() as tmp_dir:
        browser_folder = Path(tmp_dir) / "browser"
        assert not browser_folder.is_dir()
        with patch(
            "Browser.Browser.outputdir", new_callable=PropertyMock
        ) as mock_property:
            mock_property.return_value = tmp_dir
            browser._start_suite(None, {"id": "s1"})
            assert not browser_folder.is_dir()
            browser_folder.mkdir()
            browser._start_suite(None, {"id": "s1"})
            assert browser_folder.is_dir()
