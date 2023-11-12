import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
from assertionengine import AssertionOperator
import logging

import Browser
from Browser import SupportedBrowsers
from Browser.utils import PlaywrightLogTypes


PW_LOG = "playwright-log.txt"

@pytest.fixture()
def application_server():
    process = subprocess.Popen(
        ["node", "./node/dynamic-test-app/dist/server.js", "7272"]
    )
    yield
    process.terminate()


@pytest.fixture()
def browser(tmpdir):
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser()
    yield browser
    browser.close_browser("ALL")


@pytest.fixture()
def browser_no_log(tmpdir):
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser(enable_playwright_debug=PlaywrightLogTypes.disabled)
    yield browser
    browser.close_browser("ALL")


@pytest.fixture()
def browser_log_exist(tmpdir):
    log_file = Path(tmpdir, PW_LOG)
    log_file.touch()
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser()
    yield browser
    browser.close_browser("ALL")


@pytest.fixture()
def atexit_register(monkeypatch):
    import atexit

    register = Mock()
    monkeypatch.setattr(atexit, "register", register)
    return register


def test_open_page_get_text(application_server, browser):
    browser.new_page("localhost:7272/dist/")
    text = browser.get_text("h1", AssertionOperator["=="], "Login Page")
    assert text == "Login Page"


def test_readme_example(browser):
    browser.new_page("https://playwright.dev")
    assert "Playwright" in browser.get_text("h1")


def test_playwright_log(browser: Browser.Browser, application_server):
    root_folder = Path(browser.outputdir)
    log_file = root_folder / PW_LOG
    assert not log_file.is_file()
    browser.new_page("localhost:7272/dist/")
    assert log_file.is_file()


def test_playwright_log_new_file(browser_log_exist: Browser.Browser, application_server):
    root_folder = Path(browser_log_exist.outputdir)
    browser_log_exist.new_page("localhost:7272/dist/")
    log_files = [file for file in root_folder.iterdir() if file.name.startswith("playwright-log")]
    assert len(log_files) == 2


def test_playwright_log_disabled(browser_no_log: Browser.Browser, application_server):
    root_folder = Path(browser_no_log.outputdir)
    log_file = root_folder / PW_LOG
    assert not log_file.is_file()
    browser_no_log.new_page("localhost:7272/dist/")
    assert not log_file.is_file()

def test_new_browser_and_close(browser):
    browser.new_browser()
    browser.close_browser()


def test_new_browser_with_timeout_of_zero_seconds(browser):
    browser.new_browser(browser=SupportedBrowsers.chromium, headless=True, timeout="0")
    browser.close_browser("ALL")


def test_new_browser_with_default_timeout(browser):
    browser.new_browser(browser=SupportedBrowsers.chromium, headless=True)
    browser.close_browser("ALL")


def test_playwright_exit_handler(atexit_register):
    browser = Browser.Browser()
    try:
        atexit_register.assert_not_called()
        browser.new_browser()
        atexit_register.assert_called_with(browser.playwright.close)
    finally:
        browser.playwright.close()


def test_playwright_double_close():
    browser = Browser.Browser()
    browser.new_browser()
    browser.playwright.close()
    browser.playwright.close()


def test_promise_handling(browser, application_server):
    file = Path(__file__)
    browser.new_page("localhost:7272/dist/")
    browser.promise_to_upload_file(file.resolve())
    browser.click("#file_chooser")
    assert browser.get_text("#upload_result") == "test_python_usage.py"


def test_promise_to_wait_for_response_with_name_arguments(browser):
    browser.new_page()
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(logging.WARNING)
    promise = browser.promise_to("Wait For Response", "matcher=", "timeout=1s")
    # pdb.set_trace()
    browser.go_to(url="https://www.google.com")
    logger.setLevel(old_level)

    assert promise.result() is not None


def test_promise_to_wait_for_alert_with_name_arguments(browser):
    browser.new_page()
    promise = browser.promise_to(
        "Wait For Alert", "action=accept", "prompt_input=Kala", "text=Wrong Text"
    )
    browser.go_to(url="https://www.google.com")
    assert (promise.running() or promise.done()) is True


def test_promise_to_wait_for_elements_state(browser):
    browser.new_page()
    promise = browser.promise_to(
        "Wait For Elements State", "#victim", "hidden", "200ms"
    )
    browser.go_to(url="https://www.google.com")
    assert (promise.running() or promise.done()) is True


def test_promise_to_wait_for_elements_state_with_name_arguments(browser):
    browser.new_page()
    promise = browser.promise_to(
        "Wait For Elements State", 'selector="#victim"', "state=hidden", "timeout=200ms"
    )
    browser.go_to(url="https://www.google.com")
    assert (promise.running() or promise.done()) is True
