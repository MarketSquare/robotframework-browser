"""The Report as one plain-data document, for a reader that cannot click.

A Rendering, like `render_html`: it formats what `report.build` produced and
never asks the database anything of its own. What it shapes for is a language
model rather than a person, which changes what has to be in it:

- Nothing is truncated. A page hides the fifth occurrence behind a line saying
  so; there is no reason to here.
- Every distinct raw message is carried, not one example. The Error Signature
  masks what varies between runs, which is exactly the evidence: an identical
  box and a pixel count differing by three says deterministic, and `<n>` does
  not.
- The rules that decide what a row means - the suite fixture split above all -
  are stated in `about` rather than left to be rederived from the shape of the
  data, or not rederived.

See `0012_flaky_test_analysis.md`.
"""

import json
from pathlib import Path

from .report import (
    FixtureEntry,
    KnownCause,
    LogLine,
    Neighbour,
    Occurrence,
    Rate,
    Report,
    Retry,
    TestEntry,
)


def _neighbour(neighbour: Neighbour | None) -> dict | None:
    if neighbour is None:
        return None
    return {
        "run": neighbour.run,
        "commit": neighbour.commit,
        "at": neighbour.at,
        "outcome": neighbour.outcome,
    }


def _retry(retry: Retry | None) -> dict | None:
    if retry is None:
        return None
    return {
        "attempts": retry.attempts,
        "passed_on_another_attempt": retry.passed_on_another_attempt,
    }


def _log(lines: tuple[LogLine, ...]) -> list[dict]:
    return [
        {
            "level": line.level,
            "keyword": line.keyword,
            "origin": line.origin,
            "message": line.message,
        }
        for line in lines
    ]


def _rate(rate: Rate, *, measurable: bool) -> dict:
    """`measurable` is False for a Fixture Failure, which has no duration of its
    own. The key is left out rather than carried as null: a field that is null on
    every row of a whole section reads as a measurement that was attempted."""
    entry = {
        "platform": rate.platform,
        "python": rate.python,
        "rf": rate.rf,
        "node": rate.node,
        "ran": rate.ran,
        "failed": rate.failed,
    }
    if rate.zero_is_inconclusive:
        entry["zero_is_inconclusive"] = {
            "would_look_clean_anyway": rate.zero_is_inconclusive.would_look_clean_anyway,
            "runs_for_a_meaningful_zero": rate.zero_is_inconclusive.runs_for_a_meaningful_zero,
        }
    if measurable:
        measured = rate.pass_ms
        entry["pass_ms"] = (
            None
            if measured is None
            else {
                "min": measured.min,
                "median": measured.median,
                "p95": measured.p95,
                "max": measured.max,
            }
        )
    return entry


def _occurrence(occurrence: Occurrence, *, fixture: bool) -> dict:
    entry = {
        "run": occurrence.run,
        "run_url": occurrence.run_url,
        "commit": occurrence.commit,
        "event": occurrence.event,
        "at": occurrence.at,
        "platform": occurrence.platform,
        "python": occurrence.python,
        "rf": occurrence.rf,
        "node": occurrence.node,
        "leg": occurrence.leg,
        "attempt": occurrence.attempt,
        "executors": occurrence.executors,
        "node_process": occurrence.node_process,
        "artifact_url": occurrence.artifact_url,
    }
    if fixture:
        entry["tests_marked"] = occurrence.tests_marked
    else:
        entry["elapsed_ms"] = occurrence.elapsed_ms
    entry["previous_run_on_this_leg"] = _neighbour(occurrence.previous_run_on_this_leg)
    entry["next_run_on_this_leg"] = _neighbour(occurrence.next_run_on_this_leg)
    entry["retry"] = _retry(occurrence.retry)
    entry["also_failed_in_this_leg"] = [
        {"subject": item.subject, "scope": item.scope}
        for item in occurrence.also_failed_in_this_leg
    ]
    if occurrence.also_failed_in_this_leg_not_listed:
        entry["also_failed_in_this_leg_not_listed"] = (
            occurrence.also_failed_in_this_leg_not_listed
        )
    # Each Occurrence's own lines and its own screenshots. Two failures of one
    # test on one masked signature are routinely two different keywords failing
    # on two different files, and a Group cannot say so.
    entry["log"] = _log(occurrence.log)
    entry["screenshots"] = list(occurrence.screenshots)
    entry["screenshot_status"] = occurrence.screenshot_status
    return entry


def _cause(cause: KnownCause | None) -> dict:
    return {
        "cause": cause.cause,
        "reference": cause.reference,
        "recorded": cause.recorded,
        "fixed_by": cause.fixed_by,
        "fix_verified": cause.fix_verified,
    }


def _test(entry: TestEntry) -> dict:
    out = {
        "test": entry.test,
        "scope": entry.scope,
        "where_to_look": {
            "test_file": entry.where_to_look.test_file,
            "keyword": entry.where_to_look.keyword,
            "keyword_defined": entry.where_to_look.keyword_defined,
            "keyword_owner": entry.where_to_look.keyword_owner,
            "keyword_kind": entry.where_to_look.keyword_kind,
        },
        "signature": entry.signature,
        "raw_messages": [
            {"message": m.message, "occurrences": m.occurrences}
            for m in entry.raw_messages
        ],
        "counts": {
            "failures": entry.counts.failures,
            "ran": entry.counts.ran,
            "rate": round(entry.counts.rate, 4),
            "distinct_commits": entry.counts.distinct_commits,
            "first_attempt": {
                "failures": entry.counts.first_attempt.failures,
                "ran": entry.counts.first_attempt.ran,
                "rate": round(entry.counts.first_attempt.rate, 4),
            },
        },
        "rates": [_rate(r, measurable=True) for r in entry.rates],
        "never_ran_on": list(entry.never_ran_on),
        "occurrences": [_occurrence(o, fixture=False) for o in entry.occurrences],
    }
    if entry.known_cause:
        out["known_cause"] = _cause(entry.known_cause)
    if entry.signature_variants:
        out["signature_variants"] = [
            {"signature": v.signature, "occurrences": v.occurrences}
            for v in entry.signature_variants
        ]
    return out


def _fixture(entry: FixtureEntry) -> dict:
    out = {
        "suite": entry.suite,
        "scope": entry.scope,
        "where_to_look": {
            "test_file": entry.where_to_look.test_file,
            "keyword": entry.where_to_look.keyword,
            "keyword_defined": entry.where_to_look.keyword_defined,
            "keyword_owner": entry.where_to_look.keyword_owner,
            "keyword_kind": entry.where_to_look.keyword_kind,
        },
        "signature": entry.signature,
        "raw_messages": [
            {"message": m.message, "occurrences": m.occurrences}
            for m in entry.raw_messages
        ],
        "counts": {
            "failures": entry.counts.failures,
            "suite_runs": entry.counts.suite_runs,
            "rate": round(entry.counts.rate, 4),
            "distinct_commits": entry.counts.distinct_commits,
            "test_rows_marked_failed": entry.counts.test_rows_marked_failed,
            "first_attempt": {
                "failures": entry.counts.first_attempt.failures,
                "ran": entry.counts.first_attempt.ran,
                "rate": round(entry.counts.first_attempt.rate, 4),
            },
        },
        "affected_tests": list(entry.affected_tests),
        "rates": [_rate(r, measurable=False) for r in entry.rates],
        "never_ran_on": list(entry.never_ran_on),
        "occurrences": [_occurrence(o, fixture=True) for o in entry.occurrences],
    }
    if entry.known_cause:
        out["known_cause"] = _cause(entry.known_cause)
    if entry.signature_variants:
        out["signature_variants"] = [
            {"signature": v.signature, "occurrences": v.occurrences}
            for v in entry.signature_variants
        ]
    return out


def document(report: Report) -> dict:
    """The Report as plain data."""
    newest = report.window.latest_run
    return {
        "about": report.about,
        "window": {
            "runs": report.window.runs,
            "legs": report.window.legs,
            "results": report.window.results,
            "failures": report.window.failures,
            "distinct_tests": report.window.distinct_tests,
            "legs_with_unknown_attempt": report.window.legs_with_unknown_attempt,
            "since": report.window.since,
            "until": report.window.until,
            "latest_run": (
                {}
                if newest is None
                else {
                    "run": newest.run,
                    "commit": newest.commit,
                    "event": newest.event,
                    "at": newest.at,
                    "failures": newest.failures,
                }
            ),
        },
        "platforms": [
            {
                "platform": row.platform,
                "legs": row.legs,
                "failures": row.failures,
                "per_leg": row.per_leg,
            }
            for row in report.platforms
        ],
        "since_last_report": report.since_last_report,
        "fixture_failures": [_fixture(entry) for entry in report.fixture_failures],
        "test_failures": [_test(entry) for entry in report.test_failures],
    }


def write(report: Report, destination: Path) -> Path:
    """Writes the document for a Report somebody else built."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document(report), indent=2) + "\n", encoding="utf-8"
    )
    return destination
