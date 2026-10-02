"""One Leg's artifact, fetched again for triage.

Ingest keeps nothing but the parsed rows, so the screenshots, `log.html` and
`playwright-log.txt` behind an Occurrence have to come down again once a failure
turns out to deserve them. Downloaded on demand rather than kept: by the time a
failure matters it is simpler to fetch it again than to have stored every leg.

An artifact holds hundreds of files, most of them other tests', and a list of
them all buries the few that matter. `shortlist` reads them from the artifact's
own output.xml instead: the Executor that ran the test, the test apps its suite
setups started, and every file its log links to.

Unpacked under `ci_failures/artifacts/`, which is gitignored, and removed with
`clean` once the triage is done.
"""

import re
import shutil
import tempfile
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from robot.api import ExecutionResult

from . import github
from .db import UnanswerableError
from .history import resolve
from .legs import leg_name
from .locate import artifact_relative
from .refusal import UnreachableError


class NoSuchLegError(UnanswerableError):
    """The run has no test artifact for that Leg."""


def _directory(root: Path, run: int, leg: str, attempt: int) -> Path:
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", leg_name(leg)).strip("-")
    return root / f"{run}-{slug}-attempt-{attempt}"


def fetch(run: int, leg: str, root: Path, attempt: int = 1) -> Path:
    """One Leg's artifact, unpacked under `root`, and the directory it is in.

    `leg` is the Leg as the report names it, or the artifact's own name.
    `attempt` is the Occurrence's: a Leg re-run by hand uploaded once per
    attempt under the same name, and a flake's failure is in the attempt that
    failed, not the one that passed. Raises `NoSuchLegError` when the run has no
    such Leg, and `UnreachableError` when GitHub cannot be reached.
    """
    directory = _directory(root, run, leg, attempt)
    if directory.is_dir():
        return directory
    try:
        return _download(run, leg, root, attempt, directory)
    except (github.GhError, OSError, zipfile.BadZipFile) as unreachable:
        raise UnreachableError(
            f"Could not fetch the artifact from GitHub - the network, `gh auth "
            f"status`, or an artifact past its 90 days:\n{unreachable}"
        ) from unreachable


def _download(run: int, leg: str, root: Path, attempt: int, directory: Path) -> Path:
    wanted = leg_name(leg)
    artifacts = github.with_attempts(
        github.list_test_artifacts(run), github.attempt_starts(github.get_run(run))
    )
    artifact = next(
        (a for a in artifacts if leg_name(a.name) == wanted and a.attempt == attempt),
        None,
    )
    if artifact is None:
        known = "\n  ".join(
            sorted(f"{leg_name(a.name)} (attempt {a.attempt})" for a in artifacts)
        )
        raise NoSuchLegError(
            f"Run {run} has no leg {leg!r} on attempt {attempt}. It has:\n  {known}"
        )
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=root) as work_dir:
        work = Path(work_dir)
        zip_path = github.download_artifact(artifact.id, work / "artifact.zip")
        (work / "unpacked").mkdir()
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(work / "unpacked")
        # Moved into place only once whole, so a download cut off halfway is
        # fetched again rather than reused.
        (work / "unpacked").rename(directory)
    return directory


@dataclass(frozen=True)
class Entry:
    """One file on a shortlist, by its path inside the artifact."""

    label: str
    path: str
    note: str = ""
    missing: bool = False


@dataclass(frozen=True)
class Shortlist:
    """The files in one Leg's artifact that bear on one test.

    In three tiers: the Leg's; the Executor's that ran the test, with the log
    of each test app its suite setups started; and the files the test's own log
    links to. `others` counts what is left, by extension, so
    that what was left out can be seen to exist.
    """

    directory: Path
    test: str | None
    entries: tuple[Entry, ...]
    others: tuple[tuple[str, int], ...]

    def lines(self) -> list[str]:
        lines = [f"{'directory:':<11} {self.directory}"]
        for entry in self.entries:
            line = f"{entry.label + ':':<11} {entry.path}"
            if entry.note:
                line += f" ({entry.note})"
            if entry.missing:
                line += " MISSING"
            lines.append(line)
        if self.test is None:
            lines.append(f"{'test:':<11} pass --test to list one test's files")
        if self.others:
            total = sum(count for _, count in self.others)
            shown = ", ".join(f"{count} {suffix}" for suffix, count in self.others)
            lines.append(f"{'also:':<11} {total} more files: {shown}")
        return lines


# `atest/library/common.py` starts every test app the suite talks to and logs
# the port it returns; the app writes `test-app/test-app-<port>.log`. Matched by
# library and keyword name, so a keyword renamed there must be renamed here.
_SERVER_LIBRARY = "common"
_STARTS_SERVER = re.compile(r"^Start Test \w*\s*Server$")
_ASSIGNED_PORT = re.compile(r"^\$\{\w+\} = (\d+)$")


def _ports(keyword) -> list[tuple[str, str]]:
    if keyword.owner == _SERVER_LIBRARY and _STARTS_SERVER.match(keyword.name or ""):
        return [
            (keyword.name, assigned.group(1))
            for message in keyword.body
            if (assigned := _ASSIGNED_PORT.match(getattr(message, "message", "") or ""))
        ]
    return [
        port
        for child in keyword.body
        if getattr(child, "type", None) == "KEYWORD"
        for port in _ports(child)
    ]


def _test_apps(directory: Path, test) -> list[Entry]:
    suites = []
    suite = test.parent
    while suite is not None:
        suites.append(suite)
        suite = suite.parent
    return [
        Entry(
            "test-app",
            path,
            f"{keyword} in {suite.full_name}",
            missing=not (directory / path).is_file(),
        )
        for suite in reversed(suites)
        if suite.has_setup
        for keyword, port in _ports(suite.setup)
        for path in [f"test-app/test-app-{port}.log"]
    ]


# A file the test's log links to: a screenshot or any other file a keyword
# logged as a link, and the node log the library names when a keyword fails.
_LINK = re.compile(r'href="([^"]+)"')
_SEE_ALSO = re.compile(r"See also (file://\S+) for additional details")
_REMOTE = re.compile(r"^(?:https?|mailto|data):|^#", re.IGNORECASE)
_KINDS = (
    (re.compile(r"\.(?:png|jpe?g|webp|gif)$", re.IGNORECASE), "screenshot"),
    (re.compile(r"(?:^|/)playwright-log[^/]*\.txt$"), "node log"),
    (re.compile(r"\.zip$"), "trace"),
    (re.compile(r"\.(?:webm|mp4)$"), "video"),
)


def _kind(path: str) -> str:
    return next((kind for pattern, kind in _KINDS if pattern.search(path)), "file")


def _links(item, found: list[str]) -> None:
    for child in getattr(item, "body", None) or []:
        if getattr(child, "type", None) == "MESSAGE":
            message = child.message or ""
            for link in _LINK.findall(message) + _SEE_ALSO.findall(message):
                if not _REMOTE.match(link) and link not in found:
                    found.append(link)
        else:
            _links(child, found)


def _resolved(directory: Path, executor: Path, link: str) -> tuple[str, bool]:
    """Where a linked file sits in the artifact, and whether it is there.

    A link is relative to the Executor's output directory, or absolute on the
    runner, which `artifact_relative` cuts back to `atest/output`.
    """
    path = artifact_relative(link)
    for candidate in (directory / path, executor / path, _merged(directory, path)):
        if candidate is not None and candidate.is_file():
            return _relative(candidate, directory), True
    return path, False


_IN_EXECUTOR = re.compile(r"^pabot_results/(\d+)/(.+)$")


def _merged(directory: Path, path: str) -> Path | None:
    """Where pabot's merge put an Executor's file at the top of the artifact.

    `pabot_results/4/browser/screenshot/x.png` becomes
    `browser/screenshot/<run timestamp>-4-x.png`.
    """
    inside = _IN_EXECUTOR.match(path)
    if not inside:
        return None
    executor, rest = inside.groups()
    target = directory / rest
    stamped = re.compile(rf"^\d{{8}}_\d{{6}}-{executor}-{re.escape(target.name)}$")
    if not target.parent.is_dir():
        return None
    return next(
        (f for f in sorted(target.parent.iterdir()) if stamped.match(f.name)), None
    )


def _linked(directory: Path, executor: Path, test) -> list[Entry]:
    links: list[str] = []
    for part in (test.setup, test, test.teardown):
        _links(part, links)
    entries: list[Entry] = []
    for link in links:
        path, there = _resolved(directory, executor, link)
        entry = Entry(_kind(path), path, missing=not there)
        if entry.label == "node log" and not there and _node_process_shared(test):
            entry = _shared_node_log(directory) or entry
        if entry not in entries:
            entries.append(entry)
    if not any(entry.label == "node log" for entry in entries):
        entries.extend(_default_node_log(directory, executor))
    return entries


def _node_process_shared(test) -> bool:
    suite = test.parent
    while suite.parent is not None:
        suite = suite.parent
    return suite.metadata.get("Node Process") == "shared"


def _shared_node_log(directory: Path) -> Entry | None:
    """The log of the one node process every Executor of a pabot Leg talked to.

    The library names the log in its own output directory, where it would be
    had it started the process itself; the shared process writes at the top.
    """
    if (directory / "playwright-log.txt").is_file():
        return Entry("node log", "playwright-log.txt", "the Leg's shared node process")
    return None


def _default_node_log(directory: Path, executor: Path) -> list[Entry]:
    """The node log a test that named none most likely wrote to.

    The library names its log only when one of its keywords fails, so a test
    failing elsewhere names none. The file without a timestamp belongs to the
    library instance that started first, which nearly every test uses; the
    note keeps it from being read as the test's own.
    """
    for candidate in (
        executor / "playwright-log.txt",
        directory / "playwright-log.txt",
    ):
        if candidate.is_file():
            return [
                Entry(
                    "node log", _relative(candidate, directory), "not named by the test"
                )
            ]
    return []


def _find(suite, test_name: str):
    for test in suite.all_tests:
        if test.full_name == test_name:
            return test
    return None


# What a pabot Executor leaves in its own `pabot_results/<n>/`. A serial Leg's
# one Executor leaves the same at the top of the artifact, beside output.xml.
_EXECUTOR_FILES = (
    ("syslog", "syslog.txt"),
    ("stdout", "robot_stdout.out"),
    ("stderr", "robot_stderr.out"),
)


def _executor_of(directory: Path, test_name: str) -> Path:
    """The directory of the Executor that ran the test.

    On a pabot Leg, the Executor whose own output.xml has the test: the merged
    one keeps every Executor's top suite setup under one suite, so what the test
    talked to cannot be read from it. A serial Leg is its own Executor.
    """
    for output in sorted(directory.glob("pabot_results/*/output.xml")):
        if _find(ExecutionResult(output, include_keywords=False).suite, test_name):
            return output.parent
    return directory


def _relative(path: Path, directory: Path) -> str:
    return path.relative_to(directory).as_posix()


def _leg_entries(directory: Path) -> list[Entry]:
    return [
        Entry(label, name)
        for label, name in (("output.xml", "output.xml"), ("log", "log.html"))
        if (directory / name).is_file()
    ]


def _executor_entries(directory: Path, executor: Path) -> list[Entry]:
    if executor == directory:
        entries = [Entry("executor", ".", "serial")]
    else:
        entries = [
            Entry("executor", _relative(executor, directory)),
            Entry("output.xml", _relative(executor / "output.xml", directory)),
        ]
    entries.extend(
        Entry(label, _relative(executor / name, directory))
        for label, name in _EXECUTOR_FILES
        if (executor / name).is_file()
    )
    return entries


def shortlist(directory: Path, test_name: str | None) -> Shortlist:
    """The files in an unpacked artifact worth opening for `test_name`.

    Without a test, only the Leg's own files: which Executor and which links
    matter is a question about one test. Raises `NoSuchTestError` for a Test
    Name the Leg did not run.
    """
    if test_name is None:
        entries = _leg_entries(directory)
        return Shortlist(directory, None, tuple(entries), _others(directory, entries))
    names = [
        test.full_name
        for test in ExecutionResult(
            directory / "output.xml", include_keywords=False
        ).suite.all_tests
    ]
    test_name = resolve(test_name, names, "this Leg")
    executor = _executor_of(directory, test_name)
    test = _find(ExecutionResult(executor / "output.xml").suite, test_name)
    entries = (
        _leg_entries(directory)
        + _executor_entries(directory, executor)
        + _test_apps(directory, test)
        + _linked(directory, executor, test)
    )
    return Shortlist(directory, test_name, tuple(entries), _others(directory, entries))


def _others(directory: Path, entries: list[Entry]) -> tuple[tuple[str, int], ...]:
    listed = {entry.path for entry in entries}
    suffixes = Counter(
        path.suffix.lower() or "(no extension)"
        for path in directory.rglob("*")
        if path.is_file() and _relative(path, directory) not in listed
    )
    return tuple(sorted(suffixes.items(), key=lambda item: (-item[1], item[0])))


def clean(root: Path) -> bool:
    """Removes every artifact fetched for triage. False when there were none."""
    if not root.exists():
        return False
    shutil.rmtree(root)
    return True
