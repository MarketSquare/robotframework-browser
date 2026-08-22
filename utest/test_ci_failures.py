"""Tests for tools/ci_failures. See 0012_flaky_test_analysis.md."""

import sqlite3
import zipfile
from pathlib import Path

import pytest
from robot import run as robot_run

from tools.ci_failures import github, ingest
from tools.ci_failures.parse import error_signature, parse
from tools.ci_failures.report import failure_groups, totals

SUITE = """\
*** Test Cases ***
Passing Test
    Log    fine

Failing Test
    Outer Keyword

Skipped Test
    Skip    not today

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
        assert result["tests"] == 3
        assert result["failures"] == 1

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
            == 3
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
