from typing import IO
import pytest
from subprocess import PIPE, run, Popen
from pathlib import Path
import locale

from assertionengine import AssertionOperator


def test_simple_select_and_back():
    with Popen(
        [
            "python",
            str(Path(__file__).parent / "utils" / "create_new_browser_instance.py"),
        ],
        encoding=locale.getpreferredencoding(False),
        stdin=PIPE,
        stdout=PIPE,
    ) as proc:
        assert proc.stdout is not None
        port = proc.stdout.readline()

        import Browser

        browser2 = Browser.Browser()
        browser2.playwright.port = port  # type: ignore

        browser2.new_page("https://google.com")
        # browser2.close_page()

        # assert browser2.get_browser_catalog() != browser.get_browser_catalog()

        playwright_state_list = browser2.playwright.list_playwright_states()  # type: ignore

        assert len(playwright_state_list) == 2  # type: ignore
        browser2.playwright.select_playwright_state(playwright_state_list[0])  # type: ignore

        # assert browser2.get_browser_catalog() == browser.get_browser_catalog()

        # browser.close_browser("ALL")
        proc.communicate("stop", timeout=10)
        proc.kill()


# @pytest.fixture()
# def browser():
#     import Browser
#
#     browser = Browser.Browser()
#     yield browser
#     browser.close_browser("ALL")
