#!/usr/bin/env python3
import argparse
import re
import sys
from collections import defaultdict
from typing import Any

from robot.api import ExecutionResult, ResultVisitor
from robot.result.model import TestCase

DEFAULT_OUTPUT_XML = "atest/output/output.xml"

LogEntry = dict[str, str]
TestEntry = dict[str, Any]


class ResultCollector(ResultVisitor):
    def __init__(self, include_keyword_logs: bool = False) -> None:
        self.failed: list[TestEntry] = []
        self.skipped: list[TestEntry] = []
        self.error_groups: defaultdict[str, list[str]] = defaultdict(list)
        self.include_keyword_logs = include_keyword_logs

    def _collect_logs(self, item: TestCase) -> list[LogEntry]:
        """Recursively collect all log messages from an item and its children."""
        messages: list[LogEntry] = []
        for child in getattr(item, "body", []):
            if getattr(child, "type", None) == "MESSAGE":
                ts: str = child.timestamp
                if hasattr(ts, "strftime"):
                    ts = ts.strftime("%Y%m%d %H:%M:%S.%f")[:-3]
                message = re.sub(r"<[^>]+>", "", child.message)
                messages.append(
                    {"timestamp": ts, "level": child.level, "message": message}
                )
            else:
                messages.extend(self._collect_logs(child))
        return messages

    def visit_test(self, test: TestCase) -> None:
        if test.failed:
            failing_item = next(
                (item for item in test.body if hasattr(item, "status") and item.failed),
                None,
            )
            entry: TestEntry = {
                "name": test.full_name,
                "message": test.message,
                "failing_keyword": failing_item.name if failing_item else None,
                "failing_library": getattr(failing_item, "libname", None)
                if failing_item
                else None,
            }
            if self.include_keyword_logs:
                entry["keyword_logs"] = self._collect_logs(test)
            self.failed.append(entry)
            if test.message:
                self.error_groups[test.message].append(test.full_name)
        elif test.skipped:
            self.skipped.append({"name": test.full_name, "message": test.message})
        super().visit_test(test)


def print_summary(result: ExecutionResult) -> None:
    stats = result.statistics
    total = stats.total
    rate = (total.passed / total.total * 100) if total.total else 0.0
    print(
        f"Pass rate: {rate:.1f}%  "
        f"({total.passed} passed / {total.failed} failed / {total.skipped} skipped  "
        f"of {total.total} total)"
    )
    print()

    def print_suite(suite: Any, indent: int = 0) -> None:
        st = suite.statistics
        suite_total = st.passed + st.failed + st.skipped
        suite_rate = (st.passed / suite_total * 100) if suite_total else 0.0
        prefix = "  " * indent
        print(
            f"{prefix}{suite.name}  {suite_rate:.0f}%  "
            f"passed={st.passed}  failed={st.failed}  skipped={st.skipped}"
        )
        for child in suite.suites:
            print_suite(child, indent + 1)

    print_suite(result.suite)


def print_failures(collector: ResultCollector) -> None:
    print(f"\n--- Failures ({len(collector.failed)}) ---\n")
    if not collector.failed:
        print("No failures.")
        return

    for t in collector.failed:
        print(f"FAIL  {t['name']}")
        if t["failing_keyword"]:
            lib = f" ({t['failing_library']}" + ")" if t["failing_library"] else ""
            print(f"      keyword: {t['failing_keyword']}{lib}")
        if t["message"]:
            for line in t["message"].splitlines():
                print(f"      {line}")
        if t.get("keyword_logs"):
            print("      --- keyword logs ---")
            for log in t["keyword_logs"]:
                print(f"      {log['timestamp']}  {log['level']:<8}  {log['message']}")
        print()

    if collector.skipped:
        print(f"({len(collector.skipped)} test(s) skipped)")


def print_error_groups(collector: ResultCollector) -> None:
    print("\n--- Recurring errors ---\n")
    if not collector.error_groups:
        print("No failures.")
        return

    ranked = sorted(
        collector.error_groups.items(), key=lambda x: len(x[1]), reverse=True
    )
    print(f"{len(ranked)} distinct error message(s):\n")
    for msg, tests in ranked:
        print(f"[{len(tests)}x]  {msg.splitlines()[0]}")
        if len(msg.splitlines()) > 1:
            for line in msg.splitlines()[1:]:
                print(f"       {line}")
        for name in tests:
            print(f"  - {name}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Robot Framework output.xml")
    parser.add_argument(
        "output_xml",
        nargs="?",
        default=DEFAULT_OUTPUT_XML,
        help=f"Path to output.xml (default: {DEFAULT_OUTPUT_XML})",
    )
    parser.add_argument(
        "--keyword-logs",
        action="store_true",
        default=False,
        help="Include all keyword log messages (timestamp, level, message) for each failing test",
    )
    args = parser.parse_args()

    try:
        result = ExecutionResult(args.output_xml)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    collector = ResultCollector(include_keyword_logs=args.keyword_logs)
    result.visit(collector)

    print_summary(result)
    print_failures(collector)
    print_error_groups(collector)

    return result.return_code


if __name__ == "__main__":
    sys.exit(main())
