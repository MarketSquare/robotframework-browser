"""A **Subject History**: what the archive recorded about one test or one suite.

A Test Name runs from the top suite down, and the name typed is often less of
it: the test's own name, or the path without `Test.`. It is resolved against
the names where it is looked for - the archive, one Run, one Leg's output.xml -
and a name starting at another top suite is the same test spelled another way,
as a Leg that ran several suite directories at once spells all of its tests.
Anything looser is offered, never assumed: every name ending in what was typed,
all of them, since about one in six test names is shared by tests in different
suites and offering one would be a guess. Only when none ends in it is it taken
for a typo and matched by similarity.

Imports nothing that builds a Report, so the artifact fetch can resolve a name
without it.
"""

from collections.abc import Iterable
from difflib import get_close_matches

from .reading import UnanswerableError

MOST_SUGGESTIONS = 5
CANONICAL_TOP_SUITE = "Test"


class NoSuchTestError(UnanswerableError):
    """No Result where the name was looked for has this Test Name."""

    def __init__(self, test: str, where: str, suggestions: tuple[str, ...]):
        self.suggestions = suggestions
        message = f"No test named {test!r} in {where}."
        if suggestions:
            message += " Did you mean:" + "".join(f"\n  {s}" for s in suggestions)
        super().__init__(message)


def _top(name: str) -> str:
    return name.partition(".")[0]


def _below_top(name: str) -> str:
    return name.partition(".")[2]


def resolve(test: str, names: Iterable[str], where: str) -> str:
    """The name in `names` that `test` is. Raises `NoSuchTestError` with the
    names it may mean when there is none, or more than one."""
    known = sorted(set(names))
    if test in known:
        return test
    same: list[str] = []
    if _top(test) in {CANONICAL_TOP_SUITE, *map(_top, known)}:
        same = [name for name in known if _below_top(name) == _below_top(test)]
        if len(same) == 1:
            return same[0]
    raise NoSuchTestError(test, where, tuple(same) or _close_to(test, known))


def _close_to(name: str, names: list[str]) -> tuple[str, ...]:
    ending = [known for known in names if known.endswith(f".{name}")]
    if ending:
        return tuple(ending)
    return tuple(get_close_matches(name, names, n=MOST_SUGGESTIONS))
