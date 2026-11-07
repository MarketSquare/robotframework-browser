import subprocess
import sys
from pathlib import Path

import pytest
from robot.api import ExecutionResult

SUITE = """
*** Settings ***
Library    Browser    auto_closing_level=MANUAL    run_on_failure=Failure Handled

*** Test Cases ***
Test Timeout With Teardown
    [Timeout]    0.5 seconds
    [Teardown]    No Operation
    Sleep    3 seconds

Failure Without Timeout
    [Teardown]    No Operation
    Fail    plain failure

Test Timeout With Nested Teardown
    [Timeout]    0.5 seconds
    [Teardown]    Clean Up
    Sleep    3 seconds

*** Keywords ***
Clean Up
    No Operation
    [Teardown]    No Operation

Failure Handled
    Log    on-failure keyword ran
"""


@pytest.fixture(scope="module")
def result(tmp_path_factory):
    folder = tmp_path_factory.mktemp("teardown")
    suite = Path(folder, "teardown.robot")
    suite.write_text(SUITE)
    subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(folder), str(suite)],
        check=False,
        capture_output=True,
    )
    return ExecutionResult(str(folder / "output.xml"))


def teardown_of(result, test_name: str):
    return next(t for t in result.suite.all_tests if t.name == test_name).teardown


def keyword_names(step) -> list[str]:
    return [item.name for item in step.body if item.type == "KEYWORD"]


def test_teardown_after_a_test_timeout_runs_the_on_failure_keyword(result):
    teardown = teardown_of(result, "Test Timeout With Teardown")
    assert keyword_names(teardown) == ["Failure Handled"]


def test_teardown_after_another_failure_does_not_run_it_again(result):
    teardown = teardown_of(result, "Failure Without Timeout")
    assert keyword_names(teardown) == []


def test_user_keyword_test_teardown_runs_the_on_failure_keyword_first(result):
    teardown = teardown_of(result, "Test Timeout With Nested Teardown")
    assert keyword_names(teardown) == ["Failure Handled", "No Operation"]


def test_keyword_teardown_inside_the_test_teardown_does_not_run_it_again(result):
    teardown = teardown_of(result, "Test Timeout With Nested Teardown")
    assert keyword_names(teardown.teardown) == []
