from contextlib import suppress
import hashlib
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import time
import traceback
import urllib.request
import webbrowser
import zipfile
import signal

from collections.abc import Iterable
from pathlib import Path, PurePath

from invoke import Exit, task
from invoke.context import Context

try:
    import tomllib
except ModuleNotFoundError:
    # Python 3.10, which the on-push.yml testing matrix still runs tasks.py on.
    import tomli as tomllib

try:
    import bs4
    import pytest
    import robotstatuschecker
    from rellu import ReleaseNotesGenerator, Version
    from robot import __version__ as rf_version
    from robot import rebot_cli
    from robot.libdoc import libdoc
    from robot import version as robot_version_module
except ModuleNotFoundError:
    traceback.print_exc()
    print('Assuming that this is for "inv deps" command and ignoring error.')

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST_LIB_DIR = ROOT_DIR / "atest" / "library"
ATEST_OUTPUT = ROOT_DIR / "atest" / "output"
CI_FAILURES_DB = ROOT_DIR / "ci_failures" / "ci_failures.sqlite3"
CI_REPORT_HTML = ROOT_DIR / "ci_failures" / "ci_report.html"
UTEST_OUTPUT = ROOT_DIR / "utest" / "output"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
BROWSER_BATTERIES_DIR = ROOT_DIR / "browser_batteries"
BROWSER_BATTERIES_BIN_DIR = BROWSER_BATTERIES_DIR / "BrowserBatteries" / "bin"
# The NodeJS we ship and the platform floors its wheel tags promise. They live
# in a file of their own so the bot in .github/workflows/on-schedule.yml can
# rewrite them without touching code, and nodejs_pin.toml is where each of them
# is explained.
NODE_PIN_FILE = ROOT_DIR / "nodejs_pin.toml"
NODE_PIN = tomllib.loads(NODE_PIN_FILE.read_text(encoding="utf-8"))
NODE_VERSION = NODE_PIN["version"]
NODE_SHASUMS_SHA256 = NODE_PIN["shasums_sha256"]
NODE_MIN_GLIBC = NODE_PIN["min_glibc"]
NODE_MIN_MACOS = NODE_PIN["min_macos"]
NODE_DIST_BASE = "https://nodejs.org/dist"
NODE_DIST_INDEX = f"{NODE_DIST_BASE}/index.json"
GITHUB_API = "https://api.github.com/repos/MarketSquare/robotframework-browser"
# The release the nightly wheels are downloaded from. It is created once and
# then only ever has its assets replaced, because publishing a release is what
# notifies everybody watching the repository and a build of main is not news.
NIGHTLY_TAG = "nightly"
RELEASE_PROCESS = (
    "Raise an issue and add it to the release milestone so this reaches the "
    "release notes, then close it once the PR is merged."
)
# Every target a BrowserBatteries wheel is published for, named the way
# nodejs.org names it. `inv node-floor-check` walks the list from one machine to
# check min_glibc and min_macos against the binaries themselves, and
# `inv node-pin-bump` walks the same list to work out what they should be.
# win-x64 is missing on purpose: a win_amd64 wheel tag carries no OS version, so
# there is nothing about it to get wrong.
NODE_FLOOR_TARGETS = ("linux-x64", "linux-arm64", "darwin-x64", "darwin-arm64")
# Read out of the NodeJS binaries to check those constants. A versioned glibc
# symbol looks like GLIBC_2.28 in the ELF dynamic string table, and a Mach-O
# states its oldest macOS in one of two load commands.
GLIBC_SYMBOL = re.compile(rb"GLIBC_(\d+)\.(\d+)")
MACHO_MAGIC_64 = 0xFEEDFACF
LC_VERSION_MIN_MACOSX = 0x24
LC_BUILD_VERSION = 0x32
SKIP_BROWSER_DOWNLOAD = "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"
PYTHON_SRC_DIR = ROOT_DIR / "Browser"
python_protobuf_dir = PYTHON_SRC_DIR / "generated"
WRAPPER_DIR = PYTHON_SRC_DIR / "wrapper"
node_protobuf_dir = ROOT_DIR / "node" / "playwright-wrapper" / "generated"
node_dir = ROOT_DIR / "node"
NODE_MODULES = ROOT_DIR / "node_modules"
npm_deps_timestamp_file = NODE_MODULES / ".installed"

ATEST_TIMEOUT = 900
cpu_count = os.cpu_count() or 1
EXECUTOR_COUNT = str(cpu_count - 1 or 1)
IN_CI = os.getenv("GITHUB_WORKFLOW")
IS_GITPOD = "gitpod.io" in os.environ.get("GITPOD_HOST", "")

ZIP_DIR = ROOT_DIR / "zip_results"
RELEASE_NOTES_PATH = Path("docs/releasenotes/Browser-{version}.md")
RELEASE_NOTES_TITLE = "Browser library {version}"
REPOSITORY = "MarketSquare/robotframework-browser"
VERSION_PATH = Path("Browser/version.py")
RELEASE_NOTES_INTRO = """
[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library {version} is a new release with **UPDATE** enhancements and bug fixes.
All issues targeted for Browser library {version.milestone} can be found
from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3A{version.milestone}).
For first time installation with [pip](https://pip.pypa.io/en/stable/) and
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
just run
```bash
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
```
to install the latest available release. If you upgrading
from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
```
For first time installation with [pip](http://pip-installer.org) with Browser
library only, just run
```bash
   pip install robotframework-browser
   rfbrowser init
```
If you upgrading from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
```
Alternatively you can download the source distribution from
[PyPI](https://pypi.org/project/robotframework-browser/) and
install it manually. Browser library {version} was released on {date}.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright REPLACE_PW_VERSION. BrowserBatteries package was
released with NodeJS REPLACE_BB_NODE_VERSION.

"""


def _node_deps(context: Context):
    context.run(
        "npm install --parseable true --progress false",
        env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
    )
    if os.environ.get(SKIP_BROWSER_DOWNLOAD):
        print(f"{SKIP_BROWSER_DOWNLOAD} is set, skipping browser binaries.")
    else:
        context.run(
            "npx --quiet playwright install  --with-deps",
            env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
        )
    npm_deps_timestamp_file.touch()


@task
def deps(c, system=False, force=False, uv=False):
    """Install dependencies for development.

    Args:
        system: When set, installs packages to system Python instead of user.
        force: When set, installs dependencies even there is no changes.
        uv: When set, skips pip install step assuming uv is already installed.
    """
    try:
        c.run("pip --version", hide=True)
    except Exception as error:
        if "Encountered a bad command exit code" in str(error):
            uv = True
    if uv:
        print("No pip install.")
    else:
        c.run("pip install -U pip")
        c.run("pip install -U uv")
    print("Installing dev dependencies.")

    package_manager_dev_cmd = f"uv pip install -r Browser/dev-requirements.txt{' --system' * (system or IS_GITPOD)}"
    package_manager_deps_cmd = (
        f"uv pip install -r pyproject.toml{' --system' * (system or IS_GITPOD)}"
    )
    if IN_CI:
        print(f"Install packages to Python found from {sys.executable}.")
        package_manager_dev_cmd = f"{package_manager_dev_cmd} --python {sys.executable}"
        package_manager_deps_cmd = (
            f"{package_manager_deps_cmd} --python {sys.executable}"
        )
    c.run(package_manager_dev_cmd)
    print("Install package dependencies.")
    c.run(package_manager_deps_cmd)
    if IN_CI:
        shutil.rmtree(str(NODE_MODULES), ignore_errors=True)

    if _sources_changed([ROOT_DIR / "./package-lock.json"], npm_deps_timestamp_file):
        print("Installing node dependencies.")
        _node_deps(c)
    elif force:
        print("Forcing to install node dependencies.")
        _node_deps(c)
    else:
        print("no changes in package-lock.json, skipping npm install")


@task
def clean_mini(c):
    """Cleans only build and test artifacts."""
    for target in [
        DIST_DIR,
        BUILD_DIR,
        UTEST_OUTPUT,
        ATEST_OUTPUT,
        ZIP_DIR,
        BROWSER_BATTERIES_BIN_DIR,
        BROWSER_BATTERIES_DIR / "dist",
        BROWSER_BATTERIES_DIR / "build",
        Path("./playwright-log.txt"),
        PYTHON_SRC_DIR / "rfbrowser.log",
    ]:
        if target.exists():
            shutil.rmtree(target, ignore_errors=True)


@task(clean_mini)
def clean(c):
    """Cleans build artifacts and temporary files."""
    for target in [
        python_protobuf_dir,
        node_protobuf_dir,
        Path("./htmlcov"),
        Path("./.mypy_cache"),
        PYTHON_SRC_DIR / "wrapper",
        BROWSER_BATTERIES_DIR / "build",
    ]:
        if target.exists():
            shutil.rmtree(target)
    pyi_file = PYTHON_SRC_DIR / "__init__.pyi"
    for file in [
        npm_deps_timestamp_file,
        Path("./.coverage"),
        pyi_file,
        Path("./.ruff_cache"),
        Path("./.pytest_cache"),
    ]:
        with suppress(OSError):
            file.unlink()


@task
def protobuf(c):
    """Compile grpc protobuf files."""
    if not python_protobuf_dir.exists():
        python_protobuf_dir.mkdir()
        (python_protobuf_dir / "__init__.py").touch()
    if not node_protobuf_dir.exists():
        node_protobuf_dir.mkdir()
    _python_protobuf_gen(c)
    _node_protobuf_gen(c)


def _python_protobuf_gen(c):
    c.run(
        f"python -m grpc_tools.protoc -I protobuf --python_out=Browser/generated --grpc_python_out={python_protobuf_dir} --mypy_out={python_protobuf_dir} protobuf/*.proto"
    )
    genfile = python_protobuf_dir / "playwright_pb2_grpc.py"
    content = (
        open(genfile)
        .read()
        .replace(
            "import playwright_pb2 as playwright__pb2",
            "from Browser.generated import playwright_pb2 as playwright__pb2",
        )
    )
    with open(genfile, "w") as outfile:
        outfile.write(content)


def _node_protobuf_gen(c):
    plugin_suffix = ".cmd" if platform.platform().startswith("Windows") else ""
    protoc_ts_proto_plugin = (
        NODE_MODULES / ".bin" / f"protoc-gen-ts_proto{plugin_suffix}"
    )
    cmd = (
        "npm run grpc_tools_node_protoc -- "
        f"--plugin=protoc-gen-ts_proto={protoc_ts_proto_plugin} "
        f"--ts_proto_out={node_protobuf_dir} "
        "--ts_proto_opt=outputServices=grpc-js,env=node "
        "-I ./protobuf protobuf/*.proto"
    )
    c.run(cmd)


def _gen_stub(c: Context):
    shutil.rmtree("mypy_stub/", ignore_errors=True)
    Path("Browser/browser.pyi").unlink(missing_ok=True)
    c.run("stubgen --output mypy_stub Browser")
    c.run("python -m Browser.gen_stub")


@task(protobuf)
def node_build(c: Context):
    c.run("npm run build")
    shutil.rmtree(WRAPPER_DIR / "static", ignore_errors=True)
    shutil.copytree(node_dir / "playwright-wrapper" / "static", WRAPPER_DIR / "static")
    _gen_stub(c)


@task
def create_test_app(c):
    c.run("npm run build-test-app")


@task(deps, protobuf, node_build, create_test_app)
def build(c: Context):
    _gen_stub(c)


def _os_platform() -> str:
    pl = platform.system().lower()
    if pl == "darwin":
        return "macos"
    if pl == "windows":
        return "win"
    return "linux"


def _node_dist_infix() -> str:
    """Name nodejs.org uses for this machine, as in node-v<version>-<infix>.

    Always the machine running the build. NodeJS is downloaded prebuilt and the
    wheel is tagged from `sysconfig.get_platform()`, so building for anything
    but the host would produce a wheel whose own tag says it fits where its
    NodeJS cannot run. Every published target has its own CI runner.

    `platform.machine()` reports the machine name, which is not what nodejs.org
    calls the same architecture.
    """
    machine = platform.machine().lower()
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64"}.get(machine, machine)
    os_platform = _os_platform()
    if os_platform == "macos":
        return f"darwin-{arch}"
    if os_platform == "win":
        return f"win-{arch}"
    return f"linux-{arch}"


DOWNLOAD_ATTEMPTS = 5
DOWNLOAD_TIMEOUT = 60


def _download(url: str, destination: Path):
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


def _shasums_digest(version: str) -> str:
    """sha256 of the SHASUMS256.txt nodejs.org publishes for a release."""
    with tempfile.TemporaryDirectory() as tmp:
        checksums = Path(tmp) / "SHASUMS256.txt"
        _download(f"{NODE_DIST_BASE}/v{version}/SHASUMS256.txt", checksums)
        return hashlib.sha256(checksums.read_bytes()).hexdigest()


def _verify_shasums(checksums: Path, version: str, expected: str):
    """Check SHASUMS256.txt itself against the digest we expect for a release.

    Has to happen before anything trusts the manifest, because on its own the
    manifest only proves the archive arrived intact from whoever served it.
    Everything but `inv node-pin-bump` passes the pinned version and digest;
    the bump passes the candidate it is about to propose, so a release it has
    never shipped is held to the same standard.
    """
    digest = hashlib.sha256(checksums.read_bytes()).hexdigest()
    if digest == expected:
        print(f"SHASUMS256.txt matches the expected digest for NodeJS {version}")
        return
    raise Exit(
        f"SHASUMS256.txt for NodeJS {version} hashes to {digest}, but "
        f"{expected} was expected.\n"
        f"If the version in {NODE_PIN_FILE.name} was just changed, set "
        f"shasums_sha256 to {digest} there.\n"
        "If it was not, stop: the manifest is not the one nodejs.org published "
        "for this version, and the archive it vouches for must not be shipped "
        "until that is explained."
    )


def _verify_checksum(archive: Path, checksums: str):
    """Check the archive against nodejs.org's SHASUMS256.txt."""
    expected = None
    for line in checksums.splitlines():
        digest, _, name = line.partition("  ")
        if name.strip() == archive.name:
            expected = digest
            break
    if not expected:
        raise Exit(f"{archive.name} is not listed in SHASUMS256.txt")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != expected:
        raise Exit(f"Checksum mismatch for {archive.name}: {digest} != {expected}")
    print(f"Checksum verified for {archive.name}")


def _extract_member(source, destination: Path):
    if source is None:
        raise Exit(f"Could not read {destination.name} from the NodeJS archive")
    with source, destination.open("wb") as out:
        shutil.copyfileobj(source, out)


def _elf_section(data: bytes, wanted: str) -> bytes:
    """Contents of a named section of an ELF64 file."""
    sh_offset, sh_entry_size, sh_count, sh_str_index = struct.unpack_from(
        "<Q10xHHH", data, 0x28
    )
    headers = [
        struct.unpack_from("<IIQQQQ", data, sh_offset + index * sh_entry_size)
        for index in range(sh_count)
    ]
    names_offset = headers[sh_str_index][4]
    for name_offset, _type, _flags, _addr, offset, size in headers:
        start = names_offset + name_offset
        if data[start : data.index(b"\0", start)].decode() == wanted:
            return data[offset : offset + size]
    raise Exit(f"Found no {wanted} section in the ELF file")


def _glibc_floor(binary: Path) -> tuple:
    """Oldest glibc an ELF binary can load against, from its symbol versions."""
    # The dynamic string table only, never the whole file. NodeJS carries a copy
    # of its own JavaScript inside the executable, and a stray "GLIBC_2.99" in
    # there would fail a build over nothing.
    table = _elf_section(binary.read_bytes(), ".dynstr")
    versions = {
        (int(major), int(minor)) for major, minor in GLIBC_SYMBOL.findall(table)
    }
    if not versions:
        raise Exit(f"{binary.name} references no versioned glibc symbols")
    return max(versions)


def _macos_floor(binary: Path) -> tuple:
    """Oldest macOS a Mach-O binary declares it runs on, as (major, minor)."""
    data = binary.read_bytes()
    (magic,) = struct.unpack_from("<I", data, 0)
    if magic != MACHO_MAGIC_64:
        raise Exit(f"{binary.name} is not a thin 64 bit Mach-O file")
    (command_count,) = struct.unpack_from("<I", data, 16)
    offset = 32
    for _ in range(command_count):
        command, size = struct.unpack_from("<II", data, offset)
        # Both commands carry the same packed xxxx.yy.zz version, the newer one
        # behind a platform field.
        if command in (LC_BUILD_VERSION, LC_VERSION_MIN_MACOSX):
            version_at = offset + (12 if command == LC_BUILD_VERSION else 8)
            (version,) = struct.unpack_from("<I", data, version_at)
            return (version >> 16, (version >> 8) & 0xFF)
        offset += size
    raise Exit(f"{binary.name} declares no minimum macOS version")


def _check_node_floor(binary: Path, infix: str) -> tuple:
    """Check a NodeJS binary against the floor its wheel tag will promise.

    That tag is all that stands between a user on too old a platform and a
    loader error after an install that looked fine, and nothing else in the
    build reads what the binary actually needs. Returns a line for the report
    and a problem, the problem being empty when the declared floor is right.
    """
    if infix.startswith("win-"):
        return f"* {infix}: wheel tag makes no OS version claim, nothing to check", ""
    if infix.startswith("linux-"):
        actual = _glibc_floor(binary)
        declared = tuple(int(part) for part in NODE_MIN_GLIBC.split("_"))
        if actual > declared:
            return "", (
                f"{infix}: NodeJS needs glibc {_as_version_string(actual)} but "
                f"min_glibc promises {_as_version_string(declared)}. Everyone "
                "in between installs the wheel and then cannot start it. Raise "
                f"min_glibc in {NODE_PIN_FILE.name} and fix the platform table "
                "in browser_batteries/README.md to match."
            )
        if actual < declared:
            return "", (
                f"{infix}: NodeJS needs no more than glibc "
                f"{_as_version_string(actual)}, but min_glibc promises "
                f"{_as_version_string(declared)}, so pip refuses the wheel on "
                f"platforms it would have run on. Lower min_glibc in "
                f"{NODE_PIN_FILE.name} and fix the platform table in "
                "browser_batteries/README.md to match."
            )
        return f"* {infix}: needs glibc {_as_version_string(actual)}, matches", ""
    actual = _macos_floor(binary)
    declared = tuple(int(part) for part in NODE_MIN_MACOS.split("_"))
    if actual[0] != declared[0] or declared[1] != 0:
        return "", (
            f"{infix}: NodeJS declares macOS {_as_version_string(actual)} but "
            f"min_macos says {_as_version_string(declared)}. Set it to "
            f"{actual[0]}_0 in {NODE_PIN_FILE.name} and fix the platform table "
            "in browser_batteries/README.md to match."
        )
    covers = f"min_macos {NODE_MIN_MACOS} covers it"
    return f"* {infix}: needs macOS {_as_version_string(actual)}, {covers}", ""


def _fetch_node(
    destination: Path,
    infix: str | None = None,
    version: str | None = None,
    shasums_sha256: str | None = None,
) -> Path:
    """Put the official NodeJS binary and its licence into destination.

    Defaults to the machine this runs on and to the pinned release. `inv
    node-floor-check` passes an infix explicitly, because reading a binary works
    from any platform even though running one does not, and `inv node-pin-bump`
    also passes a version, because it reads releases we do not ship yet.
    """
    infix = infix or _node_dist_infix()
    version = version or NODE_VERSION
    shasums_sha256 = shasums_sha256 or NODE_SHASUMS_SHA256
    windows = infix.startswith("win-")
    suffix = "zip" if windows else "tar.xz"
    archive_name = f"node-v{version}-{infix}.{suffix}"
    base_url = f"{NODE_DIST_BASE}/v{version}"
    node_name = "node.exe" if windows else "node"

    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / archive_name
        _download(f"{base_url}/{archive_name}", archive)
        checksums = Path(tmp) / "SHASUMS256.txt"
        _download(f"{base_url}/SHASUMS256.txt", checksums)
        _verify_shasums(checksums, version, shasums_sha256)
        _verify_checksum(archive, checksums.read_text(encoding="utf-8"))
        root = f"node-v{version}-{infix}"
        node_member = f"{root}/{node_name}" if windows else f"{root}/bin/{node_name}"
        node_binary = destination / node_name
        if windows:
            with zipfile.ZipFile(archive) as zip_file:
                _extract_member(zip_file.open(node_member), node_binary)
                _extract_member(
                    zip_file.open(f"{root}/LICENSE"), destination / "NODE_LICENSE"
                )
        else:
            with tarfile.open(archive) as tar:
                _extract_member(tar.extractfile(node_member), node_binary)
                _extract_member(
                    tar.extractfile(f"{root}/LICENSE"), destination / "NODE_LICENSE"
                )
    node_binary.chmod(0o755)
    return node_binary


def _assemble_wrapper(c: Context, destination: Path):
    """Stage the JS the GRPC server runs, with its production dependencies."""
    destination.mkdir(parents=True, exist_ok=True)
    # Named explicitly: WRAPPER_DIR is also where a development checkout runs
    # `rfbrowser init`, so it can hold node_modules, downloaded browsers and log
    # files that must not be shipped.
    shutil.copy(WRAPPER_DIR / "index.js", destination)
    shutil.copytree(WRAPPER_DIR / "static", destination / "static", dirs_exist_ok=True)
    shutil.copy(ROOT_DIR / "package.json", destination)
    shutil.copy(ROOT_DIR / "package-lock.json", destination)
    print(f"Installing production node dependencies to {destination}")
    with c.cd(str(destination)):
        # The browsers are installed by `rfbrowser install` on the user's
        # machine, they must not end up in the wheel.
        c.run(
            "npm ci --omit=dev --no-audit --no-fund",
            env={SKIP_BROWSER_DOWNLOAD: "1"},
        )
    # npm leaves behind CLI shims and its own lock file that nothing needs at
    # runtime, and setuptools does not pick up dot-directories anyway.
    for leftover in [
        destination / "node_modules" / ".bin",
        destination / "node_modules" / ".package-lock.json",
    ]:
        if leftover.is_dir():
            shutil.rmtree(leftover, ignore_errors=True)
        elif leftover.exists():
            leftover.unlink()


def _directory_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def _as_version(version: str) -> tuple:
    return tuple(int(part) for part in version.lstrip("v").split("."))


def _as_version_string(version: tuple) -> str:
    return ".".join(str(part) for part in version)


def _report(lines: list, heading: str):
    """Print, and on GitHub Actions also show on the run's summary page."""
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(f"### {heading}\n{report}\n")


def _step_output(key: str, value: str):
    """Hand a value to later steps of the same GitHub Actions job."""
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"{key}={value}\n")


def _node_release_state() -> tuple:
    """What nodejs.org offers now, next to what we pin.

    Returns the pinned version, the newest release in the line we ship and the
    newest LTS line, all as comparable tuples. `inv node-version-check` and
    `inv node-pin-bump` both work from this, so they cannot come to different
    conclusions about the same day's releases.
    """
    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "index.json"
        _download(NODE_DIST_INDEX, index)
        releases = json.loads(index.read_text(encoding="utf-8"))
    pinned = _as_version(NODE_VERSION)
    same_line = [r for r in releases if _as_version(r["version"])[0] == pinned[0]]
    if not same_line:
        raise Exit(f"nodejs.org lists no releases for NodeJS {pinned[0]}.x")
    newest = max(_as_version(r["version"]) for r in same_line)
    lts_releases = [_as_version(r["version"]) for r in releases if r["lts"]]
    return pinned, newest, max(lts_releases) if lts_releases else None


@task
def node_version_check(c):
    """Fail when the NodeJS we ship is no longer the one we should ship.

    Two things make the pin stale. A newer release in the line we already ship
    is a plain version bump, and the daily `inv node-pin-bump` proposes those as
    a pull request rather than leaving them to be noticed. A new LTS line is the
    moment to move over, and that is not a bump: the platforms the official
    builds run on change with the line, so min_glibc, min_macos and the wheel
    tags they produce all have to be worked out again. Both fail here, because
    both are work we want to hear about on the day it appears rather than the
    next time somebody happens to look.

    Always exits non-zero on a stale pin, on every run and everywhere. That
    makes it the right check for the release wheel build, where it is the last
    step of the job on purpose, so the wheels are built and uploaded before it
    can fire. The daily workflow runs `inv node-pin-bump` instead, which is the
    same reasoning without the part that would keep a nightly permanently red
    while a bump waits to be merged.
    """
    pinned, newest, newest_lts = _node_release_state()
    lts_report = _as_version_string(newest_lts) if newest_lts else "none listed"
    lines = [
        f"* shipped in BrowserBatteries: {NODE_VERSION}",
        f"* newest NodeJS {pinned[0]}.x: {_as_version_string(newest)}",
        f"* newest LTS on nodejs.org: {lts_report}",
    ]
    stale = []
    move_to = newest if newest > pinned else None
    if newest_lts and newest_lts[0] > pinned[0]:
        move_to = max(move_to or newest_lts, newest_lts)
    if newest > pinned:
        behind = _as_version_string(newest)
        lines.append(
            f"* version in {NODE_PIN_FILE.name} is behind, update it to {behind} "
            "and let CI rebuild the wheels."
        )
        stale.append(f"NodeJS {NODE_VERSION} is behind {behind}.")
    if newest_lts and newest_lts[0] > pinned[0]:
        lines.append(
            f"* NodeJS {newest_lts[0]}.x is the new LTS line and BrowserBatteries "
            f"still ships {pinned[0]}.x. Moving over is more than a version "
            f"bump: check which platforms the official {newest_lts[0]}.x builds "
            "still run on, then update min_glibc, min_macos and the table in "
            "browser_batteries/README.md to match, because those decide who "
            "gets a wheel. `inv node-pin-bump` deliberately leaves this alone."
        )
        stale.append(f"NodeJS {newest_lts[0]}.x is the new LTS line.")
    if move_to:
        target = _as_version_string(move_to)
        lines.append(
            f"* shasums_sha256 for {target} is {_shasums_digest(target)}, set "
            f"that in {NODE_PIN_FILE.name} in the same commit as version."
        )
    if stale:
        lines.append(f"* {RELEASE_PROCESS}")
        _report(lines, "NodeJS version check")
        raise Exit(f"{' '.join(stale)} {RELEASE_PROCESS}")
    lines.append("* up to date, nothing to do.")
    _report(lines, "NodeJS version check")


def _derive_pin(version: str) -> dict:
    """Work out the whole pin for a NodeJS release nobody has shipped yet.

    Downloads every target a wheel is published for and reads the floors out of
    the binaries, which is the same thing `inv node-floor-check` does to the
    release we already ship. The digest comes first because every download is
    checked against it, so a proposed bump is held to the standard the pinned
    version is held to rather than trusting whatever nodejs.org served today.
    """
    digest = _shasums_digest(version)
    floors = {}
    with tempfile.TemporaryDirectory() as tmp:
        for infix in NODE_FLOOR_TARGETS:
            target = Path(tmp) / infix
            target.mkdir()
            binary = _fetch_node(target, infix, version, digest)
            floors[infix] = (
                _glibc_floor(binary)
                if infix.startswith("linux-")
                else _macos_floor(binary)
            )
    # One value has to cover every architecture, because that is all the wheel
    # tags can say. They agree today, and _check_node_floor demands each target
    # match exactly, so a release that split them could not be expressed at all.
    # Saying so is better than picking one and shipping a tag that is wrong for
    # somebody: fixing it properly means per-architecture values here and in
    # package-nodejs, which is not work to do speculatively.
    linux = {i: f for i, f in floors.items() if i.startswith("linux-")}
    darwin = {i: f[0] for i, f in floors.items() if i.startswith("darwin-")}
    for name, derived in (("min_glibc", linux), ("min_macos", darwin)):
        if len(set(derived.values())) > 1:
            spread = ", ".join(f"{i} needs {f}" for i, f in sorted(derived.items()))
            raise Exit(
                f"NodeJS {version} does not have one {name} across its targets: "
                f"{spread}. A single wheel-tag value cannot describe that, so "
                f"this bump needs {NODE_PIN_FILE.name} and package_nodejs to "
                f"carry a value per architecture first. {RELEASE_PROCESS}"
            )
    return {
        "version": version,
        "shasums_sha256": digest,
        "min_glibc": "_".join(str(part) for part in next(iter(linux.values()))),
        # NodeJS targets 13.5, pip only generates macosx_<major>_0_* tags.
        "min_macos": f"{next(iter(darwin.values()))}_0",
    }


def _write_pin(pin: dict) -> list:
    """Set the derived values in the pin file, leaving everything else alone.

    Substitutes the assignments line by line rather than re-serialising the
    parsed document, because the comments in that file are the only explanation
    of what the values mean and no stdlib writer preserves them.
    """
    text = NODE_PIN_FILE.read_text(encoding="utf-8")
    changed = []
    for key, value in pin.items():
        if NODE_PIN[key] == value:
            continue
        text, count = re.subn(
            rf'^{key} = ".*"$',
            lambda _match, k=key, v=value: f'{k} = "{v}"',
            text,
            flags=re.MULTILINE,
        )
        if count != 1:
            raise Exit(
                f"Expected exactly one '{key} = ...' line in "
                f"{NODE_PIN_FILE.name}, found {count}. Not writing anything."
            )
        changed.append(f"* {key}: {NODE_PIN[key]} -> {value}")
    if changed:
        NODE_PIN_FILE.write_text(text, encoding="utf-8")
    return changed


@task
def node_pin_bump(c, write=False, report=None):
    """Propose the newest NodeJS in the line we already ship.

    The daily workflow runs this with --write and turns the result into a pull
    request, so a bump arrives already carrying its digest and platform floors,
    all of them read off the official binaries rather than typed in. Without
    --write it only reports, which is what the release checklist wants.

    A stale pin is not a failure here, because the pull request is the signal
    and a nightly that stays red until somebody merges it teaches people to
    ignore red. A new LTS line still fails: that changes which platforms get a
    wheel at all, and it is not a thing to rubber-stamp.

    Args:
        write:  Write the derived values to nodejs_pin.toml.
        report: Also write the report as markdown to this path, for a PR body.
    """
    pinned, newest, newest_lts = _node_release_state()
    lines = [
        f"* shipped in BrowserBatteries: {NODE_VERSION}",
        f"* newest NodeJS {pinned[0]}.x: {_as_version_string(newest)}",
    ]
    changed = []
    if newest > pinned:
        candidate = _as_version_string(newest)
        lines.append(f"* deriving the pin for NodeJS {candidate}")
        changed = _write_pin(_derive_pin(candidate)) if write else []
        lines.extend(changed or [f"* run with --write to update {NODE_PIN_FILE.name}"])
        _step_output("version", candidate)
    else:
        lines.append("* up to date, nothing to bump.")
    lts_stale = newest_lts and newest_lts[0] > pinned[0]
    if lts_stale:
        lines.append(
            f"* NodeJS {newest_lts[0]}.x is the new LTS line and BrowserBatteries "
            f"still ships {pinned[0]}.x. That is left to a human: it changes the "
            "wheel tags, so min_glibc, min_macos and the platform table in "
            "browser_batteries/README.md all have to be worked out again."
        )
        lines.append(f"* {RELEASE_PROCESS}")
    _report(lines, "NodeJS pin bump")
    if report:
        Path(report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if lts_stale:
        raise Exit(f"NodeJS {newest_lts[0]}.x is the new LTS line. {RELEASE_PROCESS}")


@task
def node_floor_check(c):
    """Check min_glibc and min_macos against every NodeJS we ship.

    Runs anywhere, Linux or macOS, because it reads the downloaded binaries
    rather than running them. A platform's own build only ever checks its own
    binary, so a value that is wrong for some other platform would otherwise
    surface as a broken install for whoever is on it. The daily workflow runs
    this, and so does the release checklist. Windows is not in the list, its
    wheel tag promises no OS version.
    """
    lines = [f"* NodeJS {NODE_VERSION}"]
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        for infix in NODE_FLOOR_TARGETS:
            target = Path(tmp) / infix
            target.mkdir()
            line, problem = _check_node_floor(_fetch_node(target, infix), infix)
            lines.append(line or f"* {infix}: WRONG, see below")
            if problem:
                problems.append(problem)
    lines.extend(f"* {problem}" for problem in problems)
    if problems:
        lines.append(f"* {RELEASE_PROCESS}")
    _report(lines, "NodeJS platform floor check")
    if problems:
        raise Exit(
            f"{len(problems)} of {len(NODE_FLOOR_TARGETS)} targets disagree. "
            f"{RELEASE_PROCESS}"
        )


def _build_nodejs(c: Context):
    """Put the official NodeJS binary next to the wrapper sources.

    This is the layout Playwright itself uses for its Python, Java and .NET
    drivers. Playwright is written against ordinary NodeJS, so anything it does
    at run time - loading builtins, resolving paths, forking helper processes -
    works the way its own tests expect.
    """
    print(f"Assemble NodeJS side to '{BROWSER_BATTERIES_BIN_DIR}'.")
    _copy_package_files()
    BROWSER_BATTERIES_BIN_DIR.mkdir(parents=True, exist_ok=True)
    node_binary = _fetch_node(BROWSER_BATTERIES_BIN_DIR)
    c.run(f'"{node_binary}" --version')
    line, problem = _check_node_floor(node_binary, _node_dist_infix())
    print(line or problem)
    if problem:
        raise Exit(f"{problem} {RELEASE_PROCESS}")
    wrapper = BROWSER_BATTERIES_BIN_DIR / "wrapper"
    _assemble_wrapper(c, wrapper)
    with c.cd(str(wrapper)):
        c.run(f'"{node_binary}" --check index.js')
        c.run(
            f'"{node_binary}" -e "require.resolve(\'./node_modules/playwright-core\')"'
        )
    print(
        f"NodeJS binary at '{node_binary}' ({node_binary.stat().st_size / 1e6:.1f} MB)"
    )
    print(f"Wrapper payload at '{wrapper}' ({_directory_size(wrapper) / 1e6:.1f} MB)")


@task(clean, build)
def build_nodejs(c: Context):
    """Assemble the NodeJS side of BrowserBatteries.

    Downloads the NodeJS binary for the machine this runs on and stages it with
    the wrapper sources and their production dependencies. Run `inv
    package-nodejs` to turn the result into a wheel.
    """
    _build_nodejs(c)


def _sources_changed(source_files: Iterable[Path], timestamp_file: Path):
    if timestamp_file.exists():
        last_built = timestamp_file.lstat().st_mtime
        src_last_modified = [f.lstat().st_mtime for f in source_files]
        return not all(last_built >= modified for modified in src_last_modified)
    return True


@task
def utest(c, reporter=None, suite=None):
    """Run utest.

    Args:
        reporter: Defines which approval test reporter to use.
                  Must be full path to the diff program.
                  For more details see:
                  https://pypi.org/project/pytest-approvaltests/
                  https://github.com/approvals/ApprovalTests.Python
        suite:    Defines which test suite file to run. Same as: pytest path/to/test.py
                  Must be path to the test suite file

    To create coverage use: coverage run -m invoke utest
    """
    args = [
        "--showlocals",
        "--junitxml=utest/output/pytest_xunit.xml",
        "--tb=long",
        "-o",
        "log_cli=True",
        "-o",
        "log_cli_level=INFO",
    ]
    if reporter:
        args.append(f"--approvaltests-add-reporter={reporter}")
    if suite:
        args.append(suite)
    status = pytest.main(args)
    raise Exit(status)


@task
def utest_watch(c):
    c.run("ptw --ignore ./node_modules --ignore ./.venv")


@task
def utest_node(c, coverage=False):
    """Run Node.js unit tests with Jest.

    Args:
        coverage: When set, runs with Istanbul coverage report (output: node/coverage/).
    """
    script = "test:coverage" if coverage else "test"
    c.run(f"npm run {script}")
    if coverage:
        report = ROOT_DIR / "node" / "coverage" / "index.html"
        print(f"\nCoverage report: {report}")


@task
def clean_atest(c):
    if ATEST_OUTPUT.exists():
        shutil.rmtree(ATEST_OUTPUT)
    _clean_zip_dir()


def _batteries(batteries: bool):
    batteries_dir = str(BROWSER_BATTERIES_DIR)
    if batteries:
        print("Running with BrowserBatteries")
        sys.path.append(batteries_dir)
        browser_path = NODE_MODULES / "playwright-core" / ".local-browsers"
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_path)
    return batteries_dir


def _get_listener_args():
    return [
        "--listener",
        str(ATEST_LIB_DIR / "test_app_listener.py"),
    ]


@task(clean_atest, create_test_app)
def atest(
    c,
    suite=None,
    test=None,
    include=None,
    shard=None,
    debug=False,
    include_mac=False,
    smoke=False,
    processes=None,
    framed=False,
    exclude=None,
    loglevel=None,
    batteries=False,
):
    """Runs Robot Framework acceptance tests with pabot.

    Args:
        suite: Select which suite to run.
        test: Select which test to run.
        include: Select test by tag
        shard: Shard tests
        debug: Use robotframework-debugger as test listener
        smoke: If true, runs only tests that take less than 500ms.
        include_mac: Does not exclude no-mac-support tags. Should be only used in local testing
        loglevel: Set log level for robot framework
        batteries: Run test with BrowserBatteries. Assumes the NodeJS side is
            already assembled, see `inv build-nodejs`.
    """
    if IS_GITPOD and (not processes or int(processes) > 6):
        processes = "6"

    args = [] if processes is None else ["--processes", processes]

    args.extend(
        [
            "--ordering",
            "atest/atest_order.data",
            "--pythonpath",
            ".",
        ]
    )
    args.extend(_get_listener_args())
    if suite:
        args.extend(["--suite", suite])
    if test:
        args.extend(["--test", test])
    if include:
        args.extend(["--include", include])
    if debug:
        args.extend(["--listener", "Debugger"])
    if smoke:
        args.extend(["--exclude", "slow"])
    if exclude:
        args.extend(["--exclude", exclude])
    if framed:
        args.extend(["--variable", "SUFFIX:framing.html?url="])
        args.extend(["--variable", "SELECTOR_PREFIX:id=iframe_id >>>"])
        args.extend(["--exclude", "no-iframe"])
    loglevel = loglevel or "DEBUG"
    args.extend(["--exclude", "tidy-transformer"])
    ATEST_OUTPUT.mkdir(parents=True, exist_ok=True)
    _batteries(batteries)
    from Browser.utils import spawn_node_process

    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "debug"
    background_process, port = spawn_node_process(ATEST_OUTPUT / "playwright-log.txt")
    try:
        os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = port
        rc = _run_pabot(args, shard, include_mac, loglevel=loglevel)
    finally:
        background_process.kill()
    sys.exit(rc)


def _clean_zip_dir():
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


def _clean_pabot_results(rc: int):
    if rc == 0:

        def on_error(function, path, excinfo):
            print(f"Could not delete {path} with excinfo: {excinfo}")

        pabot_results = ATEST_OUTPUT / "pabot_results"
        shutil.rmtree(pabot_results, onerror=on_error)
    else:
        print("Not deleting pabot_results on error")


@task(clean_atest)
def atest_robot(c, smoke=False, suite=None, batteries=False):
    """Run atest with Robot Framework

    Arguments:
        smoke: If true, runs only tests that take less than 500ms.
        suite: Select which suite to run.
        batteries: If true, includes BrowserBatteries in the test run.
    """
    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "debug"
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    sys_var_ci = int(os.environ.get("SYS_VAR_CI_INSTALL_TEST", 0))
    sys_var_cmd = (
        "SYS_VAR_CI_INSTALL_TEST:True"
        if sys_var_ci
        else "SYS_VAR_CI_INSTALL_TEST:False"
    )
    command_args = (
        [sys.executable, "-m", "robot", "--exclude", "not-implemented"]
        + (["--exclude", "slow"] if smoke else [])
        + [
            "--loglevel",
            "DEBUG",
            "--report",
            "NONE",
            "--log",
            "NONE",
            "--xunit",
            "robot_xunit.xml",
            "--variable",
            sys_var_cmd,
            "--outputdir",
            str(ATEST_OUTPUT),
        ]
    )
    command_args.extend(_get_listener_args())
    if suite:
        command_args.extend(["--suite", suite])
    if batteries:
        batteries_dir = _batteries(batteries)
        command_args.extend(["--pythonpath", batteries_dir])
    command_args = _add_skips(command_args)
    command_args.append("atest/test")
    env = os.environ.copy()
    process = subprocess.Popen(command_args, env=env)
    process.wait(ATEST_TIMEOUT)
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    _clean_pabot_results(rc)
    print(f"DONE rc=({rc})")
    sys.exit(rc)


@task(clean_atest)
def atest_global_pythonpath(c):
    args = ["--variable", "SYS_VAR_CI:True"]
    args.extend(_get_listener_args())
    rc = _run_pabot(args)
    _clean_pabot_results(rc)
    sys.exit(rc)


@task()
def atest_failed(c):
    args = ["--rerunfailed", "atest/output/output.xml"]
    args.extend(_get_listener_args())
    sys.exit(_run_pabot(args))


@task()
def atest_coverage(
    c,
    suite=None,
    test=None,
    include=None,
    debug=False,
    exclude=None,
    loglevel=None,
):
    """Run acceptance tests with both Python and Node.js coverage.

    Builds the Node.js wrapper, runs acceptance tests with coverage
    collection enabled for both Python and Node.js, then generates
    coverage reports.

    Args:
        suite:    Select which suite to run.
        test:     Select which test to run.
        include:  Select tests by tag.
        debug:    Use robotframework-debugger as test listener.
        exclude:  Exclude tests by tag.
        loglevel: Set log level for robot framework.

    To use with coverage.py tracking:
        coverage run -m invoke utest
        coverage run --append -m invoke atest-coverage
        coverage combine (if needed)
        coverage report
        coverage html

    Node.js coverage output: atest/output/node-coverage-report/
    Python coverage output: htmlcov/

    NodeJS coverage is not supported in Windows.
    """
    from Browser.utils import spawn_node_process

    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "debug"
    os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE"] = "1"
    node_build(c)
    clean_atest(c)
    create_test_app(c)
    ATEST_OUTPUT.mkdir(parents=True, exist_ok=True)

    if sys.platform == "win32":
        print("Node.js V8 coverage is not supported on Windows.")
    else:
        v8_coverage_dir = ATEST_OUTPUT / "browser" / "node-v8-coverage"
        v8_coverage_dir.mkdir(parents=True, exist_ok=True)
        os.environ["NODE_V8_COVERAGE"] = str(v8_coverage_dir)

    args = _get_listener_args()
    if suite:
        args.extend(["--suite", suite])
    if test:
        args.extend(["--test", test])
    if include:
        args.extend(["--include", include])
    if debug:
        args.extend(["--listener", "Debugger"])
    if exclude:
        args.extend(["--exclude", exclude])

    background_process, port = spawn_node_process(ATEST_OUTPUT / "playwright-log.txt")
    try:
        os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = port
        rc = _run_robot_with_coverage(args, loglevel or "DEBUG")

    finally:
        # SIGTERM allows Node.js to flush V8 coverage before exiting
        try:
            background_process.send_signal(signal.SIGTERM)
            background_process.wait(timeout=10)
            print("Node process exited gracefully, V8 coverage flushed")
        except Exception:
            background_process.kill()

    c.run("node node/process-coverage.mjs", warn=True)
    print(
        f"\nNode.js coverage report: {ATEST_OUTPUT / 'node-coverage-report' / 'index.html'}"
    )
    print(f"\nPython coverage: Run 'coverage html' to generate htmlcov/index.html")
    sys.exit(rc)


def _run_robot_with_coverage(extra_args=None, loglevel="DEBUG"):
    """Run robot with Python coverage collection."""
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    robot_args = [
        "-m",
        "robot",
        "--xunit",
        "robot_xunit.xml",
        "--exclude",
        "not-implemented",
        "--loglevel",
        loglevel,
        "--report",
        "NONE",
        "--log",
        "NONE",
        "--outputdir",
        str(ATEST_OUTPUT),
    ]
    robot_args = _add_skips_list(robot_args, False)
    robot_args.extend(["--exclude", "no-coverage-support"])

    cmd = (
        [sys.executable, "-m", "coverage", "run"]
        + robot_args
        + (extra_args or [])
        + ["atest/test"]
    )
    process = subprocess.Popen(cmd, env=os.environ)
    process.wait(ATEST_TIMEOUT)

    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    print(f"DONE rc=({rc})")
    return rc


@task()
def run_tests(c, tests, batteries=False):
    """Run robot with dev Browser.

    Arguments:
        tests: is the path to tests to run.
        batteries: If true, includes BrowserBatteries in the test run.
    """
    _batteries(batteries)
    env = os.environ.copy()
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "robot",
            "--xunit",
            "robot_xunit.xml",
            "--loglevel",
            "DEBUG",
            "--exclude",
            "tidy-transformer",
            "-d",
            "outs",
            tests,
        ],
        env=env,
    )
    return process.wait(ATEST_TIMEOUT)


def _run_pabot(extra_args=None, shard=None, include_mac=False, loglevel="DEBUG"):
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    pabot_args = [
        sys.executable,
        "-m",
        "pabot.pabot",
        "--pabotlib",
        "--pabotlibport",
        "0",
        "--processes",
        EXECUTOR_COUNT,
        "--chunk",
        "--artifacts",
        "png,webm,zip",
        "--artifactsinsubfolders",
    ] + (["--shard", shard] if shard else [])
    default_args = [
        "--xunit",
        "robot_xunit.xml",
        "--exclude",
        "not-implemented",
        "--loglevel",
        loglevel,
        "--report",
        "NONE",
        "--log",
        "NONE",
        "--outputdir",
        str(ATEST_OUTPUT),
    ]
    default_args = _add_skips(default_args, include_mac)
    default_args.append("atest/test")
    process = subprocess.Popen(
        pabot_args + (extra_args or []) + default_args, env=os.environ
    )
    process.wait(ATEST_TIMEOUT)
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    print(f"DONE rc=({rc})")
    return rc


def _get_rf_version() -> tuple:
    def integer(s) -> int:
        try:
            return int(s)
        except ValueError:
            return 0

    return tuple(map(integer, robot_version_module.get_version().split(".")))


def _add_skips(default_args, include_mac=False):
    if platform.platform().lower().startswith("windows"):
        print("Running in Windows exclude no-windows-support tags")
        default_args.extend(["--exclude", "no-windows-support"])
    if not include_mac and (
        platform.platform().lower().startswith("mac")
        or platform.platform().lower().startswith("darwin")
    ):
        print("Running in Mac exclude no-mac-support tags")
        default_args.extend(["--exclude", "no-mac-support"])
    default_args.extend(["--exclude", "tidy-transformer"])

    rf_version = _get_rf_version()
    if rf_version < (7, 4):
        print(
            "Running with Robot Framework version < 7.4, exclude require-rf-7.4+ tags"
        )
        default_args.extend(["--exclude", "require-rf-7.4+"])
    return default_args


def _add_skips_list(default_args, include_mac=False):
    """Add skip/exclude arguments to a list for robot command."""
    if platform.platform().lower().startswith("windows"):
        print("Running in Windows exclude no-windows-support tags")
        default_args.extend(["--exclude", "no-windows-support"])
    if not include_mac and (
        platform.platform().lower().startswith("mac")
        or platform.platform().lower().startswith("darwin")
    ):
        print("Running in Mac exclude no-mac-support tags")
        default_args.extend(["--exclude", "no-mac-support"])
    default_args.extend(["--exclude", "tidy-transformer"])
    rf_version = _get_rf_version()
    if rf_version < (7, 4):
        print(
            "Running with Robot Framework version < 7.4, exclude require-rf-7.4+ tags"
        )
        default_args.extend(["--exclude", "require-rf-7.4+"])
    return default_args


@task
def lint_python(c, fix=False):
    ruff_cmd_format = [
        "ruff",
        "format",
        "--config",
        "pyproject.toml",
        "Browser/",
        "bootstrap.py",
        "tasks.py",
        "utest",
        "browser_batteries",
        ".github/skills/",
        "tools/",
    ]
    ruff_cmd_check = [
        "ruff",
        "check",
        "--config",
        "pyproject.toml",
        "Browser/",
        "browser_batteries/",
        "bootstrap.py",
        ".github/skills/",
        "tools/",
    ]
    if fix:
        ruff_cmd_check.insert(2, "--fix")
    else:
        ruff_cmd_format.insert(2, "--check")
    print(f"Run ruff format: {ruff_cmd_format}")
    c.run(" ".join(ruff_cmd_format))
    print(f"Run ruff check: {ruff_cmd_check}")
    c.run(" ".join(ruff_cmd_check))
    print("Run mypy:")
    mypy_cmd = [
        "mypy",
        "--exclude",
        ".venv",
        "--config-file",
        "Browser/mypy.ini",
        "Browser/",
        "bootstrap.py",
        "browser_batteries/",
        ".github/skills/",
        "tools/",
    ]
    c.run(" ".join(mypy_cmd))


@task
def lint_node(c: Context):
    """Lint node files."""
    if IN_CI:
        c.run("npm run format:check")
        c.run("npm run lint:check")
    else:
        c.run("npm run format")
        c.run("npm run lint")


@task
def lint_robot(c):
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    atest_folder = Path("atest/").resolve()
    config_file = Path("pyproject.toml").resolve()
    cmd = [
        "robocop",
        "format",
        "--config",
        str(config_file),
    ]
    if IN_CI:
        cmd.insert(2, "--check")
        cmd.insert(3, "--diff")
    atest_11_tidy_transformer = atest_folder.joinpath(
        "test", "11_tidy_transformer", "network_idle_file.robot"
    )
    atest_resrouces = list(atest_folder.joinpath("test").glob("*.resource"))
    cmd.extend(
        [
            "--exclude",
            str(atest_11_tidy_transformer),
            "--exclude",
            str(atest_resrouces[0]),
            "--exclude",
            str(atest_resrouces[1]),
            str(atest_folder),
        ]
    )
    print(cmd)
    c.run(" ".join(cmd))


@task(lint_python, lint_node, lint_robot)
def lint(c):
    pass


@task
def docker_stable_image(c):
    from Browser.version import __version__ as VERSION

    c.run(
        f"docker buildx build --load --tag docker.pkg.github.com/marketsquare/robotframework-browser/rfbrowser-stable:{VERSION} --file docker/Dockerfile.latest_release ."
    )


@task
def docker_tester(c):
    c.run(
        "docker buildx build --load --tag rfbrowser-tests:latest --file docker/Dockerfile.tests ."
    )


@task(clean_atest, create_test_app, build)
def docker_test(c):
    c.run("mkdir atest/output")
    c.run("chmod -R 777 atest/output")
    c.run(
        """docker run\
        --rm \
        --ipc=host\
        --security-opt seccomp=docker/seccomp_profile.json \
        -v $(pwd)/atest/:/app/atest \
        -v $(pwd)/node/:/app/node/ \
        --workdir /app \
        rfbrowser-tests \
        sh -c "xvfb-run python3 -m invoke atest-robot"
        """
    )


@task()
def docker_run_tmp_tests(c):
    """
    Run robot with dev Browser from docker against tmp dir.
    """
    c.run(
        """docker run\
        --rm \
        --ipc=host\
        --security-opt seccomp=docker/seccomp_profile.json \
        -v $(pwd)/tmp/:/app/tmp \
        -v $(pwd)/node/:/app/node/ \
        --workdir /app \
        rfbrowser \
        sh -c "ROBOT_SYSLOG_FILE=/app/atest/output/syslog.txt PATH=$PATH:~/.local/bin robot --loglevel debug --outputdir /app/tmp/output /app/tmp/"
        """
    )


@task(build)
def run_test_app(c: Context):
    """Run dynamic test app."""
    c.run("node node/dynamic-test-app/dist/server.js")


@task
def run_test_app_no_build(c: Context, asynchronous=False):
    """Run dynamic test app without building.

    Args:
        asynchronous: When true, returns immediately after starting the subprocess.
    """
    print("Running test app without building.")
    c.run("node node/dynamic-test-app/dist/server.js", asynchronous=asynchronous)
    time.sleep(4)
    print(f"Test app started with asynchronous mode {asynchronous}.")


@task
def docker_copy_output(c: Context):
    """Copy atest output from docker container to host."""
    output = ROOT_DIR / "docker_last_container.txt"
    output.unlink(missing_ok=True)
    c.run(f"docker ps --all --last 1 --format '{{{{.ID}}}}' > {output}")
    with output.open("r") as file:
        container_id = file.read().strip()
    c.run(f"docker cp {container_id}:/home/pwuser/output ./output_docker")


@task
def docs(c, version=None):
    """Generate library keyword documentation.

    Args:
        version: Creates keyword documentation with version
        suffix in the name. Documentation is moved to docs/vesions
        folder.
    """
    output = ROOT_DIR / "docs" / "Browser.html"
    libdoc("Browser", str(output))
    with output.open("r") as file:
        data = file.read()
    soup = bs4.BeautifulSoup(data, "html.parser")
    script_async = soup.new_tag(
        "script", src="https://www.googletagmanager.com/gtag/js?id=UA-106835747-3"
    )
    script_async.attrs["async"] = None
    soup.head.append(script_async)
    script_data = soup.new_tag("script")
    script_data.string = """
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-106835747-3', {
            'anonymize_ip': true,
            'page_path': location.pathname+location.search+location.hash });
      window.onhashchange = function() {
            gtag('event', 'HashChange', {
            'event_category': 'Subsection',
            'event_label': window.location.hash
            });
       }
    """
    soup.head.append(script_data)
    with output.open("w") as file:
        file.write(str(soup))
    if version is not None:
        target = (
            ROOT_DIR / "docs" / "versions" / f"Browser-{version.replace('v', '')}.html"
        )
        output.rename(target)


def _copy_package_files():
    WRAPPER_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT_DIR / "package.json", WRAPPER_DIR)
    shutil.copy(ROOT_DIR / "package-lock.json", WRAPPER_DIR)


@task
def create_package(c):
    _copy_package_files()
    c.run("python -m build")


@task(clean_mini, build, docs, create_package)
def package(c: Context):
    """Build python wheel for Browser release."""


@task(clean_mini, build)
def package_nodejs(c: Context):
    """Build Python wheel from BrowserBattiers release."""
    _build_nodejs(c)
    with c.cd(BROWSER_BATTERIES_DIR):
        print(f"Building Browser Batteries package in {BROWSER_BATTERIES_DIR}")
        # Without --wheel, `build` makes an sdist first and then unpacks it to
        # build the wheel out of. That tars, gzips and extracts the whole NodeJS
        # payload, a few hundred megabytes of it, to produce an artifact nothing
        # publishes.
        c.run("python -m build --wheel")
    _os_platform = sysconfig.get_platform()
    print(f"Current os platform: {_os_platform}")
    _os_platform = _os_platform.replace("-", "_").replace(".", "_").replace(" ", "_")
    if _os_platform.startswith("macosx"):
        # sysconfig reports the deployment target of the Python running the
        # build, which says nothing about the NodeJS we ship next to it.
        _os_platform = f"macosx_{NODE_MIN_MACOS}_{platform.machine().lower()}"
    elif sysconfig.get_platform().lower() == "linux-x86_64":
        _os_platform = f"manylinux_{NODE_MIN_GLIBC}_x86_64"
    elif sysconfig.get_platform().lower() == "linux-aarch64":
        _os_platform = f"manylinux_{NODE_MIN_GLIBC}_aarch64"
    dist_dir = BROWSER_BATTERIES_DIR.joinpath("dist")
    wheel_pkg = dist_dir.glob("*.whl")
    wheel_pkg = list(wheel_pkg)[0]
    wheel_pkg_os_platform = wheel_pkg.name.replace("any", _os_platform)
    wheel_pkg_os_platform = dist_dir / wheel_pkg_os_platform
    print(f"Renaming {wheel_pkg} to have platform tag {wheel_pkg_os_platform}")
    wheel_pkg.rename(wheel_pkg_os_platform)


@task
def release_notes(c, version=None, username=None, password=None, write=False):
    """Generates release notes based on issues in the issue tracker.

    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise just print them to the
                  terminal.
    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    pattern = '__version__ = "(.*)"'
    if write and not RELEASE_NOTES_PATH.parent.is_dir():
        RELEASE_NOTES_PATH.parent.mkdir(parents=True)
    version = Version(version, VERSION_PATH, pattern)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    release_notes_intro = RELEASE_NOTES_INTRO.replace(
        "REPLACE_PW_VERSION", _get_pw_version()
    ).replace("REPLACE_BB_NODE_VERSION", NODE_VERSION)
    generator = ReleaseNotesGenerator(
        REPOSITORY,
        RELEASE_NOTES_TITLE,
        release_notes_intro,
    )
    generator.generate(version, username, password, file)


def _get_pw_version() -> str:
    with open(ROOT_DIR / "package.json") as file:
        data = json.load(file)
    version = data["dependencies"]["playwright"]
    match = re.search(r"\d+\.\d+\.\d+", version)
    return match.group(0)


@task(package)
def release(c):
    c.run("python -m twine upload dist/*")


@task()
def version(c, version):
    if not version:
        print("Give version with inv version <version>")
    py_version_file = ROOT_DIR / "Browser" / "version.py"
    py_version_matcher = re.compile("__version__ = .*")
    _replace_version(py_version_file, py_version_matcher, f'__version__ = "{version}"')
    node_version_file = ROOT_DIR / "package.json"
    node_version_matcher = re.compile('"version": ".*"')
    _replace_version(node_version_file, node_version_matcher, f'"version": "{version}"')
    package_lock = ROOT_DIR / "package-lock.json"
    data = json.loads(package_lock.read_text())
    data["version"] = version
    data["packages"][""]["version"] = version
    package_lock.write_text(json.dumps(data, indent=2))
    py_project_toml = ROOT_DIR / "pyproject.toml"
    py_project_toml_matcher = re.compile('version = ".*"')
    _replace_version(
        py_project_toml, py_project_toml_matcher, f'version = "{version}"', 1
    )
    py_project_toml = BROWSER_BATTERIES_DIR / "pyproject.toml"
    _replace_version(
        py_project_toml, py_project_toml_matcher, f'version = "{version}"', 1
    )
    py_project_toml_matcher = re.compile(
        r'dependencies = \["robotframework-browser==.*"\]'
    )
    _replace_version(
        py_project_toml,
        py_project_toml_matcher,
        f'dependencies = ["robotframework-browser=={version}"]',
        1,
    )
    dockerfile = ROOT_DIR / "docker" / "Dockerfile.latest_release"
    docker_version_matcher = re.compile("robotframework-browser==.*")
    _replace_version(
        dockerfile, docker_version_matcher, f"robotframework-browser=={version}"
    )


def _released_version() -> str:
    """What Browser/version.py says, read without importing the library."""
    version_file = ROOT_DIR / "Browser" / "version.py"
    match = re.search(
        r'__version__ = "([^"]+)"', version_file.read_text(encoding="utf-8")
    )
    if not match:
        raise Exit(f"No __version__ in {version_file}.")
    return match.group(1)


def _open_milestone_titles() -> list:
    """Titles of the milestones that are still open, or [] if we cannot ask.

    Only ever called to work out a nightly version, and a nightly is not worth
    failing a build of main over, so an unreachable or unhappy API falls back to
    the version file rather than raising.
    """
    request = urllib.request.Request(
        f"{GITHUB_API}/milestones?state=open&per_page=100",
        headers={"Accept": "application/vnd.github+json"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return [milestone["title"] for milestone in json.load(response)]
    except Exception as error:
        print(f"Could not read the open milestones ({error}), using version.py.")
        return []


def _next_version(milestone_titles: Iterable[str], released: str) -> str:
    """The version main is working towards, for a nightly wheel to carry.

    The lowest open milestone is the next release, so that is the number the
    wheels built from main belong to. Milestones named something other than a
    plain version are ignored, and with none left the next patch of the released
    version is the honest guess.
    """
    planned = [
        _as_version(match.group(1))
        for match in (
            re.fullmatch(r"v?(\d+\.\d+\.\d+)", title.strip())
            for title in milestone_titles
        )
        if match
    ]
    if planned:
        return _as_version_string(min(planned))
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", released)
    if not match:
        raise Exit(f"Cannot read a version number out of '{released}'.")
    major, minor, patch = (int(part) for part in match.groups())
    return _as_version_string((major, minor, patch + 1))


@task
def dev_version(c):
    """Print the version a wheel built from main should carry.

    A nightly has to sort above the release that is out and below the release it
    is heading for, or pip has no way to tell a tester's `--pre` install from
    the version they already have. PEP 440 spells that as a .devN of the coming
    release, and the coming release is whatever the lowest open milestone says,
    so nobody has to remember to bump anything here. The timestamp is UTC and
    goes down to the second, because two pushes to main can land in one minute.

    Prints the version and, on GitHub Actions, hands it to later steps as
    `version`. Both wheels are stamped with it by `inv version`, which keeps the
    `robotframework-browser==` pin in the BrowserBatteries wheel matching.
    """
    version = _next_version(_open_milestone_titles(), _released_version())
    stamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    _step_output("version", f"{version}.dev{stamp}")
    print(f"{version}.dev{stamp}")


def _replace_version(filepath, matcher, version, count=0):
    content = filepath.open().read()
    with open(filepath, "w") as out:
        out.write(matcher.sub(version, content, count))


@task
def gh_pages_index(c):
    import os

    links = [
        f"""<a href="versions/{i}">{i}</a>"""
        for i in sorted(os.listdir("docs/versions"))
    ]

    index_contents = f"""
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta charset="utf-8"/>
            <title>Robot Framework Browser</title>
            <link rel="stylesheet" href="style.css" type="text/css" />
        </head>
        <body>
            <p>
                Check out our GitHub homepage for details.
                <a href="https://github.com/MarketSquare/robotframework-browser">Project Home</a>
            </p>
            <p>
                <a href="Browser.html">Keyword Documentation</a>
            </p>
            <p>
                <h3> Old releases</h3>
                {links}
            </p>
        </body>
    </html>
    """

    with open("docs/index.html", "w") as f:
        f.write(index_contents)


# TODO: should this depend on `create_test_app` ?
@task
def demo_app(c):
    """Zip demo application to OS specific package for CI"""
    _clean_zip_dir()
    zip_dir = ZIP_DIR / "demoapp"
    zip_dir.mkdir(parents=True)
    zip_name = f"demo-app-{sys.platform}.zip"
    zip_path = zip_dir / zip_name
    demo_app = Path("node", "dynamic-test-app").resolve()
    print(f"Creating zip  in: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, "w")
    for file in demo_app.glob("**/*.*"):
        file = PurePath(file)
        arc_name = file.relative_to(str(ROOT_DIR))
        zip_file.write(file, arc_name)
    zip_file.close()
    return zip_path


def _window_of_days(days):
    """`--days N` as a Window, or an Exit saying which part of N was wrong.

    Shared by ci-ingest and ci-report so the flag means the same thing in both
    and refuses the same way - it was written twice and the second copy was a
    copy of the first, bug included.

    The two conversions are caught separately on purpose. `int()` is what knows
    about "seven" and `of_days` is what knows about 0, and one `except
    ValueError` around both threw away whichever message was the true one:
    `--days 0` used to be told it was not a whole number.
    """
    from tools.ci_failures.window import of_days

    try:
        whole_days = int(days)
    except (TypeError, ValueError):
        raise Exit(f"--days wants a whole number of days, got {days!r}.", 2) from None
    try:
        return of_days(whole_days)
    except ValueError as refused:
        raise Exit(str(refused), 2) from None


@task
def ci_ingest(c, limit=None, days=None, db=None, dry_run=False):
    """Pulls CI test results into the local database.

    Incremental: legs already ingested are skipped, so running this often only
    costs what is new. See `tools/ci_failures/README.md`.

    Args:
        limit: How many runs to consider, newest first. Defaults to 25. Runs,
            not days - 25 is about a week of this repository and 100 about a
            month, and the rate moves with how busy it is. Above roughly 100 the
            two events stop coming back in the same proportion and 200 is the
            ceiling, so a question deeper than that wants --days.
        days: Consider runs from the last this-many whole local days instead,
            the same span --days means on the report. This is the one that means
            the same thing next month, and the one that can reach past a page of
            listing: both events are walked to the same date rather than to the
            same count. Artifacts live 90 days, so nothing older can be ingested
            however it is asked for.
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        dry_run: Say which legs would be fetched and fetch nothing. A full
            ingest is download-bound and can run for hours; this reads one
            artifact listing per run instead, so it is minutes for a wide
            window and worth doing before a long ingest.
    """
    from tools.ci_failures.ingest import ingest

    if limit is not None and days is not None:
        raise Exit("--limit and --days ask the same question two ways; pass one.", 2)
    since = _window_of_days(days).cutoff if days is not None else None

    totals = ingest(
        db_path=Path(db) if db else CI_FAILURES_DB,
        limit=25 if limit is None else int(limit),
        since=since,
        dry_run=bool(dry_run),
    )
    if dry_run:
        print(f"\nWould fetch {totals.legs} leg(s) across {totals.runs} run(s).")
        return
    print(f"\n{totals.line()}")


@task
def ci_backfill_attempts(c, db=None):
    """Resolves the attempt of legs ingested before it was being recorded.

    Downloads nothing - a run says how many attempts it had and the artifact
    listing says when each was created, which is all the resolution needs.

    Run by hand rather than on every ingest, which is where it used to sit. Its
    whole population is databases predating the column, so on any other it was a
    connection opened and a query returning no rows, every time.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
    """
    from tools.ci_failures.ingest import backfill_attempts

    backfill_attempts(Path(db) if db else CI_FAILURES_DB)


@task
def ci_report(
    c,
    db=None,
    html=None,
    json=None,
    limit=100,
    open_it=False,
    mark_seen=False,
    days=None,
):
    """Shows which tests fail and on which error.

    Two renderings of one report: a page to read, and a document for a language
    model to read. There was a third, printed to the terminal, and it was the
    worst of them - it showed 8 of the 24 fields the others show, cut every
    message to 110 characters, and dropped the source locations, the versions,
    the screenshots, the log lines and everything about what surrounded a
    failure. Anyone reading it was reading less than the page for no gain.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        html: Write a self-contained HTML page here. Defaults to
            ci_failures/ci_report.html.
        json: Write the report as JSON here, for a language model to read.
            Goes with --html: both are renderings of the one Report.
        limit: How many test/error groups to show.
        open_it: Open the HTML page in a browser once written.
        mark_seen: Record what this report said, so the next one can say what
            changed. Never done automatically: a report that moved its own
            baseline would answer differently the second time it was run on
            unchanged data.
        days: Report only on the last this-many whole local days, today
            included: 1 is today, 2 is today and yesterday. The window is a hard
            scope - every count, rate and denominator comes from inside it, and
            a test that did not fail inside it does not appear at all. That is
            what makes it answer "did what I fixed come back", which no
            all-history report can. It cannot reach further back than the
            database does: ask for more days than have been ingested and the
            answer covers what is there, so read `since` against the span the
            label claims. Goes with everything except --mark-seen; see
            `tools/ci_failures/window.py`.
    """
    from tools.ci_failures.report import (
        NoDatabaseError,
        UnanswerableError,
        WindowedBaselineError,
        build,
        snapshot_entries,
    )
    from tools.ci_failures.window import ALL_HISTORY

    window = _window_of_days(days) if days is not None else ALL_HISTORY
    db_path = Path(db) if db else CI_FAILURES_DB

    # Built once. Both renderings and the baseline are of the same Report, and
    # the reasons there may not be one are the tool's to state, not this task's.
    try:
        report = build(db_path, limit=int(limit), window=window)
    except NoDatabaseError as absent:
        print(absent)
        return
    except UnanswerableError as why:
        raise Exit(str(why), 1) from None

    if mark_seen:
        from tools.ci_failures.annotations import write_snapshot

        try:
            seen = snapshot_entries(report)
        except WindowedBaselineError as why:
            raise Exit(str(why), 2) from None
        print(f"Baseline recorded at {write_snapshot(db_path, seen)}")

    written = []
    if json:
        from tools.ci_failures.render_json import write as write_json

        written.append(write_json(report, Path(json)))
    # The page unless only the document was asked for. Both used to be an
    # either/or that silently dropped --html whenever --json was given.
    if html or not json:
        from tools.ci_failures.render_html import write as write_page

        page_at = write_page(report, Path(html) if html else CI_REPORT_HTML)
        written.append(page_at)
        if open_it:
            webbrowser.open(page_at.resolve().as_uri())
    for destination in written:
        print(f"Wrote {destination}")


@task
def ci_recompute(c, db=None, what="all"):
    """Works the derived columns out again from what is already stored.

    There is no re-parse: nothing is kept but the parsed rows, so changing what
    is read out of output.xml costs the whole window again. That is not true of
    a derived column whose source is itself in the database, and there are four
    of those - none of these needs the network or the artifacts.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        what: `signatures` after changing the masking rules in `parse.py`;
            `locations` after moving a keyword, after changing `locate._ROOTS`,
            or after an ingest that reported a library it could not import -
            that answer is cached for the whole run, so one failed import
            leaves three columns null on every row it wrote. `all` does both.
    """
    from tools.ci_failures.ingest import (
        recompute_keyword_locations,
        recompute_signatures,
    )

    known = {"all", "signatures", "locations"}
    if what not in known:
        raise Exit(f"--what wants one of {sorted(known)}, got {what!r}.", 2)
    db_path = Path(db) if db else CI_FAILURES_DB
    if not db_path.exists():
        print(f"No database at {db_path}. Run `inv ci-ingest` first.")
        return
    if what in ("all", "signatures"):
        recompute_signatures(db_path)
    if what in ("all", "locations"):
        recompute_keyword_locations(db_path)
