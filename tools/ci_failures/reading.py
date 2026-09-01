"""The database as one Report reads it.

A **Reading** is the rows a Report is allowed to see: the database restricted to
the Report's Window, with Subjects already resolved. Every query that builds one
Report is asked of the same Reading, and a Reading is made once.

## Why it is a thing rather than a path

The restriction is two steps. `window.apply` hangs shadowing views off the
connection so every later statement is windowed without saying so;
`subject.apply` then adds `test_failure` and `fixture_failure`, so no query has
to remember which rows a broken suite fixture wrote. Both have to have happened
before a query runs, and until this type existed the only thing making that so
was that every query went through one private helper - a query written not to
would have been answered from the whole archive, and nothing anywhere would have
noticed.

So the restriction stops being a rule each query has to have followed and
becomes the thing a query is handed. There is no way to ask a question of an
unrestricted database by accident, because the only argument the queries take is
a Reading and the only way to get one is to have done the restriction.

**On the order of the two.** They are applied Window first because that is the
order they read in, not because SQLite requires it: a TEMP view resolves the
names in its body when it is queried rather than when it is created, and resolves
them against `temp` before `main`, so the Subject views sit on the Window's
shadowing views whichever went up first. Measured, both ways round, on a database
holding one Fixture Failure inside a one-day window and one forty days outside
it: one row either way. What the Subject views must not become is **permanent**
ones. A view in `main` resolves its body against `main`, cannot see a temp view,
and the same measurement returns both rows - a windowed report quietly answered
from the whole archive, no error anywhere. That is the hazard `subject.py`
describes, and it is about where the views live rather than about the order they
are made in.

## Why one, and not one per question

Each Reading costs a `connect` - which re-runs the schema - then materialises
the Window: three temp tables, one of them a pass over every result row. Twenty
queries opening their own paid that twenty-one times to answer twenty-one
questions, and the cost grows with the archive while the Report does not.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Any

from . import subject
from .db import connect
from .window import ALL_HISTORY, Window

_SUBJECT_VIEWS = frozenset({"test_failure", "fixture_failure"})


@dataclass(frozen=True)
class Reading:
    """A connection that can only see the Window, and knows what a Subject is."""

    connection: Connection

    def __post_init__(self) -> None:
        """Refuses a connection that has not been through `of`.

        Cheap, once per Report, and it is the one check standing between a
        hand-made connection and a report that silently spans all history.
        """
        present = {
            row[0]
            for row in self.connection.execute(
                "SELECT name FROM temp.sqlite_temp_master WHERE type = 'view'"
            )
        }
        missing = _SUBJECT_VIEWS - present
        if missing:
            raise ValueError(
                f"not a Reading: {', '.join(sorted(missing))} missing. "
                "Build one with `reading.of`, which applies the Window and then "
                "the Subject views, in that order."
            )

    def execute(self, sql: str, parameters: Iterable[Any] = ()) -> Cursor:
        return self.connection.execute(sql, parameters)

    def close(self) -> None:
        self.connection.close()

    # `typing.Self` is 3.11; this repo still supports 3.10.
    def __enter__(self) -> "Reading":  # noqa: PYI034
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def of(db_path: Path, window: Window = ALL_HISTORY) -> Reading:
    """Opens the database and restricts it, in the order the restriction needs."""
    connection = connect(db_path)
    window.apply(connection)
    # After the Window, never before: these read the shadowed table names, so
    # they inherit the restriction rather than reaching past it.
    subject.apply(connection)
    return Reading(connection)
