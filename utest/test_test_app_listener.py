from robot import run as robot_run
from robot.api import ExecutionResult

from atest.library.test_app_server import ROOT_DIR

LISTENER = ROOT_DIR / "atest" / "library" / "test_app_listener.py"


def test_a_failed_post_adds_nothing_to_the_test_body(tmp_path):
    suite = tmp_path / "suite.robot"
    suite.write_text(
        "*** Test Cases ***\nT\n    Log    first keyword\n", encoding="utf-8"
    )
    with open(tmp_path / "stdout.txt", "w", encoding="utf-8") as captured:
        robot_run(
            str(suite),
            listener=str(LISTENER),
            variable="SERVER:localhost:1",
            loglevel="DEBUG",
            outputdir=str(tmp_path),
            log=None,
            report=None,
            stdout=captured,
        )
    test = ExecutionResult(str(tmp_path / "output.xml")).suite.tests[0]
    assert [item.type for item in test.body] == ["KEYWORD"]
