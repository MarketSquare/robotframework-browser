
import pytest
import subprocess

from Browser.assertion_engine import AssertionOperator


@pytest.fixture()
def application_server():
    process = subprocess.Popen(
        ["node", "./node/dynamic-test-app/dist/server.js", "7272"]
    )
    yield
    process.terminate()


@pytest.fixture()
def browser(monkeypatch):
    import Browser

    browser = Browser.Browser()
    yield browser
    browser.close_browser("ALL")


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
