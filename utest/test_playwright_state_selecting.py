import Browser


def test_behaviour_without_shared_port():
    browser = Browser.Browser()
    browser.new_page("https://youtube.com")

    browser2 = Browser.Browser()
    browser2.new_page("https://google.com")
    assert browser.playwright.port != browser2.playwright.port

    assert browser2.get_browser_catalog() != browser.get_browser_catalog()

    playwright_state_list = browser2.playwright.list_playwright_states()  # type: ignore
    assert len(playwright_state_list) == 1  # type: ignore
    playwright_state_list = browser.playwright.list_playwright_states()  # type: ignore
    assert len(playwright_state_list) == 1  # type: ignore

    browser.close_browser("ALL")


def test_simplest_select_and_back():
    browser = Browser.Browser()
    browser.new_page("https://youtube.com")
    assert browser.playwright.port
    port: str = browser.playwright.port

    browser2 = Browser.Browser()
    browser2.playwright.port = port  # type: ignore
    assert browser.playwright.port == browser2.playwright.port
    browser2.new_page("https://google.com")
    assert browser.playwright.port == browser2.playwright.port

    assert browser2.get_browser_catalog() == browser.get_browser_catalog()

    playwright_state_list = browser2.playwright.list_playwright_states()  # type: ignore
    assert len(playwright_state_list) == 1  # type: ignore

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


# @pytest.fixture()
# def browser():
#     import Browser
#
#     browser = Browser.Browser()
#     yield browser
#     browser.close_browser("ALL")
