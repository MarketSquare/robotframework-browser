#!/usr/bin/env python3
import argparse
import sys
from collections import defaultdict

from robot.api import ExecutionResult, ResultVisitor


DEFAULT_OUTPUT_XML = "atest/output/output.xml"


class ResultCollector(ResultVisitor):
    def __init__(self):
        self.failed = []
        self.skipped = []
        self.error_groups = defaultdict(list)

    def visit_test(self, test):
        if test.failed:
            failing_item = next(
                (item for item in test.body if hasattr(item, "status") and item.failed),
                None,
            )
            self.failed.append({
                "name": test.full_name,
                "message": test.message,
                "failing_keyword": failing_item.name if failing_item else None,
                "failing_library": getattr(failing_item, "libname", None) if failing_item else None,
            })
            if test.message:
                self.error_groups[test.message].append(test.full_name)
        elif test.skipped:
            self.skipped.append({"name": test.full_name, "message": test.message})


def print_summary(result):
    stats = result.statistics
    total = stats.total
    rate = (total.passed / total.total * 100) if total.total else 0.0
    print(f"Pass rate: {rate:.1f}%  "
          f"({total.passed} passed / {total.failed} failed / {total.skipped} skipped  "
          f"of {total.total} total)")
    print()

    def print_suite(suite, indent=0):
        st = suite.statistics
        suite_total = st.passed + st.failed + st.skipped
        suite_rate = (st.passed / suite_total * 100) if suite_total else 0.0
        prefix = "  " * indent
        print(f"{prefix}{suite.name}  {suite_rate:.0f}%  "
              f"passed={st.passed}  failed={st.failed}  skipped={st.skipped}")
        for child in suite.suites:
            print_suite(child, indent + 1)

    print_suite(result.suite)


def print_failures(collector):
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
        print()

    if collector.skipped:
        print(f"({len(collector.skipped)} test(s) skipped)")


def print_error_groups(collector):
    print(f"\n--- Recurring errors ---\n")
    if not collector.error_groups:
        print("No failures.")
        return

    ranked = sorted(collector.error_groups.items(), key=lambda x: len(x[1]), reverse=True)
    print(f"{len(ranked)} distinct error message(s):\n")
    for msg, tests in ranked:
        print(f"[{len(tests)}x]  {msg.splitlines()[0]}")
        if len(msg.splitlines()) > 1:
            for line in msg.splitlines()[1:]:
                print(f"       {line}")
        for name in tests:
            print(f"  - {name}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Parse Robot Framework output.xml")
    parser.add_argument(
        "output_xml",
        nargs="?",
        default=DEFAULT_OUTPUT_XML,
        help=f"Path to output.xml (default: {DEFAULT_OUTPUT_XML})",
    )
    args = parser.parse_args()

    try:
        result = ExecutionResult(args.output_xml)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    collector = ResultCollector()
    result.suite.visit(collector)

    print_summary(result)
    print_failures(collector)
    print_error_groups(collector)

    return result.return_code


if __name__ == "__main__":
    sys.exit(main())
