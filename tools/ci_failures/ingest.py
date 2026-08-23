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
        "python_version, rf_version, platform, node_version, generated_at, ingested_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
            "scope_owner) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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


def ingest(
    db_path: Path,
    *,
    limit: int = 25,
    repo: str = github.DEFAULT_REPO,
    branch: str = "main",
    events: tuple[str, ...] = ("push", "schedule"),
    report: Callable[[str], None] = print,
) -> dict:
    """Ingests up to ``limit`` runs, newest first, skipping what is already in."""
    connection = connect(db_path)
    already = ingested_artifact_ids(connection)
    totals = {
        "runs": 0,
        "legs": 0,
        "tests": 0,
        "failures": 0,
        "expired": 0,
        "skipped": 0,
    }

    runs = github.list_runs(repo=repo, branch=branch, events=events, limit=limit)
    report(f"{len(runs)} run(s) to consider on {branch} ({', '.join(events)})")

    for run in runs:
        artifacts = [
            a
            for a in github.list_test_artifacts(run.id, repo=repo)
            if a.id not in already
        ]
        expired = [a for a in artifacts if a.expired]
        pending = [a for a in artifacts if not a.expired]
        totals["expired"] += len(expired)
        if expired:
            report(f"  run {run.id}: {len(expired)} artifact(s) expired, unrecoverable")
        if not pending:
            totals["skipped"] += 1
            continue

        _insert_run(connection, run)
        totals["runs"] += 1
        report(f"  run {run.id} ({run.event}, {run.created_at}): {len(pending)} leg(s)")

        for artifact in pending:
            with tempfile.TemporaryDirectory() as work_dir:
                work = Path(work_dir)
                zip_path = github.download_artifact(
                    artifact.id, work / "artifact.zip", repo=repo
                )
                output_xml = _extract_output_xml(zip_path, work / "unpacked")
                if output_xml is None:
                    report(f"    {artifact.name}: no output.xml, skipped")
                    continue
                info, results = parse(output_xml)
                leg_id = _insert_leg(connection, run, artifact, info)
                tests, failures = _insert_results(connection, leg_id, results)
            totals["legs"] += 1
            totals["tests"] += tests
            totals["failures"] += failures
            already.add(artifact.id)
            connection.commit()
            report(f"    {artifact.name}: {tests} tests, {failures} failed")

    connection.commit()
    connection.close()
    return totals


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
