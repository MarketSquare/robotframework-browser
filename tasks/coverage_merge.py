import shutil
import sys
from pathlib import Path
from typing import NamedTuple

from invoke import Exit, task

from tasks.shared import ATEST_OUTPUT, COVERAGE_DIR, ROOT_DIR, show_report

JEST_LCOV = ROOT_DIR / "node" / "coverage" / "lcov.info"
ATEST_NODE_LCOV = ATEST_OUTPUT / "node-coverage-report" / "lcov.info"


def _lcov_records(lcov: str) -> list[str]:
    return [record + "end_of_record\n" for record in lcov.split("end_of_record\n")[:-1]]


def _drop_never_loaded_records(lcov: str) -> str:
    return "".join(record for record in _lcov_records(lcov) if "\nLH:0\n" not in record)


class LcovTotals(NamedTuple):
    lines_hit: int
    lines_found: int
    branches_hit: int
    branches_found: int


def _lcov_totals(lcov: str) -> LcovTotals:
    sums = {"LH": 0, "LF": 0, "BRH": 0, "BRF": 0}
    for line in lcov.splitlines():
        key, _, value = line.partition(":")
        if key in sums:
            sums[key] += int(value)
    return LcovTotals(sums["LH"], sums["LF"], sums["BRH"], sums["BRF"])


# Istanbul records branches on lines with no statement, which lcov 2 calls
# inconsistent, and genhtml 2.0 cannot put such a line into a category. Naming
# a category twice also silences its warnings.
LCOV_OPTIONS = "--branch-coverage --ignore-errors inconsistent,inconsistent"
GENHTML_OPTIONS = f"{LCOV_OPTIONS},category,category"


COVERAGE_SUITES = ["utest", "utest-node --coverage", "atest-coverage"]


@task()
def coverage(c):
    """Run every test suite with coverage and merge it into one HTML report.

    Runs `inv utest`, `inv utest-node --coverage` and `inv atest-coverage` in
    that order, then `inv coverage-report`. A failing suite does not stop the
    ones after it, so the report covers everything that ran. Fails at the end
    when any suite failed. Takes as long as the whole acceptance test run.
    """
    failed = [
        suite
        for suite in COVERAGE_SUITES
        if c.run(f'"{sys.executable}" -m invoke {suite}', warn=True).failed
    ]
    coverage_report(c)
    if failed:
        raise Exit(f"Failed: {', '.join(f'inv {suite}' for suite in failed)}", code=1)


@task()
def coverage_report(c):
    """Merge the coverage of every test suite into one HTML report.

    `inv coverage` runs every suite and then this task. Reads whatever the
    earlier runs left, so a partial run still gives a report:
        inv utest                  .coverage
        inv utest-node --coverage  node/coverage/lcov.info
        inv atest-coverage         .coverage.* and
                                   atest/output/node-coverage-report/lcov.info

    Writes coverage/python.info, coverage/python.xml (Cobertura, for SonarQube),
    coverage/node.info, the merged coverage/all.info and the HTML report
    coverage/html/index.html. Jest records with no line hit
    are dropped first: they are files Jest never loads, and only list as zero
    because of collectCoverageFrom. The totals and the inputs that contributed
    are printed, and on GitHub Actions also shown on the run's summary page.
    The inputs are reported even when merging fails. Needs `lcov` and
    `genhtml` on PATH.
    """
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)
    COVERAGE_DIR.mkdir()
    python_info = COVERAGE_DIR / "python.info"
    jest_info = COVERAGE_DIR / "jest.info"
    node_info = COVERAGE_DIR / "node.info"
    all_info = COVERAGE_DIR / "all.info"
    python_xml = COVERAGE_DIR / "python.xml"

    inputs = {
        "Python unit tests (`.coverage`)": (ROOT_DIR / ".coverage").exists(),
        "Python acceptance tests (`.coverage.*`)": any(ROOT_DIR.glob(".coverage.*")),
        f"Node.js unit tests (`{JEST_LCOV.relative_to(ROOT_DIR)}`)": JEST_LCOV.exists(),
        f"Node.js acceptance tests (`{ATEST_NODE_LCOV.relative_to(ROOT_DIR)}`)": ATEST_NODE_LCOV.exists(),
    }
    try:
        _merge_coverage(c, python_info, python_xml, jest_info, node_info, all_info)
        show_report(
            _coverage_totals(all_info, {"Python": python_info, "Node.js": node_info}),
            "Coverage",
        )
        print(f"HTML report: {COVERAGE_DIR / 'html' / 'index.html'}")
    finally:
        show_report(
            ["| Input | Contributed |", "| --- | --- |"]
            + [
                f"| {name} | {'yes' if found else '**no**'} |"
                for name, found in inputs.items()
            ],
            "Coverage inputs",
        )


def _merge_coverage(
    c,
    python_info: Path,
    python_xml: Path,
    jest_info: Path,
    node_info: Path,
    all_info: Path,
):
    if (ROOT_DIR / ".coverage").exists() or any(ROOT_DIR.glob(".coverage.*")):
        c.run(f'coverage lcov --keep-combined -o "{python_info}"')
        c.run(f'coverage xml --keep-combined -o "{python_xml}"')
    if JEST_LCOV.exists():
        jest_info.write_text(_drop_never_loaded_records(JEST_LCOV.read_text()))
    node_inputs = [path for path in (jest_info, ATEST_NODE_LCOV) if path.exists()]
    if node_inputs:
        _lcov_merge(c, node_inputs, node_info)
    language_infos = [path for path in (python_info, node_info) if path.exists()]
    if not language_infos:
        raise Exit("No coverage data found. Run the test suites first.", code=1)
    _lcov_merge(c, language_infos, all_info)
    c.run(
        f'genhtml {GENHTML_OPTIONS} --quiet --output-directory "{COVERAGE_DIR / "html"}" "{all_info}"'
    )


def _lcov_merge(c, tracefiles: list[Path], output: Path):
    adds = " ".join(f'--add-tracefile "{path}"' for path in tracefiles)
    c.run(f'lcov {LCOV_OPTIONS} --quiet {adds} --output-file "{output}"')


def _percent(hit: int, found: int) -> str:
    if found == 0:
        return "not measured"
    return f"{100 * hit / found:.1f}% ({hit:,} of {found:,})"


def _coverage_totals(all_info: Path, language_infos: dict[str, Path]) -> list[str]:
    total = _lcov_totals(all_info.read_text())
    lines = [
        f"**Lines: {_percent(total.lines_hit, total.lines_found)}**",
        "",
        "| Language | Lines | Branches |",
        "| --- | --- | --- |",
    ]
    for language, info in language_infos.items():
        if info.exists():
            totals = _lcov_totals(info.read_text())
            lines.append(
                f"| {language} | {_percent(totals.lines_hit, totals.lines_found)} "
                f"| {_percent(totals.branches_hit, totals.branches_found)} |"
            )
        else:
            lines.append(f"| {language} | no data | no data |")
    return lines
