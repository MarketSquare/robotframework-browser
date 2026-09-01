"""Pulls output.xml out of each CI artifact and into the database.

Incremental: an artifact already in the database is never downloaded again, so
this can be run as often as wanted and only does what is new. Nothing is kept on
disk except the database - the artifact is downloaded, output.xml is read out of
it, and the zip is thrown away. The artifact's URL is stored so that whatever
else is in it can be fetched later, if a particular failure turns out to deserve
it.
"""

import sqlite3
import tempfile
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import github
from .db import connect, ingested_artifact_ids
from .parse import LegInfo, TestResult, error_signature, parse

OUTPUT_XML = "output.xml"


def _extract_output_xml(zip_path: Path, into: Path) -> Path | None:
    with zipfile.ZipFile(zip_path) as archive:
        if OUTPUT_XML not in archive.namelist():
            return None
        archive.extract(OUTPUT_XML, into)
    return into / OUTPUT_XML


def _mark_unusable(
    connection: sqlite3.Connection,
    run: github.Run,
    artifact: github.Artifact,
    reason: str,
) -> None:
    connection.execute(
        "INSERT OR REPLACE INTO unusable_artifact "
        "(artifact_id, run_id, name, reason, noticed_at) VALUES (?, ?, ?, ?, ?)",
        (
            artifact.id,
            run.id,
            artifact.name,
            reason,
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        ),
    )


def _insert_run(connection: sqlite3.Connection, run: github.Run) -> None:
    connection.execute(
        "INSERT OR REPLACE INTO run (id, event, head_sha, head_branch, created_at, "
        "conclusion, url) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            run.id,
            run.event,
            run.head_sha,
            run.head_branch,
            run.created_at,
            run.conclusion,
            run.url,
        ),
    )


def _insert_leg(
    connection: sqlite3.Connection,
    run: github.Run,
    artifact: github.Artifact,
    info: LegInfo,
) -> int:
    cursor = connection.execute(
        "INSERT INTO leg (run_id, artifact_id, artifact_name, artifact_url, "
        "python_version, rf_version, platform, node_version, generated_at, "
        "ingested_at, attempt, executors, node_process) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            run.id,
            artifact.id,
            artifact.name,
            artifact.url,
            info.python_version,
            info.rf_version,
            info.platform,
            info.node_version,
            info.generated_at,
            datetime.now(timezone.utc).isoformat(),
            artifact.attempt,
            info.executors,
            info.node_process,
        ),
    )
    return int(cursor.lastrowid)


def _insert_results(
    connection: sqlite3.Connection, leg_id: int, results: list[TestResult]
) -> tuple[int, int]:
    failures = 0
    for result in results:
        cursor = connection.execute(
            "INSERT INTO test_result (leg_id, longname, name, suite_longname, status, "
            "elapsed_ms, message, error_signature, failing_keyword, failure_scope, "
            "scope_owner, test_source, test_lineno, keyword_owner, keyword_kind, "
            "keyword_source, keyword_lineno, screenshots, screenshot_status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                leg_id,
                result.longname,
                result.name,
                result.suite_longname,
                result.status,
                result.elapsed_ms,
                result.message,
                result.error_signature,
                result.failing_keyword,
                result.failure_scope,
                result.scope_owner,
                result.test_source,
                result.test_lineno,
                result.keyword_owner,
                result.keyword_kind,
                result.keyword_source,
                result.keyword_lineno,
                result.screenshots,
                result.screenshot_status,
            ),
        )
        if result.status == "FAIL":
            failures += 1
        if result.log_messages:
            connection.executemany(
                "INSERT INTO log_message "
                "(test_result_id, seq, level, keyword, origin, message) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (cursor.lastrowid, m.seq, m.level, m.keyword, m.origin, m.message)
                    for m in result.log_messages
                ],
            )
    return len(results), failures


@dataclass(frozen=True)
class Ingested:
    """What one ingest did.

    A record rather than a dict: it is read half an hour after the work started,
    by a caller that has no way to be told it asked for a key that is not there.
    """

    runs: int = 0
    legs: int = 0
    tests: int = 0
    failures: int = 0
    expired: int = 0
    skipped: int = 0
    unreachable: int = 0
    #: Artifacts that came down and held no output.xml. Recorded so they are not
    #: fetched again; see `unusable_artifact` in `schema.sql`.
    unusable: int = 0
    #: Runs whose artifact listing could not be read. Nothing was lost - they
    #: are picked up next time - but the count says the window is incomplete.
    unlisted: int = 0

    def line(self) -> str:
        return (
            f"Ingested {self.runs} run(s), {self.legs} leg(s), {self.tests} results, "
            f"{self.failures} failures. {self.skipped} run(s) already complete, "
            f"{self.expired} artifact(s) expired, {self.unusable} without output.xml, "
            f"{self.unreachable} could not be downloaded, "
            f"{self.unlisted} run(s) could not be listed."
        )


def _ingest_legs(
    connection: sqlite3.Connection,
    run: github.Run,
    pending: list[github.Artifact],
    *,
    already: set[int],
    totals: dict[str, int],
    report: Callable[[str], None],
) -> None:
    """Every Leg of one Run, each contained so one bad artifact costs one Leg."""
    for number, artifact in enumerate(pending, start=1):
        # Said before the download rather than after it. A leg is about ten
        # megabytes and the line used to appear only once it was parsed and
        # inserted, so a long ingest showed nothing at all in between.
        report(f"    [{number}/{len(pending)}] {artifact.name}")
        try:
            with tempfile.TemporaryDirectory() as work_dir:
                work = Path(work_dir)
                zip_path = github.download_artifact(artifact.id, work / "artifact.zip")
                output_xml = _extract_output_xml(zip_path, work / "unpacked")
                if output_xml is None:
                    # A fact about the artifact, not about the network, so
                    # it is remembered. It used to be re-downloaded on every
                    # future ingest and counted in nothing.
                    _mark_unusable(connection, run, artifact, "no output.xml")
                    connection.commit()
                    already.add(artifact.id)
                    totals["unusable"] += 1
                    report("        no output.xml - will not be fetched again")
                    continue
                info, results = parse(output_xml)
                leg_id = _insert_leg(connection, run, artifact, info)
                tests, failures = _insert_results(connection, leg_id, results)
        except Exception as error:
            # One artifact that will not come down, or comes down truncated,
            # or will not parse, must not cost the other hundred and fifty.
            # Catching only GhError left a corrupt zip and a malformed
            # output.xml ending the run. Ingest is incremental, so the next
            # run picks this leg up and nothing committed is lost.
            totals["unreachable"] += 1
            report(f"        {type(error).__name__}: {error}")
            connection.rollback()
            continue
        totals["legs"] += 1
        totals["tests"] += tests
        totals["failures"] += failures
        already.add(artifact.id)
        connection.commit()
        report(f"        {tests} tests, {failures} failed")


def ingest(
    db_path: Path,
    *,
    limit: int = 25,
    report: Callable[[str], None] = print,
    dry_run: bool = False,
) -> Ingested:
    """Ingests up to ``limit`` runs, newest first, skipping what is already in.

    `dry_run` says what would be fetched and fetches nothing. The listing it
    needs is the listing the real thing starts with, so the answer costs a few
    requests rather than the half hour of downloads it is asked about.
    """
    connection = connect(db_path)
    already = ingested_artifact_ids(connection)
    totals = dict.fromkeys(
        (
            "runs",
            "legs",
            "tests",
            "failures",
            "expired",
            "skipped",
            "unreachable",
            "unusable",
            "unlisted",
        ),
        0,
    )

    runs = github.list_runs(limit=limit)
    report(
        f"{len(runs)} run(s) to consider on {github.BRANCH} "
        f"({', '.join(github.EVENTS)})"
    )

    for run in runs:
        try:
            artifacts = github.with_attempts(
                [a for a in github.list_test_artifacts(run.id) if a.id not in already],
                github.attempt_starts(run),
            )
        except github.GhError as error:
            # These used to sit outside the per-leg guard, so one bad response
            # twenty minutes in ended the whole ingest with a traceback and no
            # summary. Nothing is lost by skipping the run: it is picked up next
            # time, and the count says the window is short.
            totals["unlisted"] += 1
            report(f"  run {run.id}: cannot list artifacts: {error}")
            continue
        expired = [a for a in artifacts if a.expired]
        pending = [a for a in artifacts if not a.expired]
        totals["expired"] += len(expired)
        if expired:
            report(f"  run {run.id}: {len(expired)} artifact(s) expired, unrecoverable")
        if not pending:
            totals["skipped"] += 1
            continue
        if dry_run:
            totals["runs"] += 1
            totals["legs"] += len(pending)
            report(
                f"  run {run.id} ({run.event}, {run.created_at}): "
                f"would fetch {len(pending)} leg(s)"
            )
            continue

        _insert_run(connection, run)
        # Committed before its legs: a leg that fails rolls back, and that
        # rollback must not take the run row with it and leave the next leg of
        # the same run with nothing to point at.
        connection.commit()
        totals["runs"] += 1
        report(f"  run {run.id} ({run.event}, {run.created_at}): {len(pending)} leg(s)")

        _ingest_legs(
            connection,
            run,
            pending,
            already=already,
            totals=totals,
            report=report,
        )

    connection.commit()
    connection.close()
    return Ingested(**totals)


def backfill_attempts(
    db_path: Path,
    *,
    report: Callable[[str], None] = print,
) -> int:
    """Fills in the attempt of legs ingested before it was being recorded.

    Downloads nothing. A run says how many attempts it had and the artifact
    listing says when each artifact was created, which is all the resolution
    needs, so this is one request per run plus one per extra attempt - seconds
    against the hours a re-ingest of the same window would take.

    Runs on every ingest. Once there is nothing left to fill it is a single
    query that returns no rows, and a leg the API can no longer account for
    stays NULL rather than being called attempt 1.
    """
    connection = connect(db_path)
    run_ids = [
        row["run_id"]
        for row in connection.execute(
            "SELECT DISTINCT run_id FROM leg WHERE attempt IS NULL ORDER BY run_id"
        )
    ]
    if not run_ids:
        connection.close()
        report("every leg already carries the attempt that produced it")
        return 0
    report(f"resolving the attempt of legs in {len(run_ids)} run(s)")
    filled = 0
    for run_id in run_ids:
        try:
            run = github.get_run(run_id)
            artifacts = github.with_attempts(
                github.list_test_artifacts(run_id),
                github.attempt_starts(run),
            )
        except github.GhError as error:
            report(f"  run {run_id}: {error}")
            continue
        cursor = connection.executemany(
            "UPDATE leg SET attempt = ? WHERE artifact_id = ? AND attempt IS NULL",
            [(a.attempt, a.id) for a in artifacts],
        )
        filled += cursor.rowcount if cursor.rowcount > 0 else 0
        connection.commit()
    unresolved = connection.execute(
        "SELECT COUNT(*) FROM leg WHERE attempt IS NULL"
    ).fetchone()[0]
    connection.close()
    report(f"  filled {filled} leg(s), {unresolved} still unresolved")
    return filled


def recompute_signatures(db_path: Path, report: Callable[[str], None] = print) -> int:
    """Recomputes every error signature from the messages already stored.

    The masking rules change as more failures are seen, and the message itself is
    in the database, so re-grouping never needs the artifacts again.
    """
    connection = connect(db_path)
    rows = connection.execute(
        "SELECT id, message FROM test_result WHERE status = 'FAIL' AND message IS NOT NULL"
    ).fetchall()
    connection.executemany(
        "UPDATE test_result SET error_signature = ? WHERE id = ?",
        [(error_signature(row["message"]), row["id"]) for row in rows],
    )
    connection.commit()
    connection.close()
    report(f"recomputed {len(rows)} signature(s)")
    return len(rows)
