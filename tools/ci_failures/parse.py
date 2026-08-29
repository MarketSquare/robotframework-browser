"""Reads a Robot Framework output.xml into rows.

Everything the database holds about an execution comes from here, which is what
keeps output.xml the single source of truth.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from robot.api import ExecutionResult

from .locate import (
    artifact_relative,
    keyword_location,
    owner_kind,
    repo_relative,
)

# Only these can name a culprit. Everything else in a keyword body is a control
# structure - FOR, IF/ELSE ROOT, TRY/EXCEPT ROOT - which is descended into but
# never named, because "IF/ELSE ROOT" is not an answer to "which keyword broke".
_NAMEABLE = {"KEYWORD", "SETUP", "TEARDOWN"}

# "Rebot 7.1.1 (Python 3.13.15 on linux)"
_GENERATOR = re.compile(
    r"^\S+ (?P<rf>[\d.]+\S*) \(Python (?P<python>[\d.]+\S*) on (?P<platform>\w+)\)"
)

_MASKS: tuple[tuple[re.Pattern, str], ...] = (
    # Longest and most specific first, or a uuid gets eaten digit by digit.
    (re.compile(r"\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b"), "<uuid>"),
    (re.compile(r"\b[0-9a-fA-F]{16,}\b"), "<hex>"),
    (
        re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b"),
        "<timestamp>",
    ),
    (re.compile(r"https?://[^\s'\"]+"), "<url>"),
    (re.compile(r"(?<![\w/])(?:[A-Za-z]:)?[\\/](?:[\w.\-]+[\\/])+[\w.\-]+"), "<path>"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*ms\b"), "<duration>"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*s(?:econds?)?\b"), "<duration>"),
    (re.compile(r"\b\d+(?:\.\d+)?\b"), "<n>"),
)
_WHITESPACE = re.compile(r"\s+")

# Robot Framework embeds screenshots into the log as a base64 data URI. One of
# them is 35KB of text that decodes to a PNG: nothing can read it as it stands,
# and three of them accounted for 77% of every log byte stored. The fact that a
# screenshot was taken is worth keeping; the bytes are in the artifact.
_DATA_URI = re.compile(r"data:([\w/+.-]+);base64,([A-Za-z0-9+/=]+)")


# Robot Framework logs a screenshot either as a link to a file, which is the
# useful case because the path is where it sits inside the artifact, or as a
# base64 blob embedded in log.html, which is not readable as text.
_IMAGE_LINK = re.compile(r'href="([^"]+\.(?:png|jpe?g|webp|gif))"', re.IGNORECASE)
_EMBEDDED_IMAGE = re.compile(r"data:image/[\w.+-]+;base64,")
# The library takes a screenshot on failure by default, and says so when it
# cannot - which is itself worth knowing, because "no screenshot" usually means
# there was no page to photograph.
_NO_SCREENSHOT = re.compile(r"could not be run on failure", re.IGNORECASE)


def strip_embedded_data(message: str | None) -> str | None:
    """Replaces embedded base64 payloads with a note of what was there."""
    if not message:
        return message

    def replace(match: re.Match) -> str:
        mime = match.group(1)
        kilobytes = max(1, len(match.group(2)) * 3 // 4 // 1024)
        return f"<{mime}, ~{kilobytes} KB, embedded in the log - see the artifact>"

    return _DATA_URI.sub(replace, message)


# `robotstatuschecker` rewrites the message of every checked test, so this prefix
# sits in front of every failure and says nothing about any of them. The real
# error is what follows it.
_STATUS_CHECKER = re.compile(
    r"^Expected \w+ status, got \w+\.\s*(?:Original message:\s*)?", re.IGNORECASE
)


def error_signature(message: str | None, max_length: int = 300) -> str | None:
    """Masks the parts of a message that vary between runs.

    Without this, grouping by error is grouping by near-unique string: the same
    problem carries a different timeout, selector id or pixel count every time.
    """
    if not message:
        return None
    signature = _STATUS_CHECKER.sub("", message)
    for pattern, replacement in _MASKS:
        signature = pattern.sub(replacement, signature)
    return _WHITESPACE.sub(" ", signature).strip()[:max_length]


@dataclass
class LegInfo:
    python_version: str | None
    rf_version: str | None
    platform: str | None
    node_version: str | None
    generated_at: str | None
    # How many test executions ran at once, and whether they shared one node
    # process. Both null for runs ingested from before the metadata reached CI.
    executors: int | None = None
    node_process: str | None = None


@dataclass
class LogMessage:
    seq: int
    level: str | None
    keyword: str | None
    message: str | None
    # None when the line came from the test's own keywords. Otherwise it names
    # the setup or teardown that failed, which may belong to an enclosing suite
    # and may have run long after the test itself finished.
    origin: str | None = None


@dataclass
class TestResult:
    longname: str
    name: str
    suite_longname: str
    status: str
    elapsed_ms: int | None
    message: str | None
    error_signature: str | None
    failing_keyword: str | None
    # What actually failed. A suite fixture fails every test beneath it, so
    # "suite_teardown" means this test was marked failed by something that is
    # not in it and may have run after it finished.
    # Where to start looking. output.xml has the test's file and line; the
    # keyword's owner is there too, but its location has to be resolved.
    test_source: str | None = None
    test_lineno: int | None = None
    # Relative to the run's output directory, which is also where they sit
    # inside the artifact.
    screenshots: str | None = None
    screenshot_status: str | None = None
    keyword_owner: str | None = None
    keyword_kind: str | None = None
    keyword_source: str | None = None
    keyword_lineno: int | None = None
    failure_scope: str | None = None
    # The suite or test owning that fixture. For a suite fixture this is the
    # suite that broke, which can be an ancestor rather than the parent.
    scope_owner: str | None = None
    log_messages: list["LogMessage"] = field(default_factory=list)


def _innermost_failing_keyword(item: Any) -> Any:
    """The deepest keyword on the failing branch, which is the one that broke."""
    deepest = None
    for child in getattr(item, "body", None) or []:
        if getattr(child, "status", None) != "FAIL":
            continue
        if str(getattr(child, "type", "") or "").upper() not in _NAMEABLE:
            # A control structure. Descend, but it is never the answer. Checked
            # before .name is read, which is deprecated on If and IfBranch and
            # goes away in Robot Framework 8.
            deepest = _innermost_failing_keyword(child) or deepest
            continue
        if not getattr(child, "name", None):
            continue
        deepest = _innermost_failing_keyword(child) or child
    return deepest


# A failing keyword can log a lot - a traceback, a byte-level dump - and a
# proof of concept does not need all of it to show what went wrong.
MAX_LOG_MESSAGES = 60

# Lines from failures that were caught and never reached the test are kept under
# their own budget, so a suite that expects errors on purpose - this one runs
# `Run Keyword And Expect Error` in nearly every test - cannot crowd out the
# lines of the failure that actually stopped the test.
MAX_SWALLOWED_MESSAGES = 40


def _collect_log_messages(
    item: Any,
    out: list[LogMessage],
    keyword: str | None = None,
    origin: str | None = None,
) -> None:
    """Messages logged by the keywords on the failing branch, in order.

    ``keyword`` is None until we are inside a keyword that actually failed, and
    messages are only taken from there. Messages sitting directly under the test
    are the test's own logging and say nothing about why it failed - when the
    failure is in a suite teardown they are actively misleading, describing work
    that succeeded before the thing that broke ever ran.

    TRACE is skipped: it is argument-level bookkeeping, and it buries the lines
    that say what happened.
    """
    for child in getattr(item, "body", None) or []:
        if len(out) >= MAX_LOG_MESSAGES:
            return
        child_type = str(getattr(child, "type", "") or "").upper()
        if child_type == "MESSAGE":
            if keyword is None:
                continue
            level = getattr(child, "level", None)
            if level == "TRACE":
                continue
            out.append(
                LogMessage(
                    seq=len(out),
                    level=level,
                    keyword=keyword,
                    message=strip_embedded_data(getattr(child, "message", None)),
                    origin=origin,
                )
            )
            continue
        if getattr(child, "status", None) != "FAIL":
            continue
        name = keyword
        if child_type in _NAMEABLE:
            name = getattr(child, "name", None) or keyword
        _collect_log_messages(child, out, name, origin)


def _catcher_name(item: Any) -> str | None:
    """A readable name for the thing that swallowed a failure.

    `Run Keyword And Expect Error` is a keyword and names itself. A TRY/EXCEPT is
    a control structure with no name, so its type is what there is to say.
    """
    kind = str(getattr(item, "type", "") or "").upper()
    # .name is read only where it is meaningful: it is deprecated on If and
    # TryBranch and goes away in Robot Framework 8, and reading it warns.
    if kind in _NAMEABLE:
        name = getattr(item, "name", None)
        if name:
            return str(name)
    return kind.replace(" ROOT", "") or None


def _collect_swallowed_messages(
    item: Any,
    out: list[LogMessage],
    caught_by: str | None = None,
    on_failing_branch: bool = True,
    catcher: str | None = None,
) -> None:
    """Lines from failures that were caught before they reached the test.

    ``_collect_log_messages`` follows the branch that is FAIL all the way up,
    which is the branch that stopped the test. A keyword that failed inside
    `Run Keyword And Expect Error`, or inside a TRY whose EXCEPT handled it, is
    not on that branch: its parent passed, so the walk turns back at the parent
    and everything the failing keyword logged is lost.

    Those lines are evidence. `Screenshot On Failure` logs whether it highlighted
    anything from inside a `Get Text` that an expected-error wrapper swallows, so
    the one fact that says whether the highlight was ever applied is exactly the
    fact the failing-branch rule drops.

    They are not the failure, though, and must never be mistaken for it, so each
    one is stamped with the keyword that caught it.
    """
    for child in getattr(item, "body", None) or []:
        if len(out) >= MAX_SWALLOWED_MESSAGES:
            return
        child_type = str(getattr(child, "type", "") or "").upper()
        if child_type == "MESSAGE":
            if caught_by is None:
                continue
            level = getattr(child, "level", None)
            if level == "TRACE":
                continue
            out.append(
                LogMessage(
                    seq=len(out),
                    level=level,
                    keyword=_catcher_name(item),
                    message=strip_embedded_data(getattr(child, "message", None)),
                    origin=f"caught by {caught_by}",
                )
            )
            continue
        failed = getattr(child, "status", None) == "FAIL"
        # The failing branch is the chain of FAIL nodes running from the test
        # down to the keyword that stopped it. A node is on it only if every
        # ancestor is too - which is what makes a FAIL node under a PASS parent
        # a swallowed failure rather than the failure.
        child_on_branch = on_failing_branch and failed
        caught = caught_by
        if caught is None and failed and not child_on_branch:
            caught = catcher or "an enclosing block"
        _collect_swallowed_messages(
            child,
            out,
            caught,
            child_on_branch,
            # Whatever passed most recently is what will have caught anything
            # failing below it.
            _catcher_name(child) if not failed else catcher,
        )


def _swallowed_messages(test: Any) -> list[LogMessage]:
    """Caught failures anywhere in the test, including its own fixtures."""
    messages: list[LogMessage] = []
    for part in (getattr(test, "setup", None), test, getattr(test, "teardown", None)):
        if part is None:
            continue
        _collect_swallowed_messages(
            part,
            messages,
            on_failing_branch=getattr(part, "status", None) == "FAIL",
            catcher=_catcher_name(part),
        )
    for index, entry in enumerate(messages):
        entry.seq = index
    return messages


def _as_int(value: str | None) -> int | None:
    """Left null rather than defaulted where the run did not say."""
    return int(value) if value and value.isdigit() else None


def leg_info(result: Any) -> LegInfo:
    """What output.xml says about the machine that produced it."""
    metadata = {
        str(k).lower(): str(v) for k, v in (result.suite.metadata or {}).items()
    }
    generator = _GENERATOR.match(result.generator or "")
    return LegInfo(
        python_version=metadata.get("python version")
        or (generator["python"] if generator else None),
        rf_version=metadata.get("robot framework version")
        or (generator["rf"] if generator else None),
        platform=metadata.get("os") or (generator["platform"] if generator else None),
        node_version=metadata.get("node version"),
        generated_at=metadata.get("generated"),
        executors=_as_int(metadata.get("executors")),
        node_process=metadata.get("node process"),
    )


def suite_fixture_failures(suite: Any) -> list[tuple]:
    """The failed setup and teardown of one suite, with their messages.

    Returned rather than attached here because a suite fixture fails the tests
    of every suite beneath it too, and the tests do not know about it: Robot
    Framework simply marks them failed. Each entry is
    (kind, origin, suite name, messages, the fixture keyword itself).
    """
    found = []
    for kind in ("setup", "teardown"):
        fixture = getattr(suite, kind, None)
        if not fixture or fixture.status != "FAIL":
            continue
        origin = f"suite {kind} of {suite.full_name}"
        messages: list[LogMessage] = []
        _collect_log_messages(
            fixture, messages, getattr(fixture, "name", None) or kind, origin
        )
        found.append((kind, origin, suite.full_name, messages, fixture))
    return found


# Robot Framework stamps a merged artifact with the run's timestamp and the
# pabot worker that produced it: `20260825_104829-4-fail-screenshot-1.png`. The
# keyword that used the file logged the name it had at the time, without the
# stamp, so the two never match on their face.
_ARTIFACT_STAMP = re.compile(r"^\d{8}_\d{6}-\d+-")


def _screenshot_key(path: str) -> str:
    """One file, one key.

    Two things put the same picture under two names. A pabot leg's merged log
    references it once as `pabot_results/4/browser/screenshot/x.png`, which is
    where it really sits inside the artifact, and once as the worker's own
    `browser/screenshot/x.png`, which does not exist at the top of the artifact
    at all. And the merge stamps the file itself, so the name in the directory
    is not the name the keyword logged. Left alone they take two of the few
    slots there are, name one file, and defeat the match against the paths the
    failing keyword named.
    """
    return _ARTIFACT_STAMP.sub("", path.rsplit("/", 1)[-1])


def _screenshot_evidence(item: Any, found: list[str], state: dict) -> None:
    """Screenshot references anywhere under ``item``, whatever its status.

    A separate walk from the log messages on purpose. The screenshot the library
    takes on failure runs as a keyword that *passes*, hanging off the one that
    failed, so the failing-branch walk never sees it - and a screenshot is often
    the first thing worth looking at.
    """
    for child in getattr(item, "body", None) or []:
        if str(getattr(child, "type", "") or "").upper() == "MESSAGE":
            message = getattr(child, "message", None) or ""
            for match in _IMAGE_LINK.finditer(message):
                path = artifact_relative(match.group(1))
                if path not in found:
                    found.append(path)
            if _EMBEDDED_IMAGE.search(message):
                state["embedded"] = True
            if _NO_SCREENSHOT.search(message):
                state["unavailable"] = True
            continue
        _screenshot_evidence(child, found, state)


# Generous on purpose. The cap is applied here and the ranking happens at report
# time, so anything cut here is invisible to the ranker no matter how good the
# evidence for it: a picture that never reaches the database cannot be promoted
# to the top of the list. Paths are short and failures are rare, so the cheap
# answer is to keep far more than anyone will read. The earlier limit of three
# was set when this function did the ranking, and it cut the two pictures the
# one test that compares two pictures was actually about.
MAX_SCREENSHOTS = 20


def screenshots_of(test: Any, fixtures: list[tuple]) -> tuple[str | None, str | None]:
    """Every distinct screenshot this failure left behind, and whether there are any.

    Deduplicated but deliberately **not ranked**. Which picture matters most is
    a question about the log lines, the log lines are in the database, and
    working it out here would bake a display decision into stored data that only
    a full re-download can change (§1). The report ranks them; see
    `report.rank_screenshots`.
    """
    found: list[str] = []
    state: dict = {}
    _screenshot_evidence(test, found, state)
    for fixture in fixtures:
        _screenshot_evidence(fixture[4], found, state)
    if found:
        by_file: dict[str, str] = {}
        for path in found:
            key = _screenshot_key(path)
            # The longer path is the one carrying the pabot prefix, and so the
            # one that resolves inside the artifact.
            if key not in by_file or len(path) > len(by_file[key]):
                by_file[key] = path
        return ",".join(sorted(by_file.values())[:MAX_SCREENSHOTS]), "file"
    if state.get("embedded"):
        return None, "embedded"
    if state.get("unavailable"):
        return None, "unavailable"
    return None, None


def classify_failure(
    test: Any, setups: list[tuple], teardowns: list[tuple]
) -> tuple[str, str]:
    """What failed, and who owns it.

    Ordered by what actually stopped this test. Its own body first, then its own
    fixtures, then the suite fixtures above it: the outermost failing setup,
    because an outer setup failing is why the inner ones never ran, and the
    innermost failing teardown, because that is the one nearest the test.
    """
    if any(
        getattr(c, "status", None) == "FAIL" for c in getattr(test, "body", None) or []
    ):
        return "test", test.full_name
    own_setup = getattr(test, "setup", None)
    if own_setup and own_setup.status == "FAIL":
        return "test_setup", test.full_name
    own_teardown = getattr(test, "teardown", None)
    if own_teardown and own_teardown.status == "FAIL":
        return "test_teardown", test.full_name
    if setups:
        return "suite_setup", setups[0][2]
    if teardowns:
        return "suite_teardown", teardowns[-1][2]
    # Marked failed with nothing to point at. Rare, but it must not be silently
    # relabelled as something it is not.
    return "unknown", test.full_name


def _collect_failing_messages(test: Any) -> list[LogMessage]:
    """What failed inside this test, in the order it ran.

    Setup and teardown are not part of ``body``, so they are walked separately.
    A test whose own setup, body and teardown all passed contributes nothing:
    it was failed by something outside itself, and borrowing unrelated lines to
    fill the gap would only mislead whoever reads them.
    """
    messages: list[LogMessage] = []
    setup = getattr(test, "setup", None)
    if setup and setup.status == "FAIL":
        _collect_log_messages(setup, messages, getattr(setup, "name", None) or "Setup")
    _collect_log_messages(test, messages)
    teardown = getattr(test, "teardown", None)
    if teardown and teardown.status == "FAIL":
        _collect_log_messages(
            teardown, messages, getattr(teardown, "name", None) or "Teardown"
        )
    return messages


def parse(path: Path) -> tuple[LegInfo, list[TestResult]]:
    """Every test in ``path``, plus what it says about its environment."""
    result = ExecutionResult(path)
    results: list[TestResult] = []

    def visit(suite: Any, inherited: list[tuple]) -> None:
        # A failed suite fixture fails every test below it, in this suite and in
        # its child suites, so it travels down with the walk.
        fixtures = inherited + suite_fixture_failures(suite)
        setups = [f for f in fixtures if f[0] == "setup"]
        teardowns = [f for f in fixtures if f[0] == "teardown"]

        for test in suite.tests:
            failed = test.status == "FAIL"
            message = test.message or None if failed else None
            scope = scope_owner_name = None
            keyword = None
            keyword_owner = keyword_src = keyword_line = None
            shots = shot_status = None
            messages: list[LogMessage] = []

            if failed:
                scope, scope_owner_name = classify_failure(test, setups, teardowns)
                if scope.startswith("suite_"):
                    # The keyword that broke is inside the fixture. The test has
                    # none of its own: that is what makes it a fixture failure.
                    fixture = (setups + list(reversed(teardowns)))[0][4]
                    keyword = _innermost_failing_keyword(fixture) or fixture
                else:
                    keyword = _innermost_failing_keyword(test)
                keyword_owner = getattr(keyword, "owner", None) or getattr(
                    keyword, "libname", None
                )
                keyword_src, keyword_line = keyword_location(
                    keyword_owner, getattr(keyword, "name", None)
                )
                # Run order: the setups that failed above it, then the test's
                # own, then the teardowns, innermost first as they unwind.
                for _, _, _, lines, _ in setups:
                    messages.extend(lines)
                messages.extend(_collect_failing_messages(test))
                for _, _, _, lines, _ in reversed(teardowns):
                    messages.extend(lines)
                # Caught failures last: they did not stop the test and must not
                # be read as if they had, but they are the only record of what
                # a keyword did before something else swallowed it.
                messages.extend(_swallowed_messages(test))
                for index, entry in enumerate(messages):
                    entry.seq = index
                shots, shot_status = screenshots_of(test, setups + teardowns)

            results.append(
                TestResult(
                    longname=test.full_name,
                    name=test.name,
                    suite_longname=suite.full_name,
                    status=test.status,
                    elapsed_ms=int(test.elapsed_time.total_seconds() * 1000)
                    if test.elapsed_time
                    else None,
                    message=message,
                    error_signature=error_signature(message),
                    failing_keyword=getattr(keyword, "name", None),
                    test_source=repo_relative(getattr(test, "source", None)),
                    test_lineno=getattr(test, "lineno", None),
                    screenshots=shots,
                    screenshot_status=shot_status,
                    keyword_owner=keyword_owner,
                    keyword_kind=owner_kind(keyword_owner) if keyword else None,
                    keyword_source=keyword_src,
                    keyword_lineno=keyword_line,
                    failure_scope=scope,
                    scope_owner=scope_owner_name,
                    log_messages=messages,
                )
            )
        for child in suite.suites:
            visit(child, fixtures)

    visit(result.suite, [])
    return leg_info(result), results
