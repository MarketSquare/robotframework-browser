import re
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from .utils.data_types import AssertionOperator
from .utils.robot_booleans import is_truthy

NumericalOperators = [
    AssertionOperator["=="],
    AssertionOperator["!="],
    AssertionOperator[">="],
    AssertionOperator[">"],
    AssertionOperator["<="],
    AssertionOperator["<"],
]

SequenceOperators = [
    AssertionOperator["*="],
    AssertionOperator["validate"],
    AssertionOperator["=="],
    AssertionOperator["!="],
]

handlers: Dict[AssertionOperator, Tuple[Callable, str]] = {
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
    AssertionOperator["validate"]: (
        lambda a, b: BuiltIn().evaluate(b, namespace={"value": a}),
        "should validate to true with",
    ),
}

T = TypeVar("T")


def verify_assertion(
    value: T, operator: Optional[AssertionOperator], expected: Any, message=""
) -> Any:
    if operator is None:
        return value
    if operator is AssertionOperator["then"]:
        return cast(T, BuiltIn().evaluate(expected, namespace={"value": value}))
    handler = handlers.get(operator)
    if handler is None:
        raise RuntimeError(f"{message} `{operator}` is not a valid assertion operator")
    validator, text = handler
    if not validator(value, expected):
        raise AssertionError(f"{message} `{value}` {text} `{expected}`")
    return value


def int_str_verify_assertion(
    value: T, operator: Optional[AssertionOperator], expected: Any, message=""
):
    if operator is None:
        return value
    elif operator in NumericalOperators:
        expected = int(expected)

    elif operator in [
        AssertionOperator["validate"],
        AssertionOperator["then"],
    ]:
        expected = str(expected)
    else:
        raise ValueError(f"Operator '{operator.name}' is not allowed.")
    return verify_assertion(value, operator, expected, message)


def bool_verify_assertion(
    value: T, operator: Optional[AssertionOperator], expected: Any, message=""
):
    if operator and operator not in [
        AssertionOperator["=="],
        AssertionOperator["!="],
    ]:
        raise ValueError(f"Operators '==' and '!=' are allowed, not '{operator.name}'.")

    expected_bool = is_truthy(expected)
    return verify_assertion(value, operator, expected_bool, message)


def map_list(selected: List):
    if not selected or len(selected) == 0:
        return None
    elif len(selected) == 1:
        return selected[0]
    else:
        return selected


def list_verify_assertion(
    value: List, operator: Optional[AssertionOperator], expected: List, message="",
):
    if operator and operator not in SequenceOperators:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed in this Keyword."
            f"Allowed operators are: '{SequenceOperators}'"
        )
    expected.sort()
    value.sort()

    return verify_assertion(map_list(value), operator, map_list(expected), message)


def dict_verify_assertion(
    value: Dict,
    operator: Optional[AssertionOperator],
    expected: Optional[Dict],
    message="",
):
    if operator and operator not in SequenceOperators:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed in this Keyword."
            f"Allowed operators are: {SequenceOperators}"
        )
    else:
        return verify_assertion(value, operator, expected, message)


def int_dict_verify_assertion(
    value: Dict[str, int],
    operator: Optional[AssertionOperator],
    expected: Optional[Dict[str, int]],
    message="",
):
    if not operator:
        return value
    elif expected and operator in NumericalOperators:
        for k, v in value.items():
            exp = expected[k]
            verify_assertion(v, operator, exp, message)
        return True
    elif operator in SequenceOperators:
        return verify_assertion(value, operator, expected, message)
    else:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed in this Keyword."
            f"Allowed operators are: {NumericalOperators} and {SequenceOperators}"
        )
