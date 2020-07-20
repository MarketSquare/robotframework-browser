from enum import Enum
from typing import (
    Any,
    Dict,
    Tuple,
    Callable,
    TypeVar,
    cast,
    Optional,
    List,
    Union,
    Sequence,
)
import re

from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from .generated.playwright_pb2 import Response
from .utils.robot_booleans import is_truthy
from .keywords.input import SelectAttribute

AssertionOperator = Enum(
    "AssertionOperator",
    {
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
        "validate": "validate",
        "then": "then",
        "evaluate": "then",
    },
)

NumericalOperators = [
    AssertionOperator["=="],
    AssertionOperator["!="],
    AssertionOperator[">="],
    AssertionOperator[">"],
    AssertionOperator["<="],
    AssertionOperator["<"],
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
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if isinstance(expected, list) and len(expected) == 1:
        expected = expected[0]

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
    else:
        if operator in NumericalOperators:
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
    if operator is not None:
        if operator not in [
            AssertionOperator["=="],
            AssertionOperator["!="],
        ]:
            raise ValueError(
                f"Operators '==' and '!=' are allowed," f" not '{operator.name}'."
            )

        expected_bool: bool = is_truthy(expected)
        return verify_assertion(value, operator, expected_bool, message)


def wrap_return(selected: List):
    if not selected or len(selected) == 0:
        return None
    elif len(selected) == 1:
        return selected[0]
    else:
        return list(selected)


def list_verify_assertion(
    value: Response.Select,
    expected: Sequence[Any],
    option_attribute: SelectAttribute = SelectAttribute.label,
    operator: Optional[AssertionOperator] = None,
    message="",
):
    if operator is None:
        return wrap_return(list(value.entry))

    list_expected = list(expected)
    selected: Union[List[int], List[str]]
    if option_attribute is SelectAttribute.value:
        selected = [sel.value for sel in value.entry if sel.selected]
    elif option_attribute is SelectAttribute.label:
        selected = [sel.label for sel in value.entry if sel.selected]
    elif option_attribute is SelectAttribute.index:
        selected = [index for index, sel in enumerate(value.entry) if sel.selected]
        list_expected = [int(exp) for exp in list_expected]

    list_expected.sort()
    selected.sort()

    if operator in [
        AssertionOperator["*="],
        AssertionOperator["validate"],
    ]:
        if len(list_expected) != 1:
            raise AttributeError(
                f"Operator '{operator.name}' expects '1'"
                f" expected value but got '{len(list_expected)}'."
            )
        list_expected = list_expected[0]
    elif operator not in [
        AssertionOperator["=="],
        AssertionOperator["!="],
    ]:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed " f"in this Keyword."
        )
    if len(list_expected) == 0:
        list_expected = None  # type: ignore

    return verify_assertion(wrap_return(selected), operator, list_expected, message)
