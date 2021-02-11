from Browser.keywords.playwright_state import PlaywrightState


def test_pause_on_failure():
    def whole_lib():
        pass

    whole_lib._pause_on_failure = set()
    whole_lib.playwright = whole_lib
    browser = PlaywrightState(whole_lib)

    def func(*args, **kwargs):
        pass

    browser.new_browser = func
    browser.new_context = func
    browser.new_page = func
    browser.open_browser()
    assert whole_lib._pause_on_failure
