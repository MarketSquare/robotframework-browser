"""Every question the Report asks of the database, and nothing else.

Which tests fail, and on which error. A test that fails twice on one error and
four times on another is two problems, not one, so the pair is the unit - not the
test, and not the error.

No flakiness verdict, and no judgement of any kind: `report.py` decides what the
numbers mean.

This used to be written as "if a function here does not run SQL it is in the
wrong file", which is a sharper rule than the one actually kept. Four functions
run none. `_subject_key` and `_row_without_key` shape a row on its way out;
`_spread` picks four order statistics out of a sorted list; `_verdict` reads a
Leg's statuses and says what the Subject did in that Run - and that last one is
a judgement by any reading. It is here because it is called from inside the lane
walk in `runs_either_side` and its fixture twin, where moving it would mean
handing `report.py` raw status tuples instead of an answer. Worth knowing about
rather than worth pretending away.
"""

from dataclasses import dataclass
from typing import NamedTuple

from .reading import Reading

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


# --- What a query hands back -------------------------------------------------
#
# Rows, not dicts. `report.py` used to reach into these by string key about
# sixty times, naming SQL aliases it could not see, and half of those shapes had
# two producers that were free to drift apart - which is the defect ADR 0001 was
# written against, one layer below where it was applied. Built with `**` off the
# row wherever the shape comes straight from SQL, so a renamed or dropped alias
# is a TypeError here rather than a KeyError, a None, or a section that quietly
# renders empty.


def _subject_key(row) -> "SubjectKey":
    return SubjectKey(row["subject_owner"], row["subject_scope"], row["signature_key"])


def _row_without_key(row) -> dict:
    """The row's own columns. The three key ones identify it, they are not it."""
    return {
        name: value
        for name, value in dict(row).items()
        if name not in ("subject_owner", "subject_scope", "signature_key")
    }


class SubjectKey(NamedTuple):
    """What a Group or a Fixture Failure is keyed on: one Subject, one signature.

    A NamedTuple rather than a class, so it still compares equal to the plain
    tuple every lookup used to build by hand.
    """

    owner: str
    scope: str
    signature: str


class FixtureLegKey(NamedTuple):
    """A Fixture Failure in one Leg.

    Also three fields, and it is not a SubjectKey - the third is a Leg, not a
    signature. They were both bare 3-tuples and telling them apart was left to
    whoever was reading.
    """

    owner: str
    scope: str
    leg_id: int


class Outcome:
    """What a Subject did in one Run on one Leg.

    Five values, of which exactly one used to be a named constant. The page
    asked `outcome in ("fail", "mixed")` with the list written out, so a sixth
    verdict would have rendered as healthy and nothing would have said so.
    """

    PASS = "pass"
    FAIL = "fail"
    MIXED = "mixed"
    SKIP = "skip"
    # No verdict rather than a bad one: every row was marked by a suite fixture,
    # so the Run says nothing about this Subject.
    SUITE_BROKE = "suite broke"

    #: The outcomes that mean this Subject was not healthy in that Run.
    BAD = frozenset({FAIL, MIXED})


@dataclass(frozen=True)
class OccurrenceRow:
    """One Occurrence, whether its Subject is a test or a suite fixture.

    The two producers selected the same columns and returned different shapes -
    one hand-listed eighteen keys, the other passed the row through whole - so
    one concept arrived at `report.py` as two dicts. The fields that genuinely
    differ are the last three, and they differ because the grains do: a test's
    Occurrence is one Result and has a duration, a fixture's is one Leg and has
    the number of rows it marked.
    """

    result_id: int
    run_id: int
    head_sha: str | None
    event: str | None
    created_at: str | None
    run_url: str | None
    platform: str | None
    python_version: str | None
    rf_version: str | None
    node_version: str | None
    artifact_name: str | None
    artifact_url: str | None
    attempt: int | None
    executors: int | None
    node_process: str | None
    screenshots: str | None
    screenshot_status: str | None
    elapsed_ms: int | None = None  # tests only
    leg_id: int | None = None  # fixtures only
    tests_marked: int | None = None  # fixtures only


@dataclass(frozen=True)
class CoverageRow:
    """How often one configuration ran a Subject, and how often it failed it."""

    platform: str | None
    python_version: str | None
    rf_version: str | None
    node_version: str | None
    ran: int
    failed: int


@dataclass(frozen=True)
class Spread:
    """Four numbers, because the shape is what carries the argument."""

    min: int
    median: int
    p95: int
    max: int


@dataclass(frozen=True)
class AdjacentRun:
    """What the same Subject did in the Run either side of this one, same Leg."""

    run: int
    commit: str | None
    at: str | None
    outcome: str


@dataclass(frozen=True)
class Retry:
    """A Leg re-run by hand, and whether the Subject passed on one of the tries."""

    attempts: int
    passed_on_another_attempt: bool


@dataclass(frozen=True)
class Around:
    """Everything that surrounded one Occurrence but is not part of it."""

    previous_run_on_this_leg: AdjacentRun | None
    next_run_on_this_leg: AdjacentRun | None
    retry: Retry | None


#: What is known about an Occurrence nothing surrounds - no Run either side on
#: its Leg, and nobody re-ran it. A default that is the right shape, because a
#: `.get(key, {})` that missed used to hand `report.py` a dict where a row
#: belonged and take the whole section down with it.
NOTHING_AROUND = Around(
    previous_run_on_this_leg=None, next_run_on_this_leg=None, retry=None
)


@dataclass(frozen=True)
class CoFailure:
    """Another Subject that failed in the same Leg."""

    subject: str
    scope: str | None


@dataclass(frozen=True)
class MessageRow:
    """One distinct raw message behind a Subject, and how often it occurred."""

    message: str
    occurrences: int


@dataclass(frozen=True)
class VariantRow:
    """One spelling of an Error Signature, and how often it occurred."""

    signature: str
    occurrences: int


@dataclass(frozen=True)
class LogRow:
    """One line a failing keyword logged."""

    level: str | None
    keyword: str | None
    origin: str | None
    message: str | None


@dataclass(frozen=True)
class PlatformRow:
    """How much of the window one platform ran, and how much of it failed."""

    platform: str | None
    legs: int
    failures: int
    per_leg: float


@dataclass(frozen=True)
class LatestRun:
    """The newest Run in the window, and how many failures it carried."""

    run: int
    commit: str | None
    event: str | None
    at: str | None
    failures: int


@dataclass(frozen=True)
class Totals:
    """What the window holds at all, which is what every rate is divided by."""

    runs: int
    legs: int
    results: int
    failures: int
    tests: int
    legs_without_attempt: int
    since: str | None
    until: str | None


@dataclass
class FailureGroup:
    longname: str
    error_signature: str | None
    failing_keyword: str | None
    failures: int
    total_runs: int  # how many times the test ran at all

    test_source: str | None
    test_lineno: int | None
    keyword_owner: str | None
    keyword_kind: str | None
    keyword_source: str | None
    keyword_lineno: int | None

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


def failure_groups(db: Reading, limit: int = 100) -> list[FailureGroup]:
    """Every (test, error) pair that has failed, most failures first."""
    rows = db.execute(
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
               COUNT(*)                       AS failures,
               COUNT(DISTINCT r.head_sha)     AS distinct_shas,
               runs_per_test.total            AS total_runs
        FROM test_failure f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        JOIN runs_per_test ON runs_per_test.longname = f.longname
        GROUP BY f.longname, LOWER(IFNULL(f.error_signature, ''))
        ORDER BY failures DESC, f.longname
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
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

    test_source: str | None
    failing_keyword: str | None
    keyword_owner: str | None
    keyword_kind: str | None
    keyword_source: str | None
    keyword_lineno: int | None

    distinct_shas: int

    @property
    def failure_rate(self) -> float:
        return self.occurrences / self.suite_runs if self.suite_runs else 0.0

    @property
    def signature_key(self) -> str:
        """What this group is keyed on. See `_KEY`."""
        return (self.error_signature or "").lower()


def fixture_failures(db: Reading, limit: int = 50) -> list[FixtureFailure]:
    """Suite setup and teardown failures, one row per fixture and error."""
    rows = db.execute(
        """
        SELECT f.scope_owner,
               f.failure_scope,
               MIN(f.error_signature)            AS error_signature,
               COUNT(DISTINCT r.head_sha)        AS distinct_shas,
               MIN(f.test_source)                AS test_source,
               f.failing_keyword,
               f.keyword_owner,
               f.keyword_kind,
               f.keyword_source,
               f.keyword_lineno,
               COUNT(DISTINCT l.id)              AS occurrences,
               COUNT(*)                          AS tests_marked,
               GROUP_CONCAT(DISTINCT f.name)     AS affected_tests,
               (SELECT COUNT(DISTINCT l2.id) FROM test_result f2
                  JOIN leg l2 ON l2.id = f2.leg_id
                 WHERE f2.suite_longname = f.scope_owner
                    OR f2.suite_longname LIKE f.scope_owner || '.%') AS suite_runs
        FROM fixture_failure f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        GROUP BY f.scope_owner, f.failure_scope,
                 LOWER(IFNULL(f.error_signature, ''))
        ORDER BY occurrences DESC, f.scope_owner
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [FixtureFailure(**dict(row)) for row in rows]


def occurrences_by_test(db: Reading) -> dict[SubjectKey, list[OccurrenceRow]]:
    """Every individual failure behind a group: which run, which commit, when.

    A group's counts cannot say whether four failures are one bad commit seen
    four times or a problem that has survived four of them. The commit and the
    event are in the database and were simply never asked for.
    """
    rows = db.execute(
        """
        SELECT f.subject_owner, f.subject_scope, f.signature_key,
               f.id AS result_id, f.elapsed_ms,
               f.screenshots, f.screenshot_status,
               r.id AS run_id, r.head_sha, r.event, r.created_at, r.url AS run_url,
               l.platform, l.python_version, l.rf_version, l.node_version,
               l.artifact_name, l.artifact_url, l.attempt,
               l.executors, l.node_process
        FROM test_failure f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        ORDER BY r.created_at DESC
        """
    ).fetchall()
    grouped: dict[SubjectKey, list[OccurrenceRow]] = {}
    for row in rows:
        grouped.setdefault(_subject_key(row), []).append(
            OccurrenceRow(**_row_without_key(row))
        )
    return grouped


def coverage_by_test(db: Reading) -> dict[str, list[CoverageRow]]:
    """Per configuration, how often a test ran and how often it failed.

    One global rate hides the only thing that matters about it. Screenshot On
    Failure is 3 of 81 overall, which says nothing; it is 3 of 55 on linux and
    0 of 26 on darwin, which says where to look. Configurations with no failures
    are included: 26 clean runs is evidence, and a configuration missing from
    this list never ran the test at all, which is not the same as passing it.

    The numerator counts only what the test itself did. A row a broken suite
    fixture marked is a Fixture Failure and is counted in its own section, and
    counting it here made the rates disagree with the Group they sat under.
    `ran` stays every row: the test really did run, whatever failed it.
    """
    rows = db.execute(
        """
        SELECT f.longname, l.platform, l.python_version, l.rf_version,
               l.node_version,
               COUNT(*) AS ran,
               SUM(CASE WHEN f.status = 'FAIL'
                         AND IFNULL(f.failure_scope, 'test')
                             NOT IN ('suite_setup', 'suite_teardown')
                        THEN 1 ELSE 0 END) AS failed
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        GROUP BY f.longname, l.platform, l.python_version, l.rf_version,
                 l.node_version
        ORDER BY failed DESC, ran DESC
        """
    ).fetchall()
    grouped: dict[str, list[CoverageRow]] = {}
    for row in rows:
        grouped.setdefault(row["longname"], []).append(
            CoverageRow(
                platform=row["platform"],
                python_version=row["python_version"],
                rf_version=row["rf_version"],
                node_version=row["node_version"],
                ran=row["ran"],
                failed=row["failed"] or 0,
            )
        )
    return grouped


def _spread(values: list[int]) -> Spread:
    """Four numbers, because the shape is what carries the argument.

    A cliff between the passes and the failures is a keyword that broke. A tail
    that reaches up into them is a margin that ran out. `min` and `max` alone
    cannot tell those apart; the median says where the mass sits.
    """
    last = len(values) - 1
    return Spread(
        min=values[0],
        median=values[last // 2],
        p95=values[min(last, round(0.95 * last))],
        max=values[last],
    )


def pass_durations_by_test(db: Reading) -> dict[tuple, Spread]:
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
    rows = db.execute(
        """
        SELECT f.longname, l.platform, l.python_version, l.rf_version,
               l.node_version, f.elapsed_ms
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE f.status = 'PASS' AND f.elapsed_ms IS NOT NULL
          AND f.longname IN (SELECT longname FROM test_result WHERE status = 'FAIL')
        """
    ).fetchall()
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


# What an Adjacent Run says when the only thing that happened to this Subject
# was its suite breaking above it. Not "fail": nothing about this Subject broke,
# and reading it as a failure makes a healthy test look like it had been failing
# for days. Not null either - that already means there was no such run at all.
SUITE_BROKE = "suite broke"


def _verdict(statuses: list[tuple[str, str | None]]) -> str:
    """The outcome of one Subject in one Run on one Leg.

    Rows a suite fixture marked are set aside first. They are the fixture's
    outcome, not this Subject's, and a Run where that is all that happened has no
    verdict to give - which is a third answer rather than a bad one.
    """
    own = {
        status
        for status, scope in statuses
        if (scope or "test") not in ("suite_setup", "suite_teardown")
    }
    if not own:
        return SUITE_BROKE
    if "FAIL" in own:
        return "mixed" if "PASS" in own else "fail"
    return "pass" if "PASS" in own else "skip"


def runs_either_side(db: Reading) -> dict[int, Around]:
    """The Adjacent Runs of each failure: what the same test did on the same Leg
    in the Run immediately before this one and the one immediately after.

    Named for the Runs and not for anything inside a test. The keywords a few
    lines above the one that broke are a different question and this does not
    answer it - see **Adjacent Run** in `CONTEXT.md`, and `0012` section 10 for
    the question that would.

    A rate says how often a test fails. It cannot say whether a failure is a blip
    on a leg that is otherwise healthy or the point where something broke and
    stayed broken, and those want opposite responses. The run before and the run
    after answer it, and both are already here: the passing rows are stored for
    exactly this kind of question and were never asked it.

    The comparison is per leg, not per run. A test that only fails on win32 has
    nothing to learn from the linux run that happened to come next.

    Retries answer the same question with the commit held constant, which is the
    one thing the Adjacent Runs cannot do - a real regression, fixed by the
    next commit, has passing neighbours and looks like a flake. There is no
    automatic retry in any of the three workflows, so a leg that ran more than
    once in one run was re-run by hand; when the test passed on one of those
    attempts it failed and passed on one commit, minutes apart. Its absence means
    nobody pressed the button - the decision follows queue pressure and where the
    run sat in the day's merges, not what failed - so a retry is reported when it
    exists and nothing at all is concluded from it when it does not.
    """
    rows = db.execute(
        """
        SELECT f.id AS result_id, f.longname, f.status, f.failure_scope,
               l.artifact_name, l.id AS leg_id,
               r.id AS run_id, r.head_sha, r.created_at
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.longname IN (SELECT longname FROM test_result WHERE status = 'FAIL')
        ORDER BY r.created_at, r.id
        """
    ).fetchall()

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
        run["statuses"].append((row["status"], row["failure_scope"]))
        run["legs"].add(row["leg_id"])

    def seen(run: dict) -> AdjacentRun:
        return AdjacentRun(
            run=run["run"],
            commit=run["commit"],
            at=run["at"],
            outcome=_verdict(run["statuses"]),
        )

    outcomes: dict[int, Around] = {}
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
            retry = Retry(
                attempts=len(mine["legs"]),
                passed_on_another_attempt=any(
                    status == "PASS" for status, _ in mine["statuses"]
                ),
            )
        outcomes[row["result_id"]] = Around(
            previous_run_on_this_leg=seen(lane[order[here - 1]]) if here else None,
            next_run_on_this_leg=(
                seen(lane[order[here + 1]]) if here + 1 < len(order) else None
            ),
            retry=retry,
        )
    return outcomes


def co_failures(db: Reading) -> dict[int, list[CoFailure]]:
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

    Reported per Subject, so a broken suite fixture is one line naming the suite
    rather than one line for each of the twelve tests it marked. Twelve names
    that are one event is an anti-hint: it buries the tests that broke on their
    own account, which are the ones worth reading.
    """
    rows = db.execute(
        """
        SELECT a.id AS result_id,
               CASE WHEN b.failure_scope IN ('suite_setup', 'suite_teardown')
                    THEN b.scope_owner ELSE b.longname END AS subject,
               IFNULL(b.failure_scope, 'test') AS scope
        FROM test_result a
        JOIN test_result b
          ON b.leg_id = a.leg_id AND b.id <> a.id AND b.status = 'FAIL'
        WHERE a.status = 'FAIL'
        GROUP BY a.id, subject, scope
        ORDER BY a.id, subject
        """
    ).fetchall()
    grouped: dict[int, list[CoFailure]] = {}
    for row in rows:
        grouped.setdefault(row["result_id"], []).append(
            CoFailure(subject=row["subject"], scope=row["scope"])
        )
    return grouped


def _failing_fixtures(db) -> list:
    return db.execute(
        """
        SELECT DISTINCT subject_owner AS scope_owner,
                        subject_scope  AS failure_scope
        FROM fixture_failure WHERE subject_owner IS NOT NULL
        """
    ).fetchall()


def _fixture_legs(db, scope_owner: str, failure_scope: str) -> list:
    """Every leg that ran the suite, and whether this fixture broke in it.

    The denominator for a fixture is legs that ran the suite, never test rows:
    one broken teardown marks every test beneath it, so counting rows counts
    the suite's size. `suite_longname LIKE owner || '.%'` is what includes the
    child suites the fixture also fails.
    """
    return db.execute(
        """
        SELECT l.id AS leg_id, l.artifact_name, l.platform, l.python_version,
               l.rf_version, l.node_version, l.attempt,
               r.id AS run_id, r.head_sha, r.created_at,
               MAX(CASE WHEN f.status = 'FAIL' AND f.failure_scope = ?
                         AND f.scope_owner = ? THEN 1 ELSE 0 END) AS broke
        FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.suite_longname = ? OR f.suite_longname LIKE ? || '.%'
        GROUP BY l.id
        ORDER BY r.created_at, r.id
        """,
        (failure_scope, scope_owner, scope_owner, scope_owner),
    ).fetchall()


def occurrences_by_fixture(db: Reading) -> dict[SubjectKey, list[OccurrenceRow]]:
    """Every leg a fixture broke in: which run, which commit, which leg.

    One entry per leg, not per marked test row. Five teardown failures of
    `Hangs Setup` produced ten failed tests, and listing ten occurrences would
    put back exactly the double count section 3 exists to remove. How many rows
    each leg lost is carried as `tests_marked` instead, where it is a fact about
    the leg rather than a multiplier on the count.
    """
    rows = db.execute(
        """
        SELECT f.subject_owner, f.subject_scope, f.signature_key,
               l.id AS leg_id, f.occurrence_id AS result_id,
               COUNT(*) AS tests_marked,
               -- Every row this fixture marked in one leg carries the same
               -- fixture evidence, so any of them stands for the occurrence.
               MAX(f.screenshots) AS screenshots,
               MAX(f.screenshot_status) AS screenshot_status,
               r.id AS run_id, r.head_sha, r.event, r.created_at,
               r.url AS run_url,
               l.platform, l.python_version, l.rf_version, l.node_version,
               l.artifact_name, l.artifact_url, l.attempt,
               l.executors, l.node_process
        FROM fixture_failure f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        GROUP BY f.occurrence_id
        ORDER BY r.created_at DESC
        """
    ).fetchall()
    grouped: dict[SubjectKey, list[OccurrenceRow]] = {}
    for row in rows:
        grouped.setdefault(_subject_key(row), []).append(
            OccurrenceRow(**_row_without_key(row))
        )
    return grouped


def coverage_by_fixture(db: Reading) -> dict[tuple, list[CoverageRow]]:
    """Per configuration, how often the suite ran and how often the fixture broke.

    `seen_on` said which matrix legs a fixture had been seen failing on and how
    often, with no denominator. That is the same shape section 6 rejected for
    tests: 5 occurrences is not a rate, and 3 of 68 on win32 against 0 of 46
    everywhere else is where to look.
    """
    grouped: dict[tuple, list[CoverageRow]] = {}
    for fixture in _failing_fixtures(db):
        owner = fixture["scope_owner"]
        scope = fixture["failure_scope"]
        counts: dict[tuple, list[int]] = {}
        for row in _fixture_legs(db, owner, scope):
            key = (
                row["platform"],
                row["python_version"],
                row["rf_version"],
                row["node_version"],
            )
            tally = counts.setdefault(key, [0, 0])
            tally[0] += 1
            tally[1] += row["broke"]
        grouped[(owner, scope)] = sorted(
            (
                CoverageRow(
                    platform=configuration[0],
                    python_version=configuration[1],
                    rf_version=configuration[2],
                    node_version=configuration[3],
                    ran=ran,
                    failed=failed,
                )
                for configuration, (ran, failed) in counts.items()
            ),
            key=lambda entry: (-entry.failed, -entry.ran),
        )
    return grouped


def fixture_runs_either_side(db: Reading) -> dict[FixtureLegKey, Around]:
    """`runs_either_side` for suite fixtures, keyed by the leg it broke in.

    The same question and the same answer, with one difference in what counts as
    an outcome: a fixture has no status of its own in `test_result`, so the leg
    passed if the suite ran there and the fixture is not among the failures.
    """
    outcomes: dict[FixtureLegKey, Around] = {}
    for fixture in _failing_fixtures(db):
        owner = fixture["scope_owner"]
        scope = fixture["failure_scope"]
        rows = _fixture_legs(db, owner, scope)
        lanes: dict[str, dict] = {}
        for row in rows:
            lane = lanes.setdefault(row["artifact_name"], {})
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
            run["statuses"].append(("FAIL" if row["broke"] else "PASS", None))
            run["legs"].add(row["leg_id"])

        def seen(run: dict) -> AdjacentRun:
            return AdjacentRun(
                run=run["run"],
                commit=run["commit"],
                at=run["at"],
                outcome=_verdict(run["statuses"]),
            )

        for row in rows:
            if not row["broke"]:
                continue
            lane = lanes[row["artifact_name"]]
            order = sorted(lane)
            here = order.index((row["created_at"], row["run_id"]))
            mine = lane[order[here]]
            retry = None
            if len(mine["legs"]) > 1:
                retry = Retry(
                    attempts=len(mine["legs"]),
                    passed_on_another_attempt=any(
                        status == "PASS" for status, _ in mine["statuses"]
                    ),
                )
            outcomes[FixtureLegKey(owner, scope, row["leg_id"])] = Around(
                previous_run_on_this_leg=(
                    seen(lane[order[here - 1]]) if here else None
                ),
                next_run_on_this_leg=(
                    seen(lane[order[here + 1]]) if here + 1 < len(order) else None
                ),
                retry=retry,
            )
    return outcomes


def fixture_co_failures(db: Reading) -> dict[FixtureLegKey, list[CoFailure]]:
    """What else broke in a leg the fixture broke in.

    The tests this fixture marked are excluded. They are the same event already
    counted once, and listing them here would restate the fixture's own damage
    as if it were context.
    """
    rows = db.execute(
        """
        SELECT a.scope_owner, a.failure_scope, a.leg_id, b.longname,
               IFNULL(b.failure_scope, 'test') AS scope
        FROM (SELECT DISTINCT subject_owner AS scope_owner,
                             subject_scope  AS failure_scope, leg_id
                FROM fixture_failure WHERE subject_owner IS NOT NULL) a
        JOIN test_result b ON b.leg_id = a.leg_id AND b.status = 'FAIL'
        WHERE NOT (IFNULL(b.failure_scope, 'test') = a.failure_scope
                   AND IFNULL(b.scope_owner, '') = a.scope_owner)
        GROUP BY a.scope_owner, a.failure_scope, a.leg_id, b.longname
        ORDER BY a.leg_id, b.longname
        """
    ).fetchall()
    grouped: dict[FixtureLegKey, list[CoFailure]] = {}
    for row in rows:
        key = FixtureLegKey(row["scope_owner"], row["failure_scope"], row["leg_id"])
        grouped.setdefault(key, []).append(
            CoFailure(subject=row["longname"], scope=row["scope"])
        )
    return grouped


def messages_by_fixture(db: Reading) -> dict[SubjectKey, list[MessageRow]]:
    """`messages_by_test` for suite fixtures. Robot Framework writes the
    fixture's message onto every test it marked, so counting rows would report
    one teardown failure as ten; the Occurrence is the Leg."""
    return _messages(db, "fixture_failure")


def first_attempt_counts_by_test(db: Reading) -> tuple[dict[str, int], dict]:
    """How often a test ran and failed on runs nobody had to re-run.

    A leg is only ever re-run because it failed, so re-attempts land exactly
    where the failures are and the ordinary denominator is inflated where it
    hurts. Which legs got re-run is not a fact about the test either: it follows
    queue time and where the run sat in the day's merges. Counting only first
    attempts asks the one question that has a clean answer - how often does a
    run nobody touched come back red.

    Counting only the last attempt would be the other obvious choice and is
    wrong: the last attempt is the one that passed, so the failure disappears.

    A leg whose first attempt was cancelled before it uploaded anything is in
    neither count. There is no result to count, and inventing one either way
    would be worse than the gap.

    Returns runs by test and failures by (test, signature), separately, so that
    a group whose every failure landed on a re-attempt still gets a denominator
    instead of vanishing.
    """
    runs = {
        row["longname"]: row["ran"]
        for row in db.execute(
            """
            SELECT f.longname, COUNT(*) AS ran
            FROM test_result f
            JOIN leg l ON l.id = f.leg_id
            WHERE l.attempt = 1
            GROUP BY f.longname
            """
        )
    }
    failures = {
        (row["subject_owner"], row["subject_scope"], row["signature_key"]): row[
            "failures"
        ]
        for row in db.execute(
            """
            SELECT f.subject_owner, f.subject_scope, f.signature_key,
                   COUNT(*) AS failures
            FROM test_failure f
            JOIN leg l ON l.id = f.leg_id
            WHERE l.attempt = 1
            GROUP BY f.subject_owner, f.subject_scope, f.signature_key
            """
        )
    }
    return runs, failures


def first_attempt_counts_by_fixture(db: Reading) -> tuple[dict[tuple, int], dict]:
    """`first_attempt_counts_by_test` for suite fixtures, counted in legs."""
    runs: dict[tuple, int] = {}
    for fixture in _failing_fixtures(db):
        identity = (fixture["scope_owner"], fixture["failure_scope"])
        runs[identity] = sum(
            1 for row in _fixture_legs(db, *identity) if row["attempt"] == 1
        )
    failures = {
        (row["subject_owner"], row["subject_scope"], row["signature_key"]): row["legs"]
        for row in db.execute(
            """
            SELECT f.subject_owner, f.subject_scope, f.signature_key,
                   COUNT(DISTINCT l.id) AS legs
            FROM fixture_failure f
            JOIN leg l ON l.id = f.leg_id
            WHERE l.attempt = 1
            GROUP BY f.subject_owner, f.subject_scope, f.signature_key
            """
        )
    }
    return runs, failures


def latest_run(db: Reading) -> LatestRun | None:
    """The newest run in the window, and how many failures it carried.

    The rates answer "how often does this break". They do not answer "is it
    broken now", which is the question a merge is judged on, and a window whose
    newest run is clean is a different situation from one whose newest run is
    not - however bad the rates in between.
    """
    row = db.execute(
        "SELECT id, created_at, event, head_sha FROM run "
        "ORDER BY created_at DESC, id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return None
    failures = db.execute(
        """
        SELECT COUNT(*) FROM test_result f
        JOIN leg l ON l.id = f.leg_id
        WHERE l.run_id = ? AND f.status = 'FAIL'
        """,
        (row["id"],),
    ).fetchone()[0]
    return LatestRun(
        run=row["id"],
        commit=row["head_sha"],
        event=row["event"],
        at=row["created_at"],
        failures=failures,
    )


def _messages(db: Reading, view: str) -> dict[SubjectKey, list[MessageRow]]:
    """Every distinct raw message behind a Subject's group, with how often each
    occurred.

    Counted in Occurrences rather than rows, which is one expression for both
    scopes: a test's Occurrence is its own row, and a suite fixture's is the Leg,
    so `COUNT(DISTINCT occurrence_id)` is `COUNT(*)` on one side and a count of
    Legs on the other without saying so twice.
    """
    rows = db.execute(
        f"""
        SELECT f.subject_owner, f.subject_scope, f.signature_key,
               f.message, COUNT(DISTINCT f.occurrence_id) AS occurrences
        FROM {view} f
        WHERE f.message IS NOT NULL
        GROUP BY f.subject_owner, f.subject_scope, f.signature_key, f.message
        ORDER BY occurrences DESC
        """
    ).fetchall()
    grouped: dict[SubjectKey, list[MessageRow]] = {}
    for row in rows:
        grouped.setdefault(_subject_key(row), []).append(
            MessageRow(message=row["message"], occurrences=row["occurrences"])
        )
    return grouped


def messages_by_test(db: Reading) -> dict[SubjectKey, list[MessageRow]]:
    """The signature masks what varies, which is what makes grouping possible
    and is also what throws away the evidence. Three failures of Compare Images
    carry an identical box and a pixel count differing by three - deterministic,
    not jittery - and the signature renders all of that as `<n>`."""
    return _messages(db, "test_failure")


def _variants(db: Reading, view: str) -> dict[SubjectKey, list[VariantRow]]:
    """Parameterised on the view, like `_messages`, which is its twin.

    It used to take the SQL itself and how many leading columns made the key -
    always three, and always one of two formattings of the same template. The
    key was then built by position, so "the first three columns are the key"
    was written down nowhere but in the query text.
    """
    rows = db.execute(_VARIANT_SQL.format(view=view)).fetchall()
    grouped: dict[SubjectKey, list[VariantRow]] = {}
    for row in rows:
        grouped.setdefault(_subject_key(row), []).append(
            VariantRow(
                signature=row["error_signature"],
                occurrences=row["occurrences"],
            )
        )
    # Only the groups the case-folded key actually merged. One spelling is the
    # normal case and saying so on every entry would bury the one that matters.
    return {key: value for key, value in grouped.items() if len(value) > 1}


_VARIANT_SQL = """
    SELECT f.subject_owner, f.subject_scope, f.signature_key,
           f.error_signature, COUNT(DISTINCT f.occurrence_id) AS occurrences
    FROM {view} f
    WHERE f.error_signature IS NOT NULL
    GROUP BY f.subject_owner, f.subject_scope, f.signature_key, f.error_signature
    ORDER BY occurrences DESC
"""


def signature_variants(db: Reading) -> dict[SubjectKey, list[VariantRow]]:
    """The distinct spellings of one test group's signature, with counts.

    Only ever more than one when two libraries name the same condition, which is
    exactly the case the case-folded key exists to merge. See `_KEY`.
    """
    return _variants(db, "test_failure")


def fixture_signature_variants(db: Reading) -> dict[SubjectKey, list[VariantRow]]:
    """`signature_variants` for suite fixtures, counted in Legs."""
    return _variants(db, "fixture_failure")


def log_messages_by_result(db: Reading) -> dict[int, list[LogRow]]:
    """The same lines, for every failure at once, keyed on the occurrence.

    One query rather than one per occurrence, because every occurrence needs its
    own. Reporting a single occurrence's lines against a group that has several
    is not a saving, it is a wrong answer that looks like a right one: the four
    `Screenshot On Failure` failures in one window split two and two across two
    different image comparisons, and the group showed only the newer pair.
    """
    rows = db.execute(
        "SELECT test_result_id, seq, level, keyword, origin, message "
        "FROM log_message ORDER BY test_result_id, seq"
    ).fetchall()
    grouped: dict[int, list[LogRow]] = {}
    for row in rows:
        grouped.setdefault(row["test_result_id"], []).append(
            LogRow(
                level=row["level"],
                keyword=row["keyword"],
                origin=row["origin"] or None,
                message=row["message"],
            )
        )
    return grouped


def platform_breakdown(db: Reading) -> list[PlatformRow]:
    """Failures per matrix leg, by platform.

    Per leg rather than absolute, because the matrix does not run the platforms
    an equal number of times and the raw counts would say more about the matrix
    than about the platforms.
    """
    rows = db.execute(
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
    return [
        PlatformRow(
            platform=row["platform"],
            legs=row["legs"],
            failures=row["failures"] or 0,
            per_leg=(row["failures"] or 0) / row["legs"] if row["legs"] else 0.0,
        )
        for row in rows
    ]


def totals(db: Reading) -> Totals:
    row = db.execute(
        "SELECT (SELECT COUNT(*) FROM run) AS runs, "
        "(SELECT COUNT(*) FROM leg) AS legs, "
        "(SELECT COUNT(*) FROM test_result) AS results, "
        "(SELECT COUNT(*) FROM test_result WHERE status='FAIL') AS failures, "
        "(SELECT COUNT(DISTINCT longname) FROM test_result) AS tests, "
        "(SELECT COUNT(*) FROM leg WHERE attempt IS NULL) AS legs_without_attempt, "
        "(SELECT MIN(created_at) FROM run) AS since, "
        "(SELECT MAX(created_at) FROM run) AS until"
    ).fetchone()
    return Totals(**dict(row))
