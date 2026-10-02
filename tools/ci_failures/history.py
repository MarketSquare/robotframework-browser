"""A **Subject History**: what the archive recorded about one test or one suite.

What triaging one test and verifying one fix both read: a test's Results and
the Runs it ran in, its Occurrences, the Fixture Failures of its Enclosing
Suites, and the Legs of one Run that ran it, with the Controls among them.

A Test Name runs from the top suite down, and the name typed is often less of
it: the test's own name, or the path without `Test.`. It is resolved against
the names where it is looked for - the archive, one Run, one Leg's output.xml -
and a name starting at another top suite is the same test spelled another way,
as a Leg that ran several suite directories at once spells all of its tests.
Anything looser is offered, never assumed: every name ending in what was typed,
all of them, since about one in six test names is shared by tests in different
suites and offering one would be a guess. Only when none ends in it is it taken
for a typo and matched by similarity.

The Legs of a Run are read from the database and never from GitHub, which could
not say where the test passed; see ADR 0006.

Imports nothing that builds a Report, so the artifact fetch can resolve a name
without it.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from difflib import get_close_matches
from itertools import groupby
from pathlib import Path

from . import reading
from .legs import leg_name
from .queries import SUITE_BROKE, verdict
from .reading import Reading, UnanswerableError
from .window import ALL_HISTORY, Window

MOST_SUGGESTIONS = 5
CANONICAL_TOP_SUITE = "Test"


class NoSuchTestError(UnanswerableError):
    """No Result where the name was looked for has this Test Name."""

    def __init__(self, test: str, where: str, suggestions: tuple[str, ...]):
        self.suggestions = suggestions
        message = f"No test named {test!r} in {where}."
        if suggestions:
            message += " Did you mean:" + "".join(f"\n  {s}" for s in suggestions)
        super().__init__(message)


class NotIngestedError(UnanswerableError):
    """The database holds no Run with this id."""

    def __init__(self, run: int):
        super().__init__(f"Run {run} is not in the database; `inv ci-ingest` first.")


class NotInWindowError(UnanswerableError):
    """The test is in the archive and has no Result inside the Window."""


def _top(name: str) -> str:
    return name.partition(".")[0]


def _below_top(name: str) -> str:
    return name.partition(".")[2]


def resolve(test: str, names: Iterable[str], where: str) -> str:
    """The name in `names` that `test` is. Raises `NoSuchTestError` with the
    names it may mean when there is none, or more than one."""
    known = sorted(set(names))
    if test in known:
        return test
    same: list[str] = []
    if _top(test) in {CANONICAL_TOP_SUITE, *map(_top, known)}:
        same = [name for name in known if _below_top(name) == _below_top(test)]
        if len(same) == 1:
            return same[0]
    raise NoSuchTestError(test, where, tuple(same) or _close_to(test, known))


def encloses(suite: str, test: str) -> bool:
    """Whether `suite` is an Enclosing Suite of `test`. `runs_of_subject` asks
    the same in SQL."""
    return test.startswith(f"{suite}.")


def _close_to(name: str, names: list[str]) -> tuple[str, ...]:
    ending = [known for known in names if known.endswith(f".{name}")]
    if ending:
        return tuple(ending)
    return tuple(get_close_matches(name, names, n=MOST_SUGGESTIONS))


# --- What the archive recorded ------------------------------------------


@dataclass(frozen=True)
class SubjectRun:
    """A Run in which a Subject ran, whatever it did there."""

    run_id: int
    head_sha: str | None
    created_at: str | None
    run_url: str | None


@dataclass(frozen=True)
class SubjectFailure:
    """How often a Subject failed in one Run on one Error Signature."""

    run_id: int
    head_sha: str | None
    run_url: str | None
    signature_key: str
    error_signature: str | None
    occurrences: int


def runs_of_subject(db: Reading, subject: str) -> list[SubjectRun]:
    """Every Run a test ran in, or a suite ran in - the suites it encloses
    included, which is where a suite fixture's failures land. The SQL spelling
    of `encloses`."""
    rows = db.execute(
        """
        SELECT DISTINCT r.id AS run_id, r.head_sha, r.created_at, r.url AS run_url
        FROM test_result t
        JOIN leg l ON l.id = t.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE t.longname = ?1 OR t.suite_longname = ?1
              OR substr(t.suite_longname, 1, length(?1) + 1) = ?1 || '.'
        ORDER BY r.created_at, r.id
        """,
        (subject,),
    ).fetchall()
    return [SubjectRun(**dict(row)) for row in rows]


def failures_of_subject(db: Reading, subject: str) -> list[SubjectFailure]:
    """A Subject's Occurrences per Run and signature, on any signature."""
    rows = db.execute(
        """
        SELECT r.id AS run_id, r.head_sha, r.url AS run_url, f.signature_key,
               MIN(f.error_signature) AS error_signature,
               COUNT(DISTINCT f.occurrence_id) AS occurrences
        FROM (
            SELECT leg_id, subject_owner, signature_key, error_signature,
                   occurrence_id FROM test_failure
            UNION ALL
            SELECT leg_id, subject_owner, signature_key, error_signature,
                   occurrence_id FROM fixture_failure
        ) f
        JOIN leg l ON l.id = f.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE f.subject_owner = ?
        GROUP BY r.id, f.signature_key
        ORDER BY r.created_at, r.id
        """,
        (subject,),
    ).fetchall()
    return [SubjectFailure(**dict(row)) for row in rows]


@dataclass(frozen=True)
class TestOutcomes:
    """How a test's Results came out, however many Groups it has."""

    ran: int
    failed: int
    skipped: int
    last_ran: str | None


def _outcomes_of_test(db: Reading, test: str) -> TestOutcomes:
    """Every Result of one Test Name, Groups or none."""
    row = db.execute(
        """
        SELECT COUNT(*) AS ran,
               COALESCE(SUM(t.status = 'FAIL'), 0) AS failed,
               COALESCE(SUM(t.status = 'SKIP'), 0) AS skipped,
               MAX(r.created_at) AS last_ran
        FROM test_result t
        JOIN leg l ON l.id = t.leg_id
        JOIN run r ON r.id = l.run_id
        WHERE t.longname = ?
        """,
        (test,),
    ).fetchone()
    return TestOutcomes(**dict(row))


def test_names(db: Reading) -> list[str]:
    """Every Test Name with a Result in the Reading."""
    return [row[0] for row in db.execute("SELECT DISTINCT longname FROM test_result")]


@dataclass(frozen=True)
class IngestedRun:
    """A Run the database holds, and its commit."""

    run: int
    commit: str | None


def _ingested_run(db: Reading, run: int) -> IngestedRun | None:
    """The Run, or None when the database does not hold it."""
    row = db.execute("SELECT head_sha FROM run WHERE id = ?", (run,)).fetchone()
    return IngestedRun(run, row["head_sha"]) if row else None


def _test_names_of_run(db: Reading, run: int) -> list[str]:
    """Every Test Name with a Result in one Run."""
    return [
        row[0]
        for row in db.execute(
            "SELECT DISTINCT t.longname FROM test_result t "
            "JOIN leg l ON l.id = t.leg_id WHERE l.run_id = ?",
            (run,),
        )
    ]


@dataclass(frozen=True)
class RunLeg:
    """One Leg of a Run that ran a test, and what the test did there."""

    artifact_name: str
    install: str | None
    attempt: int | None
    outcome: str


def _legs_of_run(db: Reading, run: int, test: str) -> list[RunLeg]:
    """The Legs of one Run that ran this test, each with the test's outcome.

    The Legs a **Control** is chosen from. A Leg of another shard has no Result
    for the test and is not here, which is the point: those are most of a Run.
    """
    rows = db.execute(
        """
        SELECT l.id AS leg_id, l.artifact_name, l.install, l.attempt,
               t.status, t.failure_scope
        FROM test_result t
        JOIN leg l ON l.id = t.leg_id
        WHERE l.run_id = ? AND t.longname = ?
        ORDER BY l.id
        """,
        (run, test),
    ).fetchall()
    legs: dict[int, dict] = {}
    for row in rows:
        leg = legs.setdefault(row["leg_id"], {"row": row, "statuses": []})
        leg["statuses"].append((row["status"], row["failure_scope"]))
    return [
        RunLeg(
            artifact_name=leg["row"]["artifact_name"],
            install=leg["row"]["install"],
            attempt=leg["row"]["attempt"],
            outcome=verdict(leg["statuses"]),
        )
        for leg in legs.values()
    ]


# --- A test with no Group --------------------------------------------------


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" + ("" if count == 1 else "s")


@dataclass(frozen=True)
class NeverFailed:
    """A test that ran inside the Window and has no Group there."""

    test: str
    window: str
    ran: int
    failed: int
    skipped: int

    def line(self) -> str:
        return (
            f"{self.test!r} ran {_plural(self.ran, 'time')} in {self.window}: "
            f"{_plural(self.failed, 'failure')}, {_plural(self.skipped, 'skip')}."
        )


def in_archive(db_path: Path, test: str) -> str:
    """The Test Name `test` is in the archive. Raises `NoSuchTestError`."""
    with reading.of(db_path) as everything:
        return resolve(test, test_names(everything), "the archive")


def never_failed(db_path: Path, test: str, window: Window = ALL_HISTORY) -> NeverFailed:
    """What there is to say about a test `of_test` found no Groups for.

    Raises rather than answering when the name is in no Result at all, or in
    none inside the Window, since either would otherwise read as a healthy test.
    """
    test = in_archive(db_path, test)
    with reading.of(db_path) as everything:
        last_ran = _outcomes_of_test(everything, test).last_ran
    with reading.of(db_path, window) as db:
        outcomes = _outcomes_of_test(db, test)
    if not outcomes.ran:
        raise NotInWindowError(
            f"{test!r} did not run in {window.label}; it last ran on "
            f"{(last_ran or '')[:10]}. Widen --days."
        )
    return NeverFailed(
        test=test,
        window=window.label,
        ran=outcomes.ran,
        failed=outcomes.failed,
        skipped=outcomes.skipped,
    )


# --- The Legs of a Run, for choosing a Control ---------------------------


# Failures first: they are what the Controls are compared against.
_ORDER = ("fail", "mixed", SUITE_BROKE, "skip", "pass")


def _label(outcome: str) -> str:
    return "control" if outcome == "pass" else outcome


def _attempt(leg: RunLeg) -> str:
    return "?" if leg.attempt is None else str(leg.attempt)


@dataclass(frozen=True)
class RunListing:
    """Every Leg of one Run that ran one test, by Install, Controls marked."""

    run: int
    commit: str | None
    test: str
    legs: tuple[RunLeg, ...]

    def lines(self) -> list[str]:
        ordered = sorted(
            self.legs,
            key=lambda leg: (
                leg.install or "",
                _ORDER.index(leg.outcome),
                leg_name(leg.artifact_name),
                leg.attempt or 0,
            ),
        )
        label_width = max(len(_label(leg.outcome)) for leg in ordered)
        name_width = max(len(leg_name(leg.artifact_name)) for leg in ordered)
        lines = [f"Run {self.run} · commit {(self.commit or '?')[:7]} · {self.test}"]
        for install, legs in groupby(ordered, key=lambda leg: leg.install):
            lines.append(install or "(install unknown)")
            lines.extend(
                f"  {_label(leg.outcome):<{label_width}}  "
                f"{leg_name(leg.artifact_name):<{name_width}}   "
                f"--attempt {_attempt(leg)}"
                for leg in legs
            )
        lines.append(
            f'fetch one: inv ci-artifact --run {self.run} --leg "<leg>" '
            f'--attempt <n> --test "{self.test}"'
        )
        if any(leg.attempt is None for leg in ordered):
            lines.append(
                "attempt ? is not yet resolved: try --attempt 1, or "
                "`inv ci-backfill-attempts` first."
            )
        return lines


def of_run(db_path: Path, run: int, test: str) -> RunListing:
    """The Legs of `run` that ran `test`. Raises `NotIngestedError` for a Run
    the database lacks, and `NoSuchTestError` for a test the Run lacks."""
    with reading.of(db_path) as db:
        found = _ingested_run(db, run)
        if found is None:
            raise NotIngestedError(run)
        test = resolve(test, _test_names_of_run(db, run), f"Run {run}")
        legs = _legs_of_run(db, run, test)
    return RunListing(run, found.commit, test, tuple(legs))
