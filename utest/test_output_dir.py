from pathlib import Path

import Browser
from Browser.playwright import Playwright
from Browser.utils import PlaywrightLogTypes


def test_output_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(Browser.Browser, "_output_dir", ".")
    browser = Browser.Browser()
    assert browser.outputdir == str(Path.cwd())
    assert Path(browser.outputdir).is_absolute()
    browser.outputdir = "/foo/bar"
    assert browser.outputdir == "/foo/bar"
    monkeypatch.setattr(Browser.Browser, "_output_dir", str(tmp_path))
    assert Browser.Browser().outputdir == str(tmp_path)


def test_default_output_paths_stay_in_construction_cwd(monkeypatch, tmp_path):
    caller_cwd = (tmp_path / "caller").resolve()
    other_cwd = (tmp_path / "other").resolve()
    caller_cwd.mkdir()
    other_cwd.mkdir()
    monkeypatch.setattr(Browser.Browser, "_output_dir", ".")
    monkeypatch.chdir(caller_cwd)
    browser = Browser.Browser()
    monkeypatch.chdir(other_cwd)

    assert Browser.Browser._output_dir == "."
    assert browser.outputdir == str(caller_cwd)
    assert browser.screenshots_output == caller_cwd / "browser" / "screenshot"
    assert browser.traces_output == caller_cwd / "browser" / "traces"
    assert browser.traces_temp == caller_cwd / "browser" / "traces" / "temp"
    assert Path(browser.adopted_context_options()["tracesDir"]).parent == (
        caller_cwd / "browser" / "traces" / "temp"
    )
    assert browser._browser_control._get_screenshot_path(
        "robotframework-browser-screenshot-{index}", "png"
    ) == (caller_cwd / "browser" / "screenshot" / "robotframework-browser-screenshot-1")


def test_playwright_log_creates_missing_output_dir(tmp_path):
    log_file = tmp_path / "missing" / "playwright-log.txt"
    playwright = Playwright(
        Browser.Browser(), PlaywrightLogTypes.library, playwright_log=log_file
    )
    playwright._get_logfile().close()
    assert log_file.is_file()
