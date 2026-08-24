"""Where a failure lives in this repository.

output.xml says which library owns a keyword but not where that keyword is
defined - `<kw name="Compare Images" owner="screenshot">` and nothing more. The
location is recoverable from the library itself, and there are only ever a
handful of distinct failing keywords, so it is resolved here at ingest time.

That resolution reflects the working copy as it is now, not as it was when the
run happened. If a keyword has moved since, the recorded location is where it
lives today; `run.head_sha` is stored so the run's own commit can be checked out
when a location looks wrong.
"""

import sys
from functools import cache
from pathlib import Path

from robot.libraries import STDLIBS

REPO_ROOT = Path(__file__).resolve().parents[2]

# Directories that mark the start of a repo-relative path. CI paths are absolute
# and platform specific - /home/runner/work/robotframework-browser/robotframework-browser/atest/...
# on Linux, D:\a\robotframework-browser\robotframework-browser\atest\... on
# Windows - and the same file must not look like two places.
_ROOTS = ("atest", "Browser", "utest", "node", "tools", "browser_batteries", "docs")

# Where this repo keeps test-only keyword libraries, so they can be imported.
_LIBRARY_PATHS = (REPO_ROOT / "atest" / "library",)

BROWSER_LIBRARY = "Browser"


def repo_relative(path: str | None) -> str | None:
    """Turns an absolute CI path into one that means something in this checkout."""
    if not path:
        return None
    normalised = str(path).replace("\\", "/")
    parts = normalised.split("/")
    for index, part in enumerate(parts):
        if part in _ROOTS:
            return "/".join(parts[index:])
    return normalised


# The artifact is the run's output directory zipped up, so a path relative to
# that directory is also the path inside the artifact.
_OUTPUT_DIR = "atest/output/"


def artifact_relative(path: str) -> str:
    """Turns a screenshot reference into its path inside the artifact.

    Robot Framework writes these either relative to the output directory already
    or as an absolute file:// URL, depending on which logger produced them.
    """
    normalised = path.replace("\\", "/")
    normalised = normalised.removeprefix("file://")
    index = normalised.find(_OUTPUT_DIR)
    if index != -1:
        return normalised[index + len(_OUTPUT_DIR) :]
    return normalised.lstrip("/")


def owner_kind(owner: str | None) -> str:
    """Which side of the repo a keyword belongs to.

    Matched exactly against Robot Framework's own list, never case insensitively:
    this repo has an `atest/library/screenshot.py` whose owner is `screenshot`,
    and Robot Framework ships a `Screenshot` library. They differ by one letter's
    case and are entirely different code.
    """
    if not owner:
        return "unknown"
    if owner in STDLIBS:
        return "standard"
    if owner == BROWSER_LIBRARY or owner.startswith(f"{BROWSER_LIBRARY}."):
        return "library"
    return "project"


@cache
def _library_keywords(owner: str) -> dict[str, tuple[str | None, int | None]]:
    """Keyword name to (source, line) for one library, or empty if unavailable."""
    for path in _LIBRARY_PATHS:
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    try:
        from robot.libdocpkg import LibraryDocumentation  # noqa: PLC0415

        documentation = LibraryDocumentation(owner)
    except Exception:
        # A library that cannot be imported here - renamed, removed, or simply
        # not installed - costs a location, never an ingest.
        return {}
    return {
        keyword.name: (repo_relative(keyword.source), keyword.lineno)
        for keyword in documentation.keywords
    }


def keyword_location(
    owner: str | None, keyword: str | None
) -> tuple[str | None, int | None]:
    """Where a keyword is defined, as far as this checkout can tell.

    Standard libraries are not resolved: they live in site-packages, which is
    not a place anyone reading this report is going to go and edit. Knowing the
    failure came from BuiltIn is the useful part, and that is the owner.
    """
    if not owner or not keyword or owner_kind(owner) == "standard":
        return None, None
    return _library_keywords(owner).get(keyword, (None, None))
