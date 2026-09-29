"""One Leg's artifact, fetched again for triage.

Ingest keeps nothing but the parsed rows, so the screenshots, `log.html` and
`playwright-log.txt` behind an Occurrence have to come down again once a failure
turns out to deserve them. Downloaded on demand rather than kept: by the time a
failure matters it is simpler to fetch it again than to have stored every leg.

Unpacked under `ci_failures/artifacts/`, which is gitignored, and removed with
`clean` once the triage is done.
"""

import re
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from . import github
from .legs import leg_name


@dataclass(frozen=True)
class Unpacked:
    """Where one Leg's artifact was unpacked, and the files worth opening."""

    directory: Path
    output_xml: Path | None
    logs: tuple[Path, ...]
    node_logs: tuple[Path, ...]
    screenshots: tuple[Path, ...]


class NoSuchLegError(LookupError):
    """The run has no test artifact for that Leg."""


def _directory(root: Path, run: int, leg: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", leg_name(leg)).strip("-")
    return root / f"{run}-{slug}"


def _found(directory: Path) -> Unpacked:
    output_xml = directory / "output.xml"
    return Unpacked(
        directory=directory,
        output_xml=output_xml if output_xml.exists() else None,
        logs=tuple(sorted(directory.rglob("log.html"))),
        node_logs=tuple(sorted(directory.rglob("playwright-log*.txt"))),
        screenshots=tuple(sorted(directory.rglob("*.png"))),
    )


def fetch(run: int, leg: str, root: Path) -> Unpacked:
    """One Leg's artifact, unpacked under `root`.

    `leg` is the Leg as the report names it, or the artifact's own name. Raises
    `NoSuchLegError` when the run has no such Leg, and `github.GhError` when GitHub
    cannot be reached.
    """
    directory = _directory(root, run, leg)
    if directory.is_dir():
        return _found(directory)
    wanted = leg_name(leg)
    artifacts = github.list_test_artifacts(run)
    artifact = next((a for a in artifacts if leg_name(a.name) == wanted), None)
    if artifact is None:
        known = "\n  ".join(sorted(leg_name(a.name) for a in artifacts))
        raise NoSuchLegError(f"Run {run} has no leg {leg!r}. It has:\n  {known}")
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=root) as work_dir:
        work = Path(work_dir)
        zip_path = github.download_artifact(artifact.id, work / "artifact.zip")
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(work / "unpacked")
        # Moved into place only once whole, so a download cut off halfway is
        # fetched again rather than reused.
        (work / "unpacked").rename(directory)
    return _found(directory)


def clean(root: Path) -> bool:
    """Removes every artifact fetched for triage. False when there were none."""
    if not root.exists():
        return False
    shutil.rmtree(root)
    return True
