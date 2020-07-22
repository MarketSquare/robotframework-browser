import pytest
from Browser.assertion_engine import AssertionOperator
import robot.api.logger  # type: ignore


def info(msg: str, html=False):
    print(f"Info: {msg}")


def debug(msg: str, html=False):
    print(f"Debug: {msg}")


def warn(msg: str, html=False):
    print(f"Warn: {msg}")


@pytest.fixture()
def browser(monkeypatch):
    monkeypatch.setattr(robot.api.logger, "info", info)
    monkeypatch.setattr(robot.api.logger, "debug", debug)
    monkeypatch.setattr(robot.api.logger, "warn", warn)
    import Browser

    browser = Browser.Browser()
    yield browser
    browser.close_all_browsers()
    browser._close


def test_open_page_get_text(browser):
    browser.new_page("localhost:7272/dist/")
    text = browser.get_text("h1", AssertionOperator["=="], "Login Page")
    assert text == "Login Page"


def test_new_browser_and_close(browser):
    browser.new_browser()
    browser.close_browser()
