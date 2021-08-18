import Browser


def test_separate_playwright_port():
    browser = Browser.Browser()
    browser.new_page("https://youtube.com")

    browser2 = Browser.Browser()
    browser2.new_page("https://google.com")
    assert browser.playwright.port != browser2.playwright.port

    assert browser2.get_browser_catalog() != browser.get_browser_catalog()

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


def test_shared_playwright_port():
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

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


# @pytest.fixture()
# def browser():
#     import Browser
#
#     browser = Browser.Browser()
#     yield browser
#     browser.close_browser("ALL")
