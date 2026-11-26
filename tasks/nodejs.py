import hashlib
import json
import os
import platform
import re
import shutil
import struct
import tarfile
import tempfile
import tomllib
import zipfile
from pathlib import Path

from invoke import Exit, task
from invoke.context import Context

from tasks.building import build, clean
from tasks.shared import (
    BROWSER_BATTERIES_BIN_DIR,
    ROOT_DIR,
    SKIP_BROWSER_DOWNLOAD,
    WRAPPER_DIR,
    as_version,
    as_version_string,
    copy_package_files,
    download,
    show_report,
    step_output,
)

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


def _shasums_digest(version: str) -> str:
    """sha256 of the SHASUMS256.txt nodejs.org publishes for a release."""
    with tempfile.TemporaryDirectory() as tmp:
        checksums = Path(tmp) / "SHASUMS256.txt"
        download(f"{NODE_DIST_BASE}/v{version}/SHASUMS256.txt", checksums)
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
                f"{infix}: NodeJS needs glibc {as_version_string(actual)} but "
                f"min_glibc promises {as_version_string(declared)}. Everyone "
                "in between installs the wheel and then cannot start it. Raise "
                f"min_glibc in {NODE_PIN_FILE.name} and fix the platform table "
                "in browser_batteries/README.md to match."
            )
        if actual < declared:
            return "", (
                f"{infix}: NodeJS needs no more than glibc "
                f"{as_version_string(actual)}, but min_glibc promises "
                f"{as_version_string(declared)}, so pip refuses the wheel on "
                f"platforms it would have run on. Lower min_glibc in "
                f"{NODE_PIN_FILE.name} and fix the platform table in "
                "browser_batteries/README.md to match."
            )
        return f"* {infix}: needs glibc {as_version_string(actual)}, matches", ""
    actual = _macos_floor(binary)
    declared = tuple(int(part) for part in NODE_MIN_MACOS.split("_"))
    if actual[0] != declared[0] or declared[1] != 0:
        return "", (
            f"{infix}: NodeJS declares macOS {as_version_string(actual)} but "
            f"min_macos says {as_version_string(declared)}. Set it to "
            f"{actual[0]}_0 in {NODE_PIN_FILE.name} and fix the platform table "
            "in browser_batteries/README.md to match."
        )
    covers = f"min_macos {NODE_MIN_MACOS} covers it"
    return f"* {infix}: needs macOS {as_version_string(actual)}, {covers}", ""


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
        download(f"{base_url}/{archive_name}", archive)
        checksums = Path(tmp) / "SHASUMS256.txt"
        download(f"{base_url}/SHASUMS256.txt", checksums)
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
    # Only a coverage build has a source map, which maps the V8 coverage of
    # this copy back to the TypeScript sources too.
    source_map = WRAPPER_DIR / "index.js.map"
    if (
        os.environ.get("ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE") == "1"
        and source_map.exists()
    ):
        shutil.copy(source_map, destination)
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


def _node_release_state() -> tuple:
    """What nodejs.org offers now, next to what we pin.

    Returns the pinned version, the newest release in the line we ship and the
    newest LTS line, all as comparable tuples. `inv node-version-check` and
    `inv node-pin-bump` both work from this, so they cannot come to different
    conclusions about the same day's releases.
    """
    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "index.json"
        download(NODE_DIST_INDEX, index)
        listed = json.loads(index.read_text(encoding="utf-8"))
    releases = [r for r in listed if "-" not in r["version"]]
    pinned = as_version(NODE_VERSION)
    same_line = [r for r in releases if as_version(r["version"])[0] == pinned[0]]
    if not same_line:
        raise Exit(f"nodejs.org lists no releases for NodeJS {pinned[0]}.x")
    newest = max(as_version(r["version"]) for r in same_line)
    lts_releases = [as_version(r["version"]) for r in releases if r["lts"]]
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
    lts_report = as_version_string(newest_lts) if newest_lts else "none listed"
    lines = [
        f"* shipped in BrowserBatteries: {NODE_VERSION}",
        f"* newest NodeJS {pinned[0]}.x: {as_version_string(newest)}",
        f"* newest LTS on nodejs.org: {lts_report}",
    ]
    stale = []
    move_to = newest if newest > pinned else None
    if newest_lts and newest_lts[0] > pinned[0]:
        move_to = max(move_to or newest_lts, newest_lts)
    if newest > pinned:
        behind = as_version_string(newest)
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
        target = as_version_string(move_to)
        lines.append(
            f"* shasums_sha256 for {target} is {_shasums_digest(target)}, set "
            f"that in {NODE_PIN_FILE.name} in the same commit as version."
        )
    if stale:
        lines.append(f"* {RELEASE_PROCESS}")
        show_report(lines, "NodeJS version check")
        raise Exit(f"{' '.join(stale)} {RELEASE_PROCESS}")
    lines.append("* up to date, nothing to do.")
    show_report(lines, "NodeJS version check")


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
        f"* newest NodeJS {pinned[0]}.x: {as_version_string(newest)}",
    ]
    changed = []
    if newest > pinned:
        candidate = as_version_string(newest)
        lines.append(f"* deriving the pin for NodeJS {candidate}")
        changed = _write_pin(_derive_pin(candidate)) if write else []
        lines.extend(changed or [f"* run with --write to update {NODE_PIN_FILE.name}"])
        step_output("version", candidate)
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
    show_report(lines, "NodeJS pin bump")
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
    show_report(lines, "NodeJS platform floor check")
    if problems:
        raise Exit(
            f"{len(problems)} of {len(NODE_FLOOR_TARGETS)} targets disagree. "
            f"{RELEASE_PROCESS}"
        )


def stage_nodejs(c: Context):
    """Put the official NodeJS binary next to the wrapper sources.

    This is the layout Playwright itself uses for its Python, Java and .NET
    drivers. Playwright is written against ordinary NodeJS, so anything it does
    at run time - loading builtins, resolving paths, forking helper processes -
    works the way its own tests expect.
    """
    print(f"Assemble NodeJS side to '{BROWSER_BATTERIES_BIN_DIR}'.")
    copy_package_files()
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
    stage_nodejs(c)
