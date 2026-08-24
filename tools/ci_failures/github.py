"""Finds CI runs and their test-result artifacts, through the `gh` CLI.

`gh` so that whoever runs this uses the authentication they already have, and no
token has to be handled here.
"""

import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REPO = "MarketSquare/robotframework-browser"
WORKFLOW_FILE = "on-push.yml"

# The artifact of one matrix leg of the `testing` job, e.g.
# "Test results-ubuntu-latest-3-3.13-22.x". Matched only to pick the right
# artifacts out of the run; what is in them is what gets stored.
_TEST_RESULTS = re.compile(r"^Test results-")


class GhError(RuntimeError):
    pass


@dataclass(frozen=True)
class Run:
    id: int
    event: str
    head_sha: str
    head_branch: str
    created_at: str
    conclusion: str | None
    url: str


@dataclass(frozen=True)
class Artifact:
    id: int
    name: str
    expired: bool
    url: str


def _paginated(endpoint: str, key: str) -> list[dict]:
    """Every page of ``endpoint``, with each page's ``key`` list flattened."""
    args = ["api", "--paginate", "--slurp", endpoint]
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise GhError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    pages = json.loads(result.stdout or "[]")
    if isinstance(pages, dict):
        pages = [pages]
    return [item for page in pages for item in (page.get(key) or [])]


def list_runs(
    repo: str = DEFAULT_REPO,
    branch: str = "main",
    events: tuple[str, ...] = ("push", "schedule"),
    limit: int = 25,
) -> list[Run]:
    """Finished CI runs, newest first.

    Only ``branch`` and only ``events``: a run on a pull request fails because of
    the pull request, which would drown out what we are looking for.
    """
    runs = [
        Run(
            id=item["id"],
            event=item.get("event", event),
            head_sha=item.get("head_sha", ""),
            head_branch=item.get("head_branch", branch),
            created_at=item.get("created_at", ""),
            conclusion=item.get("conclusion"),
            url=item.get("html_url", ""),
        )
        for event in events
        for item in _paginated(
            f"repos/{repo}/actions/workflows/{WORKFLOW_FILE}/runs"
            f"?branch={branch}&event={event}&status=completed&per_page=100",
            "workflow_runs",
        )
    ]
    runs.sort(key=lambda run: run.created_at, reverse=True)
    return runs[:limit]


def list_test_artifacts(run_id: int, repo: str = DEFAULT_REPO) -> list[Artifact]:
    return [
        Artifact(
            id=item["id"],
            name=item["name"],
            expired=bool(item.get("expired")),
            url=f"https://github.com/{repo}/actions/runs/{run_id}/artifacts/{item['id']}",
        )
        for item in _paginated(
            f"repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100", "artifacts"
        )
        if _TEST_RESULTS.match(item["name"])
    ]


DOWNLOAD_ATTEMPTS = 3


def download_artifact(
    artifact_id: int, destination: Path, repo: str = DEFAULT_REPO
) -> Path:
    """Downloads one artifact, retrying the transient failures.

    These are ten megabyte downloads over a network, and a connection reset
    partway through a long ingest is ordinary rather than exceptional.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    last_error = ""
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        with destination.open("wb") as handle:
            result = subprocess.run(
                ["gh", "api", f"repos/{repo}/actions/artifacts/{artifact_id}/zip"],
                stdout=handle,
                stderr=subprocess.PIPE,
                check=False,
            )
        if result.returncode == 0:
            return destination
        destination.unlink(missing_ok=True)
        last_error = result.stderr.decode(errors="replace").strip()
        if attempt < DOWNLOAD_ATTEMPTS:
            time.sleep(2 * attempt)
    raise GhError(
        f"Downloading artifact {artifact_id} failed after "
        f"{DOWNLOAD_ATTEMPTS} attempts: {last_error}"
    )
