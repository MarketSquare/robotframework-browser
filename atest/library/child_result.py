"""Assertions about what a child Robot Framework run did.

Used by atest/test/13_Python_Extension/python_extension.robot, which starts
child `robot` runs and then verifies their results. This lives here rather than
next to those suites on purpose: the files under 13_Python_Extension/ are
quoted by path in the documentation on robotframework-browser.org and must stay
free of test scaffolding.
"""

import json
import re
from pathlib import Path

from robot.api import logger
from robot.result import ExecutionResult, Result, TestCase


def get_child_result(output_xml: Path) -> Result:
    """Parse the output.xml of a child run."""
    result = ExecutionResult(str(output_xml))
    logger.info(f"Parsed {output_xml}")
    return result


def child_test_status_should_be(
    result: Result,
    name: str,
    status: str,
    message_pattern: str | None = None,
):
    """Verify status, and optionally the failure message, of a child run test."""
    test = _get_test(result, name)
    assert test.status == status, (
        f"Test '{name}' status was '{test.status}', expected '{status}'. "
        f"Message: {test.message}"
    )
    if message_pattern is not None:
        assert re.search(message_pattern, test.message), (
            f"Test '{name}' message '{test.message}' does not match '{message_pattern}'"
        )


def child_keyword_should_log(
    result: Result,
    test_name: str,
    owner: str,
    message_pattern: str,
):
    """Verify a message was logged inside a keyword owned by the given library.

    Browser keywords called from Python do not appear in output.xml as keywords
    of their own, but everything they log lands inside the keyword of the
    library that called them.
    """
    messages = []
    for keyword in _get_keywords(_get_test(result, test_name)):
        if keyword.owner != owner:
            continue
        for message in keyword.messages:
            messages.append(message.message)
            if re.search(message_pattern, message.message):
                logger.info(
                    f"Found '{message_pattern}' in keyword "
                    f"'{keyword.full_name}': {message.message}"
                )
                return
    raise AssertionError(
        f"No message matching '{message_pattern}' logged by a '{owner}' keyword "
        f"in test '{test_name}'. Messages: {messages}"
    )


def child_should_not_use_library(result: Result, library: str):
    """Verify the child run did not call any keyword of the given library.

    Guards context B: if a child suite ever imports Browser as a Robot
    Framework library, the listener registers and the context collapses into
    context A without any test failing.
    """
    for test in result.suite.tests:
        for keyword in _get_keywords(test):
            assert keyword.owner != library, (
                f"Test '{test.name}' called '{keyword.full_name}' "
                f"from library '{library}'"
            )


def playwright_log_should_have_rf_context(log_file: Path, expected: str):
    """Verify node side log records carry the Robot Framework test name."""
    test_names = _logged_test_names(log_file)
    assert any(expected in name for name in test_names), (
        f"No node side log record with test name containing '{expected}'. "
        f"Found: {sorted(test_names)}"
    )


def playwright_log_should_not_have_rf_context(log_file: Path):
    """Verify node side log records carry no Robot Framework test name."""
    test_names = _logged_test_names(log_file)
    assert not test_names, (
        f"Node side log records unexpectedly carry test names: {sorted(test_names)}"
    )


def _logged_test_names(log_file: Path) -> set:
    log_file = Path(log_file)
    assert log_file.is_file(), (
        f"{log_file} not found. The child run did not start its own node process."
    )
    test_names = set()
    for raw_line in log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line.startswith("{"):
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and record.get("test_name"):
            test_names.add(record["test_name"])
    logger.info(f"Test names in {log_file}: {sorted(test_names)}")
    return test_names


def _get_test(result: Result, name: str) -> TestCase:
    for test in result.suite.tests:
        if test.name == name:
            return test
    names = [test.name for test in result.suite.tests]
    raise AssertionError(f"Test '{name}' not found from child run. Found: {names}")


def _get_keywords(item) -> list:
    keywords = []
    for child in item.body:
        if child.type == child.KEYWORD:
            keywords.append(child)
            keywords.extend(_get_keywords(child))
    return keywords
