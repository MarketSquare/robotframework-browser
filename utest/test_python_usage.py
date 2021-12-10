import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
from assertionengine import AssertionOperator


@pytest.fixture()
def application_server():
    process = subprocess.Popen(
        ["node", "./node/dynamic-test-app/dist/server.js", "7272"]
    )
    yield
    process.terminate()


@pytest.fixture()
def browser():
    import Browser

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


def test_new_browser_and_close(browser):
    browser.new_browser()
    browser.close_browser()


def test_playwright_exit_handler(atexit_register):
    import Browser

    browser = Browser.Browser()
    try:
        atexit_register.assert_not_called()
        browser.new_browser()
        atexit_register.assert_called_with(browser.playwright.close)
    finally:
        browser.playwright.close()


def test_playwright_double_close():
    import Browser

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
