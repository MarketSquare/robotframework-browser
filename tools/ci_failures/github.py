"""Finds CI runs and their test-result artifacts, through the `gh` CLI.

`gh` so that whoever runs this uses the authentication they already have, and no
token has to be handled here.
"""

import json
import re
import subprocess
import time
from dataclasses import dataclass, replace
from pathlib import Path

# Not parameters. This tool reads this project's CI, imports this repository's
# library to resolve where a keyword lives, and ships with the repository - so a
# repository, a branch or an event that could vary is a door onto data the rest
# of it would then be quietly wrong about.
REPO = "MarketSquare/robotframework-browser"
WORKFLOW_FILE = "on-push.yml"
BRANCH = "main"
# A failure from a run where somebody was changing the code is not evidence
# about the library, which is what these two events select for. See
# `docs/adr/0002-only-runs-nobody-was-changing.md`.
EVENTS = ("push", "schedule")

# `on-release.yml` also runs the suite and is deliberately not read. It would
# need more than another event: it is a different workflow file, it uploads under
# `Clean_install_results_*` rather than `Test results-*`, and its Linux legs run
# `--smoke`, so its results are a different set of tests and would not share a
# denominator with these. Releases are monthly besides, which is too few to
# carry a rate.

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
    # How many times the run was started. Above 1 means someone re-ran a failed
    # job by hand; nothing here retries on its own. Comes back with the run
    # listing, so knowing it costs no extra request.
    run_attempt: int = 1


@dataclass(frozen=True)
class Artifact:
    id: int
    name: str
    expired: bool
    url: str
    created_at: str = ""
    # Which attempt uploaded it. Filled by `with_attempts`; None until then.
    attempt: int | None = None


def _api(endpoint: str) -> dict:
    result = subprocess.run(
        ["gh", "api", endpoint], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise GhError(f"gh api {endpoint} failed: {result.stderr.strip()}")
    return json.loads(result.stdout or "{}")


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


def _run(item: dict, event: str = "") -> Run:
    return Run(
        id=item["id"],
        event=item.get("event", event),
        head_sha=item.get("head_sha", ""),
        head_branch=item.get("head_branch", BRANCH),
        created_at=item.get("created_at", ""),
        conclusion=item.get("conclusion"),
        url=item.get("html_url", ""),
        run_attempt=int(item.get("run_attempt") or 1),
    )


def get_run(run_id: int) -> Run:
    return _run(_api(f"repos/{REPO}/actions/runs/{run_id}"))


def list_runs(limit: int = 25) -> list[Run]:
    """Finished CI runs on `main` from `push` and `schedule`, newest first."""
    runs = [
        _run(item, event=event)
        for event in EVENTS
        for item in _paginated(
            f"repos/{REPO}/actions/workflows/{WORKFLOW_FILE}/runs"
            f"?branch={BRANCH}&event={event}&status=completed&per_page=100",
            "workflow_runs",
        )
    ]
    runs.sort(key=lambda run: run.created_at, reverse=True)
    return runs[:limit]


def list_test_artifacts(run_id: int) -> list[Artifact]:
    return [
        Artifact(
            id=item["id"],
            name=item["name"],
            expired=bool(item.get("expired")),
            url=f"https://github.com/{REPO}/actions/runs/{run_id}/artifacts/{item['id']}",
            created_at=item.get("created_at", ""),
        )
        for item in _paginated(
            f"repos/{REPO}/actions/runs/{run_id}/artifacts?per_page=100", "artifacts"
        )
        if _TEST_RESULTS.match(item["name"])
    ]


def attempt_starts(run: Run) -> list[tuple[int, str]]:
    """When each attempt of a run began, oldest first.

    Attempt 1 began when the run did, so a run nobody re-ran costs no request at
    all, which is nearly all of them. The rest are one request each and none of
    them downloads anything.
    """
    starts = [(1, run.created_at)]
    for number in range(2, max(run.run_attempt, 1) + 1):
        attempt = _api(f"repos/{REPO}/actions/runs/{run.id}/attempts/{number}")
        starts.append(
            (number, attempt.get("run_started_at") or attempt.get("created_at") or "")
        )
    return starts


def with_attempts(
    artifacts: list[Artifact], starts: list[tuple[int, str]]
) -> list[Artifact]:
    """Which attempt uploaded each artifact.

    GitHub will not say directly. The artifact carries no attempt number, and
    `/runs/{id}/attempts/{n}/artifacts` does not exist - it answers 404. What is
    available is time: the attempts of one run do not overlap, so an artifact
    belongs to the last attempt that had already started when it was created.
    Checked against a run that was re-run twice, where the three uploads of one
    leg fall one inside each attempt's window with minutes to spare.

    An artifact with no creation time falls to the first attempt rather than the
    last, so an unknown lands on the reading that claims least.
    """
    ordered = sorted(starts, key=lambda start: start[1])
    resolved = []
    for artifact in artifacts:
        attempt = ordered[0][0] if ordered else 1
        for number, started in ordered:
            if artifact.created_at >= started:
                attempt = number
        resolved.append(replace(artifact, attempt=attempt))
    return resolved


DOWNLOAD_ATTEMPTS = 3


def download_artifact(artifact_id: int, destination: Path) -> Path:
    """Downloads one artifact, retrying the transient failures.

    These are ten megabyte downloads over a network, and a connection reset
    partway through a long ingest is ordinary rather than exceptional.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    last_error = ""
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        with destination.open("wb") as handle:
            result = subprocess.run(
                ["gh", "api", f"repos/{REPO}/actions/artifacts/{artifact_id}/zip"],
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
