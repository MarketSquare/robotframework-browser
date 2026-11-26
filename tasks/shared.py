import os
import shutil
import sys
import time
import urllib.request
from collections.abc import Iterable
from pathlib import Path

from invoke import Exit

ROOT_DIR = Path(__file__).resolve().parent.parent
# Invoke puts tasks/ on sys.path, but Browser and tools import from the root.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
ATEST_LIB_DIR = ROOT_DIR / "atest" / "library"
ATEST_OUTPUT = ROOT_DIR / "atest" / "output"
UTEST_OUTPUT = ROOT_DIR / "utest" / "output"
COVERAGE_DIR = ROOT_DIR / "coverage"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
BROWSER_BATTERIES_DIR = ROOT_DIR / "browser_batteries"
BROWSER_BATTERIES_BIN_DIR = BROWSER_BATTERIES_DIR / "BrowserBatteries" / "bin"


SKIP_BROWSER_DOWNLOAD = "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"
PYTHON_SRC_DIR = ROOT_DIR / "Browser"
python_protobuf_dir = PYTHON_SRC_DIR / "generated"
WRAPPER_DIR = PYTHON_SRC_DIR / "wrapper"
node_protobuf_dir = ROOT_DIR / "node" / "playwright-wrapper" / "generated"
node_dir = ROOT_DIR / "node"
NODE_MODULES = ROOT_DIR / "node_modules"
npm_deps_timestamp_file = NODE_MODULES / ".installed"


IN_CI = os.getenv("GITHUB_WORKFLOW")
IS_GITPOD = "gitpod.io" in os.environ.get("GITPOD_HOST", "")

ZIP_DIR = ROOT_DIR / "zip_results"


DOWNLOAD_ATTEMPTS = 5
DOWNLOAD_TIMEOUT = 60


def download(url: str, destination: Path):
    """Download url to destination, retrying a few times before giving up.

    Every build fetches the NodeJS archive and its checksums from nodejs.org,
    on each platform in the matrix, so a single hiccup there would otherwise
    fail a build for reasons that have nothing to do with the change.
    """
    last_error: Exception = RuntimeError("no attempt made")
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        try:
            print(f"Downloading {url}")
            with (
                urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response,
                destination.open("wb") as out,
            ):
                shutil.copyfileobj(response, out)
        except Exception as error:
            last_error = error
            print(f"  attempt {attempt} of {DOWNLOAD_ATTEMPTS} failed: {error}")
            if attempt < DOWNLOAD_ATTEMPTS:
                time.sleep(attempt)
        else:
            return
    raise Exit(f"Failed to download {url}: {last_error}")


def as_version(version: str) -> tuple:
    return tuple(int(part) for part in version.lstrip("v").split("."))


def as_version_string(version: tuple) -> str:
    return ".".join(str(part) for part in version)


def show_report(lines: list, heading: str):
    """Print, and on GitHub Actions also show on the run's summary page."""
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(f"### {heading}\n{report}\n")


def step_output(key: str, value: str):
    """Hand a value to later steps of the same GitHub Actions job."""
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"{key}={value}\n")


def sources_changed(source_files: Iterable[Path], timestamp_file: Path):
    if timestamp_file.exists():
        last_built = timestamp_file.lstat().st_mtime
        src_last_modified = [f.lstat().st_mtime for f in source_files]
        return not all(last_built >= modified for modified in src_last_modified)
    return True


def clean_zip_dir():
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


def copy_package_files():
    WRAPPER_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT_DIR / "package.json", WRAPPER_DIR)
    shutil.copy(ROOT_DIR / "package-lock.json", WRAPPER_DIR)
