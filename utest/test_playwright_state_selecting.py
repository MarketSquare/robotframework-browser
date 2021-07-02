import pytest

from assertionengine import AssertionOperator


def test_simple_select_and_back():

    import Browser

    browser = Browser.Browser()
    port: Int = browser.playwright.port  # type: ignore

    browser.new_page("https://youtube.com")

    browser2 = Browser.Browser()
    browser2.playwright.port = port  # type: ignore

    browser2.new_page("https://google.com")
    # browser2.close_page()

    assert browser2.get_browser_catalog() != browser.get_browser_catalog()

    playwright_state_list = browser2.playwright.list_playwright_states()

    assert len(playwright_state_list) == 2  # type: ignore
    browser2.playwright.select_playwright_state(playwright_state_list[0])

    assert browser2.get_browser_catalog() == browser.get_browser_catalog()

    browser.close_browser("ALL")


# @pytest.fixture()
# def browser():
#     import Browser
#
#     browser = Browser.Browser()
#     yield browser
#     browser.close_browser("ALL")
