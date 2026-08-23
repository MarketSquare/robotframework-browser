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
    latest_result_id: int | None

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
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_run_url,
               (SELECT f2.id FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND IFNULL(f2.error_signature, '') = IFNULL(f.error_signature, '')
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_result_id
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        JOIN runs_per_test ON runs_per_test.longname = f.longname
        WHERE f.status = 'FAIL'
          AND IFNULL(f.failure_scope, 'test') NOT IN ('suite_setup', 'suite_teardown')
        GROUP BY f.longname, f.error_signature
        ORDER BY failures DESC, f.longname
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    connection.close()
    return [FailureGroup(**dict(row)) for row in rows]


@dataclass
class FixtureFailure:
    """One suite setup or teardown that broke, and the tests it took with it.

    The unit is the fixture failing, not the tests it marked: those are the same
    event seen as many times as the suite has tests. Counting them as separate
    test failures makes one broken teardown outrank everything else.
    """

    scope_owner: str
    failure_scope: str
    error_signature: str | None
    occurrences: int  # distinct (run, leg) the fixture failed in
    suite_runs: int  # distinct legs that ran any test of that suite
    tests_marked: int  # test rows Robot Framework failed because of it
    affected_tests: str
    platforms: str
    first_seen: str
    last_seen: str
    latest_artifact_url: str | None
    latest_result_id: int | None

    @property
    def failure_rate(self) -> float:
        return self.occurrences / self.suite_runs if self.suite_runs else 0.0


def fixture_failures(db_path: Path, limit: int = 50) -> list[FixtureFailure]:
    """Suite setup and teardown failures, one row per fixture and error."""
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.scope_owner,
               f.failure_scope,
               f.error_signature,
               COUNT(DISTINCT l.id)              AS occurrences,
               COUNT(*)                          AS tests_marked,
               GROUP_CONCAT(DISTINCT f.name)     AS affected_tests,
               GROUP_CONCAT(DISTINCT l.platform) AS platforms,
               MIN(r.created_at)                 AS first_seen,
               MAX(r.created_at)                 AS last_seen,
               (SELECT COUNT(DISTINCT l2.id) FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                 WHERE f2.suite_longname = f.scope_owner
                    OR f2.suite_longname LIKE f.scope_owner || '.%') AS suite_runs,
               (SELECT l2.artifact_url FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.scope_owner = f.scope_owner
                   AND f2.status = 'FAIL'
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_artifact_url,
               (SELECT f2.id FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.scope_owner = f.scope_owner
                   AND f2.status = 'FAIL'
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_result_id
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.status = 'FAIL'
          AND f.failure_scope IN ('suite_setup', 'suite_teardown')
        GROUP BY f.scope_owner, f.failure_scope, f.error_signature
        ORDER BY occurrences DESC, f.scope_owner
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    connection.close()
    return [FixtureFailure(**dict(row)) for row in rows]


def log_messages(db_path: Path, result_id: int | None) -> list[dict]:
    """What the failing keywords logged, for one occurrence of a failure."""
    if result_id is None:
        return []
    connection = connect(db_path)
    rows = connection.execute(
        "SELECT seq, level, keyword, origin, message FROM log_message "
        "WHERE test_result_id = ? ORDER BY seq",
        (result_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def platform_breakdown(db_path: Path) -> list[dict]:
    """Failures per matrix leg, by platform.

    Per leg rather than absolute, because the matrix does not run the platforms
    an equal number of times and the raw counts would say more about the matrix
    than about the platforms.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT l.platform,
               COUNT(DISTINCT l.id) AS legs,
               SUM(CASE WHEN t.status = 'FAIL' THEN 1 ELSE 0 END) AS failures
        FROM leg l
        LEFT JOIN test_result t ON t.leg_id = l.id
        WHERE l.platform IS NOT NULL
        GROUP BY l.platform
        ORDER BY SUM(CASE WHEN t.status = 'FAIL' THEN 1 ELSE 0 END) * 1.0
                 / COUNT(DISTINCT l.id) DESC
        """
    ).fetchall()
    connection.close()
    return [
        {
            "platform": row["platform"],
            "legs": row["legs"],
            "failures": row["failures"] or 0,
            "per_leg": (row["failures"] or 0) / row["legs"] if row["legs"] else 0.0,
        }
        for row in rows
    ]


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

    fixtures = fixture_failures(db_path, limit=limit)
    if fixtures:
        out("SUITE SETUP AND TEARDOWN FAILURES")
        out("  These failed outside any test. Robot Framework marks every test")
        out("  under the suite as failed, so they are counted once here.\n")
        for fixture in fixtures:
            kind = fixture.failure_scope.replace("_", " ")
            out(
                f"{fixture.occurrences:>3} / {fixture.suite_runs:<4} "
                f"({fixture.failure_rate:5.1%})  {kind} of {fixture.scope_owner}"
            )
            out(
                f"                      {(fixture.error_signature or '(no message)')[:110]}"
            )
            out(
                f"                      marked {fixture.tests_marked} test row(s) failed"
                f"   on: {fixture.platforms}"
            )
            out(f"                      evidence: {fixture.latest_artifact_url or '-'}")
            out("")

    groups = failure_groups(db_path, limit=limit)
    out("TEST FAILURES")
    if not groups:
        out("  None.")
        return
    out("")
    for group in groups:
        out(
            f"{group.failures:>3} / {group.total_runs:<4} ({group.failure_rate:5.1%})  "
            f"{group.longname}"
        )
        out(
            f"                      keyword: {group.failing_keyword or '-'}"
            f"   on: {group.platforms}"
        )
        out(f"                      {(group.error_signature or '(no message)')[:110]}")
        out(f"                      evidence: {group.latest_artifact_url or '-'}")
        out("")
    out(f"{len(groups)} test/error group(s), {len(fixtures)} fixture failure(s).")
