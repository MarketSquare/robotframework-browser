"""The same report, shaped for a reader that cannot click.

`html_report` renders for someone who will scan a page and follow a link.
This renders for a language model, which changes what has to be in it rather
than only how it looks:

- Nothing is truncated. The terminal report cuts messages at 110 characters
  because a terminal is narrow. There is no such constraint here.
- Every distinct raw message is carried, not one example. The signature masks
  what varies between runs, which is exactly the evidence: an identical box and
  a pixel count differing by three says deterministic, and `<n>` does not.
- Rates are per configuration and carry their denominator. 3 of 81 is not a
  fact worth having; 3 of 55 on linux against 0 of 26 on darwin is.
- Configurations that never ran the test are named, because absent and clean
  are opposite findings that a zero cannot tell apart.
- The commit of every occurrence is included, so four failures across four
  commits can be told from four across one.
- The rules that decide what a row means - the suite fixture split of section 3
  above all - are stated in the document instead of being left to be rederived
  from the shape of the data, or not rederived.

See `0012_flaky_test_analysis.md`.
"""

import json
from pathlib import Path

from .report import (
    co_failures,
    coverage_by_fixture,
    coverage_by_test,
    failure_groups,
    first_attempt_counts_by_fixture,
    first_attempt_counts_by_test,
    fixture_co_failures,
    fixture_failures,
    fixture_signature_variants,
    latest_run,
    log_messages,
    messages_by_fixture,
    messages_by_test,
    neighbouring_fixture_outcomes,
    neighbouring_outcomes,
    occurrences_by_fixture,
    occurrences_by_test,
    pass_durations_by_test,
    platform_breakdown,
    signature_variants,
    totals,
)

# A leg with more failures than this in it is itself the finding, and listing
# them all on every one of them would bury the entry. Truncation is reported
# rather than done quietly: a list that stops without saying so reads as a
# complete one.
CO_FAILURE_LIMIT = 25

# Stated rather than implied. Every one of these is a rule a reader would
# otherwise have to infer from the data, and each has already been got wrong
# once by someone reading the database directly.
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
    "latest_run": (
        "'window.latest_run' is the newest run in the window and how many "
        "failures it carried. The rates say how often things break, not whether "
        "the head is green, and a merge is judged on the second question."
    ),
}


def _split(value: str | None) -> list[str]:
    return [part for part in (value or "").split(",") if part]


def _where_to_look(row) -> dict:
    keyword = getattr(row, "failing_keyword", None) or getattr(row, "keyword", None)
    defined = None
    if row.keyword_source:
        defined = row.keyword_source
        if row.keyword_lineno:
            defined = f"{defined}:{row.keyword_lineno}"
    test = row.test_source
    lineno = getattr(row, "test_lineno", None)
    if test and lineno:
        test = f"{test}:{lineno}"
    return {
        "test_file": test,
        "keyword": keyword,
        "keyword_defined": defined,
        "keyword_owner": row.keyword_owner,
        "keyword_kind": row.keyword_kind,
    }


def _rates(
    coverage: list[dict],
    known_platforms: set[str],
    durations: dict[tuple, dict] | None,
    longname: str,
) -> tuple[list, list]:
    """Per configuration, how often it ran and how often it broke.

    `durations` is None for a suite fixture, which has no duration of its own in
    the database - only the tests it marked have one. The key is then left out
    rather than carried as null: a field that is null on every row of a whole
    section reads as a measurement that was attempted and failed.
    """
    rates = []
    for entry in coverage:
        rate = {
            "platform": entry["platform"],
            "python": entry["python_version"],
            "rf": entry["rf_version"],
            "node": entry["node_version"] or None,
            "ran": entry["ran"],
            "failed": entry["failed"] or 0,
        }
        if durations is not None:
            rate["pass_ms"] = durations.get(
                (
                    longname,
                    entry["platform"],
                    entry["python_version"],
                    entry["rf_version"],
                    entry["node_version"],
                )
            )
        rates.append(rate)
    seen = {entry["platform"] for entry in coverage if entry["platform"]}
    return rates, sorted(known_platforms - seen)


def _occurrences(
    entries: list[dict], neighbours: dict[int, dict], others: dict[int, list[dict]]
) -> list[dict]:
    """One failure, with what surrounded it.

    The counts describe a group. These describe a single execution: which leg
    ran it, what that leg did either side of this run, whether anyone re-ran it,
    and what else broke alongside it.
    """
    occurrences = []
    for entry in entries:
        around = neighbours.get(entry["result_id"], {})
        alongside = others.get(entry["result_id"], [])
        occurrence = {
            "run": entry["run_id"],
            "run_url": entry["run_url"],
            "commit": entry["head_sha"],
            "event": entry["event"],
            "at": entry["created_at"],
            "platform": entry["platform"],
            "python": entry["python_version"],
            "rf": entry["rf_version"],
            "node": entry["node_version"] or None,
            "leg": entry["artifact_name"],
            "attempt": entry["attempt"],
            "artifact_url": entry["artifact_url"],
            "elapsed_ms": entry["elapsed_ms"],
            "previous_run_on_this_leg": around.get("previous_run_on_this_leg"),
            "next_run_on_this_leg": around.get("next_run_on_this_leg"),
            "retry": around.get("retry"),
            "also_failed_in_this_leg": alongside[:CO_FAILURE_LIMIT],
        }
        if len(alongside) > CO_FAILURE_LIMIT:
            occurrence["also_failed_in_this_leg_not_listed"] = (
                len(alongside) - CO_FAILURE_LIMIT
            )
        occurrences.append(occurrence)
    return occurrences


def _first_attempt(failures: int, ran: int) -> dict:
    """The rate over legs nobody had to re-run."""
    return {
        "failures": failures,
        "ran": ran,
        "rate": round(failures / ran, 4) if ran else 0.0,
    }


def _fixture_occurrences(
    entries: list[dict],
    identity: tuple,
    neighbours: dict[tuple, dict],
    others: dict[tuple, list[dict]],
) -> list[dict]:
    """One leg the fixture broke in, with what surrounded it.

    Same shape as a test occurrence, minus `elapsed_ms`: a suite fixture has no
    duration of its own in the database, only the tests it marked have one.
    """
    occurrences = []
    for entry in entries:
        leg = (*identity, entry["leg_id"])
        around = neighbours.get(leg, {})
        alongside = others.get(leg, [])
        occurrence = {
            "run": entry["run_id"],
            "run_url": entry["run_url"],
            "commit": entry["head_sha"],
            "event": entry["event"],
            "at": entry["created_at"],
            "platform": entry["platform"],
            "python": entry["python_version"],
            "rf": entry["rf_version"],
            "node": entry["node_version"] or None,
            "leg": entry["artifact_name"],
            "attempt": entry["attempt"],
            "artifact_url": entry["artifact_url"],
            "tests_marked": entry["tests_marked"],
            "previous_run_on_this_leg": around.get("previous_run_on_this_leg"),
            "next_run_on_this_leg": around.get("next_run_on_this_leg"),
            "retry": around.get("retry"),
            "also_failed_in_this_leg": alongside[:CO_FAILURE_LIMIT],
        }
        if len(alongside) > CO_FAILURE_LIMIT:
            occurrence["also_failed_in_this_leg_not_listed"] = (
                len(alongside) - CO_FAILURE_LIMIT
            )
        occurrences.append(occurrence)
    return occurrences


def _log(db_path: Path, result_id: int | None) -> list[dict]:
    """Every line, at every level.

    Not filtered down to FAIL and WARN: the traceback that names the file and
    line is logged at DEBUG, and the whole database holds 182 log lines against
    32 failures, so there is nothing to save by dropping any of them.
    """
    return [
        {
            "level": line["level"],
            "keyword": line["keyword"],
            "origin": line["origin"] or None,
            "message": line["message"],
        }
        for line in log_messages(db_path, result_id)
    ]


def build(db_path: Path, limit: int = 100) -> dict:
    """The whole report as one plain-data document."""
    summary = totals(db_path)
    platforms = {row["platform"] for row in platform_breakdown(db_path)}
    coverage = coverage_by_test(db_path)
    occurrences = occurrences_by_test(db_path)
    messages = messages_by_test(db_path)
    variants = signature_variants(db_path)
    fixture_variants = fixture_signature_variants(db_path)
    durations = pass_durations_by_test(db_path)
    neighbours = neighbouring_outcomes(db_path)
    alongside = co_failures(db_path)
    first_runs, first_failures = first_attempt_counts_by_test(db_path)

    tests = []
    for group in failure_groups(db_path, limit=limit):
        key = (group.longname, group.signature_key)
        rates, never = _rates(
            coverage.get(group.longname, []), platforms, durations, group.longname
        )
        entry = {
            "test": group.longname,
            "scope": "test",
            "where_to_look": _where_to_look(group),
            "signature": group.error_signature,
            "raw_messages": messages.get(key, []),
            "counts": {
                "failures": group.failures,
                "ran": group.total_runs,
                "rate": round(group.failure_rate, 4),
                "distinct_commits": group.distinct_shas,
                "first_attempt": _first_attempt(
                    first_failures.get(key, 0), first_runs.get(group.longname, 0)
                ),
            },
            "rates": rates,
            "never_ran_on": never,
            "first_seen": group.first_seen,
            "last_seen": group.last_seen,
            "screenshots": _split(group.screenshots),
            "screenshot_status": group.screenshot_status,
            "occurrences": _occurrences(
                occurrences.get(key, []), neighbours, alongside
            ),
            "log": _log(db_path, group.latest_result_id),
        }
        if key in variants:
            entry["signature_variants"] = variants[key]
        tests.append(entry)

    fixture_coverage = coverage_by_fixture(db_path)
    fixture_occurrences = occurrences_by_fixture(db_path)
    fixture_messages = messages_by_fixture(db_path)
    fixture_neighbours = neighbouring_fixture_outcomes(db_path)
    fixture_alongside = fixture_co_failures(db_path)
    first_fixture_runs, first_fixture_failures = first_attempt_counts_by_fixture(
        db_path
    )

    fixtures = []
    for fixture in fixture_failures(db_path, limit=limit):
        key = (fixture.scope_owner, fixture.failure_scope, fixture.signature_key)
        identity = (fixture.scope_owner, fixture.failure_scope)
        rates, never = _rates(
            fixture_coverage.get(identity, []), platforms, None, fixture.scope_owner
        )
        fixtures.append(
            {
                "suite": fixture.scope_owner,
                "scope": fixture.failure_scope,
                "where_to_look": _where_to_look(fixture),
                "signature": fixture.error_signature,
                "raw_messages": fixture_messages.get(key, []),
                "counts": {
                    "failures": fixture.occurrences,
                    "suite_runs": fixture.suite_runs,
                    "rate": round(fixture.failure_rate, 4),
                    "distinct_commits": fixture.distinct_shas,
                    "test_rows_marked_failed": fixture.tests_marked,
                    "first_attempt": _first_attempt(
                        first_fixture_failures.get(key, 0),
                        first_fixture_runs.get(identity, 0),
                    ),
                },
                "affected_tests": _split(fixture.affected_tests),
                "rates": rates,
                "never_ran_on": never,
                "first_seen": fixture.first_seen,
                "last_seen": fixture.last_seen,
                "screenshots": _split(fixture.screenshots),
                "screenshot_status": fixture.screenshot_status,
                "occurrences": _fixture_occurrences(
                    fixture_occurrences.get(key, []),
                    identity,
                    fixture_neighbours,
                    fixture_alongside,
                ),
                "log": _log(db_path, fixture.latest_result_id),
            }
        )
        if key in fixture_variants:
            fixtures[-1]["signature_variants"] = fixture_variants[key]

    return {
        "about": ABOUT,
        "window": {
            "runs": summary["runs"],
            "legs": summary["legs"],
            "results": summary["results"],
            "failures": summary["failures"],
            "distinct_tests": summary["tests"],
            "legs_with_unknown_attempt": summary["legs_without_attempt"],
            "since": summary["since"],
            "until": summary["until"],
            "latest_run": latest_run(db_path),
        },
        "fixture_failures": fixtures,
        "test_failures": tests,
    }


def render(db_path: Path, destination: Path, limit: int = 100) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(build(db_path, limit=limit), indent=2) + "\n", encoding="utf-8"
    )
    return destination
