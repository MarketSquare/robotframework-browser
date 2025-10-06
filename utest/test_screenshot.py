import os
import subprocess
import uuid

import pytest

import Browser


@pytest.fixture
def application_server():
    process = subprocess.Popen(
        ["node", "./node/dynamic-test-app/dist/server.js", "-p", "7272"]
    )
    yield
    process.terminate()


@pytest.fixture
def browser(tmpdir):
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser(highlight_on_failure=True)
    yield browser
    browser.close_browser("ALL")


def test_take_screenshot(application_server, browser):
    browser.new_page("localhost:7272/dist/")
    screenshot_path = browser.take_screenshot(rf"screenshot-{uuid.uuid4()}")
    assert os.path.exists(screenshot_path)
    screenshot_path = browser.take_screenshot()
    assert os.path.exists(screenshot_path)
