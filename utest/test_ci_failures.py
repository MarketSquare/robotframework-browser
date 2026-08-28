"""Tests for tools/ci_failures. See 0012_flaky_test_analysis.md."""

import sqlite3
import zipfile
from pathlib import Path

import pytest
from robot import run as robot_run

from tools.ci_failures import github, ingest
from tools.ci_failures.db import connect as connect_db
from tools.ci_failures.parse import error_signature, parse
from tools.ci_failures.json_report import build as build_json
from tools.ci_failures.report import (
    co_failures,
    coverage_by_fixture,
    coverage_by_test,
    first_attempt_counts_by_test,
    latest_run,
    neighbouring_outcomes,
    pass_durations_by_test,
    failure_groups,
    fixture_signature_variants,
    configurations_by_fixture,
    fixture_failures,
    configurations_by_test,
    messages_by_test,
    occurrences_by_test,
    signature_variants,
    totals,
)

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


def _run_robot(directory: Path, suite: str, metadata: tuple[str, ...] = ()) -> Path:
    """A real output.xml from a real Robot Framework run.

    Written by Robot Framework rather than hand-rolled, so these tests keep
    working against the format Robot Framework actually emits.
    """
    (directory / "suite.robot").write_text(suite, encoding="utf-8")
    robot_run(
        str(directory / "suite.robot"),
        outputdir=str(directory),
        output="output.xml",
        log=None,
        report=None,
        metadata=list(metadata),
        stdout=open(directory / "stdout.txt", "w"),  # noqa: SIM115
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
    robot_run(
        str(outer),
        outputdir=str(root),
        output="output.xml",
        log=None,
        report=None,
        stdout=open(root / "stdout.txt", "w"),  # noqa: SIM115
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
        assert info.platform == "Linux-6.8-x86_64"
        assert info.python_version
        assert info.rf_version

    def test_the_generator_line_stands_in_when_metadata_is_absent(self, tmp_path):
        # Backfilled runs predate the metadata, and still have to say something.
        info, _ = parse(_run_robot(tmp_path, SUITE))

        assert info.node_version is None
        assert info.platform in {"linux", "darwin", "win32"}
        assert info.python_version

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
    """A one-run, two-leg CI so ingest and grouping work without the network."""
    run = github.Run(
        id=111,
        event="push",
        head_sha="abc123",
        head_branch="main",
        created_at="2026-08-20T10:00:00Z",
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
    monkeypatch.setattr(
        ingest.github, "list_test_artifacts", lambda run_id, repo=None: [artifact]
    )

    def fake_download(artifact_id, destination, repo=None):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(zip_path.read_bytes())
        return destination

    monkeypatch.setattr(ingest.github, "download_artifact", fake_download)
    return {"run": run, "artifact": artifact}


class TestIngest:
    def test_a_run_becomes_rows(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"

        result = ingest.ingest(db, limit=5, report=lambda _: None)

        assert result["runs"] == 1
        assert result["legs"] == 1
        assert result["tests"] == 4
        assert result["failures"] == 2

    def test_nothing_is_written_to_disk_except_the_database(self, fake_ci, tmp_path):
        db = tmp_path / "sub" / "ci.sqlite3"

        ingest.ingest(db, limit=5, report=lambda _: None)

        assert [p.name for p in db.parent.iterdir()] == ["ci.sqlite3"]

    def test_the_artifact_link_is_kept_so_evidence_can_be_fetched(
        self, fake_ci, tmp_path
    ):
        db = tmp_path / "ci.sqlite3"

        ingest.ingest(db, limit=5, report=lambda _: None)

        connection = sqlite3.connect(db)
        connection.row_factory = sqlite3.Row
        leg = connection.execute("SELECT * FROM leg").fetchone()
        assert leg["artifact_url"] == "https://example.invalid/runs/111/artifacts/222"
        assert leg["node_version"] == "v24.15.0"

    def test_running_again_ingests_nothing_twice(self, fake_ci, tmp_path):
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, report=lambda _: None)

        second = ingest.ingest(db, limit=5, report=lambda _: None)

        assert second["legs"] == 0
        assert second["skipped"] == 1
        assert (
            sqlite3.connect(db)
            .execute("SELECT COUNT(*) FROM test_result")
            .fetchone()[0]
            == 4
        )

    def test_an_expired_artifact_is_counted_rather_than_guessed_at(
        self, fake_ci, tmp_path, monkeypatch
    ):
        gone = github.Artifact(**{**fake_ci["artifact"].__dict__, "expired": True})
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id, repo=None: [gone]
        )

        result = ingest.ingest(tmp_path / "ci.sqlite3", limit=5, report=lambda _: None)

        assert result["expired"] == 1
        assert result["legs"] == 0


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
        from tools.ci_failures.report import log_messages

        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, report=lambda _: None)

        group = failure_groups(db)[0]
        entries = log_messages(db, group.latest_result_id)
        assert [e["message"] for e in entries] == [
            "Timeout 5000ms exceeded waiting for #id-4f2a"
        ]

    def test_no_messages_is_not_an_error(self, tmp_path):
        from tools.ci_failures.db import connect
        from tools.ci_failures.report import log_messages

        db = tmp_path / "ci.sqlite3"
        connect(db).close()

        assert log_messages(db, None) == []


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
            "suite teardown of Suite"
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
        assert results[0].scope_owner == "Suite"

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
        from tools.ci_failures.db import connect

        connection = connect(db)
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

        fixtures = fixture_failures(db)

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

        assert sorted(fixture_failures(db)[0].affected_tests.split(",")) == [
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

        assert [g.longname for g in failure_groups(db)] == ["Outer.Middle.Test C"]

    def test_the_denominator_is_how_often_the_suite_ran(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "Outer.Middle", "FAIL", "suite_teardown", "Outer")])

        fixture = fixture_failures(db)[0]
        assert fixture.suite_runs == 2
        assert fixture.failure_rate == pytest.approx(1.0)


class TestVersionsOnAFailure:
    """Which versions a failure was seen on, so "is it version dependent?" is a
    question the report answers rather than one it raises."""

    def _seed(self, db: Path, legs: list[tuple]) -> None:
        from tools.ci_failures.db import connect

        connection = connect(db)
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

    def test_every_version_the_failure_was_seen_on_is_listed(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("7.4.2", "3.10.11", "v22.1.0", "win32"),
                ("7.1.1", "3.14.7", "v24.15.0", "win32"),
            ],
        )

        group = failure_groups(db)[0]

        assert sorted(group.rf_versions.split(",")) == ["7.1.1", "7.4.2"]
        assert sorted(group.python_versions.split(",")) == ["3.10.11", "3.14.7"]
        assert sorted(group.node_versions.split(",")) == ["v22.1.0", "v24.15.0"]

    def test_one_version_throughout_is_listed_once(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                ("7.4.2", "3.14.7", "v24.15.0", "win32"),
                ("7.4.2", "3.14.7", "v24.15.0", "win32"),
            ],
        )

        assert failure_groups(db)[0].rf_versions == "7.4.2"

    def test_a_backfilled_run_without_a_node_version_is_not_an_error(self, tmp_path):
        """Runs from before the metadata was added carry no NodeJS version."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("7.4.2", "3.14.7", None, "win32")])

        assert failure_groups(db)[0].node_versions is None

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

        configurations = configurations_by_test(db)[("S.Test A", "boom")]

        assert [(c["rf_version"], c["python_version"]) for c in configurations] == [
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

        configurations = configurations_by_test(db)[("S.Test A", "boom")]

        assert len(configurations) == 2
        assert configurations[0]["occurrences"] == 2, "most seen first"
        assert configurations[1]["occurrences"] == 1

    def test_a_fixture_failure_counts_legs_not_the_rows_it_marked(self, tmp_path):
        """One broken teardown marking four tests is one occurrence, not four."""
        from tools.ci_failures.db import connect

        db = tmp_path / "ci.sqlite3"
        connection = connect(db)
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

        configurations = configurations_by_fixture(db)[
            ("S", "suite_teardown", "teardown broke")
        ]

        assert len(configurations) == 1
        assert configurations[0]["occurrences"] == 1


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

    def test_the_failure_screenshot_is_listed_first(self, tmp_path):
        suite = """\
*** Test Cases ***
Several Screenshots
    Log    <a href="browser/screenshot/other.png">a</a>    html=True
    Log    <a href="browser/screenshot/fail-screenshot-1.png">b</a>    html=True
    Fail    it broke
"""
        _, results = parse(_run_robot(tmp_path, suite))

        assert results[0].screenshots.split(",")[0].endswith("fail-screenshot-1.png")

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
            ingest.github, "list_test_artifacts", lambda run_id, repo=None: [bad, good]
        )
        original = ingest.github.download_artifact

        def flaky(artifact_id, destination, repo=None):
            if artifact_id == 999:
                raise github.GhError("connection reset by peer")
            return original(artifact_id, destination, repo=repo)

        monkeypatch.setattr(ingest.github, "download_artifact", flaky)

        result = ingest.ingest(tmp_path / "ci.sqlite3", limit=5, report=lambda _: None)

        assert result["unreachable"] == 1
        assert result["legs"] == 1, "the good artifact still went in"
        assert result["tests"] == 4

    def test_the_skipped_leg_is_picked_up_next_time(
        self, fake_ci, tmp_path, monkeypatch
    ):
        """Ingest is incremental, so a transient failure costs a run, not a leg."""
        good = fake_ci["artifact"]
        bad = github.Artifact(
            **{**good.__dict__, "id": 999, "name": "Test results-bad"}
        )
        monkeypatch.setattr(
            ingest.github, "list_test_artifacts", lambda run_id, repo=None: [bad, good]
        )
        original = ingest.github.download_artifact
        broken = {"still": True}

        def flaky(artifact_id, destination, repo=None):
            if artifact_id == 999 and broken["still"]:
                raise github.GhError("connection reset by peer")
            return original(artifact_id, destination, repo=repo)

        monkeypatch.setattr(ingest.github, "download_artifact", flaky)
        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, report=lambda _: None)

        broken["still"] = False
        second = ingest.ingest(db, limit=5, report=lambda _: None)

        assert second["legs"] == 1
        assert second["unreachable"] == 0

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

        assert attempts["n"] == github.DOWNLOAD_ATTEMPTS

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
        from tools.ci_failures.db import connect

        connection = connect(db)
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

        groups = failure_groups(db)

        assert [(g.error_signature, g.failures) for g in groups] == [
            ("error Y", 4),
            ("error X", 2),
        ]

    def test_the_denominator_counts_every_run_including_the_passes(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db, [("Test A", "FAIL", "error X")] * 2 + [("Test A", "PASS", None)] * 8
        )

        group = failure_groups(db)[0]

        assert group.failures == 2
        assert group.total_runs == 10
        assert group.failure_rate == pytest.approx(0.2)

    def test_a_test_that_never_failed_is_absent(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "PASS", None)] * 5)

        assert failure_groups(db) == []

    def test_the_evidence_link_points_at_the_artifact(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "FAIL", "error X")])

        assert failure_groups(db)[0].latest_artifact_url == "a-url"

    def test_totals_count_passes_and_failures_apart(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [("Test A", "FAIL", "error X")] + [("Test B", "PASS", None)] * 3)

        summary = totals(db)

        assert summary["results"] == 4
        assert summary["failures"] == 1
        assert summary["tests"] == 2


class TestCaseFoldedGrouping:
    """`Deadline Exceeded` and `Deadline exceeded` are one problem.

    grpcio's C core spells it with a capital when the Python client's deadline
    timer fires; @grpc/grpc-js spells it small when the Node server's timer wins
    the same race. Two libraries naming one condition, not two conditions.
    """

    def _seed(self, db: Path, rows: list[dict]) -> None:
        """One row per test result, carrying the leg and run it belongs to.

        Rows sharing a (commit, platform, python) land on the same leg, which is
        what makes a per-configuration denominator mean anything. An `attempt`
        puts a row on a second leg of the same name in the same run, which is
        what a hand re-run of a failed job looks like once it is ingested.
        """
        from tools.ci_failures.db import connect

        connection = connect(db)
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
            key = (sha, platform, python, attempt)
            if key not in legs:
                legs[key] = len(legs) + 1
                connection.execute(
                    "INSERT INTO leg (id, run_id, artifact_id, artifact_name, "
                    "artifact_url, platform, python_version, rf_version, "
                    "ingested_at, attempt) "
                    "VALUES (?, ?, ?, ?, 'a-url', ?, ?, '7.4.2', 'now', ?)",
                    (
                        legs[key],
                        runs[sha],
                        legs[key],
                        f"leg-{platform}-{python}",
                        platform,
                        python,
                        attempt,
                    ),
                )
            connection.execute(
                "INSERT INTO test_result (leg_id, longname, name, suite_longname, "
                "status, elapsed_ms, message, error_signature, failure_scope, "
                "scope_owner) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                ),
            )
        connection.commit()
        connection.close()

    def _deadlines(self) -> list[dict]:
        return [
            {"test": "T", "status": "FAIL", "signature": "Deadline Exceeded"},
            {"test": "T", "status": "FAIL", "signature": "Deadline Exceeded"},
            {"test": "T", "status": "FAIL", "signature": "Deadline exceeded"},
        ]

    def test_two_spellings_of_one_error_are_one_group(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._deadlines())

        groups = failure_groups(db)

        assert len(groups) == 1
        assert groups[0].failures == 3

    def test_the_merged_group_is_keyed_case_insensitively(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._deadlines())

        assert failure_groups(db)[0].signature_key == "deadline exceeded"

    def test_the_spellings_survive_the_merge(self, tmp_path):
        """Which side of the boundary gave up first is evidence, not noise."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._deadlines())

        variants = signature_variants(db)[("T", "deadline exceeded")]

        assert variants == [
            {"signature": "Deadline Exceeded", "occurrences": 2},
            {"signature": "Deadline exceeded", "occurrences": 1},
        ]

    def test_a_group_with_one_spelling_reports_no_variants(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert signature_variants(db) == {}

    def test_suite_fixtures_are_merged_the_same_way(self, tmp_path):
        """Where it actually happens: the real case is a suite teardown."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                dict(row, scope="suite_teardown", owner="Suite X", sha=f"sha{i}")
                for i, row in enumerate(self._deadlines())
            ],
        )

        fixtures = fixture_failures(db)

        assert len(fixtures) == 1
        assert fixtures[0].occurrences == 3
        assert (
            len(
                fixture_signature_variants(db)[
                    ("Suite X", "suite_teardown", "deadline exceeded")
                ]
            )
            == 2
        )


class TestPayloadForALanguageModel:
    """What the JSON document carries that the terminal report drops.

    `print_report` emits 8 of `FailureGroup`'s fields and calls 3 of the 7
    queries. These are the facts that were missing, not reformatted.
    """

    _seed = TestCaseFoldedGrouping._seed

    def _entry(self, db: Path, test: str = "T") -> dict:
        return next(t for t in build_json(db)["test_failures"] if t["test"] == test)

    def test_a_configuration_that_never_failed_keeps_its_denominator(self, tmp_path):
        """0 of 4 on darwin is evidence. A global rate cannot say it."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom"}] * 3
            + [{"test": "T", "status": "PASS"}] * 5
            + [{"test": "T", "status": "PASS", "platform": "darwin"}] * 4,
        )

        coverage = coverage_by_test(db)["T"]

        assert {c["platform"]: (c["ran"], c["failed"]) for c in coverage} == {
            "linux": (8, 3),
            "darwin": (4, 0),
        }

    def test_a_platform_the_test_never_ran_on_is_named(self, tmp_path):
        """Absent and clean are opposite findings. A zero cannot tell them apart."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "boom"}]
            + [{"test": "Other", "status": "PASS", "platform": "win32"}],
        )

        assert self._entry(db)["never_ran_on"] == ["win32"]

    def test_every_distinct_raw_message_is_kept(self, tmp_path):
        """The signature masks what varies, which is exactly the evidence."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert self._entry(db)["occurrences"][0]["artifact_url"] == "a-url"

    def test_a_broken_suite_fixture_is_not_a_test_failure(self, tmp_path):
        """Section 3, stated in the document rather than left to be inferred."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert "suite_fixtures_are_separate" in build_json(db)["about"]

    def test_nothing_is_truncated(self, tmp_path):
        """The terminal report cuts at 110 characters for a narrow terminal."""
        db = tmp_path / "ci.sqlite3"
        long_message = "x" * 400
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        from tools.ci_failures.db import connect

        connection = connect(db)
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

    _seed = TestCaseFoldedGrouping._seed

    def _occurrence(self, db: Path, test: str = "T") -> dict:
        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == test)
        return entry["occurrences"][0]

    def test_the_runs_either_side_of_a_failure_are_reported(self, tmp_path):
        """One failure between two passes is a blip. The same failure with a
        passing run before it and failures after is where something broke."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        around = self._occurrence(db)

        assert around["previous_run_on_this_leg"] is None
        assert around["next_run_on_this_leg"] is None

    def test_a_hand_rerun_that_passed_is_reported(self, tmp_path):
        """The one comparison that holds the commit constant. A regression the
        next commit fixed also has passing neighbours; only this separates them."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])

        assert self._occurrence(db)["retry"] is None

    def test_what_else_broke_in_the_same_leg_is_named(self, tmp_path):
        """Take Screenshot fails, the VAR after it never runs, and two later
        suites fail on a variable nobody set. Three entries, one event."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                {"test": "First", "status": "FAIL", "signature": "screenshot"},
                {"test": "Second", "status": "FAIL", "signature": "no variable"},
            ],
        )

        assert self._occurrence(db, "Second")["also_failed_in_this_leg"] == [
            {"test": "First", "scope": "test"}
        ]

    def test_a_leg_that_broke_wholesale_says_what_it_left_out(self, tmp_path):
        """A list that stops without saying so reads as a complete one."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "timeout", "elapsed": 2056}]
            + [
                {"test": "T", "status": "PASS", "elapsed": ms, "sha": f"s{ms}"}
                for ms in (1001, 1400, 1853)
            ],
        )

        durations = pass_durations_by_test(db)

        assert durations[("T", "linux", "3.13.15", "7.4.2", None)] == {
            "min": 1001,
            "median": 1400,
            "p95": 1853,
            "max": 1853,
        }

    def test_the_passing_durations_reach_the_document(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [{"test": "T", "status": "FAIL", "signature": "timeout", "elapsed": 9}]
            + [{"test": "T", "status": "PASS", "elapsed": 5, "sha": "two"}],
        )

        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == "T")

        assert entry["rates"][0]["pass_ms"]["max"] == 5

    def test_a_configuration_with_no_passes_carries_no_durations(self, tmp_path):
        """A test that has only ever failed on a leg has no margin to report."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db, [{"test": "T", "status": "FAIL", "signature": "boom", "elapsed": 9}]
        )

        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == "T")

        assert entry["rates"][0]["pass_ms"] is None

    def test_the_newest_run_is_reported_with_its_failure_count(self, tmp_path):
        """The rates say how often things break, not whether the head is green."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "sha": "old"},
                {"test": "T", "status": "PASS", "sha": "new"},
            ],
        )

        assert latest_run(db)["commit"] == "new"
        assert latest_run(db)["failures"] == 0
        assert build_json(db)["window"]["latest_run"]["failures"] == 0

    def test_only_tests_that_failed_are_measured(self, tmp_path):
        """The report is asked about failures. Timing every passing test in the
        window would price the query at the size of the database."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            [
                {"test": "T", "status": "FAIL", "signature": "boom", "elapsed": 9},
                {"test": "T", "status": "PASS", "elapsed": 5, "sha": "two"},
                {"test": "Healthy", "status": "PASS", "elapsed": 5},
                {"test": "Healthy", "status": "PASS", "elapsed": 6, "sha": "two"},
            ],
        )

        assert {key[0] for key in pass_durations_by_test(db)} == {"T"}
        assert len(neighbouring_outcomes(db)) == 1


class TestFixtureEntriesAskTheSameQuestions:
    """A suite fixture entry carried none of what section 6 added for tests.

    It is the most frequent failure in the window and it was the one entry with
    no denominators, no raw messages, and nothing to hang the evidence on: the
    configurations it had been seen on, counted, with nothing to count against.
    """

    _seed = TestCaseFoldedGrouping._seed

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
        self._seed(db, self._broke(marking=4))

        fixture = self._fixture(db)

        assert fixture["counts"]["test_rows_marked_failed"] == 4
        assert len(fixture["occurrences"]) == 1
        assert fixture["occurrences"][0]["tests_marked"] == 4

    def test_the_denominator_counts_legs_that_ran_the_suite(self, tmp_path):
        """`seen_on` said which legs it had been seen failing on and how often,
        with nothing to divide by. 5 occurrences is not a rate."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._broke() + self._ran_clean(sha="two"))

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
        self._seed(
            db,
            self._broke(platform="win32")
            + self._ran_clean(sha="two", platform="win32")
            + self._ran_clean(platform="linux")
            + self._ran_clean(sha="two", platform="linux"),
        )

        assert {
            (c["platform"], c["ran"], c["failed"])
            for c in coverage_by_fixture(db)[("Suite X", "suite_teardown")]
        } == {("win32", 2, 1), ("linux", 2, 0)}

    def test_a_fixture_rate_carries_no_pass_duration(self, tmp_path):
        """A suite fixture has no duration of its own in the database. A field
        that is null on every row reads as a measurement that failed."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._broke())

        assert "pass_ms" not in self._fixture(db)["rates"][0]

    def test_the_runs_either_side_of_a_broken_fixture_are_reported(self, tmp_path):
        """A fixture has no status row of its own: the leg passed if the suite
        ran there and the fixture is not among the failures."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(db, self._broke(attempt=1) + self._ran_clean(attempt=2))

        assert self._fixture(db)["occurrences"][0]["retry"] == {
            "attempts": 2,
            "passed_on_another_attempt": True,
        }

    def test_the_tests_the_fixture_marked_are_not_listed_as_context(self, tmp_path):
        """They are its own damage, already counted once. Restating them as
        context makes one event look like a leg falling apart."""
        db = tmp_path / "ci.sqlite3"
        self._seed(
            db,
            self._broke()
            + [{"test": "Unrelated", "status": "FAIL", "signature": "other"}],
        )

        assert self._fixture(db)["occurrences"][0]["also_failed_in_this_leg"] == [
            {"test": "Unrelated", "scope": "test"}
        ]

    def test_a_raw_message_is_counted_in_legs_not_in_marked_rows(self, tmp_path):
        """Robot Framework writes the fixture's message onto every test it
        marked, so counting rows reports one teardown failure as four."""
        db = tmp_path / "ci.sqlite3"
        self._seed(db, self._broke(marking=4, message="Deadline Exceeded"))

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
            "artifact_id INTEGER, artifact_name TEXT, ingested_at TEXT);"
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
        monkeypatch.setattr(github, "get_run", lambda run_id, repo=None: run)
        monkeypatch.setattr(
            github,
            "attempt_starts",
            lambda run, repo=None: [
                (1, "2026-08-19T17:14:38Z"),
                (2, "2026-08-19T17:43:17Z"),
            ],
        )
        monkeypatch.setattr(
            github,
            "list_test_artifacts",
            lambda run_id, repo=None: [
                github.Artifact(11, "leg", False, "u", "2026-08-19T17:22:21Z"),
                github.Artifact(22, "leg", False, "u", "2026-08-19T17:50:56Z"),
            ],
        )

        filled = ingest.backfill_attempts(db, report=lambda _: None)

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
            ingest.github, "list_test_artifacts", lambda run_id, repo=None: artifacts
        )
        monkeypatch.setattr(
            ingest.github,
            "attempt_starts",
            lambda run, repo=None: [
                (1, "2026-08-19T17:14:38Z"),
                (2, "2026-08-19T17:43:17Z"),
            ],
        )

        def fake_download(artifact_id, destination, repo=None):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zip_path.read_bytes())
            return destination

        monkeypatch.setattr(ingest.github, "download_artifact", fake_download)

        db = tmp_path / "ci.sqlite3"
        ingest.ingest(db, limit=5, report=lambda _: None)

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

        def gone(run_id, repo=None):
            raise github.GhError("run not found")

        monkeypatch.setattr(github, "get_run", gone)

        ingest.backfill_attempts(db, report=lambda _: None)

        connection = connect_db(db)
        assert connection.execute("SELECT attempt FROM leg").fetchone()[0] is None
        assert totals(db)["legs_without_attempt"] == 1
        connection.close()


class TestTheDenominatorAndTheRerun:
    """A leg is only ever re-run because it failed, so re-attempts land exactly
    where the failures are and pull every rate down with them."""

    _seed = TestCaseFoldedGrouping._seed

    def _counts(self, db: Path, test: str = "T") -> dict:
        entry = next(t for t in build_json(db)["test_failures"] if t["test"] == test)
        return entry["counts"]

    def test_a_rerun_inflates_the_ordinary_denominator(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(
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
        self._seed(
            db,
            [
                {"test": "T", "status": "PASS", "attempt": 1},
                {"test": "T", "status": "FAIL", "signature": "boom", "attempt": 2},
            ],
        )

        runs, failures = first_attempt_counts_by_test(db)

        assert runs["T"] == 1
        assert ("T", "boom") not in failures

    def test_the_attempt_is_on_every_occurrence(self, tmp_path):
        db = tmp_path / "ci.sqlite3"
        self._seed(
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
        self._seed(db, [{"test": "T", "status": "FAIL", "signature": "boom"}])
        connection = connect_db(db)
        connection.execute("UPDATE leg SET attempt = NULL")
        connection.commit()
        connection.close()

        assert build_json(db)["window"]["legs_with_unknown_attempt"] == 1


class TestHtmlReport:
    def test_it_renders_a_self_contained_page(self, tmp_path):
        from tools.ci_failures.db import connect
        from tools.ci_failures.html_report import render

        db = tmp_path / "ci.sqlite3"
        connect(db).close()

        page = render(db, tmp_path / "report.html")

        text = page.read_text(encoding="utf-8")
        assert "<title>Browser CI Failures</title>" in text
        # Google Fonts is the only external host the artifact CSP admits.
        assert "fonts.googleapis.com" in text
        assert "<script" not in text
