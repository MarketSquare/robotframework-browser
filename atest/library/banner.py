import re
from typing import Any

from assertionengine.assertion_engine import AssertionOperator, verify_assertion
from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


def get_keyword_call_banner_text(
    operator: AssertionOperator = None, expected: str | None = None
):
    """Keyword is not a Browser keyword, therefore can read without influencing the keyword call banner."""
    browser: Browser = BuiltIn().get_library_instance("Browser")
    text_content = browser.evaluate_javascript(
        None,
        "() => {const e = document.getElementById('kwCallBanner');"
        " return e ? e.textContent : '';}",
    )
    content_match = re.search(r"content: '(.*?)';", text_content, re.DOTALL)
    return verify_assertion(
        content_match.group(1) if content_match else "", operator, expected
    )


def get_wrapped_page_source(
    assertion_operator: AssertionOperator | None = None,
    assertion_expected: Any | None = None,
    message: str | None = None,
) -> str | dict | tuple:
    """Keyword is not a Browser keyword, therefore is neither shown in keyword call banner, nor is it hiding it."""
    browser: Browser = BuiltIn().get_library_instance("Browser")
    return browser.get_page_source(assertion_operator, assertion_expected, message)
