import pytest
from subprocess import PIPE, Popen
import threading
import time
from pathlib import Path
import locale


ENCODING = locale.getpreferredencoding()


def test_simple_select_and_back():
    with Popen(
        [
            "python",
            str(Path(__file__).parent / "utils" / "create_new_browser_instance.py"),
        ],
        stdin=PIPE,
        stdout=PIPE,
    ) as proc:
        assert proc.stdout is not None
        assert proc.stdin is not None

        proc.stdout.flush()
        port = proc.stdout.readline().decode(ENCODING)
        time.sleep(2)

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
        proc.stdin.write("stop".encode(ENCODING))
        proc.stdin.close()
        proc.wait(1)
        proc.terminate()


# @pytest.fixture()
# def browser():
#     import Browser
#
#     browser = Browser.Browser()
#     yield browser
#     browser.close_browser("ALL")
