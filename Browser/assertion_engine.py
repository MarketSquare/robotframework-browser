from enum import Enum
from typing import Any
import re

AssertionOperator = Enum(  # type: ignore
    value="AssertionOperator",
    names={
        "noassertion": None,
        "NO_ASSERTION": None,
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


def verify_assertion(value: Any, operator: AssertionOperator, expected, message=""):
    if operator.value == "==" and not value == expected:
        raise AssertionError(f"{message} `{value}` should be `{expected}`")
    elif operator.value == "!=" and not value != expected:
        raise AssertionError(f"{message} `{value}` should not be `{expected}`")
    elif operator.value == "<" and not value < expected:
        raise AssertionError(f"{message} `{value}` should be less than `{expected}`")
    elif operator.value == ">" and not value > expected:
        raise AssertionError(f"{message} `{value}` should be greater than `{expected}`")
    elif operator.value == "<=" and not value <= expected:
        raise AssertionError(
            f"{message} `{value}` should be less than or equal `{expected}`"
        )
    elif operator.value == ">=" and not value >= expected:
        raise AssertionError(
            f"{message} `{value}` should be greater than or equal `{expected}`"
        )
    elif operator.value == "*=" and expected not in value:
        raise AssertionError(f"{message} `{value}` should contain `{expected}`")
    elif operator.value == "$" and not re.search(expected, value):
        raise AssertionError(f"{message} `{value}` should match `{expected}`")
    elif operator.value == "^=" and not re.search(f"^{re.escape(expected)}", value):
        raise AssertionError(f"{message} `{value}` should start with `{expected}`")
    elif operator.value == "$=" and not re.search(f"{re.escape(expected)}$", value):
        raise AssertionError(f"{message} `{value}` should end with `{expected}`")
    elif operator not in AssertionOperator:
        raise RuntimeError(f"{message} `{operator}` is not a valid assertion operator")
