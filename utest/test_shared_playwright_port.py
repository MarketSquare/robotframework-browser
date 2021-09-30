import Browser
import pytest


def test_separate_playwright_port():
    browser = Browser.Browser()
    browser.new_context()

    browser2 = Browser.Browser()
    browser.new_context()
    assert browser.playwright.port != browser2.playwright.port

    assert browser2.get_browser_catalog() != browser.get_browser_catalog()

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


def test_shared_playwright_port():
    browser = Browser.Browser()
    browser.new_context()
    assert browser.playwright.port
    port: str = browser.playwright.port

    browser2 = Browser.Browser(playwright_process_port=int(port))
    # assert browser.playwright.port == browser2.playwright.port
    browser2.new_context()
    assert browser.playwright.port == browser2.playwright.port

    assert browser2.get_browser_catalog() == browser.get_browser_catalog()

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


@pytest.mark.skip(
    reason="This test case does not actually test anything if both browsers are from same python process"
)
def test_forcibly_same_peer_id():
    browser = Browser.Browser()
    browser.set_peer_id("new_id")
    browser.new_page("https://youtube.com")
    catalog_with_only_youtube = browser.get_browser_catalog()
    assert browser.playwright.port
    port: str = browser.playwright.port

    browser2 = Browser.Browser(playwright_process_port=int(port))
    browser2.set_peer_id("new_id")
    # assert browser.playwright.port == browser2.playwright.port
    browser2.new_page("https://google.com")

    assert browser.playwright.port == browser2.playwright.port
    assert browser.get_browser_catalog() == browser2.get_browser_catalog()
    assert browser.get_browser_catalog() != catalog_with_only_youtube

    browser.close_browser("ALL")
    browser2.close_browser("ALL")


@pytest.mark.skip(
    reason="This case is not possible when both libs are started from same process"
)
def test_forcefully_different_peer_id():
    browser = Browser.Browser()
    browser.new_page("https://youtube.com")
    assert browser.playwright.port
    port: str = browser.playwright.port

    browser2 = Browser.Browser(playwright_process_port=int(port))
    assert browser.playwright.port == browser2.playwright.port
    assert browser.get_browser_catalog() == browser2.get_browser_catalog()
    old_id = browser2.set_peer_id("different")
    assert browser2.set_peer_id("different") == "different"
    assert old_id != "different"
    browser2.new_page("https://google.com")

    assert browser.get_browser_catalog() != browser2.get_browser_catalog()

    browser.close_browser("ALL")
    browser2.close_browser("ALL")
