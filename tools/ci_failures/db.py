"""SQLite access."""

import sqlite3
from pathlib import Path

_SCHEMA = Path(__file__).parent / "schema.sql"


def connect(db_path: Path) -> sqlite3.Connection:
    """Opens the database, creating it and its schema if it is not there yet."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(_SCHEMA.read_text(encoding="utf-8"))
    connection.commit()
    return connection


def ingested_artifact_ids(connection: sqlite3.Connection) -> set[int]:
    return {row[0] for row in connection.execute("SELECT artifact_id FROM leg")}
