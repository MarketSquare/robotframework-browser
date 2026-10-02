"""Whether a Known Cause's fix held.

A fix is **Verified** once seven days of Runs containing it saw its Group no
more. Counted from the first ingested Run whose commit contains `fixed_by`, and
"contains" is asked of git rather than of the calendar: a Run on a commit from
before the fix can be created after it, and its failure says nothing about the
fix. So `fixed_by` has to be a commit SHA; prose there is reported as `no SHA`
rather than guessed at. And the SHA on `main`: a rebase or squash gives the fix
another one there, and the branch commit, contained in no Run, would read as
`no runs yet` forever. That is reported as `not on main`.

Read-only. Writing `fix_verified` is `annotations.mark_verified`, run by the
maintainer with `inv ci-verify-fixes --mark` and never as a side effect.

Every entry is also checked for being an **orphan** - matching no Group or
Fixture Failure in the archive - whatever its state. A mistyped signature, or
one the masking rules in `parse.py` have since changed, matches nothing, and an
entry that matches nothing would otherwise read as a fix with zero recurrences.
An orphan whose test is in no Result at all says so, with the Test Names it
may have meant, since there the name is wrong rather than the signature.
"""

import re
import subprocess
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Protocol

from . import reading
from .annotations import cause_key, known_cause_entries
from .history import NoSuchTestError, resolve
from .queries import (
    SubjectFailure,
    failing_subjects,
    failures_of_subject,
    runs_of_subject,
    test_names,
)

DAYS = 7

_SHA = re.compile(r"[0-9a-fA-F]{7,40}")


class Status:
    WAITING = "waiting"
    READY = "ready"
    RECURRED = "recurred"
    NO_RUNS = "no runs yet"
    ORPHAN = "orphan"
    NO_SHA = "no SHA"
    NOT_ON_MAIN = "not on main"


MAIN = "origin/main"


class History(Protocol):
    def resolves(self, sha: str) -> bool: ...

    def on_main(self, sha: str) -> bool: ...

    def contains(self, commit: str, fix: str) -> bool | None:
        """None when the commit is not in this clone, so nobody can tell."""
        ...


class Git:
    """The history of the working copy the tool runs from."""

    def __init__(self, root: Path):
        self.root = root
        self._contains: dict[tuple[str, str], bool | None] = {}

    def _git(self, *args: str) -> int:
        return subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, check=False
        ).returncode

    def resolves(self, sha: str) -> bool:
        return self._git("cat-file", "-e", f"{sha}^{{commit}}") == 0

    def on_main(self, sha: str) -> bool:
        return self._git("merge-base", "--is-ancestor", sha, MAIN) == 0

    def contains(self, commit: str, fix: str) -> bool | None:
        key = (commit, fix)
        if key not in self._contains:
            code = self._git("merge-base", "--is-ancestor", fix, commit)
            self._contains[key] = {0: True, 1: False}.get(code)
        return self._contains[key]


@dataclass(frozen=True)
class OtherFailure:
    """The same Subject failing after the fix on a different Error Signature."""

    signature: str | None
    occurrences: int


@dataclass(frozen=True)
class Verification:
    """One Known Cause, and where its fix stands."""

    subject: str
    signature: str | None
    status: str
    reference: str | None = None
    fixed_by: str | None = None
    days: int = 0
    runs: int = 0
    recurrences: int = 0
    #: (run id, run url) of every Run the Group came back in.
    recurred_in: tuple[tuple[int, str | None], ...] = ()
    other_failures: tuple[OtherFailure, ...] = ()
    #: Runs on commits this clone does not have, so neither in nor out.
    unknown_commits: int = 0
    #: For an orphan naming a test in no Result: the Test Names it may mean.
    no_such_test: bool = False
    suggestions: tuple[str, ...] = ()
    key: tuple = field(default=(), compare=False)

    def line(self) -> str:
        if self.status == Status.NO_SHA:
            if _SHA.fullmatch(self.fixed_by or ""):
                return f"no SHA: {self.fixed_by} is not a commit in this clone"
            return "no SHA: fixed_by is prose, not a commit SHA"
        if self.status == Status.NOT_ON_MAIN:
            return (
                f"not on main: {self.fixed_by} is not on {MAIN}; record the SHA "
                "the fix has on main, or `git fetch origin main`"
            )
        if self.no_such_test:
            return f"orphan: no test named {self.subject!r} in the archive"
        counted = f"{self.runs} runs, {self.recurrences} recurrences"
        return {
            Status.WAITING: f"waiting {self.days}/{DAYS} days, {counted}",
            Status.READY: f"ready: {self.days} days, {counted}",
            Status.RECURRED: f"recurred: {self.recurrences} after fix",
            Status.NO_RUNS: "no runs yet: the fix is in no ingested run",
            Status.ORPHAN: "orphan: matches no Group in the database",
        }[self.status]

    @property
    def issue(self) -> str | None:
        """The issue number, when the reference is a GitHub issue."""
        found = re.search(r"/issues/(\d+)", self.reference or "")
        return found.group(1) if found else None


def check(
    db_path: Path,
    known_causes: Path | None = None,
    *,
    history: History,
    today: date,
) -> list[Verification]:
    """Every orphan, and every fixed and not yet verified Known Cause."""
    checked = []
    with reading.of(db_path) as db:
        present = failing_subjects(db)
        names = test_names(db)
        for subject, entry in known_cause_entries(known_causes):
            fix = entry.get("fixed_by")
            base = Verification(
                subject=subject,
                signature=entry.get("signature"),
                status=Status.ORPHAN,
                reference=entry.get("reference"),
                fixed_by=fix,
                key=cause_key(subject, entry.get("signature")),
            )
            if base.key not in present:
                if entry.get("test"):
                    try:
                        resolve(subject, names, "the archive")
                    except NoSuchTestError as unknown:
                        base = replace(
                            base, no_such_test=True, suggestions=unknown.suggestions
                        )
                checked.append(base)
            elif not fix or entry.get("fix_verified"):
                continue
            elif not _SHA.fullmatch(fix) or not history.resolves(fix):
                checked.append(replace(base, status=Status.NO_SHA))
            elif not history.on_main(fix):
                checked.append(replace(base, status=Status.NOT_ON_MAIN))
            else:
                checked.append(_since_fix(db, base, fix, history, today))
    return checked


def _since_fix(
    db: reading.Reading, base: Verification, fix: str, history: History, today: date
) -> Verification:
    containing = {}
    unknown = 0
    for run in runs_of_subject(db, base.subject):
        contains = history.contains(run.head_sha, fix) if run.head_sha else None
        if contains is None:
            unknown += 1
        elif contains:
            containing[run.run_id] = run
    if not containing:
        return replace(base, status=Status.NO_RUNS, unknown_commits=unknown)

    first = min(run.created_at or "" for run in containing.values())
    days = (today - date.fromisoformat(first[:10])).days
    after = [f for f in failures_of_subject(db, base.subject) if f.run_id in containing]
    recurred = [f for f in after if f.signature_key == base.key[1]]
    recurrences = sum(f.occurrences for f in recurred)
    others: dict[str, list[SubjectFailure]] = {}
    for failure in after:
        if failure.signature_key != base.key[1]:
            others.setdefault(failure.signature_key, []).append(failure)
    if recurrences:
        status = Status.RECURRED
    elif days >= DAYS:
        status = Status.READY
    else:
        status = Status.WAITING
    return replace(
        base,
        status=status,
        days=days,
        runs=len(containing),
        recurrences=recurrences,
        recurred_in=tuple((f.run_id, f.run_url) for f in recurred),
        other_failures=tuple(
            OtherFailure(
                signature=failures[0].error_signature,
                occurrences=sum(f.occurrences for f in failures),
            )
            for failures in others.values()
        ),
        unknown_commits=unknown,
    )
