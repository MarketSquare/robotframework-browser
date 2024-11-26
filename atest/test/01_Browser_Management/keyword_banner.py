from robot.libraries.BuiltIn import BuiltIn
from Browser import Browser
from assertionengine.assertion_engine import verify_assertion, AssertionOperator
from typing import Optional


def get_computed_banner_style():
    b: Browser = BuiltIn().get_library_instance("Browser")
    return b.evaluate_javascript(
        "!prefix body", "element => window.getComputedStyle(element,':before')"
    )


def get_real_page_source(
    operator: AssertionOperator = None, expected: Optional[str] = None
):
    b: Browser = BuiltIn().get_library_instance("Browser")
    return verify_assertion(b.get_page_source(), operator, expected)


def get_banner_content(
    operator: AssertionOperator = None, expected: Optional[str] = None
):
    style = get_computed_banner_style()
    content = (
        BuiltIn().evaluate(style["content"])
        if style["content"].startswith('"')
        else style["content"]
    )
    return verify_assertion(content, operator, expected)
