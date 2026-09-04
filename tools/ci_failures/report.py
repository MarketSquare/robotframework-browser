"""The Report: everything one run of the tool says about a Window.

Built once, out of `queries.py`, and complete. `render_html` and `render_json`
are Renderings over it. A Rendering may show less than the Report holds; it never
reaches past the Report to the queries for something the Report does not carry,
because that is exactly how the page and the document grew apart the first time.

Typed rather than a plain dict for the same reason. The defect this replaced was
silent divergence - two independent assemblies, each having quietly gained and
lost fields the other had, with nothing anywhere that could notice. A dict makes
a Rendering ignoring a field invisible; a type makes it something you can see.
See `docs/adr/0001-report-is-typed-not-a-dict.md`.

The judgements live here rather than in `queries.py`: what a clean configuration
means when the sample is small, and which screenshot is the evidence. Neither is
a question SQL can answer.
"""

import math
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from . import reading
from .annotations import compare, known_cause_for, load_known_causes, read_snapshot
from .parse import screenshot_key
from .queries import (
    NOTHING_AROUND,
    AdjacentRun,
    Around,
    CoverageRow,
    FixtureLegKey,
    LogRow,
    MessageRow,
    OccurrenceRow,
    # Re-exported deliberately. `outcome` is a Report field, so a Rendering
    # reads the vocabulary for it here rather than reaching into `queries`.
    # It is produced there because `_verdict` is, and `_verdict` is there
    # because it is called from inside a lane walk; `queries.py`'s own docstring
    # now says so rather than claiming no such function exists.
    Outcome,  # noqa: F401
    Spread,
    SubjectKey,
    VariantRow,
    archive_begins,
    co_failures,
    coverage_by_fixture,
    coverage_by_test,
    failure_groups,
    first_attempt_counts_by_fixture,
    first_attempt_counts_by_test,
    fixture_co_failures,
    fixture_failures,
    fixture_runs_either_side,
    fixture_signature_variants,
    latest_run,
    log_messages_by_result,
    messages_by_fixture,
    messages_by_test,
    occurrences_by_fixture,
    occurrences_by_test,
    pass_durations_by_test,
    platform_breakdown,
    runs_either_side,
    signature_variants,
    totals,
)
from .queries import (
    CoFailure as CoFailureRow,
)
from .queries import (
    Retry as QueryRetry,
)
from .window import ALL_HISTORY, Window

# A leg with more failures than this in it is itself the finding, and listing
# them all on every one of them would bury the entry. A cap on what the Report
# holds rather than on what a Rendering shows: past twenty-five names the list
# has stopped being the hint it exists to be. Truncation is reported rather than
# done quietly - a list that stops without saying so reads as a complete one.
CO_FAILURE_LIMIT = 25

# How likely a genuinely-as-bad-as-everywhere-else configuration has to be to
# have shown nothing yet before its zero stops being worth reading. At 0.05 a
# zero is reported plainly; above it, the zero is marked as what it is.
INCONCLUSIVE_ABOVE = 0.05

ABOUT = {
    "grain": (
        "One entry per (test, error). The same test failing on two different "
        "errors is two entries, because they are two problems."
    ),
    "suite_fixtures_are_separate": (
        "A failed suite setup or teardown fails every test beneath it, and Robot "
        "Framework records that only on the tests. Those rows are in "
        "'fixture_failures', counted once per fixture against how many times the "
        "suite ran, and are excluded from 'test_failures'. Counting them as test "
        "failures makes one broken teardown outrank everything else."
    ),
    "denominators": (
        "'ran' counts every execution including passes. A failure count without "
        "a run count is not a rate."
    ),
    "signature_vs_message": (
        "'signature' is the message with the varying parts masked, and is what "
        "entries are grouped on, case-insensitively. 'raw_messages' holds what "
        "was actually reported. Read the signature to know what kind of failure "
        "this is; read the raw messages to diagnose it."
    ),
    "keyword_kind": (
        "Where the failing keyword comes from, and so who to suspect: 'library' "
        "is the Browser library under test, 'project' a test helper in this "
        "repository, 'standard' a Robot Framework library and therefore an "
        "assertion, 'unknown' a failure above any keyword such as a test timeout."
    ),
    "keyword_locations": (
        "Resolved from the working copy at ingest time, not from the commit the "
        "run used. 'commit' on each occurrence is there for when that matters."
    ),
    "short_window": (
        "'window.short' is present only when a windowed report asked for more "
        "days than the database holds, and says how many of them were never "
        "ingested. Null means the archive covers the question - absent, not "
        "zero - and an all-history report is never short of anything. Where it "
        "is present, every count and rate below covers the days that are "
        "there, so a low failure count is not evidence of a quiet fortnight."
    ),
    "artifacts": (
        "Screenshots, traces and playwright-log.txt are not in this document. "
        "Each occurrence carries the artifact URL they can be downloaded from."
    ),
    "neighbouring_runs": (
        "Each occurrence carries what the same test did on the same matrix leg "
        "in the run before it and the run after it. A rate says how often a "
        "test fails; these say whether this failure was a blip on a leg that is "
        "otherwise healthy, or the point where something broke and stayed "
        "broken. They span commits, so a real regression that the next commit "
        "fixed also has passing neighbours - 'retry' is what tells those apart."
    ),
    "retries": (
        "Nothing in this CI retries automatically, so a leg that ran more than "
        "once in one run was re-run by hand. Where 'retry' is present the test "
        "failed and then passed on one commit minutes apart, which is the "
        "strongest evidence of a flake this data holds. Where it is absent "
        "nobody pressed the button, and that is a fact about queue time and "
        "about where the run sat in the day's merges, never about the failure: "
        "absence means nothing."
    ),
    "denominators_and_attempts": (
        "'ran' and 'rate' count every attempt, re-runs included. A leg is only "
        "re-run because it failed, so those extra runs land exactly where the "
        "failures are and pull the rate down. 'first_attempt' counts only legs "
        "nobody had to re-run, which answers the question with a clean answer: "
        "how often does a run nobody touched come back red. Counting only the "
        "last attempt would be the other obvious choice and is wrong - the last "
        "attempt is the one that passed, so the failure disappears. A leg whose "
        "first attempt was cancelled before uploading is in neither count. "
        "'window.legs_with_unknown_attempt' is how many legs could not be "
        "placed at all; while it is above zero, read 'first_attempt' as a floor."
    ),
    "pass_durations": (
        "'pass_ms' on each configuration is how long the test takes on the runs "
        "where it passes. For a timeout, whether those cluster far below the "
        "limit or run up against it is the difference between a keyword that "
        "broke and a budget that was always too thin."
    ),
    "co_failures": (
        "'also_failed_in_this_leg' names the other tests that failed in the "
        "same execution. It claims no causation. It is here because a test can "
        "fail on a variable that an earlier suite never got to set, and read "
        "alone that entry looks like an unrelated assertion failure in a file "
        "where nothing is wrong. On a fixture entry the tests that fixture "
        "marked are left out: they are its own damage, already counted once."
    ),
    "fixture_occurrences": (
        "A fixture occurrence is one leg, never one marked test row. Five "
        "teardown failures of one suite produced ten failed tests, and listing "
        "ten would put back the double count the fixture split exists to "
        "remove. What each leg lost is 'tests_marked' on that occurrence. For "
        "the same reason 'ran' on a fixture rate counts legs that ran the "
        "suite, and the occurrence count of a raw message counts legs too."
    ),
    "failures_per_leg": (
        "'platforms' counts failures per matrix leg, not in total. The matrix does "
        "not run the platforms an equal number of times, so a raw count describes "
        "the matrix rather than the platforms."
    ),
    "latest_run": (
        "'window.latest_run' is the newest run in the window and how many "
        "failures it carried. The rates say how often things break, not whether "
        "the head is green, and a merge is judged on the second question."
    ),
    "known_cause": (
        "Where an entry carries 'known_cause', somebody has already worked this "
        "one out and written down what they found; 'reference' says where. It "
        "is recorded by hand in tools/ci_failures/known_causes.json rather than "
        "in the database, because the database is derived and gets rebuilt "
        "whenever a parsing rule changes, and a conclusion nobody can re-derive "
        "must not be stored somewhere that deletes it. Its absence means "
        "nothing has been recorded, never that the cause is unknown. "
        "'fixed_by' names the change that should have fixed it and "
        "'fix_verified' the date CI confirmed it - while 'fixed_by' is set and "
        "'fix_verified' is null, the fix is merged but not yet proven."
    ),
    "since_last_report": (
        "What changed against the last snapshot somebody took, and null when "
        "nobody has taken one - which is a different thing from nothing having "
        "changed. The snapshot moves only when `inv ci-report --mark-seen` is "
        "run, never as a side effect of rendering, so running the report twice "
        "on unchanged data answers the same both times."
    ),
    "log_lines": (
        "Log lines and screenshots hang off each occurrence, not off the group. "
        "The occurrences of one group do not have to agree: four failures of "
        "one test on one masked signature were two different image comparisons "
        "breaking, and a single set of lines shown against the group said so "
        "for only half of them. An 'origin' of 'caught by ...' marks a line "
        "from a failure that something swallowed - a `Run Keyword And Expect "
        "Error` or a TRY/EXCEPT - which is evidence about what a keyword did "
        "and is never itself the failure that stopped the test. 'screenshots' "
        "is ordered, most likely to be the evidence first: the files the "
        "failing keyword itself named, then the one the library took because "
        "the test failed, then anything named only by a caught failure."
    ),
    "small_samples": (
        "A configuration with no failures carries 'zero_is_inconclusive' when a "
        "configuration exactly as broken as the rest would plausibly show "
        "nothing over that many runs. 'would_look_clean_anyway' is how often it "
        "would, and 'runs_for_a_meaningful_zero' how many runs it would take "
        "for the zero to be worth reading. Without it a rare failure looks "
        "platform specific on every platform that has not caught it yet."
    ),
    "executors": (
        "'executors' is how many test executions ran at once on that leg and "
        "'node_process' whether they shared one node process. A failure where "
        "one worker's state reaches another's exists only when there is another "
        "worker, so it looks platform specific when the platforms differ only "
        "in how many CPUs the runner has. Null for legs ingested from before "
        "this was recorded."
    ),
}


@dataclass(frozen=True)
class PassMs:
    """How long the test takes on the runs where it passes, per configuration.

    Four numbers because the shape carries the argument: a cliff between the
    passes and the failures is a keyword that broke, a tail reaching up into
    them is a margin that ran out.
    """

    min: int
    median: int
    p95: int
    max: int


@dataclass(frozen=True)
class InconclusiveZero:
    """What a configuration that has failed nothing yet is worth."""

    would_look_clean_anyway: float
    runs_for_a_meaningful_zero: int


@dataclass(frozen=True)
class Rate:
    """One configuration, how often it ran it and how often it broke."""

    platform: str | None
    python: str | None
    rf: str | None
    node: str | None
    ran: int
    failed: int
    zero_is_inconclusive: InconclusiveZero | None = None
    # None means measured and nothing to measure; a Fixture Failure has no
    # duration of its own at all, and its Renderings leave the field out rather
    # than carrying a null on every row of a whole section.
    pass_ms: PassMs | None = None


@dataclass(frozen=True)
class Neighbour:
    """What the same Leg did in the Run either side of this one."""

    run: int
    commit: str | None
    at: str | None
    #: One of `Outcome`. A Rendering that wants to know which of them mean
    #: trouble asks `Outcome.BAD` rather than writing the list out again.
    outcome: str


@dataclass(frozen=True)
class Retry:
    """A Leg someone re-ran by hand. Nothing in this CI retries on its own."""

    attempts: int
    passed_on_another_attempt: bool


@dataclass(frozen=True)
class CoFailure:
    """Another Subject that broke in the same Leg. No causation is claimed.

    A Subject, not a test: a broken suite fixture appears once, naming the suite,
    rather than once for each of the tests it marked.
    """

    subject: str
    scope: str | None


@dataclass(frozen=True)
class LogLine:
    level: str | None
    keyword: str | None
    origin: str | None
    message: str | None


@dataclass(frozen=True)
class Occurrence:
    """One individual failure, and what surrounded it.

    The counts describe a Group. These describe one execution: which Leg ran it,
    which Attempt that was, what that Leg did either side, and what else broke
    alongside. Evidence hangs here and never on the Group - the Occurrences of
    one Group do not have to agree, and a Group cannot say so.
    """

    run: int
    run_url: str | None
    commit: str | None
    event: str | None
    at: str | None
    platform: str | None
    python: str | None
    rf: str | None
    node: str | None
    leg: str | None
    attempt: int | None
    executors: int | None
    node_process: str | None
    artifact_url: str | None
    # A test Occurrence has one, a Fixture Failure's has the other.
    elapsed_ms: int | None = None
    tests_marked: int | None = None
    previous_run_on_this_leg: Neighbour | None = None
    next_run_on_this_leg: Neighbour | None = None
    retry: Retry | None = None
    also_failed_in_this_leg: tuple[CoFailure, ...] = ()
    also_failed_in_this_leg_not_listed: int = 0
    log: tuple[LogLine, ...] = ()
    screenshots: tuple[str, ...] = ()
    screenshot_status: str | None = None


@dataclass(frozen=True)
class FirstAttempt:
    """The rate over Legs nobody had to re-run."""

    failures: int
    ran: int
    # Exact. Rounding is a Rendering's decision.
    rate: float


@dataclass(frozen=True)
class TestCounts:
    failures: int
    ran: int
    rate: float
    distinct_commits: int
    first_attempt: FirstAttempt


@dataclass(frozen=True)
class FixtureCounts:
    """`suite_runs`, never `ran`.

    The denominator is Legs that ran the suite, never test rows, and the
    different name is the guard that stops it being read as a test rate.
    """

    failures: int
    suite_runs: int
    rate: float
    distinct_commits: int
    test_rows_marked_failed: int
    first_attempt: FirstAttempt


@dataclass(frozen=True)
class WhereToLook:
    """Where in this repository to start, without grepping for it."""

    test_file: str | None
    keyword: str | None
    keyword_defined: str | None
    keyword_owner: str | None
    keyword_kind: str | None


@dataclass(frozen=True)
class KnownCause:
    """A conclusion somebody already reached. Absence means nothing is written
    down, never that the cause is unknown."""

    cause: str | None
    reference: str | None
    recorded: str | None
    fixed_by: str | None
    fix_verified: str | None


@dataclass(frozen=True)
class RawMessage:
    """One distinct unmasked message. The mask is what makes grouping possible
    and also what throws the evidence away."""

    message: str | None
    occurrences: int


@dataclass(frozen=True)
class SignatureVariant:
    """One spelling behind a case-folded Group. Two libraries spell the same
    gRPC deadline differently, and which one fired is real information."""

    signature: str | None
    occurrences: int


@dataclass(frozen=True)
class TestEntry:
    """One Group: a test and the error it failed with."""

    test: str
    where_to_look: WhereToLook
    signature: str | None
    raw_messages: tuple[RawMessage, ...]
    counts: TestCounts
    rates: tuple[Rate, ...]
    never_ran_on: tuple[str, ...]
    occurrences: tuple[Occurrence, ...]
    known_cause: KnownCause | None = None
    signature_variants: tuple[SignatureVariant, ...] = ()
    scope: str = "test"


@dataclass(frozen=True)
class FixtureEntry:
    """One Fixture Failure: a suite setup or teardown and the error it broke on,
    counted once per Leg rather than once per test it marked."""

    suite: str
    scope: str
    where_to_look: WhereToLook
    signature: str | None
    raw_messages: tuple[RawMessage, ...]
    counts: FixtureCounts
    affected_tests: tuple[str, ...]
    rates: tuple[Rate, ...]
    never_ran_on: tuple[str, ...]
    occurrences: tuple[Occurrence, ...]
    known_cause: KnownCause | None = None
    signature_variants: tuple[SignatureVariant, ...] = ()


@dataclass(frozen=True)
class PlatformRow:
    """Failures per matrix Leg. Per leg, not in total: the matrix does not run
    the platforms an equal number of times."""

    platform: str | None
    legs: int
    failures: int
    per_leg: float


@dataclass(frozen=True)
class LatestRun:
    """The newest Run and its failure count. The rates say how often things
    break; a merge is judged on whether the head is green."""

    run: int
    commit: str | None
    event: str | None
    at: str | None
    failures: int


@dataclass(frozen=True)
class ShortWindow:
    """The Window asked for more days than the archive holds.

    A Window can only restrict what has been ingested, so `--days 60` over a
    sixteen-day database answers over sixteen. Both numbers were already in the
    report - the label said what was asked for and `since` said what was there -
    and nothing put them next to each other, so the reader had to notice the
    disagreement to know there was one.

    Not an error. The answer is the best one available and worth having; it just
    has to say what it is answering over. Dates are local calendar days, spelled
    as the Window spells them, because that is the unit the question was asked
    in.
    """

    asked_from: str
    holds_from: str
    missing_days: int


@dataclass(frozen=True)
class WindowSummary:
    """What the Report covers, and how much of it there was."""

    runs: int
    legs: int
    results: int
    failures: int
    distinct_tests: int
    legs_with_unknown_attempt: int
    since: str | None
    until: str | None
    latest_run: LatestRun | None
    label: str
    bounded: bool
    # None whenever the archive covers the question, which is the ordinary case
    # and has to stay silent: a note on every report is one nobody reads by the
    # third one.
    short: ShortWindow | None


@dataclass(frozen=True)
class Report:
    """Everything one run of the tool says about a Window."""

    about: dict
    window: WindowSummary
    # annotations.compare's own shape, passed through. None when nobody has
    # taken a Snapshot - and also under a Window, where an all-history baseline
    # would call every Group shrunken for the same reason a windowed baseline
    # would call every Group grown.
    since_last_report: dict | None
    fixture_failures: tuple[FixtureEntry, ...]
    test_failures: tuple[TestEntry, ...]
    platforms: tuple[PlatformRow, ...]


def zero_is_inconclusive(ran: int, overall_rate: float) -> InconclusiveZero | None:
    """Whether a configuration's clean sheet is evidence or just a small sample.

    A rate of zero and an absence of evidence render identically, and on a rare
    failure they are usually the same thing. `Screenshot On Failure` fails about
    one run in twenty; darwin ran it 25 times and passed every time, which a
    configuration exactly as broken as linux would manage more than half the
    time. Reported next to the zero, because the reader's next move - "it is
    linux-only, look at something linux does" - is only sound if the zero means
    something.
    """
    if ran <= 0 or overall_rate <= 0:
        return None
    would_look_clean = (1 - overall_rate) ** ran
    if would_look_clean <= INCONCLUSIVE_ABOVE:
        return None
    needed = math.ceil(math.log(INCONCLUSIVE_ABOVE) / math.log(1 - overall_rate))
    return InconclusiveZero(round(would_look_clean, 2), needed)


def rank_screenshots(paths: list[str], log: list[LogLine]) -> tuple[str, ...]:
    """Most likely to be the evidence first.

    A failing test leaves more pictures than anyone will open. The ones the
    failing keyword itself named are the evidence - `Compare Images` says which
    two files it compared and then fails on them - so they lead. Next comes the
    one the library took because the test failed, then anything named by a
    failure that was caught and thrown away, then the rest.

    Deliberately not done at ingest: it depends only on rows already in the
    database, and computing it during parsing would freeze it into stored data
    that only a full re-download can change. Deliberately not done in a
    Rendering either - it is the same question with the same answer for both,
    and two implementations are two chances to show the reader a different
    picture.
    """

    def named_in(lines: list[LogLine]) -> set[str]:
        return {
            screenshot_key(word.strip("'\",;:()[]<>"))
            for line in lines
            for word in (line.message or "").replace("\\", "/").split()
        }

    failing = named_in([line for line in log if not line.origin])
    caught = named_in([line for line in log if line.origin])
    return tuple(
        sorted(
            paths,
            key=lambda path: (
                screenshot_key(path) not in failing,
                "fail-screenshot" not in path,
                screenshot_key(path) not in caught,
                path,
            ),
        )
    )


def _split(value: str | None) -> tuple[str, ...]:
    return tuple(part for part in (value or "").split(",") if part)


def _where_to_look(row, test_lineno: int | None) -> WhereToLook:
    defined = None
    if row.keyword_source:
        defined = row.keyword_source
        if row.keyword_lineno:
            defined = f"{defined}:{row.keyword_lineno}"
    test = row.test_source
    if test and test_lineno:
        test = f"{test}:{test_lineno}"
    return WhereToLook(
        test_file=test,
        keyword=row.failing_keyword,
        keyword_defined=defined,
        keyword_owner=row.keyword_owner,
        keyword_kind=row.keyword_kind,
    )


def _pass_ms(measured: Spread | None) -> PassMs | None:
    if not measured:
        return None
    return PassMs(measured.min, measured.median, measured.p95, measured.max)


def _rates(
    coverage: list[CoverageRow],
    known_platforms: set,
    durations: dict[tuple, Spread] | None,
    longname: str,
    overall_rate: float = 0.0,
) -> tuple[tuple[Rate, ...], tuple[str, ...]]:
    """Per configuration, how often it ran and how often it broke.

    Configurations that never failed are kept: 3 of 81 says nothing, and 3 of 55
    on linux against 0 of 26 on darwin says where to look. A configuration
    missing from the list never ran this at all, which is the opposite finding to
    a zero, so it comes back separately.

    `durations` is None for a Fixture Failure, which has no duration of its own -
    only the tests it marked have one.
    """
    rates = []
    for entry in coverage:
        failed = entry.failed or 0
        ran = entry.ran
        measured = None
        if durations is not None:
            measured = durations.get(
                (
                    longname,
                    entry.platform,
                    entry.python_version,
                    entry.rf_version,
                    entry.node_version,
                )
            )
        rates.append(
            Rate(
                platform=entry.platform,
                python=entry.python_version,
                rf=entry.rf_version,
                node=entry.node_version or None,
                ran=ran,
                failed=failed,
                zero_is_inconclusive=(
                    None if failed else zero_is_inconclusive(ran, overall_rate)
                ),
                pass_ms=_pass_ms(measured),
            )
        )
    seen = {entry.platform for entry in coverage if entry.platform}
    return tuple(rates), tuple(sorted(known_platforms - seen))


def _neighbour(entry: AdjacentRun | None) -> Neighbour | None:
    if not entry:
        return None
    return Neighbour(entry.run, entry.commit, entry.at, entry.outcome)


def _retry(entry: QueryRetry | None) -> Retry | None:
    if not entry:
        return None
    return Retry(entry.attempts, entry.passed_on_another_attempt)


def _log_lines(rows: list[LogRow]) -> tuple[LogLine, ...]:
    return tuple(
        LogLine(row.level, row.keyword, row.origin, row.message) for row in rows
    )


# The upload step names every artifact "Test results-<leg>". The prefix is a
# fact about the upload rather than about the Leg, and leaving it on meant the
# page stripped it while the document did not - one Leg reading as two strings.
# Stripped once, here, so both Renderings say the same thing.
_ARTIFACT_PREFIX = "Test results-"


def _leg_name(artifact_name: str | None) -> str | None:
    if not artifact_name:
        return None
    return artifact_name.removeprefix(_ARTIFACT_PREFIX)


def _occurrence(
    entry: OccurrenceRow,
    around: Around,
    alongside: list[CoFailureRow],
    logs: dict[int, list[LogRow]],
    *,
    elapsed_ms: int | None = None,
    tests_marked: int | None = None,
) -> Occurrence:
    lines = _log_lines(logs.get(entry.result_id, []))
    kept = alongside[:CO_FAILURE_LIMIT]
    return Occurrence(
        run=entry.run_id,
        run_url=entry.run_url,
        commit=entry.head_sha,
        event=entry.event,
        at=entry.created_at,
        platform=entry.platform,
        python=entry.python_version,
        rf=entry.rf_version,
        node=entry.node_version or None,
        leg=_leg_name(entry.artifact_name),
        attempt=entry.attempt,
        executors=entry.executors,
        node_process=entry.node_process,
        artifact_url=entry.artifact_url,
        elapsed_ms=elapsed_ms,
        tests_marked=tests_marked,
        previous_run_on_this_leg=_neighbour(around.previous_run_on_this_leg),
        next_run_on_this_leg=_neighbour(around.next_run_on_this_leg),
        retry=_retry(around.retry),
        also_failed_in_this_leg=tuple(
            CoFailure(item.subject, item.scope) for item in kept
        ),
        also_failed_in_this_leg_not_listed=max(0, len(alongside) - CO_FAILURE_LIMIT),
        log=lines,
        screenshots=rank_screenshots(list(_split(entry.screenshots)), list(lines)),
        screenshot_status=entry.screenshot_status,
    )


def _occurrences(
    entries: list[OccurrenceRow],
    neighbours: dict[int, Around],
    others: dict[int, list[CoFailureRow]],
    logs: dict[int, list[LogRow]],
) -> tuple[Occurrence, ...]:
    return tuple(
        _occurrence(
            entry,
            neighbours.get(entry.result_id, NOTHING_AROUND),
            others.get(entry.result_id, []),
            logs,
            elapsed_ms=entry.elapsed_ms,
        )
        for entry in entries
    )


def _fixture_occurrences(
    entries: list[OccurrenceRow],
    identity: tuple[str, str],
    neighbours: dict[FixtureLegKey, Around],
    others: dict[FixtureLegKey, list[CoFailureRow]],
    logs: dict[int, list[LogRow]],
) -> tuple[Occurrence, ...]:
    """One Leg the fixture broke in. `tests_marked` is what that Leg lost, a fact
    about the Leg rather than a multiplier on the count."""
    return tuple(
        _occurrence(
            entry,
            neighbours.get(FixtureLegKey(*identity, entry.leg_id or 0), NOTHING_AROUND),
            others.get(FixtureLegKey(*identity, entry.leg_id or 0), []),
            logs,
            tests_marked=entry.tests_marked,
        )
        for entry in entries
    )


def _first_attempt(failures: int, ran: int) -> FirstAttempt:
    return FirstAttempt(failures, ran, failures / ran if ran else 0.0)


def _known_cause(known: dict, subject: str, signature: str | None) -> KnownCause | None:
    cause = known_cause_for(known, subject, signature)
    if not cause:
        return None
    return KnownCause(
        cause["cause"],
        cause["reference"],
        cause["recorded"],
        cause["fixed_by"],
        cause["fix_verified"],
    )


def _messages(rows: list[MessageRow]) -> tuple[RawMessage, ...]:
    return tuple(RawMessage(row.message, row.occurrences) for row in rows)


def _variants(rows: list[VariantRow]) -> tuple[SignatureVariant, ...]:
    return tuple(SignatureVariant(row.signature, row.occurrences) for row in rows)


def _archive_begins(db_path: Path) -> str | None:
    """How far back the database reaches, read past the Window.

    Unwindowed on purpose, for the reason `_nothing_ran` is: the Window is
    exactly what hides this. Opened only for a bounded Window, and only for one
    `MIN(created_at)` - an all-history report cannot be short of anything.
    """
    with reading.of(db_path) as everything:
        return archive_begins(everything)


def _short_window(window: Window, begins: str | None) -> ShortWindow | None:
    """How much of what `--days` asked for the archive actually holds.

    `begins` is the oldest Run in the *database*, in UTC; the Window's own
    bounds are local calendar days. Converting the one to the other here rather
    than comparing the UTC cutoff directly is what keeps the answer in the unit
    the question was asked in - a run at half past eleven at night belongs to
    the local day the reader would call it, which is the same rule `of_days`
    uses.

    Read from the archive rather than from the Window's own `since`, which is
    the oldest run *inside* the window and cannot see past it. A window whose
    first day merely had no CI runs - one delayed nightly schedule run on a day
    nobody merged - would otherwise be reported as history that was never
    ingested, and a note that cries wolf is worth less than no note at all.
    """
    if not window.bounded or window.first_day is None or not begins:
        return None
    holds_from = (
        datetime.strptime(begins, "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone.utc)
        .astimezone()
        .date()
    )
    if holds_from <= window.first_day:
        return None
    return ShortWindow(
        asked_from=str(window.first_day),
        holds_from=str(holds_from),
        missing_days=(holds_from - window.first_day).days,
    )


def snapshot_entries(report: Report) -> list[tuple[str, str | None, int]]:
    """What a Snapshot records, read off the Report rather than rebuilt.

    Rebuilding it from the queries is how a third construction of this shape
    came to exist, and a Snapshot that disagreed with the Report it was taken
    beside would make the next comparison wrong rather than merely stale.

    Refuses a windowed Report, here rather than in whatever invoked it: a
    baseline covering less data than the report that reads it makes every Group
    come back grown, and that is silent - the numbers are all plausible.
    """
    if report.window.bounded:
        raise WindowedBaselineError(
            f"A baseline cannot be taken from {report.window.label}: it covers "
            "less than the report that will read it, so every group would come "
            "back grown. Take the baseline without --days."
        )
    return [
        (entry.test, entry.signature, entry.counts.failures)
        for entry in report.test_failures
    ] + [
        (entry.suite, entry.signature, entry.counts.failures)
        for entry in report.fixture_failures
    ]


class UnanswerableError(Exception):
    """The question cannot be answered, and this says why.

    These are the conditions a caller has to have handled to use `build`
    correctly. They lived in the invoke task, which meant they were the caller's
    to remember, were checked nowhere else, and could only be exercised by
    typing `inv`.
    """


class NoDatabaseError(UnanswerableError):
    """Nothing has been ingested here yet."""


class NothingInWindowError(UnanswerableError):
    """The Window holds no Runs, so there is no report to render.

    An empty page cannot say whether nothing ran or nothing failed, and those
    are opposite findings. Refusing is the only answer that does not mislead.
    """


class WindowedBaselineError(UnanswerableError):
    """A Snapshot was asked for from a windowed Report. See `snapshot_entries`."""


def _nothing_ran(db_path: Path, window: Window) -> str:
    """Why the Window is empty, said in terms of what has been ingested.

    Read unwindowed on purpose: the useful fact is how far the archive reaches,
    which is exactly what the Window is hiding.
    """
    with reading.of(db_path) as everything:
        newest = latest_run(everything)
    seen = (
        f"newest ingested run {newest.at[:10]}"
        if newest and newest.at
        else "nothing ingested yet"
    )
    return f"No runs in {window.label} - {seen}. Run `inv ci-ingest`, or widen --days."


def build(
    db_path: Path,
    limit: int = 100,
    window: Window = ALL_HISTORY,
    known_causes: Path | None = None,
) -> Report:
    """The whole Report for one Window, or why there is not one.

    One Reading, opened here and shared by every query below. They used to open
    one each, which meant materialising the Window once per question.

    Raises `UnanswerableError` rather than returning something empty. The database is
    checked before it is opened, because opening it would create it and an
    absent archive would render as a clean one.
    """
    if not db_path.exists():
        raise NoDatabaseError(f"No database at {db_path}. Run `inv ci-ingest` first.")
    with reading.of(db_path, window) as db:
        if window.bounded and not totals(db).runs:
            raise NothingInWindowError(_nothing_ran(db_path, window))
        return _build(db, limit, window, db_path, known_causes)


def _build(
    db: reading.Reading,
    limit: int,
    window: Window,
    db_path: Path,
    known_causes: Path | None = None,
) -> Report:
    summary = totals(db)
    platform_rows = platform_breakdown(db)
    platforms = {row.platform for row in platform_rows}
    coverage = coverage_by_test(db)
    occurrences = occurrences_by_test(db)
    messages = messages_by_test(db)
    variants = signature_variants(db)
    fixture_variants = fixture_signature_variants(db)
    durations = pass_durations_by_test(db)
    neighbours = runs_either_side(db)
    alongside = co_failures(db)
    first_runs, first_failures = first_attempt_counts_by_test(db)
    logs = log_messages_by_result(db)
    known = load_known_causes(known_causes)

    tests = []
    for group in failure_groups(db, limit=limit):
        # One key shape for every Subject, test or fixture:
        # (owner, scope, signature).
        key = SubjectKey(group.longname, "test", group.signature_key)
        rates, never = _rates(
            coverage.get(group.longname, []),
            platforms,
            durations,
            group.longname,
            group.failure_rate,
        )
        tests.append(
            TestEntry(
                test=group.longname,
                where_to_look=_where_to_look(group, group.test_lineno),
                signature=group.error_signature,
                raw_messages=_messages(messages.get(key, [])),
                counts=TestCounts(
                    failures=group.failures,
                    ran=group.total_runs,
                    rate=group.failure_rate,
                    distinct_commits=group.distinct_shas,
                    first_attempt=_first_attempt(
                        first_failures.get(key, 0), first_runs.get(group.longname, 0)
                    ),
                ),
                rates=rates,
                never_ran_on=never,
                # No Group-level log or screenshots. Both used to be one
                # Occurrence's, unlabelled, and the Occurrences of a Group do
                # not have to agree: they are on the Occurrences now.
                occurrences=_occurrences(
                    occurrences.get(key, []), neighbours, alongside, logs
                ),
                known_cause=_known_cause(known, group.longname, group.error_signature),
                signature_variants=_variants(variants.get(key, [])),
            )
        )

    fixture_coverage = coverage_by_fixture(db)
    fixture_occurrences = occurrences_by_fixture(db)
    fixture_messages = messages_by_fixture(db)
    fixture_neighbours = fixture_runs_either_side(db)
    fixture_alongside = fixture_co_failures(db)
    first_fixture_runs, first_fixture_failures = first_attempt_counts_by_fixture(db)

    fixtures = []
    for fixture in fixture_failures(db, limit=limit):
        identity = (fixture.scope_owner, fixture.failure_scope)
        key = SubjectKey(*identity, fixture.signature_key)
        rates, never = _rates(
            fixture_coverage.get(identity, []),
            platforms,
            None,
            fixture.scope_owner,
            fixture.failure_rate,
        )
        fixtures.append(
            FixtureEntry(
                suite=fixture.scope_owner,
                scope=fixture.failure_scope,
                where_to_look=_where_to_look(fixture, None),
                signature=fixture.error_signature,
                raw_messages=_messages(fixture_messages.get(key, [])),
                counts=FixtureCounts(
                    failures=fixture.occurrences,
                    suite_runs=fixture.suite_runs,
                    rate=fixture.failure_rate,
                    distinct_commits=fixture.distinct_shas,
                    test_rows_marked_failed=fixture.tests_marked,
                    first_attempt=_first_attempt(
                        first_fixture_failures.get(key, 0),
                        first_fixture_runs.get(identity, 0),
                    ),
                ),
                affected_tests=_split(fixture.affected_tests),
                rates=rates,
                never_ran_on=never,
                occurrences=_fixture_occurrences(
                    fixture_occurrences.get(key, []),
                    identity,
                    fixture_neighbours,
                    fixture_alongside,
                    logs,
                ),
                known_cause=_known_cause(
                    known, fixture.scope_owner, fixture.error_signature
                ),
                signature_variants=_variants(fixture_variants.get(key, [])),
            )
        )

    newest = latest_run(db)
    report = Report(
        about=ABOUT,
        window=WindowSummary(
            runs=summary.runs,
            legs=summary.legs,
            results=summary.results,
            failures=summary.failures,
            distinct_tests=summary.tests,
            legs_with_unknown_attempt=summary.legs_without_attempt,
            since=summary.since,
            until=summary.until,
            latest_run=(
                LatestRun(
                    newest.run,
                    newest.commit,
                    newest.event,
                    newest.at,
                    newest.failures,
                )
                if newest
                else None
            ),
            label=window.label,
            bounded=window.bounded,
            short=_short_window(window, _archive_begins(db_path)),
        ),
        # A windowed Report has no comparable baseline. A Snapshot is never
        # taken from one, so the only baseline available covers more data, and
        # comparing against it would call every Group shrunken.
        since_last_report=None,
        fixture_failures=tuple(fixtures),
        test_failures=tuple(tests),
        platforms=tuple(
            PlatformRow(row.platform, row.legs, row.failures, row.per_leg)
            for row in platform_rows
        ),
    )
    if window.bounded:
        return report
    return replace(
        report,
        since_last_report=compare(read_snapshot(db_path), snapshot_entries(report)),
    )
