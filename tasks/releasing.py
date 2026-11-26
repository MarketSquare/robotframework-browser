import json
import os
import platform
import re
import sys
import sysconfig
import time
import urllib.request
from collections.abc import Iterable
from pathlib import Path

from invoke import Exit, task
from invoke.context import Context

from tasks.building import build, clean
from tasks.nodejs import NODE_MIN_GLIBC, NODE_MIN_MACOS, NODE_VERSION, stage_nodejs
from tasks.shared import (
    BROWSER_BATTERIES_DIR,
    ROOT_DIR,
    as_version,
    as_version_string,
    copy_package_files,
    step_output,
)

GITHUB_API = "https://api.github.com/repos/MarketSquare/robotframework-browser"


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
Browser supports Python 3.11+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright REPLACE_PW_VERSION. BrowserBatteries package was
released with NodeJS REPLACE_BB_NODE_VERSION.

"""


@task
def docs(c, version=None):
    """Generate library keyword documentation.

    Args:
        version: Creates keyword documentation with version
        suffix in the name. Documentation is moved to docs/versions
        folder.
    """
    import bs4
    from robot.libdoc import libdoc

    output = ROOT_DIR / "docs" / "Browser.html"
    libdoc("Browser", str(output))
    with output.open("r", encoding="utf-8") as file:
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
    with output.open("w", encoding="utf-8") as file:
        file.write(str(soup))
    if version is not None:
        target = (
            ROOT_DIR / "docs" / "versions" / f"Browser-{version.replace('v', '')}.html"
        )
        output.rename(target)


@task
def create_package(c):
    copy_package_files()
    c.run("python -m build")


@task(clean, build, docs, create_package)
def package(c: Context):
    """Build python wheel for Browser release."""


@task(clean, build)
def package_nodejs(c: Context):
    """Build Python wheel from BrowserBattiers release."""
    stage_nodejs(c)
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
    from rellu import ReleaseNotesGenerator, Version

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
    _replace_version(
        py_project_toml,
        re.compile(r'"robotframework-browser-batteries>=.*"'),
        f'"robotframework-browser-batteries>={version}"',
        1,
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
    c.run("uv lock")


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
        as_version(match.group(1))
        for match in (
            re.fullmatch(r"v?(\d+\.\d+\.\d+)", title.strip())
            for title in milestone_titles
        )
        if match
    ]
    if planned:
        return as_version_string(min(planned))
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", released)
    if not match:
        raise Exit(f"Cannot read a version number out of '{released}'.")
    major, minor, patch = (int(part) for part in match.groups())
    return as_version_string((major, minor, patch + 1))


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
    step_output("version", f"{version}.dev{stamp}")
    print(f"{version}.dev{stamp}")


def _replace_version(filepath, matcher, version, count=0):
    content = filepath.open().read()
    with open(filepath, "w") as out:
        out.write(matcher.sub(version, content, count))


@task
def gh_pages_index(c):
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
