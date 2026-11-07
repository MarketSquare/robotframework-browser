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

*** Keywords ***
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


def keywords_in_teardown(result, test_name: str) -> list[str]:
    test = next(t for t in result.suite.all_tests if t.name == test_name)
    return [item.name for item in test.teardown.body if item.type == "KEYWORD"]


def test_teardown_after_a_test_timeout_runs_the_on_failure_keyword(result):
    assert keywords_in_teardown(result, "Test Timeout With Teardown") == [
        "Failure Handled"
    ]


def test_teardown_after_another_failure_does_not_run_it_again(result):
    assert keywords_in_teardown(result, "Failure Without Timeout") == []
