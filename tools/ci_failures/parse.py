"""Reads a Robot Framework output.xml into rows.

Everything the database holds about an execution comes from here, which is what
keeps output.xml the single source of truth.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from robot.api import ExecutionResult

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
    log_messages: list["LogMessage"] = field(default_factory=list)


def _innermost_failing_keyword(item: Any) -> str | None:
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
        name = getattr(child, "name", None)
        if not name:
            continue
        deepest = _innermost_failing_keyword(child) or name
    return deepest


# A failing keyword can log a lot - a traceback, a byte-level dump - and a
# proof of concept does not need all of it to show what went wrong.
MAX_LOG_MESSAGES = 60


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
    )


def suite_fixture_failures(suite: Any) -> list[tuple[str, str, list[LogMessage]]]:
    """The failed setup and teardown of one suite, with their messages.

    Returned rather than attached here because a suite fixture fails the tests
    of every suite beneath it too, and the tests do not know about it: Robot
    Framework simply marks them failed. Each entry is (kind, origin, messages).
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
        found.append((kind, origin, messages))
    return found


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

    def visit(suite: Any, inherited: list[tuple[str, str, list[LogMessage]]]) -> None:
        # A failed suite fixture fails every test below it, in this suite and in
        # its child suites, so it travels down with the walk.
        fixtures = inherited + suite_fixture_failures(suite)
        setups = [f for f in fixtures if f[0] == "setup"]
        teardowns = [f for f in fixtures if f[0] == "teardown"]

        for test in suite.tests:
            failed = test.status == "FAIL"
            message = test.message or None if failed else None
            messages: list[LogMessage] = []
            if failed:
                # Run order: the setups that failed above it, then the test's
                # own, then the teardowns, innermost first as they unwind.
                for _, _, lines in setups:
                    messages.extend(lines)
                messages.extend(_collect_failing_messages(test))
                for _, _, lines in reversed(teardowns):
                    messages.extend(lines)
                for index, entry in enumerate(messages):
                    entry.seq = index
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
                    failing_keyword=_innermost_failing_keyword(test)
                    if failed
                    else None,
                    log_messages=messages,
                )
            )
        for child in suite.suites:
            visit(child, fixtures)

    visit(result.suite, [])
    return leg_info(result), results
