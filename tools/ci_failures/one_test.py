"""A test asked for by its Test Name, when the Report has nothing on it.

`of_test` finds no Groups for a typo, for a test that did not run in the
Window, and for a test that ran and never failed, and those used to read alike
as "did not fail". Only the last is an answer; the other two say why there is
none.

The name typed is resolved as `history.resolve` describes.
"""

from dataclasses import dataclass
from pathlib import Path

from . import reading
from .history import resolve
from .queries import outcomes_of_test, test_names
from .reading import UnanswerableError
from .window import ALL_HISTORY, Window


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


class NotInWindowError(UnanswerableError):
    """The test is in the archive and has no Result inside the Window."""


def in_archive(db_path: Path, test: str) -> str:
    """The Test Name `test` is in the archive. Raises `NoSuchTestError`."""
    with reading.of(db_path) as everything:
        return resolve(test, test_names(everything), "the archive")


def never_failed(db_path: Path, test: str, window: Window = ALL_HISTORY) -> NeverFailed:
    """What there is to say about a test `of_test` found no Groups for.

    Raises rather than answering when the name is in no Result at all, or in
    none inside the Window, since either would otherwise read as a healthy test.
    """
    test = in_archive(db_path, test)
    with reading.of(db_path) as everything:
        last_ran = outcomes_of_test(everything, test).last_ran
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
