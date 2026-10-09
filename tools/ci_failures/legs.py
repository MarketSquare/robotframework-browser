"""What an artifact's name says about the Leg that uploaded it.

The one place that knows how each job of `on-push.yml` names its test-result
artifact. Selecting the artifacts to ingest, recording each Leg's Install and
naming a Leg in the report all read the name, and they used to do it in three
places that could each drift from the workflow on their own.

See `docs/adr/0003-every-test-artifact-of-a-run.md`.
"""

import re

# One per job that uploads an acceptance suite's output directory, in the
# names the upload steps give them:
#   testing                        "Test results-ubuntu-latest-3-3.13-22.x"
#   test-install                   "ubuntu-latest 3.13 24.x Clean install results"
#   test_browser_batteries_wheels  "Clean_install_results_macos-latest"
#   docker_image                   "docker_results"
_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "source",
        re.compile(
            r"^Test results-(?P<os>.+)-(?P<shard>\d+)-(?P<python>[^-]+)-(?P<node>[^-]+)$"
        ),
    ),
    (
        "wheel",
        re.compile(
            r"^(?P<os>\S+) (?P<python>\S+) (?P<node>\S+) Clean install results$"
        ),
    ),
    ("batteries", re.compile(r"^Clean_install_results_(?P<os>.+)$")),
    ("docker", re.compile(r"^docker_results$")),
)


def _match(artifact_name: str) -> tuple[str, dict[str, str]] | None:
    for install, pattern in _PATTERNS:
        matched = pattern.match(artifact_name)
        if matched:
            return install, matched.groupdict()
    return None


def install_of(artifact_name: str) -> str | None:
    """The Install of the Leg that uploaded this artifact, or None when the
    artifact is not a Leg's at all."""
    matched = _match(artifact_name)
    return matched[0] if matched else None


def leg_name(artifact_name: str) -> str:
    """The Leg as the report names it: its Install, then what the name says it
    ran on. The same shape whichever job uploaded it, where the artifact names
    follow four conventions that only say how each upload step was written.

    An artifact name none of the patterns know comes back unchanged rather than
    as nothing, so a Leg is never shown without a name.
    """
    matched = _match(artifact_name)
    if not matched:
        return artifact_name
    install, parts = matched
    shard = parts.get("shard")
    return " · ".join(
        part
        for part in (
            install,
            parts.get("os"),
            f"shard {shard}" if shard else None,
            parts.get("python"),
            parts.get("node"),
        )
        if part
    )
