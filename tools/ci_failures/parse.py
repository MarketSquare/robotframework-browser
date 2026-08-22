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
    item: Any, out: list[LogMessage], keyword: str | None = None
) -> None:
    """Messages logged by the keywords on the failing branch, in order.

    TRACE is skipped: it is argument-level bookkeeping, and it buries the lines
    that say what happened.
    """
    for child in getattr(item, "body", None) or []:
        if len(out) >= MAX_LOG_MESSAGES:
            return
        child_type = str(getattr(child, "type", "") or "").upper()
        if child_type == "MESSAGE":
            level = getattr(child, "level", None)
            if level == "TRACE":
                continue
            out.append(
                LogMessage(
                    seq=len(out),
                    level=level,
                    keyword=keyword,
                    message=getattr(child, "message", None),
                )
            )
            continue
        if getattr(child, "status", None) != "FAIL":
            continue
        name = keyword
        if child_type in _NAMEABLE:
            name = getattr(child, "name", None) or keyword
        _collect_log_messages(child, out, name)


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


def _collect_failing_messages(test: Any) -> list[LogMessage]:
    messages: list[LogMessage] = []
    _collect_log_messages(test, messages)
    return messages


def parse(path: Path) -> tuple[LegInfo, list[TestResult]]:
    """Every test in ``path``, plus what it says about its environment."""
    result = ExecutionResult(path)
    results: list[TestResult] = []

    def visit(suite: Any) -> None:
        for test in suite.tests:
            failed = test.status == "FAIL"
            message = test.message or None if failed else None
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
                    log_messages=_collect_failing_messages(test) if failed else [],
                )
            )
        for child in suite.suites:
            visit(child)

    visit(result.suite)
    return leg_info(result), results
