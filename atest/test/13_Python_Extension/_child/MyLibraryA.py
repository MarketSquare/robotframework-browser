"""Context A: Robot Framework imports Browser, this library sits alongside it.

Demonstration library for the Browser documentation. It is quoted by path on
robotframework-browser.org, so it deliberately contains no business logic and
nothing that is not part of the example.

See MyLibraryB.py for context B, where the library owns the Browser instance.
"""

import functools

from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


def screenshot_on_failure(keyword):
    """Take a screenshot when the wrapped keyword fails, then re-raise.

    Browser runs its own ``run_on_failure`` from the Robot Framework dynamic
    library API, which is not entered when a keyword is called from Python.
    A small library can get equivalent behaviour with a decorator like this.
    Larger libraries usually intercept in one place instead, either by being a
    dynamic library themselves or by using PythonLibCore.
    """

    @functools.wraps(keyword)
    def wrapper(self, *args, **kwargs):
        try:
            return keyword(self, *args, **kwargs)
        except Exception:
            self.browser.take_screenshot("my-library-failure-{index}")
            raise

    return wrapper


class MyLibraryA:
    """Business logic in Python, with Browser still owned by Robot Framework."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._browser: Browser | None = None

    @property
    def browser(self) -> Browser:
        """The Browser instance that Robot Framework imported.

        Looked up on first use rather than in ``__init__``, because Robot
        Framework may not have imported Browser yet when this library is
        constructed.
        """
        if self._browser is None:
            self._browser = BuiltIn().get_library_instance("Browser")
        return self._browser

    def open_login_page(self, url: str):
        self.browser.new_browser(headless=True)
        self.browser.new_page(url)

    def click_heading_with_middle_mouse_button(self):
        """Call Browser with plain Python values.

        ``"middle"`` becomes a ``MouseButton``, ``"2 seconds"`` becomes a
        ``timedelta``, and the ``None`` stays ``None`` instead of turning into
        the string ``"None"``.
        """
        self.browser.wait_for_elements_state("id=heading1", "visible", "2 seconds")
        self.browser.click("id=heading1", "middle")
        return self.browser.evaluate_javascript(None, "() => 'evaluated'")

    def get_browser_output_directory(self) -> str:
        return self.browser.outputdir

    def get_heading_with_validate_and_then(self) -> list:
        validated = self.browser.get_text(
            "id=heading1", "validate", "value == 'Login Page'"
        )
        transformed = self.browser.get_text("id=heading1", "then", "value.upper()")
        return [validated, transformed]

    def set_test_scoped_browser_timeout(self, timeout: str) -> str:
        return self.browser.set_browser_timeout(timeout, "Test")

    def set_browser_timeout_and_return_previous(self, timeout: str) -> str:
        return self.browser.set_browser_timeout(timeout)

    def get_open_page_count(self) -> int:
        return sum(
            len(context["pages"])
            for browser in self.browser.get_browser_catalog()
            for context in browser["contexts"]
        )

    def click_missing_element(self):
        self.browser.click("id=this_element_does_not_exist")

    @screenshot_on_failure
    def click_missing_element_with_screenshot(self):
        self.browser.click("id=this_element_does_not_exist")
