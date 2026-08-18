import re

from assertionengine.assertion_engine import AssertionOperator, verify_assertion
from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


def get_banner_style_text(
    operator: AssertionOperator = None, expected: str | None = None
):
    """The computed style of ``body::before`` is not readable on firefox and webkit."""
    browser: Browser = BuiltIn().get_library_instance("Browser")
    style = browser.evaluate_javascript(
        None,
        "() => {const e = document.getElementById('kwCallBanner');"
        " return e ? e.textContent : '';}",
    )
    match = re.search(r"content: '(.*?)';", style, re.DOTALL)
    return verify_assertion(match.group(1) if match else "none", operator, expected)
