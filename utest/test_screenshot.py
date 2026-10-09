import os
import uuid

import pytest

import Browser


@pytest.fixture
def browser(tmpdir):
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser(highlight_on_failure=True)
    yield browser
    browser.close_browser("ALL")


def test_take_screenshot(test_app_url, browser):
    browser.new_page(f"{test_app_url}/dist/")
    screenshot_path = browser.take_screenshot(rf"screenshot-{uuid.uuid4()}")
    assert os.path.exists(screenshot_path)
    screenshot_path = browser.take_screenshot()
    assert os.path.exists(screenshot_path)
