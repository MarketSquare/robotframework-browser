from enum import Enum
from typing import Any, Dict, Tuple, Callable
import re

AssertionOperator = Enum(
    "AssertionOperator",
    {
        "noassertion": "NO_ASSERTION",
        "NO_ASSERTION": "NO_ASSERTION",
        "equal": "==",
        "==": "==",
        "shouldbe": "==",
        "inequal": "!=",
        "!=": "!=",
        "shouldnotbe": "!=",
        "lessthan": "<",
        "<": "<",
        "greaterthan": ">",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "contains": "*=",
        "*=": "*=",
        "starts": "^=",
        "^=": "^=",
        "shouldstartwith": "^=",
        "ends": "$=",
        "$=": "$=",
        "matches": "$",
    },
)


handlers: Dict[AssertionOperator, Tuple[Callable, str]] = {
    AssertionOperator["NO_ASSERTION"]: (lambda a, b: True, "no assertion"),
    AssertionOperator["=="]: (lambda a, b: a == b, "should be"),
    AssertionOperator["!="]: (lambda a, b: a != b, "should not be"),
    AssertionOperator["<"]: (lambda a, b: a < b, "should be less than"),
    AssertionOperator[">"]: (lambda a, b: a > b, "should be greater than"),
    AssertionOperator["<="]: (lambda a, b: a <= b, "should be less than or equal"),
    AssertionOperator[">="]: (lambda a, b: a >= b, "should be greater than or equal"),
    AssertionOperator["*="]: (lambda a, b: b in a, "should contain"),
    AssertionOperator["matches"]: (lambda a, b: re.search(b, a), "should match"),
    AssertionOperator["^="]: (
        lambda a, b: re.search(f"^{re.escape(b)}", a),
        "should start with",
    ),
    AssertionOperator["$="]: (
        lambda a, b: re.search(f"{re.escape(b)}$", a),
        "should end with",
    ),
}


def verify_assertion(value: Any, operator: AssertionOperator, expected, message=""):
    handler = handlers.get(operator)
    if handler is None:
        raise RuntimeError(f"{message} `{operator}` is not a valid assertion operator")
    validator, text = handler
    if not validator(value, expected):
        raise AssertionError(f"{message} `{value}` {text} `{expected}`")
