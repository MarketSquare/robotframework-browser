import pytest
from approvaltests import verify_all  # type: ignore

from Browser.assertion_engine import (
    verify_assertion,
    AssertionOperator,
    with_assertion_polling,
)
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore


def test_equals():
    results = [
        _validate_operator(AssertionOperator["=="], "actual", "actual"),
        _validate_operator(AssertionOperator["=="], "actual", "unexpected"),
        _validate_operator(AssertionOperator["=="], 1, "1"),

    ]
    verify_all("Test equals", results)


def test_not_equals():
    results = [
        _validate_operator(AssertionOperator["!="], "actual", "expected"),
        _validate_operator(AssertionOperator["!="], "actual", "actual"),
    ]
    verify_all("Not equal", results)


def test_contains():
    results = [
        _validate_operator(AssertionOperator["contains"], "actual", "ctua"),
        _validate_operator(AssertionOperator["contains"], "actual", "nope"),
        _validate_operator(AssertionOperator["*="], "actual", "tual"),
        _validate_operator(AssertionOperator["*="], "actual", "nope"),
    ]
    verify_all("Contains", results)


class FakeBrowser:
    timeout = 100
    counter = 1
    retry_assertions_for = 30

    @with_assertion_polling
    def is_three(self, value):
        return verify_assertion(value, AssertionOperator["=="], 3)

    @with_assertion_polling
    def second_run_success(self):
        current = self.counter
        self.counter += 1
        return verify_assertion(current, AssertionOperator["=="], 2)


def test_with_assertions_polling():
    fb = FakeBrowser()
    results = [
        fb.is_three(3),
        _method_validator(fb.is_three, 2),
        fb.second_run_success(),
    ]
    verify_all("Assertion polling", results)


def test_without_assertions_polling():
    fb = FakeBrowser()
    fb.retry_assertions_for = 0
    results = [
        fb.is_three(3),
        _method_validator(fb.is_three, 2),
        _method_validator(fb.second_run_success)
    ]
    verify_all("No polling", results)


def test_greater():
    results = [
        _validate_operator(AssertionOperator["<"], 1, 2),
        _validate_operator(AssertionOperator["<"], 1, 0),
    ]
    verify_all("Greater", results)


def test_less():
    results = [
        _validate_operator(AssertionOperator[">"], 2, 1),
        _validate_operator(AssertionOperator[">"], 2, 3),
    ]
    verify_all("Less", results)


def test_greater_or_equal():
    results = [
        _validate_operator(AssertionOperator["<="], 1, 2),
        _validate_operator(AssertionOperator["<="], 1, 0),
        _validate_operator(AssertionOperator["<="], 1, 1),
    ]
    verify_all("greater or equal", results)


def test_less_or_equal():
    results = [
        _validate_operator(AssertionOperator[">="], 2, 2),
        _validate_operator(AssertionOperator[">="], 2, 3),
        _validate_operator(AssertionOperator[">="], 2, 1),
    ]
    verify_all("less or equal", results)


def test_match():
    results = [
        _validate_operator(AssertionOperator["matches"], "Actual", "(?i)actual"),
        _validate_operator(AssertionOperator["matches"], "Actual", "/(\\d)+/"),
        _validate_operator(AssertionOperator["matches"], "Actual", "^Act"),
        _validate_operator(AssertionOperator["matches"], "Actual", "/(\\d)+/"),
        _validate_operator(AssertionOperator["matches"], "Actual", "ual$"),
        _validate_operator(AssertionOperator["matches"], "Actual\nmultiline", "(?m)Actual\nmultiline$"),
        _validate_operator(AssertionOperator["matches"], "Actual\nmultiline", "/(\\d)+/"),

    ]
    verify_all("match", results)


@pytest.fixture()
def with_suite():
    def ns():
        pass

    ns.variables = lambda: 0
    ns.variables.current = lambda: 0
    ns.variables.current.store = lambda: 0
    EXECUTION_CONTEXTS.start_suite("suite", ns, lambda: 0)
    yield
    EXECUTION_CONTEXTS.end_suite()


def test_validate(with_suite):
    results = [
        _validate_operator(AssertionOperator("validate"), 1, "0 < value < 2"),
        _validate_operator(AssertionOperator("validate"), 1, "value == 'hello'"),
    ]
    verify_all("validate", results)


def test_then(with_suite):
    then_op = AssertionOperator["then"]
    results = [
        verify_assertion(8, then_op, "value + 3") == 11,
        verify_assertion(2, then_op, "value + 3") == 5,
        verify_assertion("René", then_op, "'Hello ' + value + '!'") == "Hello René!"
    ]
    verify_all("then", results)


def test_start_with():
    results = [
        _validate_operator(AssertionOperator["^="], "Hello Robots", "Hello"),
        _validate_operator(AssertionOperator["^="], "Hello Robots", "Robots"),
        _validate_operator(AssertionOperator["should start with"], "Hello Robots", "Hello"),
        _validate_operator(AssertionOperator["should start with"], "Hello Robots", "Robots"),
        _validate_operator(AssertionOperator["^="], "Hel[4,5]?[1-9]+ Robots", "Hel[4,5]?[1-"),
        _validate_operator(AssertionOperator["^="], "Hel[4,5]?[1-9]+ Robots", ".*"),

    ]
    verify_all("start with", results)


def test_ends_with():
    results = [
        _validate_operator(AssertionOperator["$="], "Hello Robots", "Robots"),
        _validate_operator(AssertionOperator["$="], "Hello Robots", "Hello"),
        _validate_operator(AssertionOperator["$="], "Hel[4,5]?[1-9]+ Robots", "[1-9]+ Robots"),
        _validate_operator(AssertionOperator["$="], "Hel[4,5]?[1-9]+ Robots", ".*"),
    ]
    verify_all("ends with", results)


def _validate_operator(operator: AssertionOperator, actual, expected):
    try:
        return verify_assertion(actual, operator, expected)
    except Exception as error:
        return error


def _method_validator(method, arg=None):
    try:
        if arg is None:
            return method()
        return method(arg)
    except Exception as error:
        return error
