"""What is already known about a failure, and what changed since last time.

Two things the database cannot hold, for opposite reasons.

A conclusion someone reached by reading an artifact is not derived from
anything, so `known_causes.json` sits next to this code and is matched against
groups at report time. It is gitignored, which is a deliberate choice and not
the obvious one: it makes the file the only thing here that no rebuild and no
download can restore. The reasoning is that this tool is read by one maintainer
over a week or two of CI at a time, and a cause worth recording is a cause worth
fixing - an annotation that quietly excuses a failure is worth less than the
fix, and the fix is in the git history anyway.

The snapshot of the last report is the opposite case - entirely derived, worth
nothing once it is stale, and beside the database for that reason rather than
for any reason about version control.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

KNOWN_CAUSES = Path(__file__).parent / "known_causes.json"

# Beside the database, not in the repository: a snapshot is derived and worth
# nothing to anyone but the next run of the report.
SNAPSHOT_NAME = "last_report.json"


def _key(test: str | None, signature: str | None) -> tuple:
    """The same case-folded key groups are made on."""
    return (test or "", (signature or "").lower())


def load_known_causes(path: Path | None = None) -> dict[tuple, dict]:
    """Causes already established, keyed the way groups are.

    A missing or unreadable file is not an error: nothing here has been
    explained yet is the normal starting state, and a report that refuses to
    render because an annotation file is malformed is worse than one that
    renders without the annotations.
    """
    source = path or KNOWN_CAUSES
    try:
        entries = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(entries, list):
        return {}
    known = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        subject = entry.get("test") or entry.get("suite")
        if not subject:
            continue
        known[_key(subject, entry.get("signature"))] = {
            "cause": entry.get("cause"),
            "reference": entry.get("reference"),
            "recorded": entry.get("recorded"),
            "fixed_by": entry.get("fixed_by"),
            "fix_verified": entry.get("fix_verified"),
        }
    return known


def known_cause_for(known: dict[tuple, dict], subject: str, signature: str | None):
    """The recorded cause for one group, or None."""
    return known.get(_key(subject, signature))


@dataclass
class Change:
    """One group, and how it differs from the last report."""

    subject: str
    signature: str | None
    was: int | None
    now: int | None

    @property
    def kind(self) -> str:
        if self.was is None:
            return "new"
        if self.now is None:
            return "gone"
        if self.now > self.was:
            return "grew"
        return "shrank"


def snapshot_path(db_path: Path) -> Path:
    return db_path.parent / SNAPSHOT_NAME


def read_snapshot(db_path: Path) -> dict | None:
    try:
        data = json.loads(snapshot_path(db_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def write_snapshot(db_path: Path, entries: list[tuple[str, str | None, int]]) -> Path:
    """Records what this report said, to be the baseline for the next one.

    Written only when asked for, never as a side effect of rendering. A report
    that moved its own baseline would answer differently the second time it was
    run on unchanged data, and "what changed" would then mean "what changed
    since I last looked at this", which is not a question about CI.
    """
    destination = snapshot_path(db_path)
    destination.write_text(
        json.dumps(
            {
                "taken_at": datetime.now(timezone.utc).isoformat(),
                "groups": [
                    {"subject": subject, "signature": signature, "failures": failures}
                    for subject, signature, failures in entries
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return destination


def compare(
    snapshot: dict | None, entries: list[tuple[str, str | None, int]]
) -> dict | None:
    """What is new, gone, or moved since the snapshot was taken.

    None when there is no snapshot, which is a different thing from "nothing
    changed" and has to read as one.
    """
    if not snapshot:
        return None
    before = {
        _key(g.get("subject"), g.get("signature")): g.get("failures")
        for g in snapshot.get("groups", [])
        if isinstance(g, dict)
    }
    after = {
        _key(subject, signature): failures for subject, signature, failures in entries
    }
    labels = {
        _key(subject, signature): (subject, signature)
        for subject, signature, failures in entries
    }
    for group in snapshot.get("groups", []):
        if isinstance(group, dict):
            key = _key(group.get("subject"), group.get("signature"))
            labels.setdefault(
                key, (str(group.get("subject") or ""), group.get("signature"))
            )

    changes = []
    for key in sorted(set(before) | set(after)):
        was, now = before.get(key), after.get(key)
        if was == now:
            continue
        subject, signature = labels.get(key, (key[0], None))
        changes.append(Change(subject, signature, was, now))

    return {
        "compared_with": snapshot.get("taken_at"),
        "new": [_change_dict(c) for c in changes if c.kind == "new"],
        "gone": [_change_dict(c) for c in changes if c.kind == "gone"],
        "grew": [_change_dict(c) for c in changes if c.kind == "grew"],
        "shrank": [_change_dict(c) for c in changes if c.kind == "shrank"],
    }


def _change_dict(change: Change) -> dict:
    entry: dict = {"subject": change.subject, "signature": change.signature}
    if change.was is not None:
        entry["was"] = change.was
    if change.now is not None:
        entry["now"] = change.now
    return entry
