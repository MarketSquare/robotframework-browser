"""Turns the database into the two questions worth asking of it so far.

Which tests fail, and on which error. A test that fails twice on one error and
four times on another is two problems, not one, so the pair is the unit - not the
test, and not the error.

No flakiness verdict. Whether an error is a flake, a real bug or a broken machine
is a judgement to make while looking at the numbers, not one to bake into them.
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .db import connect


@dataclass
class FailureGroup:
    longname: str
    error_signature: str | None
    failing_keyword: str | None
    failures: int
    total_runs: int  # how many times the test ran at all
    example_message: str | None
    platforms: str
    first_seen: str
    last_seen: str
    # Where to go for the screenshots, traces and playwright-log.txt of the most
    # recent occurrence. The whole reason the artifact URL is stored.
    latest_artifact_url: str | None
    latest_run_url: str | None

    @property
    def failure_rate(self) -> float:
        return self.failures / self.total_runs if self.total_runs else 0.0


def failure_groups(db_path: Path, limit: int = 100) -> list[FailureGroup]:
    """Every (test, error) pair that has failed, most failures first."""
    connection = connect(db_path)
    rows = connection.execute(
        """
        WITH runs_per_test AS (
            SELECT longname, COUNT(*) AS total FROM test_result GROUP BY longname
        )
        SELECT f.longname,
               f.error_signature,
               f.failing_keyword,
               COUNT(*)                       AS failures,
               runs_per_test.total            AS total_runs,
               MIN(f.message)                 AS example_message,
               GROUP_CONCAT(DISTINCT l.platform) AS platforms,
               MIN(r.created_at)              AS first_seen,
               MAX(r.created_at)              AS last_seen,
               (SELECT l2.artifact_url FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND IFNULL(f2.error_signature, '') = IFNULL(f.error_signature, '')
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_artifact_url,
               (SELECT r2.url FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND IFNULL(f2.error_signature, '') = IFNULL(f.error_signature, '')
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_run_url
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        JOIN runs_per_test ON runs_per_test.longname = f.longname
        WHERE f.status = 'FAIL'
        GROUP BY f.longname, f.error_signature
        ORDER BY failures DESC, f.longname
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    connection.close()
    return [FailureGroup(**dict(row)) for row in rows]


def totals(db_path: Path) -> dict:
    connection = connect(db_path)
    row = connection.execute(
        "SELECT (SELECT COUNT(*) FROM run) AS runs, "
        "(SELECT COUNT(*) FROM leg) AS legs, "
        "(SELECT COUNT(*) FROM test_result) AS results, "
        "(SELECT COUNT(*) FROM test_result WHERE status='FAIL') AS failures, "
        "(SELECT COUNT(DISTINCT longname) FROM test_result) AS tests, "
        "(SELECT MIN(created_at) FROM run) AS since, "
        "(SELECT MAX(created_at) FROM run) AS until"
    ).fetchone()
    connection.close()
    return dict(row)


def print_report(
    db_path: Path, limit: int = 40, out: Callable[[str], None] = print
) -> None:
    """The same thing the HTML report shows, for a terminal."""
    summary = totals(db_path)
    if not summary["results"]:
        out("Nothing ingested yet. Run `inv ci-ingest` first.")
        return
    out(
        f"{summary['runs']} runs, {summary['legs']} legs, {summary['results']} results, "
        f"{summary['failures']} failures, {summary['tests']} distinct tests"
    )
    out(f"{summary['since']} .. {summary['until']}\n")

    groups = failure_groups(db_path, limit=limit)
    if not groups:
        out("No failures recorded.")
        return
    for group in groups:
        out(
            f"{group.failures:>3} / {group.total_runs:<4} ({group.failure_rate:5.1%})  {group.longname}"
        )
        out(
            f"                      keyword: {group.failing_keyword or '-'}   on: {group.platforms}"
        )
        out(f"                      {(group.error_signature or '(no message)')[:110]}")
        out(f"                      evidence: {group.latest_artifact_url or '-'}")
        out("")
    out(f"{len(groups)} (test, error) group(s).")
