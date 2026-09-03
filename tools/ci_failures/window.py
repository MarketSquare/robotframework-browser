"""Which runs a report is about.

The database is an archive and keeps growing; a report is a question asked of
some part of it. `--days 3` asks "what has failed since the day before
yesterday", which is the shape of the question you ask after fixing something:
the failures from before the fix are exactly what must not be counted.

The window is a hard scope. Every count, rate, denominator and total in a
windowed report comes from runs inside it, and a test that did not fail inside
it does not appear at all. There is no all-time figure anywhere in the document,
because a report that mixed the two would have a header and denominators that
disagree, and the reader has no way to tell which number is which.

It is a scope and not a promise. A window can only restrict what has been
ingested, so `--days 60` over an archive holding sixteen days answers over
sixteen: the label says what was asked for and `since` says what was there, and
they can disagree by any amount. That matters most where it is least visible -
just after a rebuild, when the archive is a few days deep and an ordinary
`--days 14` is quietly answered on half of them.

## How it is applied

Not by adding a predicate to each of the thirty queries in `report.py`. Those
queries reach the run through CTEs, self joins and correlated subqueries, and
several of them touch `test_result` without joining `leg` at all - `messages_by_test`
and `co_failures` among them. Thirty hand-written predicates is thirty chances
to leave one out, and a report where a single section quietly spans all history
is worse than one that fails outright.

Instead the window is applied once, to the connection. SQLite resolves an
unqualified table name against `temp` before `main`, so a TEMP VIEW named `run`
shadows the real table for every statement on that connection - inside CTEs and
subqueries too. Four such views, each restricted through the one before it, and
the queries themselves need no window at all. They cannot forget it and they
cannot disagree about it.

Only `report.py` opens a windowed connection. Ingest writes through the real
tables, and a view would refuse the writes anyway.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from sqlite3 import Connection

# The run ids in the window, then the leg and result ids that hang off them.
# Materialised rather than nested as views: `test_result` is the big table -
# 74k rows in the working database - and resolving it through two layers of view
# for every one of the thirty queries costs more than one pass to build a keyed
# temp table does.
_MATERIALISE = (
    ("window_run", "SELECT id FROM main.run WHERE created_at >= ?"),
    (
        "window_leg",
        "SELECT id FROM main.leg WHERE run_id IN (SELECT id FROM window_run)",
    ),
    (
        "window_result",
        "SELECT id FROM main.test_result WHERE leg_id IN (SELECT id FROM window_leg)",
    ),
)

# Shadowing views, in dependency order. Each names its table with `main.` so it
# reads the real one rather than itself.
_VIEWS = (
    ("run", "SELECT * FROM main.run WHERE id IN (SELECT id FROM window_run)"),
    ("leg", "SELECT * FROM main.leg WHERE id IN (SELECT id FROM window_leg)"),
    # By leg rather than by its own id, though `window_result` holds exactly the
    # same rows. `idx_result_leg` turns this into a few hundred index lookups;
    # matching 74k ids against a temp table instead cost six times as much on a
    # window wide enough to hold them all.
    (
        "test_result",
        "SELECT * FROM main.test_result WHERE leg_id IN (SELECT id FROM window_leg)",
    ),
    (
        "log_message",
        (
            "SELECT * FROM main.log_message "
            "WHERE test_result_id IN (SELECT id FROM window_result)"
        ),
    ),
)


@dataclass(frozen=True)
class Window:
    """A span of whole local days, resolved once.

    Resolved once and passed down rather than recomputed per query: a report run
    across midnight would otherwise window its sections against two different
    days and quietly disagree with itself.

    `cutoff` is the UTC instant local midnight of `first_day` fell on, which is
    what `run.created_at` is comparable with. The local dates are kept beside it
    because they are what the report says out loud, and deriving them back from
    the cutoff would reintroduce the timezone question at the point of display.
    """

    days: int | None = None
    cutoff: str | None = None  # UTC, 'YYYY-MM-DDTHH:MM:SSZ'
    first_day: date | None = None  # local
    last_day: date | None = None  # local

    @property
    def bounded(self) -> bool:
        return self.cutoff is not None

    @property
    def label(self) -> str:
        """What the report prints to say what it covers."""
        if not self.bounded:
            return "all history"
        span = (
            str(self.first_day)
            if self.first_day == self.last_day
            else f"{self.first_day}..{self.last_day}"
        )
        return f"--days {self.days} ({span} local)"

    def apply(self, connection: Connection) -> None:
        """Restricts every table a report reads to this window.

        A no-op when unbounded: with nothing to exclude, the queries should meet
        the real tables rather than a view that copies every row of them.
        """
        if not self.bounded:
            return
        for name, select in _MATERIALISE:
            connection.execute(f"CREATE TEMP TABLE {name} (id INTEGER PRIMARY KEY)")
            connection.execute(
                f"INSERT INTO {name} {select}",
                (self.cutoff,) if "?" in select else (),
            )
        for name, select in _VIEWS:
            connection.execute(f"CREATE TEMP VIEW {name} AS {select}")


ALL_HISTORY = Window()


def of_days(days: int, now: datetime | None = None) -> Window:
    """The last `days` whole local days, today included.

    1 is today, 2 is today and yesterday. Counting calendar days rather than
    24-hour periods is the point: "since I fixed it on Tuesday" is a question
    about days, and a rolling window would answer a slightly different one every
    hour of the day you asked it.

    The boundary is local midnight converted to UTC once. Converting each row
    the other way - `datetime(created_at, 'localtime')` - would give the same
    answer and give up the index on a table read thirty times per report.
    """
    if days < 1:
        raise ValueError(f"--days must be 1 or more, got {days}")
    here = now or datetime.now().astimezone()
    last_day = here.date()
    first_day = last_day - timedelta(days=days - 1)
    # Naive, then localised: `astimezone` applies the offset in force on that
    # date, so a window spanning a DST change is still whole days.
    start = datetime.combine(first_day, time.min).astimezone()
    return Window(
        days=days,
        # Spelled the way `run.created_at` is, so the comparison is the string
        # one SQLite is already indexing.
        cutoff=start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        first_day=first_day,
        last_day=last_day,
    )
