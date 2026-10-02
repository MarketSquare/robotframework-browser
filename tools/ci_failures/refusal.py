"""Why a task refused, as the exit code that says whose move it is. See ADR 0007.

`UnanswerableError` lives in `db.py` with the reasons a database gives, and is
one of these all the same.
"""


class RefusalError(Exception):
    """A question the tool will not answer, and the exit code that says why."""

    code: int


class MisaskedError(RefusalError):
    """The flags contradict themselves or are not values. No archive could answer."""

    code = 2


class UnreachableError(RefusalError):
    """GitHub could not be reached. Whether to try again is the maintainer's call."""

    code = 3
