"""A test asked for by its Test Name, when the Report has nothing on it.

`of_test` finds no Groups for a typo, for a test that did not run in the
Window, and for a test that ran and never failed, and those used to read alike
as "did not fail". Only the last is an answer; the other two say why there is
none.

A Test Name runs from the top suite down, and the name typed is often less of
it: the test's own name, or the path without `Test.`. Every Test Name ending in
what was typed is offered, all of them, since about one in six test names is
shared by tests in different suites and offering one would be a guess. Only
when none ends in it is it taken for a typo and matched by similarity.
"""

from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path

from . import reading
from .queries import outcomes_of_test, test_names
from .report import UnanswerableError
from .window import ALL_HISTORY, Window

MOST_SUGGESTIONS = 5


def close_to(name: str, names: list[str]) -> tuple[str, ...]:
    ending = sorted(known for known in names if known.endswith(f".{name}"))
    if ending:
        return tuple(ending)
    return tuple(get_close_matches(name, names, n=MOST_SUGGESTIONS))


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" + ("" if count == 1 else "s")


@dataclass(frozen=True)
class NeverFailed:
    """A test that ran inside the Window and has no Group there."""

    test: str
    window: str
    ran: int
    failed: int
    skipped: int

    def line(self) -> str:
        return (
            f"{self.test!r} ran {_plural(self.ran, 'time')} in {self.window}: "
            f"{_plural(self.failed, 'failure')}, {_plural(self.skipped, 'skip')}."
        )


class NoSuchTestError(UnanswerableError):
    """No Result anywhere in the archive has this Test Name."""

    def __init__(self, test: str, suggestions: tuple[str, ...]):
        self.suggestions = suggestions
        message = f"No test named {test!r} in the archive."
        if suggestions:
            message += " Did you mean:" + "".join(f"\n  {s}" for s in suggestions)
        super().__init__(message)


class NotInWindowError(UnanswerableError):
    """The test is in the archive and has no Result inside the Window."""


def never_failed(db_path: Path, test: str, window: Window = ALL_HISTORY) -> NeverFailed:
    """What there is to say about a test `of_test` found no Groups for.

    Raises rather than answering when the name is in no Result at all, or in
    none inside the Window, since either would otherwise read as a healthy test.
    """
    with reading.of(db_path) as everything:
        names = test_names(everything)
        last_ran = outcomes_of_test(everything, test).last_ran
    if test not in names:
        raise NoSuchTestError(test, close_to(test, names))
    with reading.of(db_path, window) as db:
        outcomes = outcomes_of_test(db, test)
    if not outcomes.ran:
        raise NotInWindowError(
            f"{test!r} did not run in {window.label}; it last ran on "
            f"{(last_ran or '')[:10]}. Widen --days."
        )
    return NeverFailed(
        test=test,
        window=window.label,
        ran=outcomes.ran,
        failed=outcomes.failed,
        skipped=outcomes.skipped,
    )
