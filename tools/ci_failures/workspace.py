"""The **Workspace**: the directory a database is in, and what is derived from it.

The Snapshot, the page and the artifacts fetched for triage all live beside the
database, so another `--db` is another Workspace and nothing of one leaks into
the other. All of it is safe to delete, which is why `known_causes.json` is not
here: it is the one thing no rebuild restores, and it belongs to the checkout.
"""

from pathlib import Path

DEFAULT_DATABASE = (
    Path(__file__).resolve().parents[2] / "ci_failures" / "ci_failures.sqlite3"
)


def database(db: str | Path | None) -> Path:
    """The database `--db` names, or the one at the repository root."""
    return Path(db) if db else DEFAULT_DATABASE


def artifacts(db_path: Path) -> Path:
    return db_path.parent / "artifacts"


def page(db_path: Path) -> Path:
    return db_path.parent / "ci_report.html"


def snapshot(db_path: Path) -> Path:
    return db_path.parent / "last_report.json"
