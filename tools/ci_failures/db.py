"""SQLite access."""

import sqlite3
from pathlib import Path

from .legs import install_of

_SCHEMA = Path(__file__).parent / "schema.sql"


# Columns added after databases existed. `CREATE TABLE IF NOT EXISTS` does
# nothing to a table that is already there, so they are added in place. The
# database is derived and rebuildable, but rebuilding it is three gigabytes of
# downloads and half an hour, and nothing here is worth that.
#
# Only `attempt` can be filled in afterwards from the API, which is what that
# reasoning was originally written about. `executors` and `node_process` come
# out of output.xml and cannot be backfilled at all: a leg ingested before the
# metadata reached CI carries neither, permanently, and they stay NULL rather
# than being invented. `install` is filled in the moment it is added, from the
# artifact name every leg already has; see `fill_installs`. Adding a column still
# means editing this and `schema.sql` both - here for the databases that exist,
# there for the ones that do not - and nothing checks that the two agree.
_ADDED_COLUMNS: dict[str, dict[str, str]] = {
    "leg": {
        "attempt": "INTEGER",
        "executors": "INTEGER",
        "node_process": "TEXT",
        "install": "TEXT",
    },
}


def _add_missing_columns(connection: sqlite3.Connection) -> set[tuple[str, str]]:
    """Adds columns a database predating them has not got, and says which.

    Always nullable and never defaulted: a value invented for a row nobody
    measured is indistinguishable from one that was, which is the failure mode
    worth more than the convenience. A column derived from one already stored is
    not invented, and `connect` fills it in once this says it was added.
    """
    added = set()
    for table, columns in _ADDED_COLUMNS.items():
        present = {
            row["name"] for row in connection.execute(f"PRAGMA table_info({table})")
        }
        if not present:  # the table itself is new; the schema just created it
            continue
        for name, definition in columns.items():
            if name not in present:
                connection.execute(
                    f"ALTER TABLE {table} ADD COLUMN {name} {definition}"
                )
                added.add((table, name))
    return added


def fill_installs(connection: sqlite3.Connection) -> int:
    """The Install of every stored Leg, read from its artifact name.

    Not invented: the name is what ingest reads it from too, and it is what
    selected the artifact in the first place. Returns how many Legs it read.
    """
    legs = connection.execute("SELECT id, artifact_name FROM leg").fetchall()
    connection.executemany(
        "UPDATE leg SET install = ? WHERE id = ?",
        [(install_of(row["artifact_name"]), row["id"]) for row in legs],
    )
    return len(legs)


def connect(db_path: Path) -> sqlite3.Connection:
    """Opens the database, creating it and its schema if it is not there yet."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    # Columns first, then the schema. `schema.sql` carries standalone
    # `CREATE INDEX` statements, so running it first meant that the day anyone
    # added a column here and an index on it there - the obvious pair of edits -
    # every database that already existed raised `no such column` on open, and
    # this is what ingest, every Reading and every report open through.
    #
    # Safe in the other order: on a database that does not exist yet there are
    # no tables to read, `_add_missing_columns` finds nothing and returns, and
    # `executescript` then creates everything including the indexes.
    if ("leg", "install") in _add_missing_columns(connection):
        fill_installs(connection)
    connection.executescript(_SCHEMA.read_text(encoding="utf-8"))
    connection.commit()
    return connection


def ingested_artifact_ids(connection: sqlite3.Connection) -> set[int]:
    """Artifacts there is no reason to download again.

    The ones already in, and the ones that came down and held no output.xml.
    Both are settled; only the ones that failed on the way are worth retrying.
    """
    return {
        row[0]
        for row in connection.execute(
            "SELECT artifact_id FROM leg "
            "UNION SELECT artifact_id FROM unusable_artifact"
        )
    }
