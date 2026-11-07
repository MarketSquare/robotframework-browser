import subprocess
import sys
from pathlib import Path

import pytest
from robot.api import ExecutionResult

SUITE = """
*** Settings ***
Library    Browser

Suite Setup    Open Shared Context
Suite Teardown    Close Browser

*** Test Cases ***
Test Adds An Init Script
    Add Init Script    window.seed = 'first test'
    New Page    ${URL}
    Get Text    id=seed-value    ==    first test

Next Test Does Not Get It
    New Page    ${URL}
    Get Text    id=seed-value    ==    undefined

*** Keywords ***
Open Shared Context
    New Browser
    New Context
"""


@pytest.fixture(scope="module")
def result(tmp_path_factory, test_app_url):
    folder = tmp_path_factory.mktemp("init_script_scope")
    suite = Path(folder, "init_script_scope.robot")
    suite.write_text(SUITE)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "robot",
            "--outputdir",
            str(folder),
            "--variable",
            f"URL:{test_app_url}/init_script.html",
            str(suite),
        ],
        check=False,
        capture_output=True,
    )
    return ExecutionResult(str(folder / "output.xml"))


def status_of(result, test_name: str) -> tuple[str, str]:
    test = next(t for t in result.suite.all_tests if t.name == test_name)
    return test.status, test.message


def test_init_script_runs_in_the_test_that_added_it(result):
    assert status_of(result, "Test Adds An Init Script") == ("PASS", "")


def test_init_script_of_a_test_does_not_reach_the_next_test(result):
    assert status_of(result, "Next Test Does Not Get It") == ("PASS", "")
