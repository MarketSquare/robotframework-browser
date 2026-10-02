"""The Legs of one Run that ran a test, for choosing a **Control**.

`inv ci-artifact --run --test` without `--leg`. A failure limited to one
Configuration needs a passing Leg of the same Run beside it, and with four
shards most of a Run's Legs never ran the test. Only the database knows which
did, so this reads it and never GitHub; a Run it does not hold is refused
rather than listed from GitHub, which could not say where the test passed.
See ADR 0006.
"""

from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from . import reading
from .history import resolve
from .legs import leg_name
from .queries import (
    SUITE_BROKE,
    RunLeg,
    ingested_run,
    legs_of_run,
    test_names_of_run,
)
from .reading import UnanswerableError

# Failures first: they are what the Controls are compared against.
_ORDER = ("fail", "mixed", SUITE_BROKE, "skip", "pass")


class NotIngestedError(UnanswerableError):
    """The database holds no Run with this id."""

    def __init__(self, run: int):
        super().__init__(f"Run {run} is not in the database; `inv ci-ingest` first.")


def _label(outcome: str) -> str:
    return "control" if outcome == "pass" else outcome


def _attempt(leg: RunLeg) -> str:
    return "?" if leg.attempt is None else str(leg.attempt)


@dataclass(frozen=True)
class RunListing:
    """Every Leg of one Run that ran one test, by Install, Controls marked."""

    run: int
    commit: str | None
    test: str
    legs: tuple[RunLeg, ...]

    def lines(self) -> list[str]:
        ordered = sorted(
            self.legs,
            key=lambda leg: (
                leg.install or "",
                _ORDER.index(leg.outcome),
                leg_name(leg.artifact_name),
                leg.attempt or 0,
            ),
        )
        label_width = max(len(_label(leg.outcome)) for leg in ordered)
        name_width = max(len(leg_name(leg.artifact_name)) for leg in ordered)
        lines = [f"Run {self.run} · commit {(self.commit or '?')[:7]} · {self.test}"]
        for install, legs in groupby(ordered, key=lambda leg: leg.install):
            lines.append(install or "(install unknown)")
            lines.extend(
                f"  {_label(leg.outcome):<{label_width}}  "
                f"{leg_name(leg.artifact_name):<{name_width}}   "
                f"--attempt {_attempt(leg)}"
                for leg in legs
            )
        lines.append(
            f'fetch one: inv ci-artifact --run {self.run} --leg "<leg>" '
            f'--attempt <n> --test "{self.test}"'
        )
        if any(leg.attempt is None for leg in ordered):
            lines.append(
                "attempt ? is not yet resolved: try --attempt 1, or "
                "`inv ci-backfill-attempts` first."
            )
        return lines


def of_run(db_path: Path, run: int, test: str) -> RunListing:
    """The Legs of `run` that ran `test`. Raises `NotIngestedError` for a Run
    the database lacks, and `NoSuchTestError` for a test the Run lacks."""
    with reading.of(db_path) as db:
        found = ingested_run(db, run)
        if found is None:
            raise NotIngestedError(run)
        test = resolve(test, test_names_of_run(db, run), f"Run {run}")
        legs = legs_of_run(db, run, test)
    return RunListing(run, found.commit, test, tuple(legs))
