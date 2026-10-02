"""Tests for tools/ci_failures. See that package's README.md and CONTEXT.md."""

import json
from datetime import datetime, timedelta, timezone
import shutil
import sqlite3
from contextlib import closing
import zipfile
from pathlib import Path

import pytest
from robot import run as robot_run

from tools.ci_failures import github, ingest, render_html
from tools.ci_failures.db import connect
from tools.ci_failures.parse import error_signature, parse
from tools.ci_failures.queries import Spread, VariantRow
from tools.ci_failures import reading
from tools.ci_failures.render_json import document as json_document
from tools.ci_failures.report import LogLine
from tools.ci_failures.report import build as build_report
from tools.ci_failures.queries import (
    coverage_by_fixture,
    coverage_by_test,
    first_attempt_counts_by_test,
    latest_run,
    runs_either_side,
    pass_durations_by_test,
    failure_groups,
    fixture_signature_variants,
    fixture_failures,
    occurrences_by_test,
    signature_variants,
    totals,
)


def connect_db(db_path: Path):
    """`db.connect`, allowed to create the database: these tests start from nothing."""
    return connect(db_path, create=True)


def build_json(db_path: Path, limit: int = 100) -> dict:
    """The JSON Rendering of a Report, which is what these tests grew up asserting on."""
    return json_document(build_report(db_path, limit=limit))


SUITE = """\
*** Test Cases ***
Passing Test
    Log    fine

Failing Test
    Outer Keyword

Skipped Test
    Skip    not today

Test Failed By Its Teardown
    [Teardown]    Fail    teardown blew up
    Log    this line is not evidence of anything

*** Keywords ***
Outer Keyword
    IF    True
        Inner Keyword
    END

Inner Keyword
    Fail    Timeout 5000ms exceeded waiting for #id-4f2a
"""


#: Readings opened by `reading_of`, closed after the test that opened them.
_OPEN_READINGS: list = []


def reading_of(db_path, window=None):
    """`reading.of`, with the closing done for you.

    These tests ask a Reading one question and drop it, forty-seven times over.
    Closing each by hand is forty-seven chances to forget, and a forgotten one
    is an unclosed sqlite3.Connection reported as a ResourceWarning against
    whatever unrelated frame the garbage collector happened to be in when it
    noticed - which is how this looked for a long time: pages of warnings
    blaming Robot Framework's parser and `inspect`.

    Production does not need this. All three `reading.of` calls in `report.py`
    are `with` statements; only the tests were treating a Reading as something
    you drop on the floor.
    """
    from tools.ci_failures.window import ALL_HISTORY

    opened = reading.of(db_path, ALL_HISTORY if window is None else window)
    _OPEN_READINGS.append(opened)
    return opened


@pytest.fixture(autouse=True)
def _close_readings():
    yield
    while _OPEN_READINGS:
        _OPEN_READINGS.pop().close()


def _run_robot(directory: Path, suite: str, metadata: tuple[str, ...] = ()) -> Path:
    """A real output.xml from a real Robot Framework run.

    Written by Robot Framework rather than hand-rolled, so these tests keep
    working against the format Robot Framework actually emits. Laid out as CI
    lays it out, with `atest/test` as the root suite, because ingest refuses a
    Leg whose root suite is anything else.
    """
    suites = directory / "atest" / "test"
    suites.mkdir(parents=True, exist_ok=True)
    (suites / "suite.robot").write_text(suite, encoding="utf-8")
    # Closed rather than left to the collector: Robot Framework is run once per
    # test here, and an open handle per run surfaced as a ResourceWarning
    # against whatever frame happened to be executing when it was noticed.
    with open(directory / "stdout.txt", "w", encoding="utf-8") as captured:
        robot_run(
            str(suites),
            outputdir=str(directory),
            output="output.xml",
            log=None,
            report=None,
            metadata=list(metadata),
            stdout=captured,
        )
    return directory / "output.xml"


BROKEN_TEARDOWN_SUITE = """\
*** Settings ***
Suite Teardown    Suite Level Cleanup

*** Test Cases ***
A Test That Passes On Its Own
    Log    this test itself is fine

*** Keywords ***
Suite Level Cleanup
    Log    cleaning up
    Fail    the suite teardown broke
"""


def leg_table_without(db: Path, column: str) -> None:
    """The `leg` table as a database from before `column` was added had it.

    Rebuilt rather than `DROP COLUMN`: older SQLite (3.40 and 3.45 do, 3.53 does
    not) rewrites the table wrongly when a comment precedes the dropped column,
    as every commented column in `schema.sql` does.
    """
    with closing(sqlite3.connect(db)) as connection:
        kept = [
            f"{row[1]} {row[2]}"
            for row in connection.execute("PRAGMA table_info(leg)")
            if row[1] != column
        ]
        names = ", ".join(definition.split()[0] for definition in kept)
        connection.executescript(
            f"CREATE TABLE old_leg ({', '.join(kept)});"
            f"INSERT INTO old_leg SELECT {names} FROM leg;"
            "DROP TABLE leg;"
            "ALTER TABLE old_leg RENAME TO leg;"
        )


def one_row(db: Path, sql: str):
    """One row, with the connection closed behind it."""
    connection = connect_db(db)
    try:
        return connection.execute(sql).fetchone()
    finally:
        connection.close()


def run_sql(db: Path, script: str) -> None:
    """A statement or two against a seeded database, and then closed."""
    connection = connect_db(db)
    try:
        connection.executescript(script)
    finally:
        connection.close()


def seed(db: Path, rows: list[dict]) -> None:
    """A database holding these results, and the Runs and Legs under them.

    The test-side counterpart of `_run_robot`: that one produces a real
    output.xml, this one produces a database without going near an artifact.

    One dict per Result. Rows sharing a (commit, platform, python, attempt) land
    on the same Leg, which is what makes a per-configuration denominator mean
    anything, and an `attempt` above 1 puts a row on a second Leg of the same
    name in the same Run - which is what a hand re-run of a failed job looks
    like once it has been ingested.

    Keys, all optional but `test` and `status`:

        test suite status signature message elapsed scope owner
        sha platform python rf node executors node_process attempt artifact
        screenshots screenshot_status logs

    `artifact` is the Leg's artifact name, and its Install is read from it.

    `logs` is a list of (level, keyword, message). There were eight seeders
    before this one, agreeing about the four columns they happened to share and
    unable between them to write `executors`, `node_process` or a screenshot -
    very nearly the set of things nothing tested.
    """
    from tools.ci_failures.legs import install_of

    connection = connect_db(db)
    runs: dict[str, int] = {}
    legs: dict[tuple, int] = {}
    for row in rows:
        sha = row.get("sha", "sha1")
        if sha not in runs:
            runs[sha] = len(runs) + 1
            created = f"2026-08-{19 + runs[sha]:02d}T10:00:00Z"
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', ?, 'main', ?, 'failure', 'u')",
                (runs[sha], sha, created),
            )
        platform = row.get("platform", "linux")
        python = row.get("python", "3.13.15")
        attempt = row.get("attempt", 1)
        artifact = row.get("artifact", f"leg-{platform}-{python}")
        key = (sha, platform, python, attempt, artifact)
        if key not in legs:
            legs[key] = len(legs) + 1
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                "artifact_url, platform, python_version, rf_version, "
                "node_version, executors, node_process, ingested_at, attempt, "
                "install) "
                "VALUES (?, ?, ?, ?, 'a-url', ?, ?, ?, ?, ?, ?, 'now', ?, ?)",
                (
                    legs[key],
                    runs[sha],
                    legs[key],
                    artifact,
                    platform,
                    python,
                    row.get("rf", "7.4.2"),
                    row.get("node"),
                    row.get("executors"),
                    row.get("node_process"),
                    attempt,
                    install_of(artifact),
                ),
            )
        cursor = connection.execute(
            "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
            "status, elapsed_ms, message, error_signature, failure_scope, "
            "scope_owner, screenshots, screenshot_status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                legs[key],
                row["test"],
                row["test"],
                row.get("suite", "S"),
                row["status"],
                row.get("elapsed"),
                row.get("message"),
                row.get("signature"),
                row.get("scope", "test"),
                row.get("owner"),
                row.get("screenshots"),
                row.get("screenshot_status"),
            ),
        )
        for seq, (level, keyword, message) in enumerate(row.get("logs", [])):
            connection.execute(
                "INSERT INTO log_message (test_result_id, seq, level, keyword, "
                "origin, message) VALUES (?, ?, ?, ?, NULL, ?)",
                (cursor.lastrowid, seq, level, keyword, message),
            )
    connection.commit()
    connection.close()


@pytest.fixture(scope="module")
def broken_teardown_xml(tmp_path_factory) -> Path:
    return _run_robot(tmp_path_factory.mktemp("teardown"), BROKEN_TEARDOWN_SUITE)


@pytest.fixture(scope="module")
def ancestor_teardown_xml(tmp_path_factory) -> Path:
    """A suite tree where the *grandparent* teardown fails.

    The shape of atest/test/08_Scope_Tests, and of anything sharing a test app
    across nested suites: the tests are two levels below the thing that breaks.
    """
    root = tmp_path_factory.mktemp("ancestor")
    outer = root / "Outer"
    (outer / "Middle").mkdir(parents=True)
    (outer / "__init__.robot").write_text(
        "*** Settings ***\n"
        "Suite Teardown    Outer Cleanup\n\n"
        "*** Keywords ***\n"
        "Outer Cleanup\n"
        "    Fail    the shared server did not shut down\n",
        encoding="utf-8",
    )
    (outer / "Middle" / "__init__.robot").write_text(
        "*** Settings ***\nDocumentation    Between the teardown and the tests.\n",
        encoding="utf-8",
    )
    (outer / "Middle" / "inner.robot").write_text(
        "*** Test Cases ***\nScope Test One\n    Log    fine\n", encoding="utf-8"
    )
    with open(root / "stdout.txt", "w", encoding="utf-8") as captured:
        robot_run(
            str(outer),
            outputdir=str(root),
            output="output.xml",
            log=None,
            report=None,
            stdout=captured,
        )
    return root / "output.xml"


@pytest.fixture(scope="module")
def output_xml(tmp_path_factory) -> Path:
    return _run_robot(
        tmp_path_factory.mktemp("robot"),
        SUITE,
        metadata=("Node Version:v24.15.0", "OS:Linux-6.8-x86_64"),
    )


class TestErrorSignature:
    def test_the_same_problem_groups_even_when_the_numbers_differ(self):
        first = error_signature("ValueError: Box (0, 117) has difference of 5046301")
        second = error_signature("ValueError: Box (0, 117) has difference of 5046304")

        assert first == second

    def test_a_uuid_is_masked_whole_rather_than_digit_by_digit(self):
        assert error_signature("context=cb049c7a-9776-4c0c-b483-ae54b58853c8 lost") == (
            "context=<uuid> lost"
        )

    def test_genuinely_different_errors_stay_apart(self):
        assert error_signature("Element not found") != error_signature("Timeout")

    def test_no_message_means_no_signature(self):
        assert error_signature(None) is None
        assert error_signature("") is None


class TestParse:
    def test_the_environment_is_read_out_of_output_xml(self, output_xml):
        info, _ = parse(output_xml)

        assert info.node_version == "v24.15.0"
        assert info.platform == "linux"
        assert info.os_release == "Linux-6.8-x86_64"
        assert info.python_version
        assert info.rf_version

    def test_the_generator_line_stands_in_when_metadata_is_absent(self, tmp_path):
        # Backfilled runs predate the metadata, and still have to say something.
        info, _ = parse(_run_robot(tmp_path, SUITE))

        assert info.node_version is None
        assert info.platform in {"linux", "darwin", "win32"}
        assert info.os_release is None
        assert info.python_version

    def test_the_generator_is_read_from_the_file_not_off_the_result(self, tmp_path):
        """`Result.generator` does not exist before Robot Framework 7.2, and
        this CI runs 7.1.1 beside 7.4.2.

        Reading it off the object raised AttributeError on every leg with the
        older one - forty tests and five errors, all of them parsing an
        output.xml - and passed everywhere anybody was likely to run it locally.
        The stand-in below has no `generator`, so this fails on any version if
        that reaches back into the Result rather than the file.
        """
        from types import SimpleNamespace

        from tools.ci_failures.parse import generator_line, leg_info

        line = generator_line(_run_robot(tmp_path, SUITE))
        assert line and line.startswith(("Robot", "Rebot")), line

        no_generator = SimpleNamespace(suite=SimpleNamespace(metadata={}))
        assert not hasattr(no_generator, "generator")

        info = leg_info(no_generator, "Robot 7.1.1 (Python 3.13.15 on linux)")

        assert (info.rf_version, info.python_version, info.platform) == (
            "7.1.1",
            "3.13.15",
            "linux",
        )

    def test_how_much_ran_at_once_is_read_too(self, tmp_path):
        """The axis a cross-worker failure lives on, and nothing else records it."""
        info, _ = parse(
            _run_robot(tmp_path, SUITE, metadata=("Executors:3", "Node Process:shared"))
        )

        assert info.executors == 3
        assert info.node_process == "shared"

    def test_a_run_that_did_not_say_carries_no_number(self, output_xml):
        """Never defaulted to 1: a leg nobody measured and a leg that really ran
        one execution are different findings, and a default hides which."""
        info, _ = parse(output_xml)

        assert info.executors is None
        assert info.node_process is None


class TestExecutorMetadata:
    """`atest/test/__init__.robot` records these; these are the helpers it calls."""

    def test_the_pabot_process_count_is_what_is_recorded(self):
        from atest.library.os_wrapper import get_executor_count

        assert get_executor_count("3") == "3"

    def test_no_pabot_means_one_execution(self):
        from atest.library.os_wrapper import get_executor_count

        assert get_executor_count("") == "1"
        assert get_executor_count("${PABOTNUMBEROFPROCESSES}") == "1"

    def test_a_shared_node_process_is_recorded_as_shared(self, monkeypatch):
        from atest.library.os_wrapper import get_node_process_sharing

        monkeypatch.setenv("ROBOT_FRAMEWORK_BROWSER_NODE_PORT", "56789")
        assert get_node_process_sharing() == "shared"

    def test_without_the_variable_each_run_starts_its_own(self, monkeypatch):
        from atest.library.os_wrapper import get_node_process_sharing

        monkeypatch.delenv("ROBOT_FRAMEWORK_BROWSER_NODE_PORT", raising=False)
        assert get_node_process_sharing() == "per-process"

    def test_every_result_is_returned_not_only_the_failures(self, output_xml):
        _, results = parse(output_xml)

        assert {r.name: r.status for r in results} == {
            "Passing Test": "PASS",
            "Failing Test": "FAIL",
            "Skipped Test": "SKIP",
            "Test Failed By Its Teardown": "FAIL",
        }

    def test_a_passing_test_carries_no_message(self, output_xml):
        _, results = parse(output_xml)
        passed = next(r for r in results if r.status == "PASS")

        assert passed.message is None
        assert passed.error_signature is None
        assert passed.failing_keyword is None

    def test_the_innermost_keyword_is_the_one_that_broke(self, output_xml):
        _, results = parse(output_xml)
        failed = next(r for r in results if r.status == "FAIL")

        assert failed.failing_keyword == "Fail"

    def test_a_teardown_failure_is_still_a_failure(self, output_xml):
        _, results = parse(output_xml)
        by_name = {r.name: r for r in results}

        assert by_name["Test Failed By Its Teardown"].status == "FAIL"

    def test_a_control_structure_is_never_named_as_the_culprit(self, output_xml):
        _, results = parse(output_xml)
        failed = next(r for r in results if r.status == "FAIL")

        assert "IF" not in (failed.failing_keyword or "")


@pytest.fixture
def fake_ci(monkeypatch, tmp_path, output_xml):
    """A one-run, two-leg CI so ingest and grouping work without the network.

    Dated yesterday, so the ingest's own pruning never takes it."""
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    run = github.Run(
        id=111,
        event="push",
        head_sha="abc123",
        head_branch="main",
        created_at=yesterday.strftime("%Y-%m-%dT%H:%M:%SZ"),
        conclusion="failure",
        url="https://example.invalid/runs/111",
    )
    artifact = github.Artifact(
        id=222,
        name="Test results-ubuntu-latest-1-3.14-22.x",
        expired=False,
        url="https://example.invalid/runs/111/artifacts/222",
    )
    zip_path = tmp_path / "artifact.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.write(output_xml, "output.xml")
        archive.writestr("playwright-log.txt", "not wanted")
        archive.writestr("log.html", "not wanted")

    monkeypatch.setattr(ingest.github, "list_runs", lambda **kwargs: [run])
    monkeypatch.setattr(ingest.github, "list_test_artifacts", lambda run_id: [artifact])

    def fake_download(artifact_id, destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(zip_path.read_bytes())
        return destination

    monkeypatch.setattr(ingest.github, "download_artifact", fake_download)
    return {"run": run, "artifact": artifact}


class TestIngest:
    def test_a_run_becomes_rows(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"

        result = ingest.ingest(db, limit=5, out=lambda _: None)

        assert result.runs == 1
        assert result.legs == 1
        assert result.tests == 4
        assert result.failures == 2

    def test_artifacts_a_triage_left_behind_are_removed_from_its_own_workspace_only(
        self, fake_ci, tmp_path
    ):
        from tools.ci_failures import workspace

        db = tmp_path / "ingested" / "ci.sqlite3"
        other = tmp_path / "other" / "ci.sqlite3"
        for leftover in (workspace.artifacts(db), workspace.artifacts(other)):
            leftover.mkdir(parents=True)

        ingest.ingest(db, limit=5, out=lambda _: None)

        assert not workspace.artifacts(db).exists()
        assert workspace.artifacts(other).exists()

    def test_a_dry_run_on_no_database_creates_none(self, fake_ci, tmp_path):
        db = tmp_path / "fresh" / "ci.sqlite3"

        totals = ingest.ingest(db, limit=5, dry_run=True, out=lambda _: None)

        assert totals.legs == 1
        assert not db.parent.exists()

    def test_nothing_is_written_to_disk_except_the_database(self, fake_ci, tmp_path):
        db = tmp_path / "sub" / "ci.sqlite3"

        ingest.ingest(db, limit=5, out=lambda _: None)

        assert [p.name for p in db.parent.iterdir()] == ["ci.sqlite3"]

    def test_the_artifact_link_is_kept_so_evidence_can_be_fetched(
        self, fake_ci, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"

        ingest.ingest(db, limit=5, out=lambda _: None)

        with closing(sqlite3.connect(db)) as connection:
            connection.row_factory = sqlite3.Row
            leg = connection.execute("SELECT * FROM leg").fetchone()
            assert leg["artifact_url"] == (
                "https://example.invalid/runs/111/artifacts/222"
            )
            assert leg["node_version"] == "v24.15.0"

    def test_running_again_ingests_nothing_twice(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        second = ingest.ingest(db, limit=5, out=lambda _: None)

        assert second.legs == 0
        assert second.skipped == 1
        with closing(sqlite3.connect(db)) as connection:
            counted = connection.execute("SELECT COUNT(*) FROM test_result").fetchone()[
                0
            ]
        assert counted == 4

    def test_an_expired_artifact_is_counted_rather_than_guessed_at(
        self, fake_ci, tmp_path, monkeypatch
    ):
        gone = github.Artifact(**{**fake_ci["artifact"].__dict__, "expired": True})
        monkeypatch.setattr(ingest.github, "list_test_artifacts", lambda run_id: [gone])

        result = ingest.ingest(tmp_path / "ci.sqlite3", limit=5, out=lambda _: None)

        assert result.expired == 1
        assert result.legs == 0


class TestLogMessages:
    def test_what_the_failing_keyword_logged_is_kept(self, output_xml):
        _, results = parse(output_xml)
        failed = next(r for r in results if r.status == "FAIL")

        assert [m.message for m in failed.log_messages] == [
            "Timeout 5000ms exceeded waiting for #id-4f2a"
        ]
        assert failed.log_messages[0].level == "FAIL"
        assert failed.log_messages[0].keyword == "Fail"

    def test_only_the_failing_keyword_contributes_lines(self, output_xml):
        """The test's own logging is not evidence of why it failed.

        `Log this line is not evidence of anything` runs and passes before the
        teardown breaks; borrowing it would describe work that succeeded.
        """
        _, results = parse(output_xml)
        failed = next(r for r in results if r.name == "Test Failed By Its Teardown")

        messages = [m.message for m in failed.log_messages]
        assert "this line is not evidence of anything" not in messages
        assert messages == ["teardown blew up"]

    def test_a_failing_teardown_is_where_the_lines_come_from(self, output_xml):
        _, results = parse(output_xml)
        failed = next(r for r in results if r.name == "Test Failed By Its Teardown")

        assert failed.log_messages[0].keyword == "Fail"
        assert failed.log_messages[0].level == "FAIL"

    def test_a_passing_test_logs_nothing_into_the_database(self, output_xml):
        _, results = parse(output_xml)

        assert next(r for r in results if r.status == "PASS").log_messages == []

    def test_they_survive_the_round_trip(self, fake_ci, tmp_path):
        from tools.ci_failures.queries import log_messages_by_result

        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        lines = log_messages_by_result(reading_of(db))

        # Keyed on the occurrence, never merged: two failures in one leg keep
        # their own lines, which is the whole reason this replaced the
        # per-group query.
        assert sorted(
            entry.message for entries in lines.values() for entry in entries
        ) == ["Timeout 5000ms exceeded waiting for #id-4f2a", "teardown blew up"]
        assert len(lines) == 2

    def test_no_messages_is_not_an_error(self, tmp_path):
        from tools.ci_failures.queries import log_messages_by_result

        db = tmp_path / "ci.sqlite3"
        connect_db(db).close()

        assert log_messages_by_result(reading_of(db)) == {}


SWALLOWED_SUITE = """\
*** Test Cases ***
Failure Caught By An Expected Error
    Run Keyword And Expect Error    *    Broken Keyword
    Fail    what actually stopped the test

Failure Caught By Try Except
    TRY
        Broken Keyword
    EXCEPT    caught and thrown away
        Log    handled
    END
    Fail    what actually stopped the test

Nothing Is Caught
    Log    quiet
    Fail    what actually stopped the test

*** Keywords ***
Broken Keyword
    Log    the evidence nobody could see
    Fail    caught and thrown away
"""


class TestSwallowedFailures:
    """A failure caught by `Run Keyword And Expect Error` or TRY/EXCEPT is not on
    the branch that stopped the test, so the failing-branch walk turns back at
    the parent and everything it logged is lost. Those lines are the only record
    of what the keyword did."""

    @pytest.fixture
    def results(self, tmp_path):
        _, results = parse(_run_robot(tmp_path, SWALLOWED_SUITE))
        return {r.name: r for r in results}

    def test_an_expected_error_keeps_the_lines_it_swallowed(self, results):
        caught = [
            m
            for m in results["Failure Caught By An Expected Error"].log_messages
            if m.origin
        ]

        assert "the evidence nobody could see" in [m.message for m in caught]
        assert caught[0].origin == "caught by Run Keyword And Expect Error"

    def test_try_except_keeps_them_too(self, results):
        caught = [
            m for m in results["Failure Caught By Try Except"].log_messages if m.origin
        ]

        assert "the evidence nobody could see" in [m.message for m in caught]
        assert caught[0].origin.startswith("caught by ")

    def test_the_failure_that_stopped_the_test_still_leads(self, results):
        """Caught lines are evidence, never the answer, and must not displace it."""
        messages = results["Failure Caught By An Expected Error"].log_messages

        assert messages[0].message == "what actually stopped the test"
        assert messages[0].origin is None

    def test_a_test_that_caught_nothing_gains_nothing(self, results):
        assert [m.origin for m in results["Nothing Is Caught"].log_messages] == [None]

    def test_the_real_failure_is_never_reported_twice(self, results):
        """The failing branch is already collected; descending it again would
        report the same line under two different origins."""
        messages = results["Nothing Is Caught"].log_messages

        assert [m.message for m in messages].count(
            "what actually stopped the test"
        ) == 1


class TestSuiteFixtureFailures:
    """A failed suite teardown fails every test under it, and Robot Framework
    records that only on the tests. The evidence is in the teardown."""

    def test_a_test_that_passed_is_still_marked_failed(self, broken_teardown_xml):
        _, results = parse(broken_teardown_xml)

        assert results[0].name == "A Test That Passes On Its Own"
        assert results[0].status == "FAIL"

    def test_the_lines_come_from_the_teardown_that_actually_failed(
        self, broken_teardown_xml
    ):
        _, results = parse(broken_teardown_xml)

        messages = [m.message for m in results[0].log_messages]
        assert "the suite teardown broke" in messages
        assert "this test itself is fine" not in messages, (
            "the test's own logging is not evidence of the teardown failing"
        )

    def test_they_are_labelled_as_not_belonging_to_the_test(self, broken_teardown_xml):
        _, results = parse(broken_teardown_xml)

        assert {m.origin for m in results[0].log_messages} == {
            "suite teardown of Test.Suite"
        }

    def test_the_keyword_that_logged_them_is_named(self, broken_teardown_xml):
        _, results = parse(broken_teardown_xml)

        assert {m.keyword for m in results[0].log_messages} == {"Fail"}

    def test_only_the_failing_part_of_the_teardown_contributes(
        self, broken_teardown_xml
    ):
        """`Log cleaning up` runs and passes before `Fail` breaks the teardown.

        The same rule as inside a test: only the branch that failed is evidence.
        """
        _, results = parse(broken_teardown_xml)

        assert "cleaning up" not in [m.message for m in results[0].log_messages]

    def test_a_test_with_no_fixture_failure_borrows_nothing(self, output_xml):
        _, results = parse(output_xml)

        assert all(m.origin is None for r in results for m in r.log_messages)


class TestFailureScope:
    """What failed, as opposed to what Robot Framework marked as failed."""

    def test_a_test_that_broke_itself_is_scoped_to_the_test(self, output_xml):
        _, results = parse(output_xml)
        failing = next(r for r in results if r.name == "Failing Test")

        assert failing.failure_scope == "test"
        assert failing.scope_owner == failing.longname

    def test_a_passing_test_has_no_scope(self, output_xml):
        _, results = parse(output_xml)

        assert next(r for r in results if r.status == "PASS").failure_scope is None

    def test_a_suite_teardown_is_scoped_to_the_suite_that_broke(
        self, broken_teardown_xml
    ):
        _, results = parse(broken_teardown_xml)

        assert results[0].failure_scope == "suite_teardown"
        assert results[0].scope_owner == "Test.Suite"

    def test_an_ancestor_teardown_is_attributed_to_the_suite_that_broke(
        self, ancestor_teardown_xml
    ):
        """Not the parent the test sits in, which did nothing wrong."""
        _, results = parse(ancestor_teardown_xml)

        assert results[0].longname == "Outer.Middle.Inner.Scope Test One"
        assert results[0].failure_scope == "suite_teardown"
        assert results[0].scope_owner == "Outer"

    def test_an_ancestor_teardown_still_supplies_its_lines(self, ancestor_teardown_xml):
        _, results = parse(ancestor_teardown_xml)

        messages = [m.message for m in results[0].log_messages]
        assert "the shared server did not shut down" in messages
        assert {m.origin for m in results[0].log_messages} == {
            "suite teardown of Outer"
        }


class TestWhereToLook:
    """The report has to say where to start, not just what broke."""

    def test_the_test_file_and_line_are_recorded(self, output_xml):
        _, results = parse(output_xml)
        failing = next(r for r in results if r.name == "Failing Test")

        assert failing.test_source.endswith("suite.robot")
        assert failing.test_lineno

    def test_a_ci_path_is_made_repo_relative(self):
        from tools.ci_failures.locate import repo_relative

        linux = "/home/runner/work/robotframework-browser/robotframework-browser/atest/test/x.robot"
        windows = (
            r"D:\a\robotframework-browser\robotframework-browser\atest\test\x.robot"
        )

        assert repo_relative(linux) == "atest/test/x.robot"
        assert repo_relative(windows) == "atest/test/x.robot", (
            "the same file must not look like two places"
        )

    def test_a_standard_library_is_told_apart_from_a_test_helper_by_case(self):
        """This repo has atest/library/screenshot.py; Robot Framework ships
        Screenshot. Matching case-insensitively would confuse the two."""
        from tools.ci_failures.locate import owner_kind

        assert owner_kind("screenshot") == "project"
        assert owner_kind("Screenshot") == "standard"
        assert owner_kind("Browser") == "library"
        assert owner_kind("BuiltIn") == "standard"
        assert owner_kind(None) == "unknown"

    def test_a_standard_library_keyword_gets_no_location(self):
        """It lives in site-packages, which is not somewhere to go and edit."""
        from tools.ci_failures.locate import keyword_location

        assert keyword_location("BuiltIn", "Should Be Equal") == (None, None)

    def test_a_library_keyword_is_located_in_this_repo(self):
        from tools.ci_failures.locate import keyword_location

        source, lineno = keyword_location("Browser", "Close Browser")

        assert source == "Browser/keywords/playwright_state.py"
        assert lineno

    def test_an_unimportable_library_costs_a_location_not_an_ingest(self):
        from tools.ci_failures.locate import keyword_location

        assert keyword_location("NoSuchLibraryAnywhere", "Whatever") == (None, None)

    def test_the_owner_of_the_failing_keyword_is_recorded(self, output_xml):
        _, results = parse(output_xml)
        failing = next(r for r in results if r.name == "Failing Test")

        assert failing.keyword_owner == "BuiltIn"
        assert failing.keyword_kind == "standard"

    def test_a_fixture_failure_names_the_keyword_inside_the_fixture(
        self, broken_teardown_xml
    ):
        """The test has no failing keyword of its own; the fixture does."""
        _, results = parse(broken_teardown_xml)

        assert results[0].failing_keyword == "Fail"
        assert results[0].keyword_owner == "BuiltIn"


class TestFixtureFailureGrouping:
    """One broken fixture is one row, however many tests it marked."""

    def _seed(self, db: Path, rows: list[tuple]) -> None:
        connection = connect_db(db)
        for run_id in (1, 2):
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', 'sha', 'main', ?, 'failure', 'u')",
                (run_id, f"2026-08-2{run_id}T10:00:00Z"),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, artifact_url, "
                "platform, ingested_at) VALUES (?, ?, ?, 'Test results-x', 'a-url', "
                "'linux', 'now')",
                (run_id, run_id, run_id),
            )
            for name, suite, status, scope, owner in rows:
                connection.execute(
                    "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                    "status, message, error_signature, failure_scope, scope_owner) "
                    "VALUES (?, ?, ?, ?, ?, 'raw', 'teardown broke', ?, ?)",
                    (run_id, f"{suite}.{name}", name, suite, status, scope, owner),
                )
        connection.commit()
        connection.close()

    def test_four_marked_tests_across_two_runs_are_one_row_of_two(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("Test A", "Outer.Middle", "FAIL", "suite_teardown", "Outer"),
                ("Test B", "Outer.Middle", "FAIL", "suite_teardown", "Outer"),
            ],
        )

        fixtures = fixture_failures(reading_of(db))

        assert len(fixtures) == 1
        assert fixtures[0].occurrences == 2, "two legs, not four test rows"
        assert fixtures[0].tests_marked == 4

    def test_the_tests_it_took_down_are_named(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("Test A", "Outer.Middle", "FAIL", "suite_teardown", "Outer"),
                ("Test B", "Outer.Middle", "FAIL", "suite_teardown", "Outer"),
            ],
        )

        assert sorted(
            fixture_failures(reading_of(db))[0].affected_tests.split(",")
        ) == [
            "Test A",
            "Test B",
        ]

    def test_fixture_failures_are_kept_out_of_the_test_ranking(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("Test A", "Outer.Middle", "FAIL", "suite_teardown", "Outer"),
                ("Test C", "Outer.Middle", "FAIL", "test", "Outer.Middle.Test C"),
            ],
        )

        assert [g.longname for g in failure_groups(reading_of(db))] == [
            "Outer.Middle.Test C"
        ]

    def test_the_denominator_is_how_often_the_suite_ran(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "Outer.Middle", "FAIL", "suite_teardown", "Outer")])

        fixture = fixture_failures(reading_of(db))[0]
        assert fixture.suite_runs == 2
        assert fixture.failure_rate == pytest.approx(1.0)


class TestTheFixtureRuleReachesEveryNumber:
    """A row a broken suite fixture marked is a Fixture Failure everywhere or
    nowhere.

    It was excluded from the Groups and counted in the rates, so one test on the
    working database rendered `1 / 108` in its heading and `2 of 30` in the
    configuration beneath it. Nothing about that looks wrong on the page, which
    is the failure mode this tool exists to catch in others.
    """

    def _seed(self, db: Path) -> None:
        """One test that broke on its own account, and was later marked failed
        by its suite's teardown.

        Two legs, one configuration, so both land in the same rate row. Both
        carry the same Error Signature and different raw messages, which is the
        case that bites: masking is what makes two unrelated failures share a
        key, so the fixture's message lands under the test's own Group.
        """
        connection = connect_db(db)
        rows = [
            (1, "test", None, "the test itself broke", "boom"),
            (2, "suite_teardown", "S", "the teardown broke", "boom"),
        ]
        for run_id, scope, owner, message, signature in rows:
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', 'sha', 'main', ?, 'failure', 'u')",
                (run_id, f"2026-08-2{run_id}T10:00:00Z"),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                "artifact_url, platform, python_version, rf_version, attempt, "
                "ingested_at) VALUES (?, ?, ?, 'Test results-x', 'u', 'linux', "
                "'3.13', '7.4', 1, 'now')",
                (run_id, run_id, run_id),
            )
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                "status, message, error_signature, failure_scope, scope_owner) "
                "VALUES (?, 'S.T', 'T', 'S', 'FAIL', ?, ?, ?, ?)",
                (run_id, message, signature, scope, owner),
            )
        connection.commit()
        connection.close()

    def test_the_rate_agrees_with_the_count_above_it(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db)

        entry = build_report(db).test_failures[0]

        assert entry.counts.failures == 1
        assert [(r.failed, r.ran) for r in entry.rates] == [(1, 2)]

    def test_the_denominator_still_counts_the_run_the_fixture_spoiled(self, tmp_path):
        """`ran` is every row. The test really did run that time, whatever
        failed it - only the numerator is about what the test itself did."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db)

        assert coverage_by_test(reading_of(db))["S.T"][0].ran == 2

    def test_a_fixture_message_is_not_evidence_about_the_test(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db)

        entry = build_report(db).test_failures[0]

        assert [m.message for m in entry.raw_messages] == ["the test itself broke"]

    def test_the_fixture_keeps_its_own_row(self, tmp_path):
        """Excluded from the test's numbers, not from the report."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db)

        fixtures = build_report(db).fixture_failures

        assert [
            (f.suite, f.scope, f.signature, f.counts.failures) for f in fixtures
        ] == [("S", "suite_teardown", "boom", 1)]


class TestVersionsOnAFailure:
    """Which versions a failure was seen on, so "is it version dependent?" is a
    question the report answers rather than one it raises."""

    def _seed(self, db: Path, legs: list[tuple]) -> None:
        connection = connect_db(db)
        for index, (rf, python, node, platform) in enumerate(legs, start=1):
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', 'sha', 'main', ?, 'failure', 'u')",
                (index, f"2026-08-2{index}T10:00:00Z"),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, artifact_url, "
                "platform, rf_version, python_version, node_version, ingested_at) "
                "VALUES (?, ?, ?, 'Test results-x', 'u', ?, ?, ?, ?, 'now')",
                (index, index, index, platform, rf, python, node),
            )
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                "status, message, error_signature, failure_scope) "
                "VALUES (?, 'S.Test A', 'Test A', 'S', 'FAIL', 'raw', 'boom', 'test')",
                (index,),
            )
        connection.commit()
        connection.close()

    def test_the_combinations_are_reported_not_the_dimensions(self, tmp_path):
        """Two legs, each pairing one rf with one Python, is two combinations.

        Listing the dimensions separately would read as four, and would suggest
        the versions can be told apart when a whole leg varies at once.
        """
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("7.1.1", "3.13.15", None, "linux"),
                ("7.4.2", "3.14.7", None, "linux"),
            ],
        )

        configurations = coverage_by_test(reading_of(db))["S.Test A"]

        assert sorted((c.rf_version, c.python_version) for c in configurations) == [
            ("7.1.1", "3.13.15"),
            ("7.4.2", "3.14.7"),
        ]

    def test_a_repeated_combination_is_counted_rather_than_repeated(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("7.4.2", "3.14.7", None, "win32"),
                ("7.4.2", "3.14.7", None, "win32"),
                ("7.1.1", "3.10.11", None, "linux"),
            ],
        )

        configurations = coverage_by_test(reading_of(db))["S.Test A"]

        assert len(configurations) == 2
        assert configurations[0].failed == 2, "most failed first"
        assert configurations[1].failed == 1

    def test_a_fixture_failure_counts_legs_not_the_rows_it_marked(self, tmp_path):
        """One broken teardown marking four tests is one occurrence, not four."""
        db = tmp_path / "ci.sqlite3"
        connection = connect_db(db)
        connection.execute(
            "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
            "conclusion, url) VALUES (1, 'push', 'sha', 'main', '2026-08-20', 'x', 'u')"
        )
        connection.execute(
            "INSERT INTO leg (id, run_id, artifact_id, artifact_name, artifact_url, "
            "platform, rf_version, python_version, ingested_at) "
            "VALUES (1, 1, 1, 'Test results-x', 'u', 'win32', '7.4.2', '3.14.7', 'now')"
        )
        for name in ("A", "B", "C", "D"):
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                "status, error_signature, failure_scope, scope_owner) VALUES "
                "(1, ?, ?, 'S', 'FAIL', 'teardown broke', 'suite_teardown', 'S')",
                (f"S.{name}", name),
            )
        connection.commit()
        connection.close()

        configurations = coverage_by_fixture(reading_of(db))[("S", "suite_teardown")]

        assert len(configurations) == 1
        assert configurations[0].failed == 1, "one leg, not the four rows it marked"
        assert configurations[0].ran == 1


class TestScreenshotEvidence:
    """A screenshot is often the quickest way to see what was on screen."""

    def test_a_screenshot_taken_by_a_passing_keyword_is_still_found(self, tmp_path):
        """The library photographs the page on failure, and that keyword passes.

        It hangs off the failing one, so the failing-branch walk never sees it.
        """
        suite = """\
*** Test Cases ***
Failing With A Screenshot
    Run Keyword And Ignore Error    Log Screenshot Link
    Fail    it broke

*** Keywords ***
Log Screenshot Link
    Log    <a href="browser/screenshot/fail-screenshot-1.png">shot</a>    html=True
"""
        _, results = parse(_run_robot(tmp_path, suite))
        failing = results[0]

        assert failing.screenshot_status == "file"
        assert failing.screenshots == "browser/screenshot/fail-screenshot-1.png"

    def test_every_distinct_picture_is_kept(self, tmp_path):
        """Parsing collects; it does not rank. Which one matters is a question
        about the log lines and is answered at report time, so that changing the
        answer does not cost a re-download."""
        suite = """\
*** Test Cases ***
Several Screenshots
    Log    <a href="browser/screenshot/other.png">a</a>    html=True
    Log    <a href="browser/screenshot/fail-screenshot-1.png">b</a>    html=True
    Fail    it broke
"""
        _, results = parse(_run_robot(tmp_path, suite))

        assert set(results[0].screenshots.split(",")) == {
            "browser/screenshot/other.png",
            "browser/screenshot/fail-screenshot-1.png",
        }

    def test_an_absolute_path_becomes_a_path_inside_the_artifact(self):
        from tools.ci_failures.locate import artifact_relative

        absolute = (
            "file:///home/runner/work/robotframework-browser/robotframework-browser/"
            "atest/output/pabot_results/4/browser/screenshot/fail-screenshot-1.png"
        )

        assert artifact_relative(absolute) == (
            "pabot_results/4/browser/screenshot/fail-screenshot-1.png"
        )

    def test_an_already_relative_path_is_left_alone(self):
        from tools.ci_failures.locate import artifact_relative

        assert artifact_relative("browser/screenshot/fail-screenshot-1.png") == (
            "browser/screenshot/fail-screenshot-1.png"
        )

    def test_one_file_referenced_two_ways_takes_one_slot(self, tmp_path):
        """A pabot leg's merged log names the same picture twice - once with the
        worker prefix, which is where it really sits inside the artifact, and
        once without, which does not exist there at all."""
        suite = """\
*** Test Cases ***
Broken
    Log    <a href="pabot_results/4/browser/screenshot/fail-screenshot-1.png">a</a>    html=True
    Log    <a href="browser/screenshot/fail-screenshot-1.png">b</a>    html=True
    Fail    it broke
"""
        _, results = parse(_run_robot(tmp_path, suite))

        assert results[0].screenshots == (
            "pabot_results/4/browser/screenshot/fail-screenshot-1.png"
        )

    def test_the_merge_stamp_does_not_make_it_a_different_file(self, tmp_path):
        """Robot Framework stamps a merged artifact with the run timestamp and
        the worker, so the file in the directory is not named what the keyword
        that used it logged."""
        suite = """\
*** Test Cases ***
Broken
    Log    <a href="browser/screenshot/20260825_104829-4-fail-screenshot-1.png">a</a>    html=True
    Log    <a href="browser/screenshot/fail-screenshot-1.png">b</a>    html=True
    Fail    it broke
"""
        _, results = parse(_run_robot(tmp_path, suite))

        assert results[0].screenshots == (
            "browser/screenshot/20260825_104829-4-fail-screenshot-1.png"
        )

    def test_no_screenshot_is_itself_recorded(self, tmp_path):
        """Usually it means there was no page to photograph."""
        suite = """\
*** Test Cases ***
Nothing To Photograph
    Log    Keyword 'Take Screenshot' could not be run on failure: no page open
    Fail    it broke
"""
        _, results = parse(_run_robot(tmp_path, suite))

        assert results[0].screenshot_status == "unavailable"
        assert results[0].screenshots is None

    def test_a_passing_test_has_no_screenshot_evidence(self, output_xml):
        _, results = parse(output_xml)

        assert next(r for r in results if r.status == "PASS").screenshot_status is None


class TestEmbeddedScreenshots:
    """An embedded screenshot is not readable text and must not be stored as it."""

    def test_a_base64_payload_becomes_a_note_of_what_it_was(self):
        from tools.ci_failures.parse import strip_embedded_data

        payload = "A" * 4096
        stripped = strip_embedded_data(f'<img src="data:image/png;base64,{payload}">')

        assert "base64" not in stripped
        assert "image/png" in stripped
        assert "KB" in stripped
        assert len(stripped) < 200

    def test_the_rest_of_the_message_survives(self):
        from tools.ci_failures.parse import strip_embedded_data

        stripped = strip_embedded_data("before data:image/png;base64,AAAA after")

        assert stripped.startswith("before ")
        assert stripped.endswith(" after")

    def test_a_message_without_one_is_untouched(self):
        from tools.ci_failures.parse import strip_embedded_data

        assert strip_embedded_data("Difference between pixles is 5046301") == (
            "Difference between pixles is 5046301"
        )
        assert strip_embedded_data(None) is None


class TestListingRunsCostsTheSameForever:
    def test_the_newest_runs_are_asked_for_rather_than_all_of_them(self, monkeypatch):
        """The one call whose cost grew with the age of the repository.

        It walked every page of the workflow's whole history, for both events,
        sorted the lot and then kept the newest few - on every invocation. The
        listing is newest first, so the newest `limit` are on the first page.
        """
        calls = []

        def capture(args, **kwargs):
            calls.append(args)

            class Result:
                returncode = 0
                stdout = '{"workflow_runs": []}'
                stderr = ""

            return Result()

        monkeypatch.setattr(github.subprocess, "run", capture)

        github.list_runs(limit=25)

        assert calls, "nothing was asked of gh"
        for args in calls:
            assert "--paginate" not in args
            assert any("per_page=25" in part for part in args)


class TestOneBadArtifactCostsOneLeg:
    """A full ingest is download-bound and runs for half an hour. Everything that
    can go wrong partway through has to cost the leg it went wrong on and no
    more, and has to be visible in the summary rather than only in the scroll."""

    def test_a_run_whose_artifacts_cannot_be_listed_is_skipped(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """The listing used to sit outside the guard, so a bad response twenty
        minutes in ended the ingest with a traceback and no summary."""

        def refuse(run_id):
            raise github.GhError("502 Bad Gateway")

        monkeypatch.setattr(ingest.github, "list_test_artifacts", refuse)
        db = tmp_path / "ci.sqlite3"

        result = ingest.ingest(db, limit=5, out=lambda _: None)

        assert (result.unlisted, result.legs) == (1, 0)

    def test_an_artifact_that_will_not_unzip_costs_one_leg(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """Catching only GhError let a truncated download end the whole run."""

        def truncated(artifact_id, destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"not a zip")
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", truncated)
        db = tmp_path / "ci.sqlite3"

        result = ingest.ingest(db, limit=5, out=lambda _: None)

        assert (result.unreachable, result.legs) == (1, 0)

    def test_an_artifact_with_no_output_xml_is_never_fetched_twice(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """There is nothing in it to ingest and there never will be, so it is
        remembered. It used to be re-downloaded on every future ingest - ten
        megabytes a time - and counted in no total at all."""
        empty = tmp_path / "empty.zip"
        with zipfile.ZipFile(empty, "w") as archive:
            archive.writestr("log.html", "no output.xml here")
        downloads = []

        def fake_download(artifact_id, destination):
            downloads.append(artifact_id)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(empty.read_bytes())
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", fake_download)
        db = tmp_path / "ci.sqlite3"

        first = ingest.ingest(db, limit=5, out=lambda _: None)
        second = ingest.ingest(db, limit=5, out=lambda _: None)

        assert first.unusable == 1
        assert len(downloads) == 1, "the second ingest downloaded nothing"
        assert second.unusable == 0

    def test_a_dry_run_says_the_size_of_the_job_and_fetches_nothing(
        self, fake_ci, tmp_path, monkeypatch
    ):
        def refuse(artifact_id, destination):
            raise AssertionError("a dry run must not download")

        monkeypatch.setattr(ingest.github, "download_artifact", refuse)
        db = tmp_path / "ci.sqlite3"

        result = ingest.ingest(db, limit=5, out=lambda _: None, dry_run=True)

        assert (result.runs, result.legs) == (1, 1)
        assert one_row(db, "SELECT COUNT(*) AS n FROM leg")["n"] == 0


class TestPruning:
    """The archive keeps 120 days; see ADR 0005."""

    # 120 days after this is 2026-08-21T00:00:00Z: `seed` dates its first Run
    # 2026-08-20 and its second 2026-08-21, one either side.
    NOW = datetime(2026, 12, 19, tzinfo=timezone.utc)

    def test_a_run_older_than_120_days_goes_with_everything_under_it(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS"},
                {"test": "U", "status": "FAIL", "logs": [("INFO", "K", "m")]},
            ],
        )
        run_sql(
            db,
            "INSERT INTO unusable_artifact (artifact_id, run_id, name, reason, "
            "noticed_at) VALUES (99, 1, 'n', 'no output.xml', 'now')",
        )

        with closing(connect_db(db)) as connection:
            pruned = ingest.prune(connection, now=self.NOW)

        assert pruned == 1
        for table in ("run", "leg", "test_result", "log_message", "unusable_artifact"):
            assert one_row(db, f"SELECT COUNT(*) AS n FROM {table}")["n"] == 0, table

    def test_a_run_younger_than_120_days_is_kept_whole(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS", "sha": "old"},
                {"test": "T", "status": "PASS", "sha": "young"},
                {
                    "test": "U",
                    "status": "FAIL",
                    "sha": "young",
                    "logs": [("INFO", "K", "m")],
                },
            ],
        )

        with closing(connect_db(db)) as connection:
            ingest.prune(connection, now=self.NOW)

        assert (
            one_row(db, "SELECT group_concat(head_sha) AS s FROM run")["s"] == "young"
        )
        assert one_row(db, "SELECT COUNT(*) AS n FROM test_result")["n"] == 2
        assert one_row(db, "SELECT COUNT(*) AS n FROM log_message")["n"] == 1

    def test_an_ingest_ends_by_pruning_and_says_so(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "PASS", "sha": "old"}])
        run_sql(db, "UPDATE run SET created_at = '2026-01-01T10:00:00Z'")

        result = ingest.ingest(
            db,
            limit=5,
            out=lambda _: None,
            now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        )

        assert result.pruned == 1
        assert "1 run(s) older than 120 days pruned" in result.line()
        assert one_row(db, "SELECT group_concat(id) AS ids FROM run")["ids"] == "111"

    def test_a_listing_that_fails_still_prunes(self, tmp_path, monkeypatch):
        def unreachable(**kwargs):
            raise github.GhError("gh: not logged in")

        monkeypatch.setattr(ingest.github, "list_runs", unreachable)
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "PASS"}])

        from tools.ci_failures.refusal import UnreachableError

        with pytest.raises(UnreachableError, match="not logged in"):
            ingest.ingest(db, limit=5, out=lambda _: None, now=self.NOW)

        assert one_row(db, "SELECT COUNT(*) AS n FROM run")["n"] == 0

    def test_a_dry_run_says_what_it_would_prune_and_deletes_nothing(
        self, fake_ci, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "PASS", "sha": "old"}])
        run_sql(db, "UPDATE run SET created_at = '2026-01-01T10:00:00Z'")
        said: list[str] = []

        result = ingest.ingest(
            db,
            limit=5,
            out=said.append,
            dry_run=True,
            now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        )

        assert result.pruned == 1
        assert "would prune 1 run(s) older than 2026-04-23" in said
        assert one_row(db, "SELECT COUNT(*) AS n FROM test_result")["n"] == 1


class TestTransientDownloadFailures:
    """A ten megabyte download over a network fails sometimes. Losing one leg is
    ordinary; losing the other hundred and fifty because of it is not."""

    def test_one_unreachable_artifact_does_not_stop_the_rest(
        self, fake_ci, tmp_path, monkeypatch
    ):
        good = fake_ci["artifact"]
        bad = github.Artifact(
            **{**good.__dict__, "id": 999, "name": "Test results-bad"}
        )
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: [bad, good]
        )
        original = ingest.github.download_artifact

        def flaky(artifact_id, destination):
            if artifact_id == 999:
                raise github.GhError("connection reset by peer")
            return original(artifact_id, destination)

        monkeypatch.setattr(ingest.github, "download_artifact", flaky)

        result = ingest.ingest(tmp_path / "ci.sqlite3", limit=5, out=lambda _: None)

        assert result.unreachable == 1
        assert result.legs == 1, "the good artifact still went in"
        assert result.tests == 4

    def test_the_skipped_leg_is_picked_up_next_time(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """Ingest is incremental, so a transient failure costs a run, not a leg."""
        good = fake_ci["artifact"]
        bad = github.Artifact(
            **{**good.__dict__, "id": 999, "name": "Test results-bad"}
        )
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: [bad, good]
        )
        original = ingest.github.download_artifact
        broken = {"still": True}

        def flaky(artifact_id, destination):
            if artifact_id == 999 and broken["still"]:
                raise github.GhError("connection reset by peer")
            return original(artifact_id, destination)

        monkeypatch.setattr(ingest.github, "download_artifact", flaky)
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        broken["still"] = False
        second = ingest.ingest(db, limit=5, out=lambda _: None)

        assert second.legs == 1
        assert second.unreachable == 0

    def test_a_download_is_retried_before_being_given_up_on(
        self, tmp_path, monkeypatch
    ):
        attempts = {"n": 0}

        def failing(args, **kwargs):
            attempts["n"] += 1

            class Result:
                returncode = 1
                stderr = b"connection reset by peer"

            return Result()

        monkeypatch.setattr(github.subprocess, "run", failing)
        monkeypatch.setattr(github.time, "sleep", lambda _: None)

        with pytest.raises(github.GhError, match="after 3 attempts"):
            github.download_artifact(1, tmp_path / "a.zip")

    def test_a_retry_that_succeeds_is_not_an_error(self, tmp_path, monkeypatch):
        attempts = {"n": 0}

        def flaky_then_fine(args, **kwargs):
            attempts["n"] += 1

            class Result:
                returncode = 0 if attempts["n"] > 1 else 1
                stderr = b"connection reset by peer"

            return Result()

        monkeypatch.setattr(github.subprocess, "run", flaky_then_fine)
        monkeypatch.setattr(github.time, "sleep", lambda _: None)

        assert github.download_artifact(1, tmp_path / "a.zip").exists()
        assert attempts["n"] == 2


class TestGrouping:
    """The one behaviour this proof of concept exists to show."""

    def _seed(self, db: Path, rows: list[tuple[str, str, str | None]]) -> None:
        connection = connect_db(db)
        connection.execute(
            "INSERT INTO run (id, event, head_sha, head_branch, created_at, conclusion, url) "
            "VALUES (1, 'push', 'sha', 'main', '2026-08-20T10:00:00Z', 'failure', 'u')"
        )
        connection.execute(
            "INSERT INTO leg (id, run_id, artifact_id, artifact_name, artifact_url, "
            "platform, ingested_at) VALUES (1, 1, 9, 'Test results-x', 'a-url', 'linux', 'now')"
        )
        for longname, status, signature in rows:
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, status, "
                "message, error_signature) VALUES (1, ?, ?, 'S', ?, ?, ?)",
                (longname, longname, status, signature and "raw", signature),
            )
        connection.commit()
        connection.close()

    def test_one_test_failing_on_two_errors_is_two_groups(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [("Test A", "FAIL", "error X")] * 2
            + [("Test A", "FAIL", "error Y")] * 4
            + [("Test A", "PASS", None)] * 4,
        )

        groups = failure_groups(reading_of(db))

        assert [(g.error_signature, g.failures) for g in groups] == [
            ("error Y", 4),
            ("error X", 2),
        ]

    def test_the_denominator_counts_every_run_including_the_passes(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db, [("Test A", "FAIL", "error X")] * 2 + [("Test A", "PASS", None)] * 8
        )

        group = failure_groups(reading_of(db))[0]

        assert group.failures == 2
        assert group.total_runs == 10
        assert group.failure_rate == pytest.approx(0.2)

    def test_a_test_that_never_failed_is_absent(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "PASS", None)] * 5)

        assert failure_groups(reading_of(db)) == []

    def test_totals_count_passes_and_failures_apart(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "FAIL", "error X")] + [("Test B", "PASS", None)] * 3)

        summary = totals(reading_of(db))

        assert summary.results == 4
        assert summary.failures == 1
        assert summary.tests == 2


class TestCaseFoldedGrouping:
    """`Deadline Exceeded` and `Deadline exceeded` are one problem.

    grpcio's C core spells it with a capital when the Python client's deadline
    timer fires; @grpc/grpc-js spells it small when the Node server's timer wins
    the same race. Two libraries naming one condition, not two conditions.
    """

    def _deadlines(self) -> list[dict]:
        return [
            {"test": "T", "status": "FAIL", "signature": "Deadline Exceeded"},
            {"test": "T", "status": "FAIL", "signature": "Deadline Exceeded"},
            {"test": "T", "status": "FAIL", "signature": "Deadline exceeded"},
        ]

    def test_two_spellings_of_one_error_are_one_group(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, self._deadlines())

        groups = failure_groups(reading_of(db))

        assert len(groups) == 1
        assert groups[0].failures == 3

    def test_the_merged_group_is_keyed_case_insensitively(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, self._deadlines())

        assert failure_groups(reading_of(db))[0].signature_key == "deadline exceeded"

    def test_the_spellings_survive_the_merge(self, tmp_path):
        """Which side of the boundary gave up first is evidence, not noise."""
        db = tmp_path / "ci.sqlite3"
        seed(db, self._deadlines())

        variants = signature_variants(reading_of(db))[
            ("T", "test", "deadline exceeded")
        ]

        assert variants == [
            VariantRow(signature="Deadline Exceeded", occurrences=2),
            VariantRow(signature="Deadline exceeded", occurrences=1),
        ]

    def test_a_group_with_one_spelling_reports_no_variants(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert signature_variants(reading_of(db)) == {}

    def test_suite_fixtures_are_merged_the_same_way(self, tmp_path):
        """Where it actually happens: the real case is a suite teardown."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                dict(row, scope="suite_teardown", owner="Suite X", sha=f"sha{i}")
                for i, row in enumerate(self._deadlines())
            ],
        )

        fixtures = fixture_failures(reading_of(db))

        assert len(fixtures) == 1
        assert fixtures[0].occurrences == 3
        assert (
            len(
                fixture_signature_variants(reading_of(db))[
                    ("Suite X", "suite_teardown", "deadline exceeded")
                ]
            )
            == 2
        )


class TestPayloadForALanguageModel:
    """What the JSON document carries that the page cannot show.

    Not the page reformatted: rates with their denominators, the
    configurations that never ran the test, the commit behind every
    occurrence, and every raw message the signature masked away.
    """

    def _entry(self, db: Path, test: str = "T") -> dict:
        return next(t for t in build_json(db)["test_failures"] if t["test"] == test)

    def test_a_configuration_that_never_failed_keeps_its_denominator(self, tmp_path):
        """0 of 4 on darwin is evidence. A global rate cannot say it."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom"}] * 3
            + [{"test": "T", "status": "PASS"}] * 5
            + [{"test": "T", "status": "PASS", "platform": "darwin"}] * 4,
        )

        coverage = coverage_by_test(reading_of(db))["T"]

        assert {c.platform: (c.ran, c.failed) for c in coverage} == {
            "linux": (8, 3),
            "darwin": (4, 0),
        }

    def test_a_platform_the_test_never_ran_on_is_named(self, tmp_path):
        """Absent and clean are opposite findings. A zero cannot tell them apart."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom"}]
            + [{"test": "Other", "status": "PASS", "platform": "win32"}],
        )

        assert self._entry(db)["never_ran_on"] == ["win32"]

    def test_every_distinct_raw_message_is_kept(self, tmp_path):
        """The signature masks what varies, which is exactly the evidence."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "diff <n>",
                    "message": "diff 5046301",
                }
            ]
            * 2
            + [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "diff <n>",
                    "message": "diff 5046304",
                }
            ],
        )

        assert self._entry(db)["raw_messages"] == [
            {"message": "diff 5046301", "occurrences": 2},
            {"message": "diff 5046304", "occurrences": 1},
        ]

    def test_the_commit_of_every_occurrence_is_carried(self, tmp_path):
        """Three failures across two commits is not three across one."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom", "sha": "aaa"}] * 2
            + [{"test": "T", "status": "FAIL", "signature": "boom", "sha": "bbb"}],
        )

        entry = self._entry(db)

        assert entry["counts"]["distinct_commits"] == 2
        assert {o["commit"] for o in entry["occurrences"]} == {"aaa", "bbb"}
        assert len(entry["occurrences"]) == 3

    def test_occurrences_carry_the_artifact_to_fetch_evidence_from(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert self._entry(db)["occurrences"][0]["artifact_url"] == "a-url"

    def test_a_broken_suite_fixture_is_not_a_test_failure(self, tmp_path):
        """Section 3, stated in the document rather than left to be inferred."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": f"T{i}",
                    "status": "FAIL",
                    "signature": "boom",
                    "scope": "suite_teardown",
                    "owner": "Suite X",
                }
                for i in range(4)
            ],
        )

        document = build_json(db)

        assert document["test_failures"] == []
        assert document["fixture_failures"][0]["suite"] == "Suite X"
        assert document["fixture_failures"][0]["counts"]["test_rows_marked_failed"] == 4

    def test_the_document_states_the_rules_it_was_built_on(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert "suite_fixtures_are_separate" in build_json(db)["about"]

    def test_nothing_is_truncated(self, tmp_path):
        """The terminal report cuts at 110 characters for a narrow terminal."""
        db = tmp_path / "ci.sqlite3"
        long_message = "x" * 400
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "boom",
                    "message": long_message,
                }
            ],
        )

        assert self._entry(db)["raw_messages"][0]["message"] == long_message

    def test_where_to_look_survives_into_the_document(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        connection = connect_db(db)
        connection.execute(
            "UPDATE test_result SET test_source = 'a.robot', test_lineno = 237, "
            "keyword_source = 'b.py', keyword_lineno = 27, keyword_kind = 'project'"
        )
        connection.commit()
        connection.close()

        assert self._entry(db)["where_to_look"] == {
            "test_file": "a.robot:237",
            "keyword": None,
            "keyword_defined": "b.py:27",
            "keyword_owner": None,
            "keyword_kind": "project",
        }


class TestWhatSurroundedTheFailure:
    """A failure on its own is a symptom. These are the facts around it.

    Nothing here is a flakiness verdict; the document states none, deliberately.
    What was missing was the evidence a reader needs to reach one, all of which
    was already in the database and none of which was ever asked for.
    """

    def _occurrence(self, db: Path, test: str = "T") -> dict:
        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == test)
        return entry["occurrences"][0]

    def test_the_runs_either_side_of_a_failure_are_reported(self, tmp_path):
        """One failure between two passes is a blip. The same failure with a
        passing run before it and failures after is where something broke."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS", "sha": "one"},
                {"test": "T", "status": "FAIL", "signature": "boom", "sha": "two"},
                {"test": "T", "status": "PASS", "sha": "three"},
            ],
        )

        around = self._occurrence(db)

        assert around["previous_run_on_this_leg"]["outcome"] == "pass"
        assert around["previous_run_on_this_leg"]["commit"] == "one"
        assert around["next_run_on_this_leg"]["outcome"] == "pass"
        assert around["next_run_on_this_leg"]["commit"] == "three"

    def test_the_neighbours_are_the_same_leg_not_the_next_run(self, tmp_path):
        """A test that fails on win32 learns nothing from the linux run that
        happened to come next, and reading one as the other invents a trend."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "boom",
                    "platform": "win32",
                    "sha": "one",
                },
                {"test": "T", "status": "PASS", "platform": "linux", "sha": "two"},
            ],
        )

        assert self._occurrence(db)["next_run_on_this_leg"] is None

    def test_a_failure_at_the_edge_of_the_window_has_no_neighbour(self, tmp_path):
        """Absent is reported as absent. A missing run is not a passing one."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        around = self._occurrence(db)

        assert around["previous_run_on_this_leg"] is None
        assert around["next_run_on_this_leg"] is None

    def test_a_hand_rerun_that_passed_is_reported(self, tmp_path):
        """The one comparison that holds the commit constant. A regression the
        next commit fixed also has passing neighbours; only this separates them."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 1},
                {"test": "T", "status": "PASS", "attempt": 2},
            ],
        )

        assert self._occurrence(db)["retry"] == {
            "attempts": 2,
            "passed_on_another_attempt": True,
        }

    def test_a_leg_that_ran_once_reports_no_retry(self, tmp_path):
        """Nothing retries automatically here, so no retry means nobody pressed
        the button. That is a fact about queue time, not about the failure, and
        it must not read as one."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert self._occurrence(db)["retry"] is None

    def test_what_else_broke_in_the_same_leg_is_named(self, tmp_path):
        """Take Screenshot fails, the VAR after it never runs, and two later
        suites fail on a variable nobody set. Three entries, one event."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "First", "status": "FAIL", "signature": "screenshot"},
                {"test": "Second", "status": "FAIL", "signature": "no variable"},
            ],
        )

        assert self._occurrence(db, "Second")["also_failed_in_this_leg"] == [
            {"subject": "First", "scope": "test"}
        ]

    def test_a_leg_that_broke_wholesale_says_what_it_left_out(self, tmp_path):
        """A list that stops without saying so reads as a complete one."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom"}]
            + [
                {"test": f"Other{index}", "status": "FAIL", "signature": "boom"}
                for index in range(30)
            ],
        )

        occurrence = self._occurrence(db)

        assert len(occurrence["also_failed_in_this_leg"]) == 25
        assert occurrence["also_failed_in_this_leg_not_listed"] == 5

    def test_how_long_the_test_takes_when_it_passes(self, tmp_path):
        """A timeout message cannot say whether a keyword broke or a budget was
        always too thin. The passing runs can."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "timeout", "elapsed": 2056}]
            + [
                {"test": "T", "status": "PASS", "elapsed": ms, "sha": f"s{ms}"}
                for ms in (1001, 1400, 1853)
            ],
        )

        durations = pass_durations_by_test(reading_of(db))

        assert durations[("T", "linux", "3.13.15", "7.4.2", None, None)] == Spread(
            min=1001, median=1400, p95=1853, max=1853
        )

    def test_the_passing_durations_reach_the_document(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "timeout", "elapsed": 9}]
            + [{"test": "T", "status": "PASS", "elapsed": 5, "sha": "two"}],
        )

        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == "T")

        assert entry["rates"][0]["pass_ms"]["max"] == 5

    def test_a_configuration_with_no_passes_carries_no_durations(self, tmp_path):
        """A test that has only ever failed on a leg has no margin to report."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom", "elapsed": 9}])

        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == "T")

        assert entry["rates"][0]["pass_ms"] is None

    def test_the_newest_run_is_reported_with_its_failure_count(self, tmp_path):
        """The rates say how often things break, not whether the head is green."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "sha": "old"},
                {"test": "T", "status": "PASS", "sha": "new"},
            ],
        )

        assert latest_run(reading_of(db)).commit == "new"
        assert latest_run(reading_of(db)).failures == 0
        assert build_json(db)["window"]["latest_run"]["failures"] == 0

    def test_only_tests_that_failed_are_measured(self, tmp_path):
        """The report is asked about failures. Timing every passing test in the
        window would price the query at the size of the database."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "elapsed": 9},
                {"test": "T", "status": "PASS", "elapsed": 5, "sha": "two"},
                {"test": "Healthy", "status": "PASS", "elapsed": 5},
                {"test": "Healthy", "status": "PASS", "elapsed": 6, "sha": "two"},
            ],
        )

        assert {key[0] for key in pass_durations_by_test(reading_of(db))} == {"T"}
        assert len(runs_either_side(reading_of(db))) == 1


class TestFixtureEntriesAskTheSameQuestions:
    """A suite fixture entry carried none of what section 6 added for tests.

    It is the most frequent failure in the window and it was the one entry with
    no denominators, no raw messages, and nothing to hang the evidence on: the
    configurations it had been seen on, counted, with nothing to count against.
    """

    def _fixture(self, db: Path) -> dict:
        return build_json(db)["fixture_failures"][0]

    def _broke(self, marking: int = 2, **row) -> list[dict]:
        """One leg where the suite teardown failed, marking `marking` tests."""
        return [
            {
                "test": f"T{index}",
                "status": "FAIL",
                "signature": "deadline",
                "scope": "suite_teardown",
                "owner": "Suite X",
                "suite": "Suite X",
                **row,
            }
            for index in range(marking)
        ]

    def _ran_clean(self, **row) -> list[dict]:
        return [
            {"test": f"T{index}", "status": "PASS", "suite": "Suite X", **row}
            for index in range(2)
        ]

    def test_an_occurrence_is_one_leg_not_one_marked_test_row(self, tmp_path):
        """Five teardown failures produced ten failed tests. Listing ten
        occurrences puts back the count section 3 exists to remove."""
        db = tmp_path / "ci.sqlite3"
        seed(db, self._broke(marking=4))

        fixture = self._fixture(db)

        assert fixture["counts"]["test_rows_marked_failed"] == 4
        assert len(fixture["occurrences"]) == 1
        assert fixture["occurrences"][0]["tests_marked"] == 4

    def test_the_denominator_counts_legs_that_ran_the_suite(self, tmp_path):
        """`seen_on` said which legs it had been seen failing on and how often,
        with nothing to divide by. 5 occurrences is not a rate."""
        db = tmp_path / "ci.sqlite3"
        seed(db, self._broke() + self._ran_clean(sha="two"))

        fixture = self._fixture(db)

        assert [(r["ran"], r["failed"]) for r in fixture["rates"]] == [(2, 1)]
        assert (
            sum(r["ran"] for r in fixture["rates"]) == fixture["counts"]["suite_runs"]
        )

    def test_a_configuration_the_fixture_never_broke_on_keeps_its_denominator(
        self, tmp_path
    ):
        """win32 breaking 5 times in 59 while nothing else breaks in 55 is the
        whole finding, and it is invisible without the clean configurations."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            self._broke(platform="win32")
            + self._ran_clean(sha="two", platform="win32")
            + self._ran_clean(platform="linux")
            + self._ran_clean(sha="two", platform="linux"),
        )

        assert {
            (c.platform, c.ran, c.failed)
            for c in coverage_by_fixture(reading_of(db))[("Suite X", "suite_teardown")]
        } == {("win32", 2, 1), ("linux", 2, 0)}

    def test_a_fixture_rate_carries_no_pass_duration(self, tmp_path):
        """A suite fixture has no duration of its own in the database. A field
        that is null on every row reads as a measurement that failed."""
        db = tmp_path / "ci.sqlite3"
        seed(db, self._broke())

        assert "pass_ms" not in self._fixture(db)["rates"][0]

    def test_the_runs_either_side_of_a_broken_fixture_are_reported(self, tmp_path):
        """A fixture has no status row of its own: the leg passed if the suite
        ran there and the fixture is not among the failures."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            self._ran_clean(sha="one")
            + self._broke(sha="two")
            + self._ran_clean(sha="three"),
        )

        occurrence = self._fixture(db)["occurrences"][0]

        assert occurrence["previous_run_on_this_leg"]["outcome"] == "pass"
        assert occurrence["next_run_on_this_leg"]["outcome"] == "pass"

    def test_a_hand_rerun_of_a_broken_fixture_is_reported(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, self._broke(attempt=1) + self._ran_clean(attempt=2))

        assert self._fixture(db)["occurrences"][0]["retry"] == {
            "attempts": 2,
            "passed_on_another_attempt": True,
        }

    def test_the_tests_the_fixture_marked_are_not_listed_as_context(self, tmp_path):
        """They are its own damage, already counted once. Restating them as
        context makes one event look like a leg falling apart."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            self._broke()
            + [{"test": "Unrelated", "status": "FAIL", "signature": "other"}],
        )

        assert self._fixture(db)["occurrences"][0]["also_failed_in_this_leg"] == [
            {"subject": "Unrelated", "scope": "test"}
        ]

    def test_a_raw_message_is_counted_in_legs_not_in_marked_rows(self, tmp_path):
        """Robot Framework writes the fixture's message onto every test it
        marked, so counting rows reports one teardown failure as four."""
        db = tmp_path / "ci.sqlite3"
        seed(db, self._broke(marking=4, message="Deadline Exceeded"))

        assert self._fixture(db)["raw_messages"] == [
            {"message": "Deadline Exceeded", "occurrences": 1}
        ]


class TestWhichAttemptRanIt:
    """GitHub will not say which attempt uploaded an artifact.

    The artifact carries no attempt number, and `/runs/{id}/attempts/{n}/
    artifacts` answers 404. What is available is time.
    """

    def _artifact(self, id_: int, created_at: str) -> github.Artifact:
        return github.Artifact(
            id=id_, name="Test results-x", expired=False, url="u", created_at=created_at
        )

    def test_an_artifact_belongs_to_the_last_attempt_already_started(self):
        """Attempts of one run do not overlap, so time settles it. Checked
        against a run re-run twice, where the three uploads of one leg fall one
        inside each attempt's window with minutes to spare."""
        starts = [(1, "2026-08-19T17:14:38Z"), (2, "2026-08-19T17:43:17Z")]
        starts.append((3, "2026-08-19T17:57:03Z"))

        resolved = github.with_attempts(
            [
                self._artifact(1, "2026-08-19T17:22:21Z"),
                self._artifact(2, "2026-08-19T17:50:56Z"),
                self._artifact(3, "2026-08-19T18:04:48Z"),
            ],
            starts,
        )

        assert [a.attempt for a in resolved] == [1, 2, 3]

    def test_a_run_nobody_rebuilt_puts_everything_on_the_first_attempt(self):
        resolved = github.with_attempts(
            [self._artifact(1, "2026-08-19T17:22:21Z")], [(1, "2026-08-19T17:14:38Z")]
        )

        assert [a.attempt for a in resolved] == [1]

    def test_an_artifact_with_no_creation_time_falls_to_the_first_attempt(self):
        """An unknown lands on the reading that claims least."""
        resolved = github.with_attempts(
            [self._artifact(1, "")],
            [(1, "2026-08-19T17:14:38Z"), (2, "2026-08-19T17:43:17Z")],
        )

        assert [a.attempt for a in resolved] == [1]

    def test_a_run_nobody_rebuilt_costs_no_request(self, monkeypatch):
        """Nearly every run. Paying a request each to learn nothing would make
        the ingest slower for the sake of a column that is already known."""

        def refuse(endpoint):
            raise AssertionError(f"asked GitHub for {endpoint}")

        monkeypatch.setattr(github, "_api", refuse)
        run = github.Run(
            id=1,
            event="push",
            head_sha="s",
            head_branch="main",
            created_at="2026-08-19T17:14:38Z",
            conclusion="failure",
            url="u",
            run_attempt=1,
        )

        assert github.attempt_starts(run) == [(1, "2026-08-19T17:14:38Z")]

    def test_a_column_added_later_is_added_to_a_database_that_predates_it(
        self, tmp_path
    ):
        """The database is rebuildable, but rebuilding it is three gigabytes of
        downloads and this column can be filled in from the API for a tenth of
        one."""
        db = tmp_path / "ci.sqlite3"
        connection = sqlite3.connect(db)
        connection.executescript(
            "CREATE TABLE leg (id INTEGER PRIMARY KEY, run_id INTEGER, "
            "artifact_id INTEGER, artifact_name TEXT, platform TEXT, "
            "ingested_at TEXT);"
        )
        connection.commit()
        connection.close()

        connection = connect_db(db)
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(leg)")}
        connection.close()

        assert "attempt" in columns

    def test_the_backfill_resolves_legs_ingested_before_it_existed(
        self, tmp_path, monkeypatch
    ):
        db = tmp_path / "ci.sqlite3"
        connection = connect_db(db)
        connection.execute(
            "INSERT INTO run (id, created_at) VALUES (7, '2026-08-19T17:14:38Z')"
        )
        for leg_id, artifact_id in ((1, 11), (2, 22)):
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                "ingested_at) VALUES (?, ?, ?, 'leg', 'now')",
                (leg_id, 7, artifact_id),
            )
        connection.commit()
        connection.close()

        run = github.Run(
            id=7,
            event="push",
            head_sha="s",
            head_branch="main",
            created_at="2026-08-19T17:14:38Z",
            conclusion="failure",
            url="u",
            run_attempt=2,
        )
        monkeypatch.setattr(github, "get_run", lambda run_id: run)
        monkeypatch.setattr(
            github,
            "attempt_starts",
            lambda run: [
                (1, "2026-08-19T17:14:38Z"),
                (2, "2026-08-19T17:43:17Z"),
            ],
        )
        monkeypatch.setattr(
            github,
            "list_test_artifacts",
            lambda run_id: [
                github.Artifact(11, "leg", False, "u", "2026-08-19T17:22:21Z"),
                github.Artifact(22, "leg", False, "u", "2026-08-19T17:50:56Z"),
            ],
        )

        filled = ingest.backfill_attempts(db, out=lambda _: None)

        connection = connect_db(db)
        assert filled == 2
        assert [
            row["attempt"]
            for row in connection.execute("SELECT attempt FROM leg ORDER BY id")
        ] == [1, 2]
        connection.close()

    def test_an_ingested_rerun_lands_on_the_right_attempt(
        self, tmp_path, monkeypatch, output_xml
    ):
        """End to end: the attempt is resolved while ingesting, not afterwards,
        so only databases predating the column ever need the backfill."""
        run = github.Run(
            id=111,
            event="push",
            head_sha="abc123",
            head_branch="main",
            created_at="2026-08-19T17:14:38Z",
            conclusion="failure",
            url="u",
            run_attempt=2,
        )
        artifacts = [
            github.Artifact(1, "leg", False, "u", "2026-08-19T17:22:21Z"),
            github.Artifact(2, "leg", False, "u", "2026-08-19T17:50:56Z"),
        ]
        zip_path = tmp_path / "artifact.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.write(output_xml, "output.xml")

        monkeypatch.setattr(ingest.github, "list_runs", lambda **kwargs: [run])
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: artifacts
        )
        monkeypatch.setattr(
            ingest.github,
            "attempt_starts",
            lambda run: [
                (1, "2026-08-19T17:14:38Z"),
                (2, "2026-08-19T17:43:17Z"),
            ],
        )

        def fake_download(artifact_id, destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zip_path.read_bytes())
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", fake_download)

        db = tmp_path / "ci.sqlite3"
        ingest.ingest(
            db,
            limit=5,
            out=lambda _: None,
            now=datetime(2026, 8, 20, tzinfo=timezone.utc),
        )

        connection = connect_db(db)
        assert [
            row["attempt"]
            for row in connection.execute(
                "SELECT attempt FROM leg ORDER BY artifact_id"
            )
        ] == [1, 2]
        connection.close()

    def test_a_leg_the_api_cannot_place_stays_unknown(self, tmp_path, monkeypatch):
        """Never defaulted to 1. A value invented for a leg nobody measured is
        indistinguishable from one that was."""
        db = tmp_path / "ci.sqlite3"
        connection = connect_db(db)
        connection.execute("INSERT INTO run (id, created_at) VALUES (7, 'x')")
        connection.execute(
            "INSERT INTO leg (id, run_id, artifact_id, artifact_name, ingested_at) "
            "VALUES (1, 7, 11, 'leg', 'now')"
        )
        connection.commit()
        connection.close()

        def gone(run_id):
            raise github.GhError("run not found")

        monkeypatch.setattr(github, "get_run", gone)

        ingest.backfill_attempts(db, out=lambda _: None)

        connection = connect_db(db)
        assert connection.execute("SELECT attempt FROM leg").fetchone()[0] is None
        assert totals(reading_of(db)).legs_without_attempt == 1
        connection.close()


class TestTheDenominatorAndTheRerun:
    """A leg is only ever re-run because it failed, so re-attempts land exactly
    where the failures are and pull every rate down with them."""

    def _counts(self, db: Path, test: str = "T") -> dict:
        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == test)
        return entry["counts"]

    def test_a_rerun_inflates_the_ordinary_denominator(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 1},
                {"test": "T", "status": "PASS", "attempt": 2},
            ],
        )

        counts = self._counts(db)

        assert (counts["failures"], counts["ran"]) == (1, 2)
        assert (
            counts["first_attempt"]["failures"],
            counts["first_attempt"]["ran"],
        ) == (1, 1)

    def test_a_failure_on_a_rerun_is_not_a_first_attempt_failure(self, tmp_path):
        """Counting only the last attempt is the other obvious choice and is
        wrong - the last attempt is the one that passed."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS", "attempt": 1},
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 2},
            ],
        )

        counts = self._counts(db)

        assert counts["failures"] == 1
        assert counts["first_attempt"] == {"failures": 0, "ran": 1, "rate": 0.0}

    def test_a_group_whose_every_failure_was_a_rerun_keeps_its_denominator(
        self, tmp_path
    ):
        """Zero of 1 is a finding. A group vanishing from the count is not."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS", "attempt": 1},
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 2},
            ],
        )

        runs, failures = first_attempt_counts_by_test(reading_of(db))

        assert runs["T"] == 1
        assert ("T", "boom") not in failures

    def test_the_attempt_is_on_every_occurrence(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "T", "status": "PASS", "attempt": 1},
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 2},
            ],
        )

        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == "T")

        assert entry["occurrences"][0]["attempt"] == 2

    def test_legs_nobody_could_place_are_counted_in_the_window(self, tmp_path):
        """While it is above zero, a first-attempt rate is a floor."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        connection = connect_db(db)
        connection.execute("UPDATE leg SET attempt = NULL")
        connection.commit()
        connection.close()

        assert build_json(db)["window"]["legs_with_unknown_attempt"] == 1


class TestHtmlReport:
    def test_it_renders_a_self_contained_page(self, tmp_path):
        from tools.ci_failures.render_html import write as write_page

        db = tmp_path / "ci.sqlite3"
        connect_db(db).close()

        page = write_page(build_report(db), tmp_path / "report.html")

        text = page.read_text(encoding="utf-8")
        assert "<title>Browser CI Failures</title>" in text
        # Google Fonts is the only external host the artifact CSP admits.
        assert "fonts.googleapis.com" in text
        assert "<script" not in text


class TestWhatThePageCanNowReach:
    """Four things the Report held that only the JSON Rendering ever showed, and
    one the page showed that the document never carried.

    None of it was a decision anybody made. Each renderer assembled its own
    document from the same queries, so a field arrived in whichever one its
    author happened to be editing.
    """

    def _page(self, db: Path, tmp_path: Path, **kwargs) -> str:
        from tools.ci_failures.render_html import write as write_page

        return write_page(
            build_report(db, **kwargs), tmp_path / "report.html"
        ).read_text(encoding="utf-8")

    def test_the_page_carries_the_messages_behind_the_signature(self, tmp_path):
        """The mask is what makes grouping possible and also what throws the
        evidence away. Three failures sharing a signature can differ by the one
        number that says whether it is deterministic."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "Box (<n>, <n>) has difference of <n>",
                    "message": "Box (0, 117) has difference of 5046301",
                },
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "Box (<n>, <n>) has difference of <n>",
                    "message": "Box (0, 117) has difference of 5046298",
                },
            ],
        )

        page = self._page(db, tmp_path)

        assert "distinct message" in page
        assert "5046301" in page
        assert "5046298" in page

    def test_the_page_names_the_spellings_a_group_merged(self, tmp_path):
        """Which side of the gRPC boundary gave up first is real information,
        and the case-folded key throws the spelling away from the heading."""
        db = tmp_path / "ci.sqlite3"
        seed(db, TestCaseFoldedGrouping()._deadlines())

        page = self._page(db, tmp_path)

        assert "spelled 2 ways" in page
        assert "Deadline Exceeded" in page
        assert "Deadline exceeded" in page

    def test_the_page_says_what_moved_since_the_baseline(self, tmp_path):
        from tools.ci_failures.annotations import write_snapshot

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "was here before"}])
        write_snapshot(db, [("Gone Test", "an error nobody sees now", 4)])

        page = self._page(db, tmp_path)

        assert "Since the last report" in page
        assert "Gone Test" in page
        assert 'data-kind="gone"' in page
        assert 'data-kind="new"' in page

    def test_the_page_says_which_kind_of_absence_a_missing_baseline_is(self, tmp_path):
        """Nobody has taken one, and a windowed report cannot use one, are
        different facts. Neither is "nothing changed"."""
        from datetime import datetime, time

        from tools.ci_failures.window import of_days

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "e"}])

        # A window the seeded run falls inside: an empty one is refused
        # outright now, which is a different message and a different test.
        seeded_day = datetime(2026, 8, 20, 12, 0).astimezone()

        never_taken = self._page(db, tmp_path)
        windowed = self._page(db, tmp_path, window=of_days(1, seeded_day))

        assert "No baseline has been taken" in never_taken
        assert "windowed report has no baseline" in windowed

    def test_the_page_states_the_rules_rather_than_restating_them(self, tmp_path):
        """The fixture rule used to be authored twice - once in `about` for the
        document, once in the page's own prose - with nothing keeping the two in
        agreement."""
        from tools.ci_failures.report import ABOUT

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "e"}])

        page = self._page(db, tmp_path)

        assert "How these numbers are built" in page
        assert "suite_fixtures_are_separate" in page
        assert ABOUT["suite_fixtures_are_separate"][:60] in page

    def test_the_document_carries_the_platform_breakdown(self, tmp_path):
        """The page had it and the document did not, which is the drift running
        the other way."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "e"}])

        platforms = build_json(db)["platforms"]

        assert platforms
        assert {"platform", "install", "legs", "failures", "per_leg"} == set(
            platforms[0]
        )


class TestWhatAFixtureMarkingIsNotEvidenceOf:
    """A broken suite fixture fails every test beneath it. Those rows are the
    fixture's outcome and not the test's, and two places were reading them as
    though they were the test's."""

    def _seed(self, db: Path, runs: list[tuple[int, list[tuple]]]) -> None:
        """runs of (run_id, [(longname, status, failure_scope, scope_owner)])."""
        connection = connect_db(db)
        for run_id, rows in runs:
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', ?, 'main', ?, 'failure', 'u')",
                (run_id, f"sha{run_id}", f"2026-08-1{run_id}T10:00:00Z"),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                "artifact_url, platform, attempt, ingested_at) VALUES "
                "(?, ?, ?, 'Test results-x', 'u', 'linux', 1, 'now')",
                (run_id, run_id, run_id),
            )
            for longname, status, scope, owner in rows:
                connection.execute(
                    "INSERT INTO test_result (leg_id, longname, name, "
                    "suite_longname, status, message, error_signature, "
                    "failure_scope, scope_owner) VALUES (?, ?, ?, 'S', ?, ?, ?, ?, ?)",
                    (
                        run_id,
                        longname,
                        longname,
                        status,
                        "raw" if status == "FAIL" else None,
                        "boom" if status == "FAIL" else None,
                        scope,
                        owner,
                    ),
                )
        connection.commit()
        connection.close()

    def test_a_broken_fixture_is_one_line_naming_the_suite(self, tmp_path):
        """Not one line for each of the tests it marked. Twelve names that are
        one event bury the test that broke on its own account."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (
                    1,
                    [
                        ("S.Broke", "FAIL", "test", None),
                        ("S.Marked1", "FAIL", "suite_teardown", "S"),
                        ("S.Marked2", "FAIL", "suite_teardown", "S"),
                        ("S.Marked3", "FAIL", "suite_teardown", "S"),
                    ],
                )
            ],
        )

        entry = next(e for e in build_report(db).test_failures if e.test == "S.Broke")

        assert [
            (c.subject, c.scope) for c in entry.occurrences[0].also_failed_in_this_leg
        ] == [("S", "suite_teardown")]

    def test_an_adjacent_run_the_fixture_decided_has_no_verdict(self, tmp_path):
        """The run happened and the test ran in it, so null would be wrong -
        that already means there was no such run. It failed, so `fail` would be
        wrong too: nothing about this test broke."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (1, [("S.T", "FAIL", "suite_teardown", "S")]),
                (2, [("S.T", "FAIL", "test", None)]),
                (3, [("S.T", "PASS", None, None)]),
            ],
        )

        entry = build_report(db).test_failures[0]
        occurrence = entry.occurrences[0]

        assert occurrence.previous_run_on_this_leg.outcome == "suite broke"
        assert occurrence.next_run_on_this_leg.outcome == "pass"

    def test_a_run_where_the_test_itself_failed_still_says_fail(self, tmp_path):
        """The abstention is only for runs where the fixture was the whole
        story."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (1, [("S.T", "FAIL", "test", None)]),
                (2, [("S.T", "FAIL", "test", None)]),
            ],
        )

        occurrence = build_report(db).test_failures[0].occurrences[0]

        assert occurrence.previous_run_on_this_leg.outcome == "fail"


class TestKnownCauses:
    """A conclusion somebody reached by reading an artifact is not derived from
    anything, so it cannot live in a database that gets rebuilt whenever a
    parsing rule changes."""

    def _file(self, tmp_path, entries):
        path = tmp_path / "known.json"
        path.write_text(json.dumps(entries), encoding="utf-8")
        return path

    def test_a_cause_is_matched_on_the_same_key_a_group_uses(self, tmp_path):
        from tools.ci_failures.annotations import known_cause_for, load_known_causes

        known = load_known_causes(
            self._file(
                tmp_path,
                [{"test": "Suite.Broken", "signature": "Box <n>", "cause": "a race"}],
            )
        )

        assert known_cause_for(known, "Suite.Broken", "Box <n>")["cause"] == "a race"

    def test_the_match_is_case_folded_like_the_grouping(self, tmp_path):
        """`Deadline Exceeded` and `Deadline exceeded` are one group, so an
        annotation on one has to reach the other."""
        from tools.ci_failures.annotations import known_cause_for, load_known_causes

        known = load_known_causes(
            self._file(
                tmp_path,
                [{"suite": "S", "signature": "Deadline Exceeded", "cause": "a timer"}],
            )
        )

        assert known_cause_for(known, "S", "Deadline exceeded")["cause"] == "a timer"

    def test_a_different_error_on_the_same_test_is_not_annotated(self, tmp_path):
        from tools.ci_failures.annotations import known_cause_for, load_known_causes

        known = load_known_causes(
            self._file(
                tmp_path, [{"test": "S.B", "signature": "Box <n>", "cause": "a race"}]
            )
        )

        assert known_cause_for(known, "S.B", "Timeout") is None

    def test_a_broken_file_costs_the_annotations_and_never_the_report(self, tmp_path):
        """Rendering without them beats refusing to render."""
        from tools.ci_failures.annotations import load_known_causes

        path = tmp_path / "known.json"
        path.write_text("{not json", encoding="utf-8")

        assert load_known_causes(path) == {}

    def test_a_missing_file_is_the_normal_starting_state(self, tmp_path):
        from tools.ci_failures.annotations import load_known_causes

        assert load_known_causes(tmp_path / "absent.json") == {}

    def test_the_local_file_parses_if_there_is_one(self):
        """Edited by hand, and a malformed one fails silently by design, so it
        is worth asserting wherever it exists.

        Which is not everywhere any more. The file is gitignored, so it exists
        on the machine of whoever has been recording causes and nowhere else -
        not in CI, not in a fresh clone. Skipped there rather than asserted:
        "nothing explained yet" is the ordinary starting state, the test above
        covers it, and a test that fails on a fresh clone teaches everyone to
        ignore it.
        """
        from tools.ci_failures.annotations import KNOWN_CAUSES, load_known_causes

        if not KNOWN_CAUSES.exists():
            pytest.skip(f"{KNOWN_CAUSES} is gitignored and not present here")

        assert load_known_causes(KNOWN_CAUSES), f"{KNOWN_CAUSES} parsed to nothing"


class TestWhatChangedSinceLastTime:
    def test_no_snapshot_is_not_the_same_as_no_change(self, tmp_path):
        from tools.ci_failures.annotations import compare

        assert compare(None, [("S.B", "Box <n>", 3)]) is None

    def test_a_group_absent_from_the_snapshot_is_new(self, tmp_path):
        from tools.ci_failures.annotations import compare, read_snapshot, write_snapshot

        db = tmp_path / "ci.sqlite3"
        write_snapshot(db, [("S.Old", "Box <n>", 2)])

        changes = compare(read_snapshot(db), [("S.New", "Timeout", 1)])

        assert [c["subject"] for c in changes["new"]] == ["S.New"]
        assert [c["subject"] for c in changes["gone"]] == ["S.Old"]

    def test_a_count_that_moved_is_reported_with_both_numbers(self, tmp_path):
        from tools.ci_failures.annotations import compare, read_snapshot, write_snapshot

        db = tmp_path / "ci.sqlite3"
        write_snapshot(db, [("S.B", "Box <n>", 2)])

        changes = compare(read_snapshot(db), [("S.B", "Box <n>", 5)])

        assert changes["grew"] == [
            {"subject": "S.B", "signature": "Box <n>", "was": 2, "now": 5}
        ]

    def test_an_unchanged_group_is_not_reported_at_all(self, tmp_path):
        from tools.ci_failures.annotations import compare, read_snapshot, write_snapshot

        db = tmp_path / "ci.sqlite3"
        write_snapshot(db, [("S.B", "Box <n>", 2)])

        changes = compare(read_snapshot(db), [("S.B", "Box <n>", 2)])

        assert changes["new"] == changes["gone"] == changes["grew"] == []

    def test_rendering_does_not_move_the_baseline(self, tmp_path):
        """A report that moved its own baseline would answer differently the
        second time it was run on unchanged data."""
        from tools.ci_failures import workspace
        from tools.ci_failures.report import build

        db = tmp_path / "ci.sqlite3"
        connect_db(db).close()

        build(db)
        build(db)

        assert not workspace.snapshot(db).exists()


# Fields the page deliberately does not show. ADR 0001 says a Rendering may show
# less than the Report holds and that what it leaves out is a choice rather than
# an absence - but nothing made the choice visible, so nineteen fields had drifted
# into one Rendering without anybody deciding. A field belongs here or on the
# page; there is no third state.
PAGE_OMITS = {
    "TestCounts.distinct_commits": "the page names the commits on the "
    "occurrences themselves, so the count restates what is already listed",
    "FixtureCounts.distinct_commits": "as above",
    "LatestRun.run": "the newest run is named by date and failure count; its id "
    "is a key to join on, which is the document's job",
    "LatestRun.event": "push and schedule run the same suite; the distinction "
    "matters when grouping, not when reading",
    "Neighbour.run": "the page says what the run either side did, not which run "
    "it was - the outcome is the finding, the id is a key",
    "Occurrence.run": "the page links the run rather than printing its id",
    "Occurrence.event": "as LatestRun.event",
    "Occurrence.executors": "null on every leg ingested so far, and a property "
    "of the leg rather than of this failure",
    "Occurrence.node_process": "as above",
    "Occurrence.elapsed_ms": "the page shows the passing spread, which is the "
    "comparison that means something; one failure's duration alone does not",
    "Retry.attempts": "the page says whether a hand re-run passed, which is the "
    "whole finding; how many tries it took is detail",
}

#: Fields the document does not carry. It is read by a language model that
#: cannot ask a follow-up question, so it carries everything.
DOCUMENT_OMITS: dict[str, str] = {}


class TestNeitherRenderingDropsAFieldByAccident:
    """ADR 0001's premise, made checkable.

    The Report is typed so that a Rendering ignoring a field is a fact you can
    see. Nothing looked, so it was not one: nineteen fields reached exactly one
    Rendering, including the commit of an Occurrence - which is the question
    CONTEXT.md says Occurrences exist to answer - and which Window the document
    covers, which the page carries a comment explaining it must say.

    Reachability is read from the Rendering sources by name. That cannot tell
    `Occurrence.commit` from `LatestRun.commit`, so a new field sharing a name
    with a rendered one slips through; a new field with a name of its own does
    not. The omission tables are the specification, and this only checks that
    nobody added to them silently.
    """

    def _fields(self) -> list[str]:
        import dataclasses

        from tools.ci_failures import report as module

        names = []
        for attribute in vars(module).values():
            if not (
                isinstance(attribute, type) and dataclasses.is_dataclass(attribute)
            ):
                continue
            if attribute.__module__ != module.__name__:
                continue
            names += [
                f"{attribute.__name__}.{field.name}"
                for field in dataclasses.fields(attribute)
            ]
        return names

    def _reached(self, rendering: str, field: str) -> bool:
        import re
        from pathlib import Path as _Path

        source = _Path(f"tools/ci_failures/{rendering}").read_text(encoding="utf-8")
        return bool(re.search(rf"\.{field.split('.')[1]}\b", source))

    def test_every_field_reaches_the_page_or_is_declared(self):
        missing = {
            field
            for field in self._fields()
            if not self._reached("render_html.py", field) and field not in PAGE_OMITS
        }

        assert not missing, (
            f"{sorted(missing)} reach the document and not the page. Show them, "
            "or add them to PAGE_OMITS with the reason."
        )

    def test_every_field_reaches_the_document_or_is_declared(self):
        missing = {
            field
            for field in self._fields()
            if not self._reached("render_json.py", field)
            and field not in DOCUMENT_OMITS
        }

        assert not missing, (
            f"{sorted(missing)} reach the page and not the document. Carry them, "
            "or add them to DOCUMENT_OMITS with the reason."
        )

    def test_the_omission_tables_do_not_outlive_what_they_describe(self):
        """A field shown after all, or deleted, leaves its excuse behind."""
        fields = set(self._fields())
        stale = (set(PAGE_OMITS) | set(DOCUMENT_OMITS)) - fields
        shown = {f for f in PAGE_OMITS if self._reached("render_html.py", f)}

        assert not stale, f"{sorted(stale)} are declared omitted but do not exist"
        assert not shown, f"{sorted(shown)} are declared omitted but are shown"


class TestWhenThereIsNoReportToGive:
    """The conditions a caller has to have handled to ask this tool a question.

    They lived in the invoke task, so a second caller had to reimplement all of
    them, and none could be exercised without typing `inv`. One of them fails
    silently when it is got wrong, which is the one worth a test most.
    """

    def test_an_absent_database_is_refused_rather_than_created(self, tmp_path):
        """Opening it would create it, and an empty archive renders as a clean
        one - a page saying nothing has ever failed."""
        from tools.ci_failures.db import NoDatabaseError

        missing = tmp_path / "nothing-here.sqlite3"

        with pytest.raises(NoDatabaseError):
            build_report(missing)

        assert not missing.exists(), "asking must not create the archive"

    def test_backfilling_an_absent_database_is_refused_rather_than_created(
        self, tmp_path
    ):
        from tools.ci_failures.db import NoDatabaseError

        missing = tmp_path / "nothing-here.sqlite3"

        with pytest.raises(NoDatabaseError):
            ingest.backfill_attempts(missing, out=lambda _: None)

        assert not missing.exists()

    def test_recomputing_an_absent_database_is_refused_rather_than_created(
        self, tmp_path
    ):
        from tools.ci_failures.db import NoDatabaseError

        missing = tmp_path / "nothing-here.sqlite3"

        with pytest.raises(NoDatabaseError):
            ingest.recompute_signatures(missing, out=lambda _: None)

        assert not missing.exists()

    def test_the_controls_of_a_run_refuse_an_absent_database_too(self, tmp_path):
        from tools.ci_failures.history import of_run
        from tools.ci_failures.db import NoDatabaseError

        missing = tmp_path / "nothing-here.sqlite3"

        with pytest.raises(NoDatabaseError):
            of_run(missing, 1, "Test.S.T")

        assert not missing.exists()

    def test_a_test_that_never_failed_refuses_an_absent_database_too(self, tmp_path):
        from tools.ci_failures.history import never_failed
        from tools.ci_failures.db import NoDatabaseError

        missing = tmp_path / "nothing-here.sqlite3"

        with pytest.raises(NoDatabaseError):
            never_failed(missing, "Test.S.T")

        assert not missing.exists()

    def test_a_window_with_no_runs_is_refused(self, tmp_path):
        """An empty page cannot say whether nothing ran or nothing failed, and
        those are opposite findings."""
        from datetime import datetime

        from tools.ci_failures.report import NothingInWindowError
        from tools.ci_failures.window import of_days

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "e"}])
        long_after = datetime(2026, 12, 25, 12, 0).astimezone()

        with pytest.raises(NothingInWindowError, match="newest ingested run 2026-08"):
            build_report(db, window=of_days(1, long_after))

    def test_a_baseline_cannot_be_taken_from_a_windowed_report(self, tmp_path):
        """The one that is silent when it goes wrong: a baseline covering less
        than the report that reads it makes every group come back grown, and
        every number involved stays plausible."""
        from datetime import datetime

        from tools.ci_failures.report import WindowedBaselineError, snapshot_entries
        from tools.ci_failures.window import of_days

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "e"}])
        seeded_day = datetime(2026, 8, 20, 12, 0).astimezone()

        assert snapshot_entries(build_report(db)), "all history is fine"
        with pytest.raises(WindowedBaselineError):
            snapshot_entries(build_report(db, window=of_days(1, seeded_day)))


class TestTheReading:
    """The database as one Report reads it: windowed, with Subjects resolved.

    Both restrictions used to hold only because every query happened to go
    through one private helper, and a query written not to would have been
    answered from the whole archive with nothing to say so.
    """

    def _two_fixture_failures(self, db: Path, now) -> None:
        """One broken teardown inside a one-day window, one forty days before."""
        from datetime import timedelta, timezone

        connection = connect_db(db)
        for index, day in enumerate((now - timedelta(days=40), now), start=1):
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', 's', 'main', ?, 'failure', 'u')",
                (index, day.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, platform, "
                "ingested_at) VALUES (?, ?, ?, 'a', 'linux', 'now')",
                (index, index, index),
            )
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                "status, message, error_signature, failure_scope, scope_owner) "
                "VALUES (?, 'S.T', 'T', 'S', 'FAIL', 'm', 'sig', 'suite_teardown', 'S')",
                (index,),
            )
        connection.commit()
        connection.close()

    def test_a_connection_nobody_restricted_is_not_a_reading(self, tmp_path):
        """The one check between a hand-made connection and a report that
        silently spans all history."""
        from tools.ci_failures.reading import Reading

        db = tmp_path / "ci.sqlite3"

        connection = connect_db(db)
        try:
            with pytest.raises(ValueError, match="not a Reading"):
                Reading(connection)
        finally:
            connection.close()

    def test_the_subject_views_are_windowed_like_everything_else(self, tmp_path):
        """The guarantee that would break if these became permanent views.

        A view in `main` resolves its body against `main`, cannot see the
        Window's shadowing views, and would answer from the whole archive - no
        error, just a windowed report that is not windowed.
        """
        from datetime import datetime

        from tools.ci_failures.window import of_days

        now = datetime.now().astimezone()
        db = tmp_path / "ci.sqlite3"
        self._two_fixture_failures(db, now)

        with reading_of(db, of_days(1, now)) as windowed:
            inside = windowed.execute(
                "SELECT COUNT(*) FROM fixture_failure"
            ).fetchone()[0]
        with reading_of(db) as everything:
            all_history = everything.execute(
                "SELECT COUNT(*) FROM fixture_failure"
            ).fetchone()[0]

        assert (inside, all_history) == (1, 2)


class TestTheLogLinesShown:
    """The opening lines and every FAIL or WARN, with a marker where lines were
    passed over. Asked of `_log_html` directly: it takes LogLines and returns a
    string, so a database would only be in the way."""

    def _lines(self, *levels: str) -> tuple[LogLine, ...]:
        return tuple(
            LogLine(level=level, keyword="K", origin=None, message=f"line {n}")
            for n, level in enumerate(levels)
        )

    def test_a_marker_stands_where_lines_were_passed_over(self):
        entries = self._lines("INFO", "INFO", "INFO", "INFO", "INFO", "FAIL")

        assert render_html._log_html(entries).count('class="logline gap"') == 1

    def test_nothing_passed_over_needs_no_marker(self):
        entries = self._lines("INFO", "INFO", "INFO", "FAIL")

        assert 'class="logline gap"' not in render_html._log_html(entries)

    def test_two_identical_lines_are_two_positions_not_one(self):
        """A LogLine is a frozen dataclass, so two identical lines compare equal.

        Looking the shown line up by value found the earlier twin instead of
        this one and made the distance negative, which silently dropped the
        marker. Robot Framework logs identical lines routinely.
        """
        warn = LogLine(level="WARN", keyword="K", origin=None, message="retrying")
        middle = self._lines("INFO", "INFO", "INFO", "INFO")
        entries = (warn, *middle, warn)

        assert render_html._log_html(entries).count('class="logline gap"') == 1


class TestWhatTheBuilderMadeReachable:
    """Four things nothing tested, because no seeder could set them up.

    Not a coincidence: the columns eight hand-rolled seeders could not write
    were very nearly the list of paths nothing exercised.
    """

    def test_a_clean_configuration_says_whether_its_zero_is_evidence(self, tmp_path):
        """The Inconclusive Zero: a rate of zero and an absence of evidence
        render identically, and on a rare failure they are usually the same
        thing. The reader's next move - "it is linux-only, look at what linux
        does" - is only sound if the zero means something."""
        db = tmp_path / "ci.sqlite3"
        # One failure in twenty on linux; darwin clean over four runs, which a
        # configuration exactly as broken would manage most of the time.
        rows = (
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "sha": "s1"},
            ]
            + [{"test": "T", "status": "PASS", "sha": f"p{n}"} for n in range(19)]
            + [
                {"test": "T", "status": "PASS", "platform": "darwin", "sha": f"d{n}"}
                for n in range(4)
            ]
        )
        seed(db, rows)

        rates = {r.platform: r for r in build_report(db).test_failures[0].rates}

        assert rates["linux"].zero_is_inconclusive is None, "it failed; not a zero"
        thin = rates["darwin"].zero_is_inconclusive
        assert thin is not None, "four clean runs cannot clear a 1-in-20 failure"
        assert 0 < thin.would_look_clean_anyway <= 1
        assert thin.runs_for_a_meaningful_zero > 4

    def test_a_configuration_with_enough_clean_runs_is_evidence(self, tmp_path):
        """The other side of it, or the field would say nothing by always
        being there."""
        db = tmp_path / "ci.sqlite3"
        # A third of all runs fail, so ten clean darwin runs would happen by
        # luck about once in sixty. That zero is worth reading.
        rows = (
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "sha": f"f{n}"}
                for n in range(10)
            ]
            + [{"test": "T", "status": "PASS", "sha": f"p{n}"} for n in range(10)]
            + [
                {"test": "T", "status": "PASS", "platform": "darwin", "sha": f"d{n}"}
                for n in range(10)
            ]
        )
        seed(db, rows)

        rates = {r.platform: r for r in build_report(db).test_failures[0].rates}

        assert rates["darwin"].ran == 10
        assert rates["darwin"].zero_is_inconclusive is None

    def test_a_known_cause_reaches_the_report(self, tmp_path):
        """Recorded by hand and matched at report time. `build` read them from
        the one path the module knows, so nothing could ask what a Report does
        with a cause - or without one."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "Boom: 5 != 6"}])
        causes = tmp_path / "known_causes.json"
        causes.write_text(
            json.dumps(
                [
                    {
                        "test": "T",
                        # Matched case-insensitively, the way groups are keyed.
                        "signature": "boom: 5 != 6",
                        "cause": "the widget is disposed by another worker",
                        "reference": "0013_highlight_cache_flake.md",
                        "recorded": "2026-08-29",
                        "fixed_by": None,
                        "fix_verified": None,
                    }
                ]
            ),
            encoding="utf-8",
        )

        explained = build_report(db, known_causes=causes).test_failures[0]
        unexplained = build_report(db, known_causes=tmp_path / "absent.json")

        assert explained.known_cause is not None
        assert explained.known_cause.reference == "0013_highlight_cache_flake.md"
        # Absence means nobody has written one down, never that it is unknown.
        assert unexplained.test_failures[0].known_cause is None

    def test_the_executor_axis_survives_into_both_renderings(self, tmp_path):
        """How many test executions ran at once, and whether they shared one
        node process. A failure where one worker reaches another's state lives
        on this axis and no other, and nothing else in the database records it.
        No seeder could write either column, so nothing checked the path."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "signature": "boom",
                    "executors": 3,
                    "node_process": "shared",
                }
            ],
        )

        report = build_report(db)
        occurrence = report.test_failures[0].occurrences[0]
        document = json_document(report)["test_failures"][0]["occurrences"][0]

        assert (occurrence.executors, occurrence.node_process) == (3, "shared")
        assert (document["executors"], document["node_process"]) == (3, "shared")


class TestTheColumnsThatNeedNoArtifact:
    """`0012` says there is no re-parse, and for most of what the database holds
    that is true. It is not true of a derived column whose source is itself
    stored, and there are four of those - the signature had a door and the three
    keyword columns did not, so changing `locate._ROOTS` or the classification
    rule read as "delete the database and download the window again"."""

    def test_a_keyword_that_moved_is_found_again_without_downloading(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        run_sql(
            db,
            "UPDATE test_result SET keyword_owner = 'Browser', "
            "failing_keyword = 'Close Browser', keyword_source = 'gone/away.py', "
            "keyword_kind = 'unknown', keyword_lineno = 1",
        )

        resolved = ingest.recompute_keyword_locations(db, out=lambda _: None)

        row = one_row(db, "SELECT keyword_kind, keyword_source FROM test_result")
        assert resolved == 1
        assert row["keyword_kind"] == "library"
        assert row["keyword_source"] == "Browser/keywords/playwright_state.py"

    def test_a_helper_beside_its_suite_is_located(self, tmp_path):
        """Robot Framework resolves `Library  helper.py` against the file that
        imports it, so a test-only library can sit anywhere under `atest/test`.
        Only `atest/library` was searched, so four failures in the working
        database pointed nowhere and nothing said why."""
        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        run_sql(
            db,
            "UPDATE test_result SET keyword_owner = 'scope_logger', "
            "failing_keyword = 'Log All Scopes'",
        )

        ingest.recompute_keyword_locations(db, out=lambda _: None)

        row = one_row(db, "SELECT keyword_kind, keyword_source FROM test_result")
        assert row["keyword_kind"] == "project"
        assert row["keyword_source"] == "atest/test/08_Scope_Tests/scope_logger.py"

    def test_a_library_that_will_not_import_is_named_rather_than_silent(self):
        """It costs a location and never an ingest, which is right - but the
        answer is cached, so one failure is every leg's answer for the rest of
        the run and a whole ingest used to finish with three columns null on
        every row and nothing anywhere saying why."""
        from tools.ci_failures import locate

        assert locate.keyword_location("NoSuchLibrary", "Whatever") == (None, None)

        assert "NoSuchLibrary" in locate.unimportable()


class TestAddingAColumnToADatabaseThatExists:
    def test_an_index_on_an_added_column_does_not_break_what_is_already_there(
        self, tmp_path, monkeypatch
    ):
        """`schema.sql` carries standalone CREATE INDEX statements, so running
        it before the ALTER TABLEs meant that adding a column in one file and an
        index on it in the other - the obvious pair of edits - raised `no such
        column` on every database that already existed, on open, which is what
        ingest and every report go through.
        """
        from tools.ci_failures import db as db_module

        schema = Path(db_module.__file__).parent / "schema.sql"
        original = schema.read_text(encoding="utf-8")
        existing = tmp_path / "existing.sqlite3"
        connect_db(existing).close()

        monkeypatch.setitem(db_module._ADDED_COLUMNS["leg"], "runner", "TEXT")
        schema.write_text(
            original.replace(
                "    os_release     TEXT\n);",
                "    os_release     TEXT,\n    runner         TEXT\n);",
            )
            + "\nCREATE INDEX IF NOT EXISTS idx_leg_runner ON leg(runner);\n",
            encoding="utf-8",
        )
        try:
            for database in (existing, tmp_path / "fresh.sqlite3"):
                connection = connect_db(database)
                columns = {
                    row["name"] for row in connection.execute("PRAGMA table_info(leg)")
                }
                indexes = {
                    row["name"] for row in connection.execute("PRAGMA index_list(leg)")
                }
                connection.close()

                assert "runner" in columns, database.name
                assert "idx_leg_runner" in indexes, database.name
        finally:
            schema.write_text(original, encoding="utf-8")


class TestRegroupingWithoutTheArtifacts:
    def test_the_signatures_are_recomputed_from_the_stored_messages(self, tmp_path):
        """What you run after changing the masking rules. It needs no network:
        the message is in the database, so re-grouping never wants the artifact
        again - which is the one thing on the cheap side of the re-parse wall."""
        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": "T",
                    "status": "FAIL",
                    "message": "Timeout 5000ms exceeded waiting for #id-4f2a",
                    "signature": "nonsense recorded by an older masking rule",
                }
            ],
        )

        changed = ingest.recompute_signatures(db, out=lambda _: None)

        after = one_row(db, "SELECT error_signature FROM test_result")[0]
        assert changed == 1
        # The parts that vary between occurrences are masked; an id inside a
        # selector is not one of them, and the message is the test's own text.
        assert after == "Timeout <duration> exceeded waiting for #id-4f2a"
        assert after != "nonsense recorded by an older masking rule"


class TestScreenshotRanking:
    """Which picture is the evidence is a question about the log lines, so it is
    answered at report time. Doing it during parsing would freeze a display
    decision into stored data that only a full re-download can change."""

    STAMPED = [
        "p/4/browser/screenshot/20260825_104829-4-fail-screenshot-1.png",
        "p/4/browser/screenshot/20260825_104829-4-rfb-screenshot-2.png",
        "p/4/browser/screenshot/20260825_104829-4-rfb-screenshot-3.png",
        "p/4/browser/screenshot/other.png",
    ]
    COMPARED = [
        LogLine(
            level="INFO",
            keyword="Compare Images",
            origin=None,
            message="Comparing image img1_path '/x/rfb-screenshot-2.png'",
        ),
        LogLine(
            level="INFO",
            keyword="Compare Images",
            origin=None,
            message="With image from path '/x/rfb-screenshot-3.png'",
        ),
    ]

    def test_the_files_the_failing_keyword_named_lead(self):
        from tools.ci_failures.report import rank_screenshots

        ranked = rank_screenshots(self.STAMPED, self.COMPARED)

        assert ranked[0].endswith("rfb-screenshot-2.png")
        assert ranked[1].endswith("rfb-screenshot-3.png")

    def test_the_merge_stamp_does_not_defeat_the_match(self):
        """The file on disk carries a run timestamp and a worker number; the
        keyword logged the name it had before the merge."""
        from tools.ci_failures.report import rank_screenshots

        ranked = rank_screenshots(
            ["a/20260825_104829-4-rfb-screenshot-2.png", "a/unrelated.png"],
            self.COMPARED,
        )

        assert ranked[0].endswith("20260825_104829-4-rfb-screenshot-2.png")

    def test_a_file_named_only_by_a_caught_failure_does_not_lead(self):
        """`fail-screenshot-1.png` is named by the `Get Text` that a
        `Run Keyword And Expect Error` swallowed, which is weaker evidence than
        the file the keyword that actually failed named."""
        from tools.ci_failures.report import rank_screenshots

        log = [
            *self.COMPARED,
            LogLine(
                level="DEBUG",
                keyword="Take Screenshot",
                origin="caught by Run Keyword And Expect Error",
                message="Screenshot successfully captured to: /x/fail-screenshot-1.png",
            ),
        ]

        ranked = rank_screenshots(self.STAMPED, log)

        assert ranked[0].endswith("rfb-screenshot-2.png")
        assert ranked[2].endswith("fail-screenshot-1.png")

    def test_with_nothing_named_the_failure_screenshot_leads(self):
        from tools.ci_failures.report import rank_screenshots

        ranked = rank_screenshots(self.STAMPED, [])

        assert ranked[0].endswith("fail-screenshot-1.png")

    def test_no_screenshots_ranks_to_nothing(self):
        from tools.ci_failures.report import rank_screenshots

        assert rank_screenshots([], self.COMPARED) == ()


class TestTheReportingWindow:
    """`--days N` asks what has failed in the last N whole local days.

    The question it exists for is "I fixed this on Tuesday, has it come back",
    and the failures from before the fix are exactly the ones that must not be
    counted. So the window is a hard scope rather than a filter on the listing:
    every count, rate and denominator comes from inside it, and a test that did
    not fail inside it does not appear at all. See `tools/ci_failures/window.py`.
    """

    @staticmethod
    def _local_utc(day, hour=12, minute=0) -> str:
        """A moment on a local calendar day, spelled the way a run is stored.

        Seeded from the local clock rather than written as a UTC literal: the
        window is defined in local days, so a fixture written in UTC would pass
        or fail depending on the machine's offset.
        """
        from datetime import datetime, time, timezone

        moment = datetime.combine(day, time(hour, minute)).astimezone()
        return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _seed(self, db: Path, runs: list[tuple[int, str, list[tuple[str, str]]]]):
        """runs of (run_id, created_at, [(test, status)]), one leg each."""
        connection = connect_db(db)
        for run_id, created_at, rows in runs:
            connection.execute(
                "INSERT INTO run (id, event, head_sha, head_branch, created_at, "
                "conclusion, url) VALUES (?, 'push', ?, 'main', ?, 'failure', 'u')",
                (run_id, f"sha{run_id}", created_at),
            )
            connection.execute(
                "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                "artifact_url, platform, attempt, ingested_at) "
                "VALUES (?, ?, ?, 'Test results-x', 'a-url', 'linux', 1, 'now')",
                (run_id, run_id, run_id),
            )
            for longname, status in rows:
                connection.execute(
                    "INSERT INTO test_result (leg_id, longname, name, "
                    "suite_longname, status, message, error_signature) "
                    "VALUES (?, ?, ?, 'S', ?, ?, ?)",
                    (
                        run_id,
                        longname,
                        longname,
                        status,
                        "raw" if status == "FAIL" else None,
                        "error X" if status == "FAIL" else None,
                    ),
                )
        connection.commit()
        connection.close()

    @pytest.fixture
    def four_days(self, tmp_path):
        """A failure today, and the same failure on each of the three days before.

        `today` is pinned so the test does not change meaning at midnight.
        """
        from datetime import date, timedelta

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (
                    n + 1,
                    self._local_utc(today - timedelta(days=n)),
                    [("Test A", "FAIL"), ("Test B", "PASS")],
                )
                for n in range(4)
            ],
        )
        return db, today

    def test_one_day_is_today(self, four_days):
        from tools.ci_failures.window import of_days
        from datetime import datetime, time

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()

        assert totals(reading_of(db, of_days(1, now))).runs == 1

    def test_two_days_is_today_and_yesterday(self, four_days):
        from tools.ci_failures.window import of_days
        from datetime import datetime, time

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()

        assert totals(reading_of(db, of_days(2, now))).runs == 2

    def test_the_denominator_is_windowed_too(self, four_days):
        """The point of the flag. A rate that kept its all-time denominator
        would answer "how often does this break" when the question asked was
        "has it broken since I fixed it"."""
        from tools.ci_failures.window import of_days
        from datetime import datetime, time

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()

        group = failure_groups(reading_of(db, of_days(2, now)))[0]

        assert (group.failures, group.total_runs) == (2, 2)

    def test_a_test_that_failed_only_before_the_window_is_absent(self, tmp_path):
        from tools.ci_failures.window import of_days
        from datetime import date, datetime, time, timedelta

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (
                    1,
                    self._local_utc(today - timedelta(days=3)),
                    [("Fixed Test", "FAIL")],
                ),
                (2, self._local_utc(today), [("Fixed Test", "PASS")]),
            ],
        )
        now = datetime.combine(today, time(9, 0)).astimezone()

        assert failure_groups(reading_of(db, of_days(1, now))) == []
        assert len(failure_groups(reading_of(db))) == 1, "still there over all history"

    def test_runs_with_nothing_failing_is_not_the_same_as_no_runs(self, tmp_path):
        """The two empty reports. One means the fix held; the other means you
        forgot to ingest, and they must not render alike."""
        from tools.ci_failures.window import of_days
        from datetime import date, datetime, time, timedelta

        today = date(2026, 8, 31)
        now = datetime.combine(today, time(9, 0)).astimezone()
        stale = self._local_utc(today - timedelta(days=5))

        clean = tmp_path / "clean.sqlite3"
        self._seed(
            clean,
            [
                (1, stale, [("Test A", "FAIL")]),
                (2, self._local_utc(today), [("Test A", "PASS")]),
            ],
        )
        unfed = tmp_path / "unfed.sqlite3"
        self._seed(unfed, [(1, stale, [("Test A", "FAIL")])])

        ran_clean = totals(reading_of(clean, of_days(1, now)))
        nothing_ran = totals(reading_of(unfed, of_days(1, now)))

        assert (ran_clean.runs, ran_clean.failures) == (1, 0)
        assert nothing_ran.runs == 0

    def test_the_window_is_calendar_days_not_the_last_n_times_24_hours(self, tmp_path):
        """A run at half past eleven last night is yesterday, whatever the hour
        it is now. A rolling window would keep pulling it in and out."""
        from tools.ci_failures.window import of_days
        from datetime import date, datetime, time, timedelta

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (
                    1,
                    self._local_utc(today - timedelta(days=1), 23, 30),
                    [("Test A", "FAIL")],
                ),
                (2, self._local_utc(today, 0, 30), [("Test B", "FAIL")]),
            ],
        )
        now = datetime.combine(today, time(1, 0)).astimezone()

        groups = failure_groups(reading_of(db, of_days(1, now)))

        assert [g.longname for g in groups] == ["Test B"]

    def test_every_derived_query_narrows_with_it(self, four_days):
        """The window is applied to the connection, so a query cannot opt out of
        it by forgetting to mention it. This is the test that says so."""
        from tools.ci_failures.window import of_days
        from datetime import datetime, time
        from tools.ci_failures.report import platform_breakdown

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()
        window = of_days(2, now)

        assert (
            sum(
                e.ran
                for v in coverage_by_test(reading_of(db, window)).values()
                for e in v
            )
            == 4
        )
        assert (
            len(
                occurrences_by_test(reading_of(db, window))[
                    ("Test A", "test", "error x")
                ]
            )
            == 2
        )
        assert len(runs_either_side(reading_of(db, window))) == 2
        assert platform_breakdown(reading_of(db, window))[0].legs == 2
        assert first_attempt_counts_by_test(reading_of(db, window))[0]["Test A"] == 2
        assert latest_run(reading_of(db, window)).run == 1

    def test_no_window_reports_over_everything(self, four_days):
        """The default is the behaviour the command already had."""
        db, _ = four_days

        assert totals(reading_of(db)).runs == 4
        assert failure_groups(reading_of(db))[0].failures == 4

    def test_a_window_needs_at_least_one_day(self):
        from tools.ci_failures.window import of_days

        for refused in (0, -1):
            with pytest.raises(ValueError):
                of_days(refused)

    def test_the_cutoff_is_local_midnight_of_the_first_day(self):
        from tools.ci_failures.window import of_days
        from datetime import date, datetime, time, timezone

        now = datetime.combine(date(2026, 8, 31), time(15, 0)).astimezone()
        window = of_days(3, now)

        expected = (
            datetime.combine(date(2026, 8, 29), time.min)
            .astimezone()
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        assert window.cutoff == expected
        assert (window.first_day, window.last_day) == (
            date(2026, 8, 29),
            date(2026, 8, 31),
        )

    def test_the_label_says_what_the_report_covers(self):
        from tools.ci_failures.window import ALL_HISTORY, of_days
        from datetime import date, datetime, time

        now = datetime.combine(date(2026, 8, 31), time(15, 0)).astimezone()

        assert of_days(1, now).label == "--days 1 (2026-08-31 local)"
        assert of_days(3, now).label == "--days 3 (2026-08-29..2026-08-31 local)"
        assert ALL_HISTORY.label == "all history"

    def test_the_page_says_which_window_it_is(self, four_days):
        """Both reports are written to the same path, and their numbers are not
        comparable. A saved page has to say which one it is."""
        from tools.ci_failures.render_html import write as write_page
        from tools.ci_failures.window import of_days
        from datetime import datetime, time

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()

        windowed = write_page(
            build_report(db, window=of_days(2, now)), tmp := (db.parent / "w.html")
        )
        everything = build_report(db)
        plain = write_page(everything, db.parent / "p.html")
        span = f"{everything.window.since[:10]} to {everything.window.until[:10]}"

        assert "--days 2 (2026-08-30..2026-08-31 local), 2 run(s)" in tmp.read_text()
        # An all-history page names no window at all - it says what has been
        # ingested instead, which is the other honest answer to the same
        # question and cannot be mistaken for a windowed one.
        assert span in plain.read_text()
        assert "--days" not in plain.read_text()
        assert windowed.exists() and plain.exists()

    def test_the_page_says_so_when_the_window_ran_clean(self, tmp_path):
        from tools.ci_failures.render_html import write as write_page
        from tools.ci_failures.window import of_days
        from datetime import date, datetime, time, timedelta

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (1, self._local_utc(today - timedelta(days=5)), [("Test A", "FAIL")]),
                (2, self._local_utc(today), [("Test A", "PASS")]),
            ],
        )
        now = datetime.combine(today, time(9, 0)).astimezone()

        page = write_page(
            build_report(db, window=of_days(1, now)), tmp_path / "w.html"
        ).read_text()

        assert "No test failures in --days 1" in page
        assert "1 run(s) and 1 matrix leg(s) examined" in page

    def test_the_document_is_windowed_like_the_page(self, four_days):
        """Both Renderings answer the same question.

        The document used to take no window at all, so `--days` with `--json`
        was refused outright and the one question the flag exists for could only
        be asked of the page.
        """
        from datetime import datetime, time

        from tools.ci_failures.window import of_days

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()

        windowed = build_report(db, window=of_days(2, now))
        everything = build_report(db)

        assert windowed.window.runs == 2
        assert everything.window.runs == 4
        assert windowed.test_failures[0].counts.failures == 2
        assert everything.test_failures[0].counts.failures == 4

    def test_a_windowed_report_has_no_baseline_to_compare_itself_with(self, four_days):
        """A Snapshot is never taken from a window, so the only baseline there
        can be covers more data than the window does. Comparing against it would
        report every Group as having shrunk, which is an artefact of the window
        rather than anything that happened in CI. Null says so; a number would
        not."""
        from datetime import datetime, time

        from tools.ci_failures.annotations import write_snapshot
        from tools.ci_failures.report import snapshot_entries
        from tools.ci_failures.window import of_days

        db, today = four_days
        now = datetime.combine(today, time(9, 0)).astimezone()
        write_snapshot(db, snapshot_entries(build_report(db)))

        assert build_report(db, window=of_days(2, now)).since_last_report is None
        assert build_report(db).since_last_report is not None


class TestAWindowWiderThanTheArchive:
    """`--days 60` over sixteen days of database answers over sixteen.

    The window can only restrict what has been ingested, so the label says what
    was asked for and the counts cover what was there, and nothing connected the
    two. Harmless while the archive is deep, and quietly wrong just after a
    rebuild, when an ordinary `--days 14` is answered on half of them - which is
    the one report anybody runs weekly.

    Not an error: the answer is the best one available and worth having. It has
    to say what it is answering over, and then it is evidence rather than a
    number that looks like one.
    """

    # Borrowed rather than inherited: subclassing would re-run that class's
    # fifteen tests under this name for nothing.
    _local_utc = staticmethod(TestTheReportingWindow._local_utc)
    _seed = TestTheReportingWindow._seed
    four_days = TestTheReportingWindow.four_days

    @staticmethod
    def _now(today):
        from datetime import datetime, time

        return datetime.combine(today, time(9, 0)).astimezone()

    def _two_days_of_archive(self, tmp_path):
        from datetime import date, timedelta

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                (n + 1, self._local_utc(today - timedelta(days=n)), [("A", "FAIL")])
                for n in range(2)
            ],
        )
        return db, today

    def test_it_says_how_much_of_what_was_asked_for_is_there(self, tmp_path):
        from datetime import timedelta

        from tools.ci_failures.window import of_days

        db, today = self._two_days_of_archive(tmp_path)

        short = build_report(db, window=of_days(10, self._now(today))).window.short

        assert short is not None, "ten days asked of a two-day archive"
        assert short.asked_from == str(today - timedelta(days=9))
        assert short.holds_from == str(today - timedelta(days=1))
        assert short.missing_days == 8

    def test_an_archive_that_covers_the_question_says_nothing(self, four_days):
        """The common case, and it has to stay quiet. A note on every report is
        a note nobody reads by the third one."""
        from tools.ci_failures.window import of_days

        db, today = four_days

        assert (
            build_report(db, window=of_days(2, self._now(today))).window.short is None
        )

    def test_all_history_is_never_short(self, four_days):
        """Nothing was asked for, so nothing can be missing. `since` already
        says where the archive begins, which is the whole of that answer."""
        db, _ = four_days

        assert build_report(db).window.short is None

    def test_both_renderings_say_so(self, tmp_path):
        """Three rules #3. A finding the page keeps to itself is one the agent
        reading the document has to derive for itself, and the other way round."""
        import json

        from tools.ci_failures.render_html import page
        from tools.ci_failures.render_json import document
        from tools.ci_failures.window import of_days

        db, today = self._two_days_of_archive(tmp_path)
        report = build_report(db, window=of_days(10, self._now(today)))

        short = report.window.short
        assert json.loads(json.dumps(document(report)))["window"]["short"] == {
            "asked_from": short.asked_from,
            "holds_from": short.holds_from,
            "missing_days": 8,
        }
        assert short.asked_from in page(report)

    def test_a_quiet_first_day_is_not_a_short_archive(self, tmp_path):
        """The false positive this note exists to avoid.

        `since` is the oldest run *inside the window*, not where the archive
        begins - the Window shadows `run`, so a query cannot see past it. Read
        that way, a window whose leading days simply had no CI runs looks like
        history that was never ingested. On this repository that is one dropped
        or delayed nightly schedule run on a day nobody merged, which is not
        rare, and a note that cries wolf is worth less than no note.
        """
        from datetime import date, timedelta

        from tools.ci_failures.window import of_days

        today = date(2026, 8, 31)
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                # Deep archive, and nothing at all on the window's first day.
                (1, self._local_utc(today - timedelta(days=9)), [("A", "FAIL")]),
                (2, self._local_utc(today - timedelta(days=1)), [("A", "FAIL")]),
                (3, self._local_utc(today), [("A", "FAIL")]),
            ],
        )

        short = build_report(db, window=of_days(3, self._now(today))).window.short

        assert short is None, (
            "the archive reaches nine days back; the window's first day was "
            f"merely quiet, but it was reported as {short}"
        )


class TestListingRunsByDate:
    """`--days` on the ingest, so "how much history" is asked for in the unit it
    is wanted in.

    `--limit` counts runs, and the exchange rate moves with how busy the
    repository is: 25 runs was a week when it was measured and 100 was a month,
    and neither is a number anybody has in mind. Worse, past 100 the one-page
    listing stops being able to answer at all - `per_event` is capped there, so
    the two events come back in different depths and the older half of the
    window quietly becomes schedule-only.

    Asking by date fixes both: pages are walked until they are older than the
    cutoff and then stopped, so the depth is whatever the question needs, and
    each event is walked to the same date rather than to the same count.
    """

    @staticmethod
    def _pages(monkeypatch, by_event):
        """Serves `gh api` from canned pages, and records what was asked for."""
        import json as json_module

        asked = []

        def fake_run(args, **kwargs):
            endpoint = next(a for a in args if a.startswith("repos/"))
            asked.append(endpoint)
            event = endpoint.split("event=")[1].split("&")[0]
            page = int(endpoint.split("page=")[-1]) if "&page=" in endpoint else 1
            pages = by_event.get(event, [])
            body = pages[page - 1] if page <= len(pages) else []

            class Result:
                returncode = 0
                stdout = json_module.dumps({"workflow_runs": body})
                stderr = ""

            return Result()

        monkeypatch.setattr(github.subprocess, "run", fake_run)
        # A short page means there is no next one, so a one-run page is a full
        # page here. Shrinking the page rather than writing out a hundred runs
        # per fixture: the rule under test is "walk until older", not the number.
        monkeypatch.setattr(github, "_PER_PAGE", 1)
        return asked

    @staticmethod
    def _run_at(run_id, created_at, event):
        return {
            "id": run_id,
            "event": event,
            "head_sha": f"sha{run_id}",
            "head_branch": "main",
            "created_at": created_at,
            "conclusion": "success",
            "html_url": "u",
            "run_attempt": 1,
        }

    def test_it_walks_past_the_first_page_to_reach_the_cutoff(self, monkeypatch):
        """The whole point. One page is 100 runs; a question that needs 12 weeks
        of a busy repository needs more than one, and `--limit` cannot ask."""
        asked = self._pages(
            monkeypatch,
            {
                "push": [
                    [self._run_at(1, "2026-08-30T10:00:00Z", "push")],
                    [self._run_at(2, "2026-07-01T10:00:00Z", "push")],
                ],
                "schedule": [[self._run_at(3, "2026-08-29T10:00:00Z", "schedule")]],
            },
        )

        runs = github.runs_since("2026-08-01T00:00:00Z")

        assert [r.id for r in runs] == [1, 3], "the July run is older than the cutoff"
        assert any("&page=2" in endpoint for endpoint in asked), "stopped at one page"

    def test_it_stops_asking_once_a_page_is_older_than_the_cutoff(self, monkeypatch):
        """Bounded by the question, not by the age of the repository - which is
        the property `_first_page` was protecting when it took one page only."""
        asked = self._pages(
            monkeypatch,
            {
                "push": [
                    [self._run_at(1, "2026-08-30T10:00:00Z", "push")],
                    [self._run_at(2, "2026-06-01T10:00:00Z", "push")],
                    [self._run_at(3, "2026-05-01T10:00:00Z", "push")],
                ],
                "schedule": [[]],
            },
        )

        github.runs_since("2026-08-01T00:00:00Z")

        assert not any("&page=3" in endpoint for endpoint in asked)

    def test_both_events_are_walked_to_the_same_date(self, monkeypatch):
        """The failure `--limit` has above 100: one page each means the busier
        event runs out first, and the older half of the window becomes the other
        event only, with nothing saying so."""
        self._pages(
            monkeypatch,
            {
                "push": [
                    [
                        self._run_at(n, f"2026-08-{30 - n:02d}T10:00:00Z", "push")
                        for n in range(1, 4)
                    ],
                    [self._run_at(9, "2026-08-02T10:00:00Z", "push")],
                ],
                "schedule": [[self._run_at(20, "2026-08-03T10:00:00Z", "schedule")]],
            },
        )

        runs = github.runs_since("2026-08-01T00:00:00Z")

        assert {r.event for r in runs} == {"push", "schedule"}
        assert min(r.created_at for r in runs) >= "2026-08-01T00:00:00Z"

    def test_the_limit_path_still_takes_one_page(self, monkeypatch):
        """`--limit` is unchanged, and `TestListingRunsCostsTheSameForever` says
        why. This says the new path did not quietly become the old one."""
        asked = self._pages(monkeypatch, {"push": [[]], "schedule": [[]]})

        github.list_runs(limit=25)

        assert not any("&page=2" in endpoint for endpoint in asked)

    def test_the_ingest_asks_by_date_when_it_is_given_one(self, tmp_path, monkeypatch):
        """The two listings are alternatives, and the ingest picks between them
        rather than asking for both and reconciling."""
        from tools.ci_failures.ingest import ingest

        asked: dict = {}
        monkeypatch.setattr(
            github,
            "runs_since",
            lambda cutoff, **kw: asked.setdefault("since", cutoff) and [],
        )
        monkeypatch.setattr(
            github,
            "list_runs",
            lambda limit=25: asked.setdefault("limit", limit) and [],
        )

        ingest(
            tmp_path / "ci.sqlite3", since="2026-08-01T00:00:00Z", out=lambda _: None
        )

        assert asked == {"since": "2026-08-01T00:00:00Z"}, "asked by count as well"

    def test_the_ingest_still_asks_by_count_by_default(self, tmp_path, monkeypatch):
        from tools.ci_failures.ingest import ingest

        asked: dict = {}
        monkeypatch.setattr(
            github,
            "list_runs",
            lambda limit=25: asked.setdefault("limit", limit) and [],
        )

        ingest(tmp_path / "ci.sqlite3", limit=7, out=lambda _: None)

        assert asked == {"limit": 7}


class TestTheListingIsNotTakenOnTrust:
    """The run listing came back different from one call to the next.

    Three identical `--dry-run --limit 100` invocations on 2026-09-03 gave two
    answers: twice 75 runs reaching 2026-08-03 with nothing expired, and once a
    different set reaching 2026-06-05 with 24 expired and eight days of runs
    simply absent. The ingest noticed none of it. A run missing from the page is
    not fetched, a run with nothing pending is counted into one silent bucket,
    and the summary line reads the same either way.

    Nothing here can make GitHub consistent. What it can do is say what it was
    given, so that "reached 2026-06-05" is visible at a glance rather than
    reconstructed afterwards from a saved dry run.
    """

    @staticmethod
    def _listing(monkeypatch, runs, conclusion="success"):
        monkeypatch.setattr(github, "list_runs", lambda limit=25: runs)
        monkeypatch.setattr(github, "list_test_artifacts", lambda run_id: [])
        # A suspect is checked against the run itself; `success` is a run that
        # really has finished and really was left out of the listing.
        monkeypatch.setattr(
            github,
            "get_run",
            lambda run_id: github.Run(
                id=run_id,
                event="push",
                head_sha=f"sha{run_id}",
                head_branch="main",
                created_at="2026-07-01T10:00:00Z",
                conclusion=conclusion,
                url="u",
            ),
        )

    @staticmethod
    def _run(run_id, created_at):
        return github.Run(
            id=run_id,
            event="push",
            head_sha=f"sha{run_id}",
            head_branch="main",
            created_at=created_at,
            conclusion="success",
            url="u",
        )

    def _lines(self, db, monkeypatch, runs):
        from tools.ci_failures.ingest import ingest

        self._listing(monkeypatch, runs)
        said: list[str] = []
        ingest(db, limit=25, out=said.append, dry_run=True)
        return said

    def test_it_says_what_the_listing_actually_spanned(self, tmp_path, monkeypatch):
        """The line that would have made the odd call obvious while it happened."""
        said = self._lines(
            tmp_path / "ci.sqlite3",
            monkeypatch,
            [
                self._run(1, "2026-09-02T10:00:00Z"),
                self._run(2, "2026-06-05T10:00:00Z"),
            ],
        )

        assert any("2026-06-05" in line and "2026-09-02" in line for line in said), said

    def test_a_run_it_already_has_but_was_not_offered_is_called_out(
        self, tmp_path, monkeypatch
    ):
        """The database is the second opinion. A run stored inside the span the
        listing claims to cover, and absent from it, means the page disagrees
        with what is known - which is exactly the shape of the bad call."""
        db = tmp_path / "ci.sqlite3"
        TestTheReportingWindow._seed(
            self, db, [(77, "2026-07-01T10:00:00Z", [("A", "PASS")])]
        )

        said = self._lines(
            db,
            monkeypatch,
            [
                self._run(1, "2026-09-02T10:00:00Z"),
                self._run(2, "2026-06-05T10:00:00Z"),
            ],
        )

        assert any("77" in line and "not offered" in line for line in said), said

    def test_a_run_being_re_run_right_now_is_not_a_disagreement(
        self, tmp_path, monkeypatch
    ):
        """Both listings ask for `status=completed`, and a job re-run by hand
        goes back to in_progress until it finishes. That run drops out of the
        listing legitimately, and calling it a disagreement would fire this
        warning during exactly the operation the tool exists to observe."""
        from tools.ci_failures.ingest import ingest

        db = tmp_path / "ci.sqlite3"
        TestTheReportingWindow._seed(
            self, db, [(77, "2026-07-01T10:00:00Z", [("A", "PASS")])]
        )
        self._listing(
            monkeypatch,
            [
                self._run(1, "2026-09-02T10:00:00Z"),
                self._run(2, "2026-06-05T10:00:00Z"),
            ],
            conclusion=None,
        )
        said: list[str] = []
        ingest(db, limit=25, out=said.append, dry_run=True)

        assert not any("not offered" in line for line in said), said

    def test_a_listing_that_agrees_with_the_database_says_nothing(
        self, tmp_path, monkeypatch
    ):
        db = tmp_path / "ci.sqlite3"
        TestTheReportingWindow._seed(
            self, db, [(1, "2026-09-02T10:00:00Z", [("A", "PASS")])]
        )

        said = self._lines(db, monkeypatch, [self._run(1, "2026-09-02T10:00:00Z")])

        assert not any("not offered" in line for line in said), said

    def test_runs_with_nothing_to_fetch_are_named_rather_than_only_counted(
        self, tmp_path, monkeypatch
    ):
        """One silent bucket held both "already have it" and "this run uploaded
        nothing", and those are different findings."""
        said = self._lines(
            tmp_path / "ci.sqlite3", monkeypatch, [self._run(5, "2026-09-02T10:00:00Z")]
        )

        assert any("run 5" in line and "no test artifacts" in line for line in said), (
            said
        )


class TestEveryTestArtifactOfARun:
    """Only the `testing` job's artifacts used to be read. The clean install,
    BrowserBatteries and docker checks upload a whole suite's output.xml from
    the same Run, and a test failing only on an installed wheel was invisible.
    See `docs/adr/0003-every-test-artifact-of-a-run.md`."""

    @staticmethod
    def _listing(monkeypatch, names):
        import json as json_module

        def fake_run(args, **kwargs):
            class Result:
                returncode = 0
                stdout = json_module.dumps(
                    [
                        {
                            "artifacts": [
                                {"id": index, "name": name, "expired": False}
                                for index, name in enumerate(names)
                            ]
                        }
                    ]
                )
                stderr = ""

            return Result()

        monkeypatch.setattr(github.subprocess, "run", fake_run)

    def test_every_install_is_listed_and_nothing_else(self, monkeypatch):
        self._listing(
            monkeypatch,
            [
                "Test results-ubuntu-latest-3-3.13-22.x",
                "ubuntu-latest 3.13 24.x Clean install results",
                "Clean_install_results_macos-latest",
                "docker_results",
                "Unit test results-ubuntu-latest-3.13-22.x",
                "node-coverage-ubuntu-latest-3.14-22.x",
                "demoapp-bb-test-macos-latest",
                "rfbrowser-wheel",
            ],
        )

        listed = [artifact.name for artifact in github.list_test_artifacts(1)]

        assert listed == [
            "Test results-ubuntu-latest-3-3.13-22.x",
            "ubuntu-latest 3.13 24.x Clean install results",
            "Clean_install_results_macos-latest",
            "docker_results",
        ]

    @staticmethod
    def _ingest_as(fake_ci, monkeypatch, db, name):
        artifact = github.Artifact(**{**fake_ci["artifact"].__dict__, "name": name})
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: [artifact]
        )
        return ingest.ingest(db, limit=5, out=lambda _: None)

    @staticmethod
    def _failing_test(db):
        return next(
            t
            for t in build_json(db)["test_failures"]
            if t["test"].endswith("Failing Test")
        )

    def test_a_failure_says_which_install_it_happened_on(
        self, fake_ci, tmp_path, monkeypatch
    ):
        db = tmp_path / "ci.sqlite3"
        self._ingest_as(
            fake_ci, monkeypatch, db, "ubuntu-latest 3.13 24.x Clean install results"
        )

        entry = self._failing_test(db)

        assert [o["install"] for o in entry["occurrences"]] == ["wheel"]
        assert [r["install"] for r in entry["rates"]] == ["wheel"]

    def test_a_wheel_install_is_its_own_configuration(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """Same machine, same versions, different Install: two rates, so that a
        test failing only on an installed wheel reads as such."""
        artifacts = [
            github.Artifact(**{**fake_ci["artifact"].__dict__, "id": id_, "name": name})
            for id_, name in (
                (1, "Test results-ubuntu-latest-1-3.13-24.x"),
                (2, "ubuntu-latest 3.13 24.x Clean install results"),
            )
        ]
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: artifacts
        )
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        entry = self._failing_test(db)

        assert sorted((r["install"], r["ran"]) for r in entry["rates"]) == [
            ("source", 1),
            ("wheel", 1),
        ]

    @pytest.mark.parametrize(
        ("artifact_name", "leg"),
        [
            (
                "Test results-ubuntu-latest-3-3.13-22.x",
                "source · ubuntu-latest · shard 3 · 3.13 · 22.x",
            ),
            (
                "ubuntu-latest 3.13 24.x Clean install results",
                "wheel · ubuntu-latest · 3.13 · 24.x",
            ),
            ("Clean_install_results_macos-15-intel", "batteries · macos-15-intel"),
            ("docker_results", "docker"),
        ],
    )
    def test_a_leg_is_named_the_same_way_whichever_job_ran_it(
        self, fake_ci, tmp_path, monkeypatch, artifact_name, leg
    ):
        db = tmp_path / "ci.sqlite3"
        self._ingest_as(fake_ci, monkeypatch, db, artifact_name)

        entry = self._failing_test(db)

        assert [o["leg"] for o in entry["occurrences"]] == [leg]

    @staticmethod
    def _serve(monkeypatch, tmp_path, write):
        """Every download is a zip that `write` fills; returns the ids fetched."""
        zip_path = tmp_path / "served.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            write(archive)
        downloads = []

        def fake_download(artifact_id, destination):
            downloads.append(artifact_id)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zip_path.read_bytes())
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", fake_download)
        return downloads

    def test_a_leg_whose_root_suite_is_not_atest_test_is_refused_for_good(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """What the docker job uploaded until it was fixed: `robot` run on the
        directory `atest/` was mounted at, which put every test one suite level
        deeper and made each of them a different test from the same one on
        every other Leg."""
        mounted = tmp_path / "home" / "pwuser" / "test"
        (mounted / "test").mkdir(parents=True)
        (mounted / "test" / "suite.robot").write_text(SUITE, encoding="utf-8")
        with open(tmp_path / "stdout.txt", "w", encoding="utf-8") as captured:
            robot_run(
                str(mounted),
                outputdir=str(tmp_path),
                output="docker.xml",
                log=None,
                report=None,
                stdout=captured,
            )
        downloads = self._serve(
            monkeypatch,
            tmp_path,
            lambda archive: archive.write(tmp_path / "docker.xml", "output.xml"),
        )
        db = tmp_path / "ci.sqlite3"

        said: list[str] = []
        first = self._ingest_as(fake_ci, monkeypatch, db, "docker_results")
        second = ingest.ingest(db, limit=5, out=said.append)

        assert (first.unusable, first.legs) == (1, 0)
        assert len(downloads) == 1, "refused once, not fetched again"
        assert second.unusable == 0
        reason = one_row(db, "SELECT reason FROM unusable_artifact")["reason"]
        assert "suite layout" in reason and "pwuser/test" in reason

    def test_an_output_xml_cut_off_by_a_timeout_is_not_fetched_again(
        self, fake_ci, output_xml, tmp_path, monkeypatch
    ):
        """What a job killed by its timeout leaves: the zip is whole and the
        output.xml in it stops mid-element. It never parses, however often it is
        downloaded, and it is twenty megabytes a time."""
        whole = output_xml.read_bytes()
        downloads = self._serve(
            monkeypatch,
            tmp_path,
            lambda archive: archive.writestr("output.xml", whole[: len(whole) // 2]),
        )
        db = tmp_path / "ci.sqlite3"

        first = ingest.ingest(db, limit=5, out=lambda _: None)
        ingest.ingest(db, limit=5, out=lambda _: None)

        assert (first.unusable, first.unreachable, first.legs) == (1, 0, 0)
        assert len(downloads) == 1
        reason = one_row(db, "SELECT reason FROM unusable_artifact")["reason"]
        assert reason.startswith("output.xml does not parse")
        assert str(tmp_path) not in reason and "/tmp" not in reason

    def test_a_zip_that_will_not_open_is_still_tried_again(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """That one is the download's fault, and the next may be whole."""
        downloads = []

        def truncated(artifact_id, destination):
            downloads.append(artifact_id)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"not a zip")
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", truncated)
        db = tmp_path / "ci.sqlite3"

        ingest.ingest(db, limit=5, out=lambda _: None)
        second = ingest.ingest(db, limit=5, out=lambda _: None)

        assert (second.unreachable, second.unusable) == (1, 0)
        assert len(downloads) == 2

    def test_legs_ingested_before_installs_were_recorded_are_source(
        self, fake_ci, tmp_path
    ):
        """Everything ingested before this came from the `testing` job, which is
        the `source` Install. Known from the stored artifact name, so nothing is
        invented and nothing has to be downloaded again."""
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)
        leg_table_without(db, "install")

        entry = self._failing_test(db)

        assert [r["install"] for r in entry["rates"]] == ["source"]

    def test_the_install_is_recomputed_from_the_stored_artifact_name(
        self, fake_ci, tmp_path, monkeypatch
    ):
        db = tmp_path / "ci.sqlite3"
        self._ingest_as(
            fake_ci, monkeypatch, db, "Clean_install_results_windows-latest"
        )
        with closing(sqlite3.connect(db)) as connection:
            connection.execute("UPDATE leg SET install = 'stale'")
            connection.commit()

        recomputed = ingest.recompute_installs(db, out=lambda _: None)

        assert recomputed == 1
        assert [r["install"] for r in self._failing_test(db)["rates"]] == ["batteries"]

    def test_failures_per_leg_are_counted_per_install_too(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """A serial whole-suite Leg runs about four times the tests a parallel
        shard does, so counting both as one leg each made "per leg" mean a
        different thing on every platform."""
        artifacts = [
            github.Artifact(**{**fake_ci["artifact"].__dict__, "id": id_, "name": name})
            for id_, name in (
                (1, "Test results-ubuntu-latest-1-3.13-24.x"),
                (2, "Test results-ubuntu-latest-2-3.13-24.x"),
                (3, "ubuntu-latest 3.13 24.x Clean install results"),
            )
        ]
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id: artifacts
        )
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        platforms = build_json(db)["platforms"]

        assert sorted((p["install"], p["legs"]) for p in platforms) == [
            ("source", 2),
            ("wheel", 1),
        ]


class TestOnePlatformPerOperatingSystem:
    """`platform.platform()` names the same runner differently under each Python
    version and after every runner image update, and it was stored in the same
    column as the `sys.platform` the generator line gives. One runner read as up
    to five platforms. See `docs/adr/0004-platform-is-the-operating-system.md`."""

    @staticmethod
    def _failing_test(db):
        return next(
            t
            for t in build_json(db)["test_failures"]
            if t["test"].endswith("Failing Test")
        )

    def test_failures_are_counted_by_platform_and_the_release_is_kept_on_each(
        self, fake_ci, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)

        entry = self._failing_test(db)

        assert [r["platform"] for r in entry["rates"]] == ["linux"]
        assert [o["platform"] for o in entry["occurrences"]] == ["linux"]
        assert [o["os_release"] for o in entry["occurrences"]] == ["Linux-6.8-x86_64"]

    def test_a_database_from_before_keeps_the_release_and_counts_by_platform(
        self, fake_ci, tmp_path
    ):
        """What was stored as the platform is moved, not lost: it is the only
        copy of it, and nothing has to be downloaded again."""
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)
        leg_table_without(db, "os_release")
        with closing(sqlite3.connect(db)) as connection:
            connection.execute("UPDATE leg SET platform = 'Linux-6.8-x86_64'")
            connection.commit()

        entry = self._failing_test(db)

        assert [r["platform"] for r in entry["rates"]] == ["linux"]
        assert [o["os_release"] for o in entry["occurrences"]] == ["Linux-6.8-x86_64"]

    def test_the_platform_is_recomputed_from_what_is_stored(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)
        with closing(sqlite3.connect(db)) as connection:
            connection.execute(
                "UPDATE leg SET platform = 'Windows-10-10.0.26100-SP0', "
                "os_release = NULL"
            )
            connection.commit()

        recomputed = ingest.recompute_platforms(db, out=lambda _: None)

        entry = self._failing_test(db)
        assert recomputed == 1
        assert [r["platform"] for r in entry["rates"]] == ["win32"]
        assert [o["os_release"] for o in entry["occurrences"]] == [
            "Windows-10-10.0.26100-SP0"
        ]

    def test_a_recompute_reads_the_release_rather_than_what_was_made_of_it(
        self, fake_ci, tmp_path
    ):
        """Once migrated, `platform` holds only the reduced value. A changed rule
        has to be applied to the full string or it can never change anything."""
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, out=lambda _: None)
        with closing(sqlite3.connect(db)) as connection:
            connection.execute(
                "UPDATE leg SET platform = 'linux', "
                "os_release = 'macOS-26.6.2-arm64-arm-64bit'"
            )
            connection.commit()

        ingest.recompute_platforms(db, out=lambda _: None)

        assert [r["platform"] for r in self._failing_test(db)["rates"]] == ["darwin"]


class TestOneTestsReport:
    """`inv ci-report --test`: the Report for one test, taken from the whole
    Report rather than asked for again, so it cannot disagree with the page."""

    def test_only_the_named_tests_groups_are_kept(self, tmp_path):
        from tools.ci_failures.report import of_test

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "S.Wanted", "status": "FAIL", "signature": "Timeout"},
                {"test": "S.Wanted", "status": "FAIL", "signature": "Box <n>"},
                {"test": "S.Other", "status": "FAIL", "signature": "Timeout"},
            ],
        )

        report = of_test(build_report(db), "S.Wanted")

        assert sorted(e.signature for e in report.test_failures) == [
            "Box <n>",
            "Timeout",
        ]
        assert {e.test for e in report.test_failures} == {"S.Wanted"}

    def test_a_broken_fixture_of_an_enclosing_suite_is_kept(self, tmp_path):
        """A suite setup that broke fails the test without the test being
        at fault, and that is the first thing to rule out."""
        from tools.ci_failures.report import of_test

        db = tmp_path / "ci.sqlite3"
        fixture = {"status": "FAIL", "signature": "setup broke"}
        seed(
            db,
            [
                {
                    **fixture,
                    "test": "Outer.Inner.Wanted",
                    "scope": "suite_setup",
                    "owner": "Outer",
                },
                {
                    **fixture,
                    "test": "Outermost.Other",
                    "scope": "suite_setup",
                    "owner": "Outermost",
                },
            ],
        )

        report = of_test(build_report(db), "Outer.Inner.Wanted")

        assert [e.suite for e in report.fixture_failures] == ["Outer"]

    @pytest.mark.parametrize("lookalike", ["Outer_Suite", "outer.suite"])
    def test_a_suite_whose_name_only_looks_alike_is_not_enclosing(
        self, tmp_path, lookalike
    ):
        from tools.ci_failures.report import of_test

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": f"{lookalike}.Other",
                    "status": "FAIL",
                    "signature": "setup broke",
                    "scope": "suite_setup",
                    "owner": lookalike,
                },
                {"test": "Outer.Suite.Wanted", "status": "FAIL", "signature": "e"},
            ],
        )

        report = of_test(build_report(db), "Outer.Suite.Wanted")

        assert report.fixture_failures == ()

    def test_what_changed_is_said_only_about_this_test(self, tmp_path):
        from tools.ci_failures.annotations import write_snapshot
        from tools.ci_failures.report import of_test

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "S.Wanted", "status": "FAIL", "signature": "Timeout"},
                {"test": "S.Other", "status": "FAIL", "signature": "Timeout"},
            ],
        )
        write_snapshot(db, [("S.Unrelated", "Timeout", 1)])

        changes = of_test(build_report(db), "S.Wanted").since_last_report

        assert changes is not None
        assert [c["subject"] for c in changes["new"]] == ["S.Wanted"]
        assert changes["gone"] == []

    def test_a_test_ranked_past_the_page_limit_is_still_found(self, tmp_path):
        """`--limit` is how many Groups the page shows; the one test asked for
        can rank anywhere."""
        from tools.ci_failures.report import of_test

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "S.Often", "status": "FAIL", "signature": "e", "sha": sha}
                for sha in ("a", "b")
            ]
            + [{"test": "S.Rarely", "status": "FAIL", "signature": "e"}],
        )

        report = of_test(build_report(db, limit=None), "S.Rarely")

        assert [e.test for e in report.test_failures] == ["S.Rarely"]


class TestTheWorkspace:
    def test_what_is_derived_from_a_database_lives_beside_it(self, tmp_path):
        from tools.ci_failures import workspace

        db = tmp_path / "scratch" / "ci.sqlite3"

        assert workspace.artifacts(db) == tmp_path / "scratch" / "artifacts"
        assert workspace.page(db) == tmp_path / "scratch" / "ci_report.html"
        assert workspace.snapshot(db) == tmp_path / "scratch" / "last_report.json"

    def test_no_database_named_is_the_one_at_the_repository_root(self):
        from tools.ci_failures import workspace

        root = Path(__file__).resolve().parents[1]

        assert workspace.database(None) == root / "ci_failures" / "ci_failures.sqlite3"
        assert workspace.database("x/y.sqlite3") == Path("x/y.sqlite3")

    def test_the_snapshot_is_taken_into_the_databases_workspace(self, tmp_path):
        from tools.ci_failures.annotations import write_snapshot

        db = tmp_path / "scratch" / "ci.sqlite3"
        seed(db, [{"test": "S.T", "status": "FAIL", "signature": "e"}])

        written = write_snapshot(db, [("S.T", "e", 1)])

        assert written.parent == db.parent

    def test_known_causes_are_not_in_the_default_workspace(self):
        from tools.ci_failures.annotations import KNOWN_CAUSES
        from tools.ci_failures import workspace

        assert workspace.database(None).parent not in KNOWN_CAUSES.parents


class TestResolvingATestName:
    """A Test Name typed for a test, resolved against the names where it was
    looked for: the archive, one Run, or one Leg's output.xml."""

    COMBINED = "03 Waiting & 05 JS Tests"
    NAMES = (
        f"{COMBINED}.05 JS Tests.Js.Run Js",
        "Test.Http.GET Text",
        "Test.Http With Waiting.GET Text",
    )

    def test_a_name_that_is_there_is_itself(self):
        from tools.ci_failures.history import resolve

        assert resolve("Test.Http.GET Text", self.NAMES, "the archive") == (
            "Test.Http.GET Text"
        )

    def test_another_top_suite_is_the_same_test(self):
        from tools.ci_failures.history import resolve

        assert resolve("Test.05 JS Tests.Js.Run Js", self.NAMES, "this Leg") == (
            f"{self.COMBINED}.05 JS Tests.Js.Run Js"
        )

    def test_every_other_top_suite_is_the_same_test(self):
        from tools.ci_failures.history import resolve

        names = ("A & B.Js.Run Js", "C & D.Js.Run Js")

        assert resolve("Test.Js.Run Js", names, "the archive") == "A & B.Js.Run Js"

    def test_a_suite_that_also_appears_below_the_top_is_not_a_top_suite(self):
        from tools.ci_failures.history import NoSuchTestError, resolve

        with pytest.raises(NoSuchTestError):
            resolve("Http.Http.GET", ("Http.Http.GET2", "Test.Http.GET"), "Run 7")

    def test_a_path_below_the_top_suite_is_offered_not_assumed(self):
        from tools.ci_failures.history import NoSuchTestError, resolve

        with pytest.raises(NoSuchTestError) as refused:
            resolve("Js.Run Js", self.NAMES, "Run 7")

        assert str(refused.value) == (
            "No test named 'Js.Run Js' in Run 7. Did you mean:\n"
            f"  {self.COMBINED}.05 JS Tests.Js.Run Js"
        )

    def test_the_fetch_does_not_load_the_report(self):
        import subprocess
        import sys

        loaded = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys, tools.ci_failures.artifacts; "
                "print('tools.ci_failures.report' in sys.modules)",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        assert loaded == "False"


class TestATestWithNoFailures:
    """`inv ci-report --test` on a test with no Groups: a typo, a test outside
    the Window and a healthy test used to read alike, as "did not fail"."""

    def test_one_that_ran_and_never_failed_says_how_often_it_ran(self, tmp_path):
        from tools.ci_failures.history import never_failed

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "Test.S.Healthy", "status": "PASS", "sha": "a"},
                {"test": "Test.S.Healthy", "status": "PASS", "sha": "b"},
                {"test": "Test.S.Healthy", "status": "SKIP", "sha": "c"},
            ],
        )

        assert never_failed(db, "Test.S.Healthy").line() == (
            "'Test.S.Healthy' ran 3 times in all history: 0 failures, 1 skip."
        )

    def test_a_name_in_no_result_is_refused_with_every_name_ending_in_it(
        self, tmp_path
    ):
        """A short name is shared across suites, and naming one of them
        would be a guess."""
        from tools.ci_failures.history import NoSuchTestError, never_failed

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "Test.Http.GET Text", "status": "PASS"},
                {"test": "Test.Http With Waiting.GET Text", "status": "PASS"},
                {"test": "Test.Http.GET Json", "status": "PASS"},
            ],
        )

        with pytest.raises(NoSuchTestError) as refused:
            never_failed(db, "GET Text")

        assert refused.value.suggestions == (
            "Test.Http With Waiting.GET Text",
            "Test.Http.GET Text",
        )
        assert str(refused.value) == (
            "No test named 'GET Text' in the archive. Did you mean:\n"
            "  Test.Http With Waiting.GET Text\n"
            "  Test.Http.GET Text"
        )

    def test_a_misspelt_name_is_matched_by_similarity(self, tmp_path):
        from tools.ci_failures.history import NoSuchTestError, never_failed

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "Test.Credentials.Add Valid Credential", "status": "PASS"},
                {"test": "Test.Http.GET Text", "status": "PASS"},
            ],
        )

        with pytest.raises(NoSuchTestError) as refused:
            never_failed(db, "Test.Credentials.Add Valid Credentail")

        assert refused.value.suggestions == ("Test.Credentials.Add Valid Credential",)

    def test_one_that_ran_only_before_the_window_says_when_it_last_ran(self, tmp_path):
        from datetime import datetime

        from tools.ci_failures.history import NotInWindowError, never_failed
        from tools.ci_failures.window import of_days

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": "Test.S.Removed", "status": "PASS", "sha": "a"},
                {"test": "Test.S.Kept", "status": "PASS", "sha": "b"},
            ],
        )
        window = of_days(1, datetime(2026, 8, 21, 12).astimezone())

        with pytest.raises(NotInWindowError) as refused:
            never_failed(db, "Test.S.Removed", window)

        assert str(refused.value) == (
            f"'Test.S.Removed' did not run in {window.label}; it last ran on "
            "2026-08-20. Widen --days."
        )


class TestTheControlsOfARun:
    """`inv ci-artifact --run --test` without `--leg`: which Legs of the Run ran
    the test, and which of them passed it - read from the database, so the
    choice of a Control costs no download. See **Control** in CONTEXT.md and
    ADR 0006."""

    TEST = "Test.Credentials.Add Valid Credential With Secret"
    BATTERIES = "Clean_install_results_windows-latest"
    WHEEL = "windows-latest 3.13 24.x Clean install results"
    SOURCE = "Test results-ubuntu-latest-2-3.13-24.x"

    def test_every_leg_that_ran_the_test_is_listed_by_install_and_passes_are_controls(
        self, tmp_path
    ):
        from tools.ci_failures.history import of_run

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": self.TEST,
                    "status": "PASS",
                    "sha": "1a2b3c4d5e",
                    "artifact": self.WHEEL,
                },
                {
                    "test": self.TEST,
                    "status": "FAIL",
                    "sha": "1a2b3c4d5e",
                    "artifact": self.BATTERIES,
                },
                {
                    "test": self.TEST,
                    "status": "PASS",
                    "sha": "1a2b3c4d5e",
                    "artifact": self.BATTERIES,
                    "attempt": 2,
                },
                {
                    "test": self.TEST,
                    "status": "PASS",
                    "sha": "1a2b3c4d5e",
                    "artifact": self.SOURCE,
                },
                {
                    "test": "Test.Other.Elsewhere",
                    "status": "PASS",
                    "sha": "1a2b3c4d5e",
                    "artifact": "Test results-ubuntu-latest-1-3.13-24.x",
                },
                {
                    "test": self.TEST,
                    "status": "FAIL",
                    "sha": "next",
                    "artifact": self.WHEEL,
                },
            ],
        )

        assert of_run(db, 1, self.TEST).lines() == [
            f"Run 1 · commit 1a2b3c4 · {self.TEST}",
            "batteries",
            "  fail     batteries · windows-latest                       --attempt 1",
            "  control  batteries · windows-latest                       --attempt 2",
            "source",
            "  control  source · ubuntu-latest · shard 2 · 3.13 · 24.x   --attempt 1",
            "wheel",
            "  control  wheel · windows-latest · 3.13 · 24.x             --attempt 1",
            f'fetch one: inv ci-artifact --run 1 --leg "<leg>" --attempt <n> '
            f'--test "{self.TEST}"',
        ]

    def test_a_listed_leg_is_what_the_fetch_takes_as_leg(self):
        """The listing prints `leg_name`, and the fetch matches `--leg` by
        `leg_name` of it - so a printed name has to come back unchanged."""
        from tools.ci_failures.legs import leg_name

        for artifact in (self.BATTERIES, self.WHEEL, self.SOURCE, "docker_results"):
            assert leg_name(leg_name(artifact)) == leg_name(artifact)

    def test_a_failure_its_suite_fixture_marked_is_not_called_a_failure(self, tmp_path):
        from tools.ci_failures.history import of_run

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": self.TEST,
                    "status": "FAIL",
                    "scope": "suite_setup",
                    "owner": "Test.Credentials",
                    "artifact": self.BATTERIES,
                },
            ],
        )

        assert of_run(db, 1, self.TEST).lines()[2] == (
            "  suite broke  batteries · windows-latest   --attempt 1"
        )

    def test_a_leg_whose_attempt_is_unknown_is_shown_not_dropped(self, tmp_path):
        from tools.ci_failures.history import of_run

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {
                    "test": self.TEST,
                    "status": "PASS",
                    "artifact": self.WHEEL,
                    "attempt": None,
                },
            ],
        )

        lines = of_run(db, 1, self.TEST).lines()

        assert lines[2] == (
            "  control  wheel · windows-latest · 3.13 · 24.x   --attempt ?"
        )
        assert lines[-1] == (
            "attempt ? is not yet resolved: try --attempt 1, or "
            "`inv ci-backfill-attempts` first."
        )

    def test_a_run_not_in_the_database_is_refused_not_looked_up_on_github(
        self, tmp_path, monkeypatch
    ):
        from tools.ci_failures.history import NotIngestedError, of_run

        db = tmp_path / "ci.sqlite3"
        seed(db, [{"test": self.TEST, "status": "PASS"}])
        monkeypatch.setattr(github, "list_test_artifacts", pytest.fail)

        with pytest.raises(NotIngestedError) as refused:
            of_run(db, 99, self.TEST)

        assert str(refused.value) == (
            "Run 99 is not in the database; `inv ci-ingest` first."
        )

    def test_a_name_the_run_did_not_run_is_refused_with_its_names(self, tmp_path):
        from tools.ci_failures.history import NoSuchTestError, of_run

        db = tmp_path / "ci.sqlite3"
        seed(
            db,
            [
                {"test": self.TEST, "status": "PASS"},
                {"test": "Test.Http.GET Text", "status": "PASS", "sha": "other"},
            ],
        )

        with pytest.raises(NoSuchTestError) as refused:
            of_run(db, 1, "Add Valid Credential With Secret")

        assert str(refused.value) == (
            "No test named 'Add Valid Credential With Secret' in Run 1. Did you mean:\n"
            f"  {self.TEST}"
        )


class TestFetchingOneLegsArtifact:
    """`inv ci-artifact`: the files ingest threw away, fetched again for one
    failure that turned out to deserve them."""

    RUN = 36044928092
    LEG = "source · macos-latest · shard 3 · 3.10 · 22.x"

    @pytest.fixture
    def one_leg(self, monkeypatch, tmp_path):
        artifact = github.Artifact(
            id=10828316847,
            name="Test results-macos-latest-3-3.10-22.x",
            expired=False,
            url="u",
        )
        other = github.Artifact(
            id=1, name="Test results-ubuntu-latest-1-3.14-22.x", expired=False, url="u"
        )
        zip_path = tmp_path / "artifact.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("output.xml", "<robot/>")
            archive.writestr("log.html", "")
            archive.writestr("playwright-log.txt", "")
            archive.writestr("pabot_results/4/browser/screenshot/fail-1.png", "")
        downloads = []

        def fake_download(artifact_id, destination):
            downloads.append(artifact_id)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zip_path.read_bytes())
            return destination

        monkeypatch.setattr(
            github, "list_test_artifacts", lambda run_id: [other, artifact]
        )
        monkeypatch.setattr(github, "download_artifact", fake_download)
        monkeypatch.setattr(
            github,
            "get_run",
            lambda run_id: github.Run(
                id=run_id,
                event="push",
                head_sha="s",
                head_branch="main",
                created_at="2026-09-27T10:00:00Z",
                conclusion="failure",
                url="u",
            ),
        )
        return downloads

    def test_the_legs_files_are_unpacked_under_root(self, one_leg, tmp_path):
        from tools.ci_failures.artifacts import fetch

        root = tmp_path / "artifacts"

        directory = fetch(self.RUN, self.LEG, root)

        assert one_leg == [10828316847]
        assert directory.parent == root
        assert (directory / "output.xml").is_file()
        assert (directory / "pabot_results/4/browser/screenshot/fail-1.png").is_file()

    def test_a_leg_already_fetched_is_not_fetched_again(self, one_leg, tmp_path):
        from tools.ci_failures.artifacts import fetch

        root = tmp_path / "artifacts"
        first = fetch(self.RUN, self.LEG, root)

        again = fetch(self.RUN, self.LEG, root)

        assert one_leg == [10828316847], "one download, not two"
        assert again == first

    def test_the_artifacts_own_name_finds_the_same_leg(self, one_leg, tmp_path):
        from tools.ci_failures.artifacts import fetch

        root = tmp_path / "artifacts"

        by_name = fetch(self.RUN, "Test results-macos-latest-3-3.10-22.x", root)

        assert by_name == fetch(self.RUN, self.LEG, root)
        assert one_leg == [10828316847]

    def test_an_unknown_leg_is_refused_with_the_legs_the_run_has(
        self, one_leg, tmp_path
    ):
        from tools.ci_failures.artifacts import NoSuchLegError, fetch

        with pytest.raises(NoSuchLegError, match="source · ubuntu-latest · shard 1"):
            fetch(self.RUN, "source · windows-latest", tmp_path / "artifacts")

        assert one_leg == []

    def test_a_failed_download_leaves_nothing_to_be_mistaken_for_the_leg(
        self, one_leg, monkeypatch, tmp_path
    ):
        """A half-unpacked directory would be reused next time as if whole."""
        from tools.ci_failures.artifacts import fetch

        def unreachable(artifact_id, destination):
            raise github.GhError("could not resolve host")

        monkeypatch.setattr(github, "download_artifact", unreachable)
        root = tmp_path / "artifacts"

        from tools.ci_failures.refusal import UnreachableError

        with pytest.raises(UnreachableError, match="could not resolve host"):
            fetch(self.RUN, self.LEG, root)

        assert list(root.iterdir()) == []

    def test_a_download_that_is_not_a_zip_is_unreachable_too(
        self, one_leg, monkeypatch, tmp_path
    ):
        from tools.ci_failures.artifacts import fetch
        from tools.ci_failures.refusal import UnreachableError

        def truncated(artifact_id, destination):
            destination.write_bytes(b"PK\x03\x04 cut off")
            return destination

        monkeypatch.setattr(github, "download_artifact", truncated)

        with pytest.raises(UnreachableError):
            fetch(self.RUN, self.LEG, tmp_path / "artifacts")

    def test_clean_removes_every_fetched_leg(self, one_leg, tmp_path):
        from tools.ci_failures.artifacts import clean, fetch

        root = tmp_path / "artifacts"
        fetch(self.RUN, self.LEG, root)

        assert clean(root) is True
        assert not root.exists()
        assert clean(root) is False, "nothing to clean is not an error"

    def test_a_rerun_legs_attempt_is_the_one_fetched(
        self, one_leg, monkeypatch, tmp_path
    ):
        """A flake that passed on the re-run uploaded the same Leg twice, and
        the failure is in the first."""
        from tools.ci_failures.artifacts import fetch

        name = "Test results-macos-latest-3-3.10-22.x"
        failed = github.Artifact(
            id=11, name=name, expired=False, url="u", created_at="2026-09-27T10:30Z"
        )
        passed = github.Artifact(
            id=12, name=name, expired=False, url="u", created_at="2026-09-27T12:30Z"
        )
        monkeypatch.setattr(
            github, "list_test_artifacts", lambda run_id: [passed, failed]
        )
        monkeypatch.setattr(
            github,
            "attempt_starts",
            lambda run: [(1, "2026-09-27T10:00Z"), (2, "2026-09-27T12:00Z")],
        )
        root = tmp_path / "artifacts"

        first = fetch(self.RUN, self.LEG, root, attempt=1)
        second = fetch(self.RUN, self.LEG, root, attempt=2)

        assert one_leg == [11, 12]
        assert first != second

    def test_an_empty_artifact_unpacks_to_an_empty_leg(
        self, one_leg, monkeypatch, tmp_path
    ):
        from tools.ci_failures.artifacts import fetch

        def empty(artifact_id, destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(destination, "w"):
                pass
            return destination

        monkeypatch.setattr(github, "download_artifact", empty)

        directory = fetch(self.RUN, self.LEG, tmp_path / "artifacts")

        assert list(directory.iterdir()) == []


FAKE_COMMON = """\
def start_test_server(port):
    return port


def start_test_https_server(port):
    return port
"""


def _run_executor(
    output_dir: Path, suites: dict[str, str], port: str, metadata: tuple[str, ...] = ()
) -> Path:
    """An Executor's output.xml, from a real Robot Framework run.

    `common.py` stands in for `atest/library/common.py`: its keywords are what
    the shortlist reads the test-app ports from, by library and keyword name.
    """
    root = output_dir / "atest" / "test"
    root.mkdir(parents=True, exist_ok=True)
    (root / "common.py").write_text(FAKE_COMMON, encoding="utf-8")
    (root / "__init__.robot").write_text(
        "*** Settings ***\n"
        "Library    common.py\n"
        "Suite Setup    Start Test Application\n\n"
        "*** Keywords ***\n"
        "Start Test Application\n"
        f"    ${{port}} =    Start Test Server    {port}\n",
        encoding="utf-8",
    )
    for name, text in suites.items():
        (root / name).write_text(text, encoding="utf-8")
    with open(output_dir / "stdout.txt", "w", encoding="utf-8") as captured:
        robot_run(
            str(root),
            outputdir=str(output_dir),
            output="output.xml",
            log=None,
            report=None,
            metadata=list(metadata),
            stdout=captured,
            stderr=captured,
        )
    shutil.rmtree(output_dir / "atest")
    (output_dir / "stdout.txt").unlink()
    return output_dir / "output.xml"


CREDENTIALS_SUITE = """\
*** Test Cases ***
Add Valid Credential
    Fail    Text 'Waiting for action...' (str) should be 'Success' (str)
"""


class TestShortlistingOneOccurrence:
    """`inv ci-artifact --test`: of everything in a Leg's artifact, the files
    that bear on one test."""

    def test_a_serial_leg_names_the_test_app_log_its_setup_started(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")
        (tmp_path / "test-app").mkdir()
        (tmp_path / "test-app" / "test-app-7001.log").write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        assert (
            Entry("test-app", "test-app/test-app-7001.log", "Start Test Server in Test")
            in listed.entries
        )

    def test_a_test_app_log_not_in_the_artifact_is_marked_missing(self, tmp_path):
        from tools.ci_failures.artifacts import shortlist

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        [test_app] = [e for e in listed.entries if e.label == "test-app"]
        assert test_app.missing

    def test_the_files_the_tests_log_links_to_are_listed_once_each(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        runner = r"file://D:\\a\\robotframework-browser\\atest\\output"
        suite = (
            "*** Test Cases ***\n"
            "Add Valid Credential\n"
            '    Log    <a href="browser/screenshot/fail-1.png">x</a>    html=True\n'
            f'    Log    <a href="{runner}\\\\browser\\\\screenshot\\\\fail-1.png">x</a>'
            "    html=True\n"
            '    Log    <a href="browser/screenshot/fail-97.png">x</a>    html=True\n'
            '    Log    <a href="https://example.invalid/page.png">x</a>    html=True\n'
            "    Log    See also file:///D:/a/robotframework-browser/atest/output/"
            "playwright-log-123.txt for additional details.\n"
            "    Fail    Text 'Waiting for action...' (str) should be 'Success' (str)\n"
        )
        _run_executor(tmp_path, {"credentials.robot": suite}, "7001")
        (tmp_path / "browser" / "screenshot").mkdir(parents=True)
        (tmp_path / "browser" / "screenshot" / "fail-1.png").write_bytes(b"")
        (tmp_path / "playwright-log-123.txt").write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        linked = [e for e in listed.entries if e.label in ("screenshot", "node log")]
        assert linked == [
            Entry("screenshot", "browser/screenshot/fail-1.png"),
            Entry("screenshot", "browser/screenshot/fail-97.png", missing=True),
            Entry("node log", "playwright-log-123.txt"),
        ]

    def test_a_pabot_executors_file_is_found_under_its_merged_name(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        runner = "file:///home/runner/work/rfb/rfb/atest/output/pabot_results/4"
        suite = (
            "*** Test Cases ***\n"
            "Add Valid Credential\n"
            f'    Log    <a href="{runner}/browser/screenshot/fail-1.png">x</a>'
            "    html=True\n"
            "    Fail    no\n"
        )
        _run_executor(tmp_path, {"credentials.robot": suite}, "7001")
        _run_executor(
            tmp_path / "pabot_results" / "4", {"credentials.robot": suite}, "7001"
        )
        merged = tmp_path / "browser" / "screenshot"
        merged.mkdir(parents=True)
        (merged / "20260928_181043-3-fail-1.png").write_bytes(b"")
        (merged / "20260928_181043-4-fail-1.png").write_bytes(b"")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        assert (
            Entry("screenshot", "browser/screenshot/20260928_181043-4-fail-1.png")
            in listed.entries
        )

    def test_a_shared_node_process_log_is_found_where_it_was_written(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        runner = "file:///home/runner/work/rfb/rfb/atest/output/pabot_results/5"
        suite = (
            "*** Test Cases ***\n"
            "Add Valid Credential\n"
            f"    Log    See also {runner}/playwright-log.txt for additional details.\n"
            "    Fail    no\n"
        )
        shared = ("Node Process:shared",)
        _run_executor(tmp_path, {"credentials.robot": suite}, "7001", shared)
        _run_executor(
            tmp_path / "pabot_results" / "5",
            {"credentials.robot": suite},
            "7001",
            shared,
        )
        (tmp_path / "playwright-log.txt").write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        assert [e for e in listed.entries if e.label == "node log"] == [
            Entry("node log", "playwright-log.txt", "the Leg's shared node process")
        ]

    def test_a_test_naming_no_node_log_gets_the_executors_default(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")
        for name in ("playwright-log.txt", "playwright-log-1790619542210617400.txt"):
            (tmp_path / name).write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        assert [e for e in listed.entries if e.label == "node log"] == [
            Entry("node log", "playwright-log.txt", "not named by the test")
        ]

    def test_a_test_not_in_the_leg_is_refused_with_the_names_it_may_mean(
        self, tmp_path
    ):
        from tools.ci_failures.artifacts import shortlist
        from tools.ci_failures.history import NoSuchTestError

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")

        with pytest.raises(NoSuchTestError) as refused:
            shortlist(tmp_path, "Credentials.Add Valid Credential")

        assert refused.value.suggestions == ("Test.Credentials.Add Valid Credential",)
        assert "in this Leg" in str(refused.value)

    def test_the_shortlist_prints_one_line_per_file_and_counts_the_rest(self):
        from tools.ci_failures.artifacts import Entry, Shortlist

        directory = Path("/a/36463000327-batteries-windows-latest-attempt-1")
        listed = Shortlist(
            directory=directory,
            test="Test.Credentials.Add Valid Credential",
            entries=(
                Entry("output.xml", "output.xml"),
                Entry("executor", ".", "serial"),
                Entry(
                    "test-app",
                    "test-app/test-app-60666.log",
                    "Start Test Server in Test",
                ),
                Entry("screenshot", "browser/screenshot/fail-97.png", missing=True),
                Entry("node log", "playwright-log.txt", "not named by the test"),
            ),
            others=((".png", 74), (".txt", 18), (".log", 2)),
        )

        assert listed.lines() == [
            f"directory:  {directory}",
            "output.xml: output.xml",
            "executor:   . (serial)",
            "test-app:   test-app/test-app-60666.log (Start Test Server in Test)",
            "screenshot: browser/screenshot/fail-97.png MISSING",
            "node log:   playwright-log.txt (not named by the test)",
            "also:       94 more files: 74 .png, 18 .txt, 2 .log",
        ]

    def test_without_a_test_only_the_legs_own_files_are_listed(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")
        (tmp_path / "log.html").write_text("", encoding="utf-8")
        (tmp_path / "browser" / "screenshot").mkdir(parents=True)
        for n in (1, 2):
            (tmp_path / "browser" / "screenshot" / f"fail-{n}.png").write_bytes(b"")

        listed = shortlist(tmp_path, None)

        assert listed.entries == (
            Entry("output.xml", "output.xml"),
            Entry("log", "log.html"),
        )
        assert listed.others == ((".png", 2),)

    def test_a_serial_leg_is_its_own_executor(self, tmp_path):
        from tools.ci_failures.artifacts import Entry, shortlist

        _run_executor(tmp_path, {"credentials.robot": CREDENTIALS_SUITE}, "7001")
        for name in ("log.html", "syslog.txt"):
            (tmp_path / name).write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Credentials.Add Valid Credential")

        assert listed.entries[:4] == (
            Entry("output.xml", "output.xml"),
            Entry("log", "log.html"),
            Entry("executor", ".", "serial"),
            Entry("syslog", "syslog.txt"),
        )

    def test_a_suite_setup_below_the_top_adds_its_own_test_app(self, tmp_path):
        from tools.ci_failures.artifacts import shortlist

        certificates = (
            "*** Settings ***\n"
            "Library    common.py\n"
            "Suite Setup    Setup\n\n"
            "*** Test Cases ***\n"
            "Client Certificate Is Sent\n"
            "    Fail    no certificate\n\n"
            "*** Keywords ***\n"
            "Setup\n"
            "    ${port} =    Start Test Https Server    7002\n"
        )
        _run_executor(tmp_path, {"client_certificates.robot": certificates}, "7001")

        listed = shortlist(
            tmp_path, "Test.Client Certificates.Client Certificate Is Sent"
        )

        assert [(e.path, e.note) for e in listed.entries if e.label == "test-app"] == [
            ("test-app/test-app-7001.log", "Start Test Server in Test"),
            (
                "test-app/test-app-7002.log",
                "Start Test Https Server in Test.Client Certificates",
            ),
        ]

    def test_a_pabot_leg_answers_from_the_executor_that_ran_the_test(self, tmp_path):
        """The merged output.xml puts every Executor's setup under one top
        suite, so the port there could be any of them."""
        from tools.ci_failures.artifacts import Entry, shortlist

        orders = "*** Test Cases ***\nOrder Is Placed\n    Fail    no order\n"
        both = {"credentials.robot": CREDENTIALS_SUITE, "orders.robot": orders}
        _run_executor(tmp_path, both, "7001")
        _run_executor(
            tmp_path / "pabot_results" / "0",
            {"credentials.robot": CREDENTIALS_SUITE},
            "7001",
        )
        executor = tmp_path / "pabot_results" / "1"
        _run_executor(executor, {"orders.robot": orders}, "7002")
        for name in ("syslog.txt", "robot_stdout.out", "robot_stderr.out"):
            (executor / name).write_text("", encoding="utf-8")

        listed = shortlist(tmp_path, "Test.Orders.Order Is Placed")

        start = listed.entries.index(Entry("executor", "pabot_results/1"))
        assert listed.entries[start : start + 5] == (
            Entry("executor", "pabot_results/1"),
            Entry("output.xml", "pabot_results/1/output.xml"),
            Entry("syslog", "pabot_results/1/syslog.txt"),
            Entry("stdout", "pabot_results/1/robot_stdout.out"),
            Entry("stderr", "pabot_results/1/robot_stderr.out"),
        )
        assert [e.path for e in listed.entries if e.label == "test-app"] == [
            "test-app/test-app-7002.log"
        ]


class FakeHistory:
    """Commits in the order they were made; a commit contains every one before it.

    All of them are on main, except those named in `off_main`.
    """

    main = "upstream/main"

    def __init__(self, *commits: str, off_main: tuple[str, ...] = ()):
        self.commits = list(commits)
        self.off_main = off_main

    def resolves(self, sha: str) -> bool:
        return sha in self.commits

    def on_main(self, sha: str) -> bool:
        return sha in self.commits and sha not in self.off_main

    def contains(self, commit: str, fix: str) -> bool | None:
        if commit not in self.commits:
            return None
        return self.commits.index(commit) >= self.commits.index(fix)


class TestVerifyingAFix:
    """A fix is Verified once seven days of runs containing it saw no recurrence.

    `seed` puts one Run on each commit, a day apart from 2026-08-20, in the
    order the commits first appear.
    """

    TEST = "S.Flaky"
    SIGNATURE = "Timeout <duration> exceeded"

    def _known(self, tmp_path, **entry):
        entry.setdefault("test", self.TEST)
        entry.setdefault("signature", self.SIGNATURE)
        entry.setdefault("cause", "a race")
        entry.setdefault("fixed_by", "f1c5000")
        path = tmp_path / "known.json"
        path.write_text(json.dumps([entry], indent=2), encoding="utf-8")
        return path

    def _fail(self, sha, signature=None, **row):
        return {
            "test": self.TEST,
            "status": "FAIL",
            "signature": signature or self.SIGNATURE,
            "sha": sha,
            **row,
        }

    def _pass(self, sha, **row):
        return {"test": self.TEST, "status": "PASS", "sha": sha, **row}

    def _check(self, tmp_path, rows, history, today, **entry):
        from datetime import date

        from tools.ci_failures.verify import check

        db = tmp_path / "db.sqlite3"
        seed(db, rows)
        return check(
            db,
            self._known(tmp_path, **entry),
            history=history,
            today=date.fromisoformat(today),
        )

    def test_a_fix_younger_than_seven_days_is_waiting(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000"), self._pass("sha3")],
            FakeHistory("sha1", "f1c5000", "sha3"),
            today="2026-08-24",
        )

        assert entry.status == "waiting"
        assert entry.line() == "waiting 3/7 days, 2 runs, 0 recurrences"

    def test_seven_days_without_a_recurrence_is_ready(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000"), self._pass("sha3")],
            FakeHistory("sha1", "f1c5000", "sha3"),
            today="2026-08-28",
        )

        assert entry.status == "ready"
        assert entry.line() == "ready: 7 days, 2 runs, 0 recurrences"

    def test_the_same_error_after_the_fix_is_a_recurrence(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000"), self._fail("sha3")],
            FakeHistory("sha1", "f1c5000", "sha3"),
            today="2026-09-10",
        )

        assert entry.status == "recurred"
        assert entry.line() == "recurred: 1 after fix"
        assert [run for run, _ in entry.recurred_in] == [3]

    def test_a_later_run_on_an_older_commit_does_not_contain_the_fix(self, tmp_path):
        """Dates are the wrong test: a run on a commit from before the fix can
        be created after it, and its failure says nothing about the fix."""
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000"), self._fail("stale")],
            FakeHistory("sha1", "stale", "f1c5000"),
            today="2026-08-24",
        )

        assert entry.status == "waiting"
        assert (entry.runs, entry.recurrences) == (1, 0)

    def test_a_fix_in_no_ingested_run_has_no_runs_yet(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("sha2")],
            FakeHistory("sha1", "sha2", "f1c5000"),
            today="2026-09-10",
        )

        assert entry.status == "no runs yet"

    def test_a_fixed_by_that_is_not_a_commit_is_no_sha(self, tmp_path):
        rows = [self._fail("sha1"), self._pass("f1c5000")]
        history = FakeHistory("sha1", "f1c5000")

        [prose] = self._check(
            tmp_path, rows, history, "2026-09-10", fixed_by="fix - rewrote the test"
        )
        [unknown] = self._check(
            tmp_path / "again", rows, history, "2026-09-10", fixed_by="abc1234"
        )

        assert prose.status == unknown.status == "no SHA"
        assert prose.line() == "no SHA: fixed_by is prose, not a commit SHA"
        assert unknown.line() == "no SHA: abc1234 is not a commit in this clone"

    def test_a_fixed_by_that_is_not_on_main_is_not_counted(self, tmp_path):
        """A rebase or squash gives the fix another SHA on main, and the branch
        one would read as `no runs yet` forever."""
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("sha2")],
            FakeHistory("sha1", "f1c5000", "sha2", off_main=("f1c5000",)),
            today="2026-09-10",
        )

        assert entry.status == "not on main"
        assert entry.line() == (
            "not on main: f1c5000 is not on upstream/main; record the SHA the fix "
            "has on main, or `git fetch upstream main`"
        )

    def test_an_issue_reference_names_the_issue_to_close(self, tmp_path):
        from tools.ci_failures.verify import Verification

        def entry(reference):
            return Verification("S.T", None, "ready", reference=reference)

        assert entry("https://github.com/o/r/issues/5223").issue == "5223"
        assert entry(None).issue is None

    def test_an_entry_matching_no_group_is_an_orphan_whatever_its_state(self, tmp_path):
        """A mistyped signature would otherwise read as zero recurrences."""
        rows = [self._fail("sha1"), self._pass("f1c5000")]
        history = FakeHistory("sha1", "f1c5000")

        [mistyped] = self._check(
            tmp_path, rows, history, "2026-09-10", signature="Timeout exceeded"
        )
        [verified] = self._check(
            tmp_path / "v",
            rows,
            history,
            "2026-09-10",
            signature="Timeout exceeded",
            fix_verified="2026-09-01",
        )
        [unfixed] = self._check(
            tmp_path / "u",
            rows,
            history,
            "2026-09-10",
            signature="Timeout exceeded",
            fixed_by=None,
        )

        assert mistyped.status == verified.status == unfixed.status == "orphan"
        assert mistyped.line() == "orphan: matches no Group in the database"

    def test_an_orphan_naming_no_test_says_so_and_what_was_meant(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000")],
            FakeHistory("sha1", "f1c5000"),
            "2026-09-10",
            test="Flaky",
        )

        assert entry.status == "orphan"
        assert entry.line() == "orphan: no test named 'Flaky' in the archive"
        assert entry.suggestions == ("S.Flaky",)

    def test_an_orphan_spelt_under_another_top_suite_is_told_the_spelling(
        self, tmp_path
    ):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000")],
            FakeHistory("sha1", "f1c5000"),
            "2026-09-10",
            test="Test.Flaky",
        )

        assert entry.line() == "orphan: no test named 'Test.Flaky' in the archive"
        assert entry.suggestions == ("S.Flaky",)

    def test_verified_and_unfixed_entries_are_not_checked(self, tmp_path):
        rows = [self._fail("sha1"), self._pass("f1c5000")]
        history = FakeHistory("sha1", "f1c5000")

        assert (
            self._check(
                tmp_path, rows, history, "2026-09-10", fix_verified="2026-09-01"
            )
            == []
        )
        assert (
            self._check(tmp_path / "u", rows, history, "2026-09-10", fixed_by=None)
            == []
        )

    def test_another_error_after_the_fix_is_a_note_not_a_recurrence(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [
                self._fail("sha1"),
                self._pass("f1c5000"),
                self._fail("sha3", signature="Browser crashed"),
            ],
            FakeHistory("sha1", "f1c5000", "sha3"),
            today="2026-08-28",
        )

        assert entry.status == "ready"
        assert [(o.signature, o.occurrences) for o in entry.other_failures] == [
            ("Browser crashed", 1)
        ]

    def test_a_suite_fixture_is_verified_over_the_runs_of_its_suite(self, tmp_path):
        teardown = {"scope": "suite_teardown", "owner": "S", "suite": "S"}
        [entry] = self._check(
            tmp_path,
            [
                self._fail("sha1", **teardown),
                self._pass("f1c5000", suite="S"),
                self._pass("sha3", suite="S.Child"),
            ],
            FakeHistory("sha1", "f1c5000", "sha3"),
            today="2026-08-24",
            test=None,
            suite="S",
        )

        assert entry.line() == "waiting 3/7 days, 2 runs, 0 recurrences"

    def test_a_suite_whose_name_only_looks_alike_is_not_enclosed(self, tmp_path):
        suite = "Test.My_Suite"
        teardown = {"scope": "suite_teardown", "owner": suite, "suite": suite}
        [entry] = self._check(
            tmp_path,
            [
                self._fail("sha1", **teardown),
                self._pass("f1c5000", suite=f"{suite}.Child"),
                self._pass("wildcard", suite="Test.MyXSuite.Child"),
                self._pass("case", suite="test.my_suite.Child"),
            ],
            FakeHistory("sha1", "f1c5000", "wildcard", "case"),
            today="2026-08-24",
            test=None,
            suite=suite,
        )

        assert entry.runs == 1

    def test_runs_on_commits_this_clone_lacks_are_counted_apart(self, tmp_path):
        [entry] = self._check(
            tmp_path,
            [self._fail("sha1"), self._pass("f1c5000"), self._pass("unfetched")],
            FakeHistory("sha1", "f1c5000"),
            today="2026-08-24",
        )

        assert (entry.runs, entry.unknown_commits) == (1, 1)
        assert entry.fetch == "`git fetch upstream main`"


class TestMarkingAFixVerified:
    def test_only_the_named_entries_are_marked_and_the_rest_is_kept(self, tmp_path):
        from tools.ci_failures.annotations import load_known_causes, mark_verified

        path = tmp_path / "known.json"
        path.write_text(
            json.dumps(
                [
                    {"test": "S.A", "signature": "Box <n>", "fixed_by": "abc"},
                    {"test": "S.B", "signature": "Box <n>", "fixed_by": "def"},
                    {"suite": "S", "signature": "Gone", "fix_verified": "2026-01-01"},
                ]
            ),
            encoding="utf-8",
        )

        marked = mark_verified({("S.A", "box <n>"), ("S", "gone")}, "2026-09-29", path)

        known = load_known_causes(path)
        assert marked == 1, "an entry already verified keeps its date"
        assert known[("S.A", "box <n>")]["fix_verified"] == "2026-09-29"
        assert known[("S.B", "box <n>")]["fix_verified"] is None
        assert known[("S", "gone")]["fix_verified"] == "2026-01-01"
        assert json.loads(path.read_text(encoding="utf-8"))[1]["fixed_by"] == "def"


class TestGitHistory:
    @pytest.fixture
    def repo(self, tmp_path):
        import subprocess

        def git(*args):
            return subprocess.run(
                ["git", "-C", str(tmp_path), *args],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        git("init", "-q")
        git("config", "user.email", "t@example.com")
        git("config", "user.name", "t")
        commits = []
        for n in range(3):
            git("commit", "-q", "--allow-empty", "-m", f"c{n}")
            commits.append(git("rev-parse", "HEAD"))
        # A fork's clone: origin is the fork, behind; upstream has the fix.
        git("remote", "add", "origin", "https://github.com/someone/fork.git")
        git("update-ref", "refs/remotes/origin/main", commits[0])
        git("remote", "add", "upstream", f"https://github.com/{github.REPO}.git")
        git("update-ref", "refs/remotes/upstream/main", commits[1])
        return tmp_path, commits, git

    def test_a_commit_contains_its_ancestors_and_not_its_descendants(self, repo):
        from tools.ci_failures.verify import Git

        root, (first, fix, last), _ = repo
        git = Git(root)

        assert git.resolves(fix[:8])
        assert not git.resolves("0" * 40)
        assert git.contains(last, fix) is True
        assert git.contains(first, fix) is False
        assert git.contains("0" * 40, fix) is None

    def test_on_main_is_asked_of_the_repository_ci_runs_on_not_a_fork(self, repo):
        """The fork's origin/main is behind the fix; upstream/main has it."""
        from tools.ci_failures.verify import Git

        root, (first, fix, last), _ = repo
        git = Git(root)

        assert git.main == "upstream/main"
        assert git.on_main(first) and git.on_main(fix[:8])
        assert not git.on_main(last)

    def test_a_clone_of_the_repository_itself_asks_origin(self, repo):
        from tools.ci_failures.verify import Git

        root, (_, fix, _), git = repo
        git("remote", "remove", "upstream")
        git("remote", "set-url", "origin", f"git@github.com:{github.REPO}.git")
        git("update-ref", "refs/remotes/origin/main", fix)

        assert Git(root).main == "origin/main"
        assert Git(root).on_main(fix)

    def test_a_clone_with_no_remote_at_the_repository_is_unanswerable(self, repo):
        from tools.ci_failures.verify import Git, NoMainError

        root, _, git = repo
        git("remote", "remove", "upstream")

        with pytest.raises(NoMainError, match="No remote of this clone") as refused:
            Git(root).main
        assert refused.value.code == 1
