"""Context B without the listener registration.

Demonstration library for the Browser documentation. It is quoted by path on
robotframework-browser.org, so it deliberately contains no business logic and
nothing that is not part of the example.

This is MyLibraryB.py with the ``ROBOT_LIBRARY_LISTENER`` line removed and
nothing else changed. Browser then gets no suite and test events, so pages are
not closed automatically and ``scope=Test`` settings do not revert. The body is
duplicated rather than shared so that either file can be read on its own.
"""

from Browser import Browser


class MyLibraryB_no_listener:  # noqa: N801
    """Browser used as a base, without giving Browser the Robot Framework events."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._browser = Browser(enable_playwright_debug=True)

    def open_login_page(self, url: str):
        self._browser.new_browser(headless=True)
        self._browser.new_page(url)

    def click_heading_with_middle_mouse_button(self):
        """Call Browser with plain Python values.

        ``"middle"`` becomes a ``MouseButton``, ``"2 seconds"`` becomes a
        ``timedelta``, and the ``None`` stays ``None`` instead of turning into
        the string ``"None"``.
        """
        self._browser.wait_for_elements_state("id=heading1", "visible", "2 seconds")
        self._browser.click("id=heading1", "middle")
        return self._browser.evaluate_javascript(None, "() => 'evaluated'")

    def get_browser_output_directory(self) -> str:
        return self._browser.outputdir

    def get_heading_with_validate_and_then(self) -> list:
        validated = self._browser.get_text(
            "id=heading1", "validate", "value == 'Login Page'"
        )
        transformed = self._browser.get_text("id=heading1", "then", "value.upper()")
        return [validated, transformed]

    def set_test_scoped_browser_timeout(self, timeout: str) -> str:
        return self._browser.set_browser_timeout(timeout, "Test")

    def set_browser_timeout_and_return_previous(self, timeout: str) -> str:
        return self._browser.set_browser_timeout(timeout)

    def get_open_page_count(self) -> int:
        return sum(
            len(context["pages"])
            for browser in self._browser.get_browser_catalog()
            for context in browser["contexts"]
        )

    def click_missing_element(self):
        self._browser.click("id=this_element_does_not_exist")

    def close_browser_library(self):
        self._browser.close_browser("ALL")
