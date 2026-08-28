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

# Two libraries implement the same gRPC deadline and spell the expiry
# differently: grpcio's C core says "Deadline Exceeded" when the Python client's
# timer fires, @grpc/grpc-js says "Deadline exceeded" when the Node server's
# timer wins the same race. Grouping on the exact string splits one problem into
# two - it did, for the most frequent failure there is: 4 legs against 1, or 8
# marked test rows against 2, depending on which of them you were counting.
# So the key is case-folded. The spelling is not noise, it names which side of
# the boundary gave up first, so it survives in `signature_variants` and in the
# raw messages; it just does not get to be a different problem.
#
# In SQL that is `LOWER(IFNULL(<alias>.error_signature, ''))`, written out at
# each use rather than interpolated: these queries are read far more often than
# they are edited, and a format placeholder in the middle of a GROUP BY hides
# the one thing a reader needs to see.


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

    test_source: str | None
    test_lineno: int | None
    keyword_owner: str | None
    keyword_kind: str | None
    keyword_source: str | None
    keyword_lineno: int | None

    rf_versions: str | None
    python_versions: str | None
    node_versions: str | None

    screenshots: str | None
    screenshot_status: str | None

    # How many different commits this was seen on. Four failures across four
    # commits is a standing problem; four across one is that one commit.
    distinct_shas: int

    @property
    def failure_rate(self) -> float:
        return self.failures / self.total_runs if self.total_runs else 0.0

    @property
    def signature_key(self) -> str:
        """What this group is keyed on. See `_KEY`."""
        return (self.error_signature or "").lower()


def failure_groups(db_path: Path, limit: int = 100) -> list[FailureGroup]:
    """Every (test, error) pair that has failed, most failures first."""
    connection = connect(db_path)
    rows = connection.execute(
        """
        WITH runs_per_test AS (
            SELECT longname, COUNT(*) AS total FROM test_result GROUP BY longname
        )
        SELECT f.longname,
               -- The group is keyed case-insensitively, so one spelling has to
               -- stand for the row. MIN is deterministic, and capitals sort
               -- first, which happens to be the spelling that occurs most.
               MIN(f.error_signature)         AS error_signature,
               f.failing_keyword,
               f.test_source,
               f.test_lineno,
               f.keyword_owner,
               f.keyword_kind,
               f.keyword_source,
               f.keyword_lineno,
               MAX(f.screenshots)             AS screenshots,
               MAX(f.screenshot_status)       AS screenshot_status,
               COUNT(*)                       AS failures,
               COUNT(DISTINCT r.head_sha)     AS distinct_shas,
               runs_per_test.total            AS total_runs,
               MIN(f.message)                 AS example_message,
               GROUP_CONCAT(DISTINCT l.platform) AS platforms,
               GROUP_CONCAT(DISTINCT l.rf_version) AS rf_versions,
               GROUP_CONCAT(DISTINCT l.python_version) AS python_versions,
               GROUP_CONCAT(DISTINCT l.node_version) AS node_versions,
               MIN(r.created_at)              AS first_seen,
               MAX(r.created_at)              AS last_seen,
               (SELECT l2.artifact_url FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND LOWER(IFNULL(f2.error_signature, ''))
                     = LOWER(IFNULL(f.error_signature, ''))
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_artifact_url,
               (SELECT r2.url FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND LOWER(IFNULL(f2.error_signature, ''))
                     = LOWER(IFNULL(f.error_signature, ''))
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_run_url,
               (SELECT f2.id FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                  JOIN run r2 ON r2.id = l2.run_id
                 WHERE f2.longname = f.longname
                   AND f2.status = 'FAIL'
                   AND LOWER(IFNULL(f2.error_signature, ''))
                     = LOWER(IFNULL(f.error_signature, ''))
                 ORDER BY r2.created_at DESC LIMIT 1) AS latest_result_id
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        JOIN runs_per_test ON runs_per_test.longname = f.longname
        WHERE f.status = 'FAIL'
          AND IFNULL(f.failure_scope, 'test') NOT IN ('suite_setup', 'suite_teardown')
        GROUP BY f.longname, LOWER(IFNULL(f.error_signature, ''))
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

    test_source: str | None
    keyword: str | None
    keyword_owner: str | None
    keyword_kind: str | None
    keyword_source: str | None
    keyword_lineno: int | None

    rf_versions: str | None
    python_versions: str | None
    node_versions: str | None

    screenshots: str | None
    screenshot_status: str | None

    distinct_shas: int

    @property
    def failure_rate(self) -> float:
        return self.occurrences / self.suite_runs if self.suite_runs else 0.0

    @property
    def signature_key(self) -> str:
        """What this group is keyed on. See `_KEY`."""
        return (self.error_signature or "").lower()


def fixture_failures(db_path: Path, limit: int = 50) -> list[FixtureFailure]:
    """Suite setup and teardown failures, one row per fixture and error."""
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.scope_owner,
               f.failure_scope,
               MIN(f.error_signature)            AS error_signature,
               COUNT(DISTINCT r.head_sha)        AS distinct_shas,
               MIN(f.test_source)                AS test_source,
               f.failing_keyword                 AS keyword,
               f.keyword_owner,
               f.keyword_kind,
               f.keyword_source,
               f.keyword_lineno,
               MAX(f.screenshots)                AS screenshots,
               MAX(f.screenshot_status)          AS screenshot_status,
               COUNT(DISTINCT l.id)              AS occurrences,
               COUNT(*)                          AS tests_marked,
               GROUP_CONCAT(DISTINCT f.name)     AS affected_tests,
               GROUP_CONCAT(DISTINCT l.platform) AS platforms,
               GROUP_CONCAT(DISTINCT l.rf_version) AS rf_versions,
               GROUP_CONCAT(DISTINCT l.python_version) AS python_versions,
               GROUP_CONCAT(DISTINCT l.node_version) AS node_versions,
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
        GROUP BY f.scope_owner, f.failure_scope,
                 LOWER(IFNULL(f.error_signature, ''))
        ORDER BY occurrences DESC, f.scope_owner
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    connection.close()
    return [FixtureFailure(**dict(row)) for row in rows]


def _configurations(
    db_path: Path, sql: str, key_length: int
) -> dict[tuple, list[dict]]:
    connection = connect(db_path)
    rows = connection.execute(sql).fetchall()
    connection.close()
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = tuple(row[index] for index in range(key_length))
        grouped.setdefault(key, []).append(
            {
                "platform": row["platform"],
                "rf_version": row["rf_version"],
                "python_version": row["python_version"],
                "node_version": row["node_version"],
                "occurrences": row["occurrences"],
            }
        )
    return grouped


def configurations_by_test(db_path: Path) -> dict[tuple, list[dict]]:
    """The matrix legs each test/error group was actually seen on, with counts.

    One row per combination rather than one list per dimension. Listing the
    dimensions separately implies every pairing of them happened: a group seen on
    rf 7.1.1 with Python 3.13.15 and on rf 7.4.2 with Python 3.14.7 reads as four
    combinations when only two ever ran, and those two are whole matrix legs, so
    the versions cannot be told apart at all.
    """
    return _configurations(
        db_path,
        """
        SELECT f.longname,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               l.platform, l.rf_version,
               l.python_version, l.node_version, COUNT(*) AS occurrences
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE f.status = 'FAIL'
          AND IFNULL(f.failure_scope, 'test') NOT IN ('suite_setup', 'suite_teardown')
        GROUP BY f.longname, LOWER(IFNULL(f.error_signature, '')), l.platform,
                 l.rf_version, l.python_version, l.node_version
        ORDER BY occurrences DESC, l.platform
        """,
        2,
    )


def configurations_by_fixture(db_path: Path) -> dict[tuple, list[dict]]:
    """The same, for suite fixtures. Counted in legs, not in the test rows a
    single broken fixture happens to mark."""
    return _configurations(
        db_path,
        """
        SELECT f.scope_owner, f.failure_scope,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               l.platform, l.rf_version, l.python_version, l.node_version,
               COUNT(DISTINCT l.id) AS occurrences
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE f.status = 'FAIL'
          AND f.failure_scope IN ('suite_setup', 'suite_teardown')
        GROUP BY f.scope_owner, f.failure_scope,
                 LOWER(IFNULL(f.error_signature, '')), l.platform,
                 l.rf_version, l.python_version, l.node_version
        ORDER BY occurrences DESC, l.platform
        """,
        3,
    )


def occurrences_by_test(db_path: Path) -> dict[tuple, list[dict]]:
    """Every individual failure behind a group: which run, which commit, when.

    A group's counts cannot say whether four failures are one bad commit seen
    four times or a problem that has survived four of them. The commit and the
    event are in the database and were simply never asked for.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.longname,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               f.id AS result_id, f.elapsed_ms,
               r.id AS run_id, r.head_sha, r.event, r.created_at, r.url AS run_url,
               l.platform, l.python_version, l.rf_version, l.node_version,
               l.artifact_name, l.artifact_url
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.status = 'FAIL'
          AND IFNULL(f.failure_scope, 'test') NOT IN ('suite_setup', 'suite_teardown')
        ORDER BY r.created_at DESC
        """
    ).fetchall()
    connection.close()
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = (row["longname"], row["signature_key"])
        grouped.setdefault(key, []).append(
            {
                "result_id": row["result_id"],
                "elapsed_ms": row["elapsed_ms"],
                "run_id": row["run_id"],
                "head_sha": row["head_sha"],
                "event": row["event"],
                "created_at": row["created_at"],
                "run_url": row["run_url"],
                "platform": row["platform"],
                "python_version": row["python_version"],
                "rf_version": row["rf_version"],
                "node_version": row["node_version"],
                "artifact_name": row["artifact_name"],
                "artifact_url": row["artifact_url"],
            }
        )
    return grouped


def coverage_by_test(db_path: Path) -> dict[str, list[dict]]:
    """Per configuration, how often a test ran and how often it failed.

    One global rate hides the only thing that matters about it. Screenshot On
    Failure is 3 of 81 overall, which says nothing; it is 3 of 55 on linux and
    0 of 26 on darwin, which says where to look. Configurations with no failures
    are included: 26 clean runs is evidence, and a configuration missing from
    this list never ran the test at all, which is not the same as passing it.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.longname, l.platform, l.python_version, l.rf_version,
               l.node_version,
               COUNT(*) AS ran,
               SUM(CASE WHEN f.status = 'FAIL' THEN 1 ELSE 0 END) AS failed
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        GROUP BY f.longname, l.platform, l.python_version, l.rf_version,
                 l.node_version
        ORDER BY failed DESC, ran DESC
        """
    ).fetchall()
    connection.close()
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["longname"], []).append(
            {
                "platform": row["platform"],
                "python_version": row["python_version"],
                "rf_version": row["rf_version"],
                "node_version": row["node_version"],
                "ran": row["ran"],
                "failed": row["failed"] or 0,
            }
        )
    return grouped


def _spread(values: list[int]) -> dict:
    """Four numbers, because the shape is what carries the argument.

    A cliff between the passes and the failures is a keyword that broke. A tail
    that reaches up into them is a margin that ran out. `min` and `max` alone
    cannot tell those apart; the median says where the mass sits.
    """
    last = len(values) - 1
    return {
        "min": values[0],
        "median": values[last // 2],
        "p95": values[min(last, round(0.95 * last))],
        "max": values[last],
    }


def pass_durations_by_test(db_path: Path) -> dict[tuple, dict]:
    """How long a test takes on the runs where it passes, per configuration.

    A timeout message supports two readings that want opposite fixes: something
    broke, or the budget was always too thin. Only the passing runs separate
    them. `Verify Removed Scope` fails on a 1500 ms click timeout waiting for a
    button the page enables after 700 ms; its linux passes span 1001-1853 ms and
    its win32 passes span 1033-1169 ms. The linux tail overlaps the failures and
    the win32 one is nowhere near them. That is a margin being spent, not a
    keyword that broke, and the message on its own says neither.

    Section 1 keeps the passing rows because a failure count without a run count
    is not a rate. This is the same argument one level down: a failure duration
    without a pass duration is not a margin.

    Keyed the same way as `coverage_by_test` groups, so the two join. Only tests
    that failed at least once are measured - nothing else is being asked about.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.longname, l.platform, l.python_version, l.rf_version,
               l.node_version, f.elapsed_ms
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE f.status = 'PASS' AND f.elapsed_ms IS NOT NULL
          AND f.longname IN (SELECT longname FROM test_result WHERE status = 'FAIL')
        """
    ).fetchall()
    connection.close()
    grouped: dict[tuple, list[int]] = {}
    for row in rows:
        key = (
            row["longname"],
            row["platform"],
            row["python_version"],
            row["rf_version"],
            row["node_version"],
        )
        grouped.setdefault(key, []).append(row["elapsed_ms"])
    return {key: _spread(sorted(values)) for key, values in grouped.items()}


def _verdict(statuses: list[str]) -> str:
    unique = set(statuses)
    if "FAIL" in unique:
        return "mixed" if "PASS" in unique else "fail"
    return "pass" if "PASS" in unique else "skip"


def neighbouring_outcomes(db_path: Path) -> dict[int, dict]:
    """What the same test did on the same leg in the runs either side of this one.

    A rate says how often a test fails. It cannot say whether a failure is a blip
    on a leg that is otherwise healthy or the point where something broke and
    stayed broken, and those want opposite responses. The run before and the run
    after answer it, and both are already here: the passing rows are stored for
    exactly this kind of question and were never asked it.

    The comparison is per leg, not per run. A test that only fails on win32 has
    nothing to learn from the linux run that happened to come next.

    Retries answer the same question with the commit held constant, which is the
    one thing the neighbouring runs cannot do - a real regression, fixed by the
    next commit, has passing neighbours and looks like a flake. There is no
    automatic retry in any of the three workflows, so a leg that ran more than
    once in one run was re-run by hand; when the test passed on one of those
    attempts it failed and passed on one commit, minutes apart. Its absence means
    nobody pressed the button - the decision follows queue pressure and where the
    run sat in the day's merges, not what failed - so a retry is reported when it
    exists and nothing at all is concluded from it when it does not.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.id AS result_id, f.longname, f.status,
               l.artifact_name, l.id AS leg_id,
               r.id AS run_id, r.head_sha, r.created_at
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.longname IN (SELECT longname FROM test_result WHERE status = 'FAIL')
        ORDER BY r.created_at, r.id
        """
    ).fetchall()
    connection.close()

    # One lane per (test, matrix leg), each holding the runs that leg made in
    # order. A run appears once even when it holds several attempts of the leg.
    lanes: dict[tuple, dict] = {}
    for row in rows:
        lane = lanes.setdefault((row["longname"], row["artifact_name"]), {})
        run = lane.setdefault(
            (row["created_at"], row["run_id"]),
            {
                "run": row["run_id"],
                "commit": row["head_sha"],
                "at": row["created_at"],
                "statuses": [],
                "legs": set(),
            },
        )
        run["statuses"].append(row["status"])
        run["legs"].add(row["leg_id"])

    def seen(run: dict) -> dict:
        return {
            "run": run["run"],
            "commit": run["commit"],
            "at": run["at"],
            "outcome": _verdict(run["statuses"]),
        }

    outcomes: dict[int, dict] = {}
    for row in rows:
        if row["status"] != "FAIL":
            continue
        lane = lanes[(row["longname"], row["artifact_name"])]
        order = sorted(lane)
        here = order.index((row["created_at"], row["run_id"]))
        mine = lane[order[here]]
        # Only claimed when the test itself ran more than once. A re-run leg that
        # never reached this test is not evidence about this test.
        retry = None
        if len(mine["legs"]) > 1:
            retry = {
                "attempts": len(mine["legs"]),
                "passed_on_another_attempt": "PASS" in mine["statuses"],
            }
        outcomes[row["result_id"]] = {
            "previous_run_on_this_leg": seen(lane[order[here - 1]]) if here else None,
            "next_run_on_this_leg": (
                seen(lane[order[here + 1]]) if here + 1 < len(order) else None
            ),
            "retry": retry,
        }
    return outcomes


def co_failures(db_path: Path) -> dict[int, list[dict]]:
    """The other tests that failed in the same leg as this one.

    Section 3 splits out the cascade Robot Framework creates structurally: a
    suite fixture fails, and every test beneath it is marked. A data dependency
    is a cascade too, and it is not structural, so nothing detects it.
    `01 Initial Import.Take Screenshot` fails on a darwin screenshot error, so
    the `VAR ... scope=GLOBAL` on the next line never runs, so the two suites
    after it fail on a variable that was never set. Three entries, three files,
    three rates - one event. Two of the three are labelled `standard`, which
    routes the reader at an assertion that is not broken.

    This claims no causation and cannot. It reports what else broke in the same
    leg, which costs one query and is the only hint the data has to offer.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT a.id AS result_id, b.longname,
               IFNULL(b.failure_scope, 'test') AS scope
        FROM test_result a
        JOIN test_result b
          ON b.leg_id = a.leg_id AND b.id <> a.id AND b.status = 'FAIL'
        WHERE a.status = 'FAIL'
        ORDER BY a.id, b.longname
        """
    ).fetchall()
    connection.close()
    grouped: dict[int, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["result_id"], []).append(
            {"test": row["longname"], "scope": row["scope"]}
        )
    return grouped


def latest_run(db_path: Path) -> dict:
    """The newest run in the window, and how many failures it carried.

    The rates answer "how often does this break". They do not answer "is it
    broken now", which is the question a merge is judged on, and a window whose
    newest run is clean is a different situation from one whose newest run is
    not - however bad the rates in between.
    """
    connection = connect(db_path)
    row = connection.execute(
        "SELECT id, created_at, event, head_sha FROM run "
        "ORDER BY created_at DESC, id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        connection.close()
        return {}
    failures = connection.execute(
        """
        SELECT COUNT(*) FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE l.run_id = ? AND f.status = 'FAIL'
        """,
        (row["id"],),
    ).fetchone()[0]
    connection.close()
    return {
        "run": row["id"],
        "commit": row["head_sha"],
        "event": row["event"],
        "at": row["created_at"],
        "failures": failures,
    }


def messages_by_test(db_path: Path) -> dict[tuple, list[dict]]:
    """Every distinct raw message behind a group, with how often each occurred.

    The signature masks what varies, which is what makes grouping possible and
    is also what throws away the evidence. Three failures of Compare Images
    carry an identical box and a pixel count differing by three - deterministic,
    not jittery - and the signature renders all of that as `<n>`. Cheap to keep:
    16 of the 18 groups have exactly one distinct message.
    """
    connection = connect(db_path)
    rows = connection.execute(
        """
        SELECT f.longname,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               f.message, COUNT(*) AS occurrences
        FROM test_result f
        WHERE f.status = 'FAIL' AND f.message IS NOT NULL
        GROUP BY f.longname, LOWER(IFNULL(f.error_signature, '')), f.message
        ORDER BY occurrences DESC
        """
    ).fetchall()
    connection.close()
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = (row["longname"], row["signature_key"])
        grouped.setdefault(key, []).append(
            {"message": row["message"], "occurrences": row["occurrences"]}
        )
    return grouped


def _variants(db_path: Path, sql: str, key_length: int) -> dict[tuple, list[dict]]:
    connection = connect(db_path)
    rows = connection.execute(sql).fetchall()
    connection.close()
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = tuple(row[index] for index in range(key_length))
        grouped.setdefault(key, []).append(
            {
                "signature": row["error_signature"],
                "occurrences": row["occurrences"],
            }
        )
    # Only the groups the case-folded key actually merged. One spelling is the
    # normal case and saying so on every entry would bury the one that matters.
    return {key: value for key, value in grouped.items() if len(value) > 1}


def signature_variants(db_path: Path) -> dict[tuple, list[dict]]:
    """The distinct spellings of one test group's signature, with counts.

    Only ever more than one when two libraries name the same condition, which is
    exactly the case the case-folded key exists to merge. See `_KEY`.
    """
    return _variants(
        db_path,
        """
        SELECT f.longname,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               f.error_signature, COUNT(*) AS occurrences
        FROM test_result f
        WHERE f.status = 'FAIL' AND f.error_signature IS NOT NULL
          AND IFNULL(f.failure_scope, 'test') NOT IN ('suite_setup', 'suite_teardown')
        GROUP BY f.longname, LOWER(IFNULL(f.error_signature, '')),
                 f.error_signature
        ORDER BY occurrences DESC
        """,
        2,
    )


def fixture_signature_variants(db_path: Path) -> dict[tuple, list[dict]]:
    """The same, for suite fixtures - which is where it actually happens.

    The `Deadline Exceeded` / `Deadline exceeded` split that motivated the
    case-folded key is a suite teardown, so keying these per test would have
    missed the only case in the data that has any.
    """
    return _variants(
        db_path,
        """
        SELECT f.scope_owner, f.failure_scope,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               f.error_signature, COUNT(DISTINCT l.id) AS occurrences
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE f.status = 'FAIL' AND f.error_signature IS NOT NULL
          AND f.failure_scope IN ('suite_setup', 'suite_teardown')
        GROUP BY f.scope_owner, f.failure_scope,
                 LOWER(IFNULL(f.error_signature, '')), f.error_signature
        ORDER BY occurrences DESC
        """,
        3,
    )


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
