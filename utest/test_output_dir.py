import Browser
from Browser.playwright import Playwright
from Browser.utils import PlaywrightLogTypes


def test_output_dir():
    browser = Browser.Browser()
    assert browser.outputdir == "."
    browser.outputdir = "/foo/bar"
    assert browser.outputdir == "/foo/bar"


def test_playwright_log_creates_missing_output_dir(tmp_path):
    log_file = tmp_path / "missing" / "playwright-log.txt"
    playwright = Playwright(
        Browser.Browser(), PlaywrightLogTypes.library, playwright_log=log_file
    )
    playwright._get_logfile().close()
    assert log_file.is_file()
