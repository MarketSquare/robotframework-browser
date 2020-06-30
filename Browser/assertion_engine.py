from enum import Enum
from typing import Any
import re

AssertionOperator = Enum(
    "AssertionOperator",
    "NO_ASSERTION == should_be != should_not_be < > <= >= *= contains matches ^= $="
)


def _normalize(operator: str):
    return operator.lower().replace('_', '').replace(' ', '')


def verify_assertion(value: Any,
                     operator: AssertionOperator,
                     expected, message=""):

    if isinstance(operator, str):
        if _normalize(operator) == "contains":
            operator = AssertionOperator["*="]
        elif _normalize(operator) == "shouldcontain":
            operator = AssertionOperator["*="]
        elif _normalize(operator) == "matches":
            operator = AssertionOperator["matches"]
        elif _normalize(operator) == "shouldbe":
            operator = AssertionOperator["=="]
        elif _normalize(operator) == "shouldnotbe":
            operator = AssertionOperator["!="]
        elif _normalize(operator) == "shouldstartwith":
            operator = AssertionOperator["^="]
        elif _normalize(operator) == "shouldendwith":
            operator = AssertionOperator["$="]
        else:
            raise SyntaxError(f"{message}"
                              f" `{operator}` is no valid assertion operator")

    if operator.name in ["==", "should_be"] and not value == expected:
        raise AssertionError(
            f"{message} `{value}` should be `{expected}`"
        )
    elif operator.name in ["!=", "should_not_be"] and not value != expected:
        raise AssertionError(
            f"{message} `{value}` should not be `{expected}`"
        )
    elif operator.name == "<" and not value < expected:
        raise AssertionError(
            f"{message} `{value}` should be less than `{expected}`"
        )
    elif operator.name == ">" and not value > expected:
        raise AssertionError(
            f"{message} `{value}` should be greater than `{expected}`"
        )
    elif operator.name == "<=" and not value <= expected:
        raise AssertionError(
            f"{message} `{value}` should be less than or equal `{expected}`"
        )
    elif operator.name == ">=" and not value >= expected:
        raise AssertionError(
            f"{message} `{value}` should be greater than or equal `{expected}`"
        )
    elif operator.name in ["contains", "*="] and expected not in value:
        raise AssertionError(
            f"{message} `{value}` should contain `{expected}`"
        )
    elif operator.name == "matches" and not re.search(expected, value):
        raise AssertionError(
            f"{message} `{value}` should match `{expected}`"
        )
    elif operator.name == "^=" and not re.search(
            f"^{re.escape(expected)}", value
    ):
        raise AssertionError(
            f"{message} `{value}` should start with `{expected}`"
        )
    elif operator.name == "$=" and not re.search(
            f"{re.escape(expected)}$", value
    ):
        raise AssertionError(
            f"{message} `{value}` should end with `{expected}`"
        )
    elif operator.name not in AssertionOperator.__members__:
        raise SyntaxError(
            f"{message} `{operator.name}` is not a valid assertion operator"
        )

