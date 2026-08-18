import re
from typing import Optional

from assertionengine.assertion_engine import AssertionOperator, verify_assertion
from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


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


def get_banner_style_text(
    operator: AssertionOperator = None, expected: Optional[str] = None
):
    """Reads the keyword call out of the injected style element.

    Unlike `Get Banner Content`, which asks for the computed style of the
    ``body::before`` pseudo element, this works on every browser engine.
    """
    b: Browser = BuiltIn().get_library_instance("Browser")
    style = b.evaluate_javascript(
        None,
        "() => {const e = document.getElementById('kwCallBanner');"
        " return e ? e.textContent : '';}",
    )
    match = re.search(r"content: '(.*?)';", style, re.DOTALL)
    return verify_assertion(match.group(1) if match else "none", operator, expected)
