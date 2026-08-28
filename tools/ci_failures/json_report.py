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
    configurations_by_fixture,
    coverage_by_test,
    failure_groups,
    fixture_failures,
    fixture_signature_variants,
    log_messages,
    messages_by_test,
    occurrences_by_test,
    platform_breakdown,
    signature_variants,
    totals,
)

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


def _rates(coverage: list[dict], known_platforms: set[str]) -> tuple[list, list]:
    rates = [
        {
            "platform": entry["platform"],
            "python": entry["python_version"],
            "rf": entry["rf_version"],
            "node": entry["node_version"] or None,
            "ran": entry["ran"],
            "failed": entry["failed"] or 0,
        }
        for entry in coverage
    ]
    seen = {entry["platform"] for entry in coverage if entry["platform"]}
    return rates, sorted(known_platforms - seen)


def _occurrences(entries: list[dict]) -> list[dict]:
    return [
        {
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
            "artifact_url": entry["artifact_url"],
            "elapsed_ms": entry["elapsed_ms"],
        }
        for entry in entries
    ]


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

    tests = []
    for group in failure_groups(db_path, limit=limit):
        key = (group.longname, group.signature_key)
        rates, never = _rates(coverage.get(group.longname, []), platforms)
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
            },
            "rates": rates,
            "never_ran_on": never,
            "first_seen": group.first_seen,
            "last_seen": group.last_seen,
            "screenshots": _split(group.screenshots),
            "screenshot_status": group.screenshot_status,
            "occurrences": _occurrences(occurrences.get(key, [])),
            "log": _log(db_path, group.latest_result_id),
        }
        if key in variants:
            entry["signature_variants"] = variants[key]
        tests.append(entry)

    fixture_configs = configurations_by_fixture(db_path)
    fixtures = []
    for fixture in fixture_failures(db_path, limit=limit):
        key = (fixture.scope_owner, fixture.failure_scope, fixture.signature_key)
        fixtures.append(
            {
                "suite": fixture.scope_owner,
                "scope": fixture.failure_scope,
                "where_to_look": _where_to_look(fixture),
                "signature": fixture.error_signature,
                "counts": {
                    "failures": fixture.occurrences,
                    "suite_runs": fixture.suite_runs,
                    "rate": round(fixture.failure_rate, 4),
                    "distinct_commits": fixture.distinct_shas,
                    "test_rows_marked_failed": fixture.tests_marked,
                },
                "affected_tests": _split(fixture.affected_tests),
                "seen_on": fixture_configs.get(key, []),
                "first_seen": fixture.first_seen,
                "last_seen": fixture.last_seen,
                "screenshots": _split(fixture.screenshots),
                "screenshot_status": fixture.screenshot_status,
                "artifact_url": fixture.latest_artifact_url,
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
            "since": summary["since"],
            "until": summary["until"],
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
