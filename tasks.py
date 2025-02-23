import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
from datetime import datetime
from pathlib import Path, PurePath
from typing import Iterable
from xml.etree import ElementTree as ET

from invoke import Exit, task

try:
    import bs4
    import pytest
    import robotstatuschecker
    from rellu import ReleaseNotesGenerator, Version
    from robot import __version__ as rf_version
    from robot import rebot_cli
    from robot.libdoc import libdoc

    from Browser.utils import spawn_node_process
except ModuleNotFoundError:
    traceback.print_exc()
    print('Assuming that this is for "inv deps" command and ignoring error.')

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST_OUTPUT = ROOT_DIR / "atest" / "output"
UTEST_OUTPUT = ROOT_DIR / "utest" / "output"
FLIP_RATE = ROOT_DIR / "flip_rate"
dist_dir = ROOT_DIR / "dist"
build_dir = ROOT_DIR / "build"
proto_sources = (ROOT_DIR / "protobuf").glob("*.proto")
PYTHON_SRC_DIR = ROOT_DIR / "Browser"
python_protobuf_dir = PYTHON_SRC_DIR / "generated"
wrapper_dir = PYTHON_SRC_DIR / "wrapper"
node_protobuf_dir = ROOT_DIR / "node" / "playwright-wrapper" / "generated"
node_dir = ROOT_DIR / "node"
npm_deps_timestamp_file = ROOT_DIR / "node_modules" / ".installed"
node_lint_timestamp_file = node_dir / ".linted"
ATEST_TIMEOUT = 900
cpu_count = os.cpu_count() or 1
EXECUTOR_COUNT = str(cpu_count - 1 or 1)
IN_CI = os.getenv("GITHUB_WORKFLOW")
IS_GITPOD = "gitpod.io" in os.environ.get("GITPOD_HOST", "")

ZIP_DIR = ROOT_DIR / "zip_results"
RELEASE_NOTES_PATH = Path("docs/releasenotes/Browser-{version}.rst")
RELEASE_NOTES_TITLE = "Browser library {version}"
REPOSITORY = "MarketSquare/robotframework-browser"
VERSION_PATH = Path("Browser/version.py")
RELEASE_NOTES_INTRO = """
Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library {version} is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library {version.milestone} can be found
from the `issue tracker`_.
For first time installation with pip_, just run
::
   pip install robotframework-browser
   rfbrowser init
to install the latest available release. If you upgrading
from previous release with pip_, run
::
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
Alternatively you can download the source distribution from PyPI_ and
install it manually. Browser library {version} was released on {date}.
Browser supports Python 3.9+, Node 18/20/22 LTS and Robot Framework 5.0+.
Library was tested with Playwright REPLACE_PW_VERSION

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones/{version.milestone}
"""


@task
def deps(c, system=False):
    c.run("pip install -U pip")
    c.run("pip install -U uv")
    uv_cmd = f"uv pip install -r Browser/dev-requirements.txt{' --system'*(system or IS_GITPOD)}"
    if IN_CI:
        print(f"Install packages to Python found from {sys.executable}.")
        uv_cmd = f"{uv_cmd} --python {sys.executable}"
    c.run(uv_cmd)
    if os.environ.get("CI"):
        shutil.rmtree("node_modules", ignore_errors=True)

    if _sources_changed([ROOT_DIR / "./package-lock.json"], npm_deps_timestamp_file):
        arch = " --target_arch=x64" if platform.processor() == "arm" else ""
        c.run(
            f"npm install{arch} --parseable true --progress false",
            env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
        )
        c.run(
            "npx --quiet playwright install  --with-deps",
            env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
        )
        npm_deps_timestamp_file.touch()
    else:
        print("no changes in package-lock.json, skipping npm install")


@task
def clean(c):
    for target in [
        dist_dir,
        build_dir,
        python_protobuf_dir,
        node_protobuf_dir,
        UTEST_OUTPUT,
        FLIP_RATE,
        Path("./htmlcov"),
        ATEST_OUTPUT,
        ZIP_DIR,
        Path("./.mypy_cache"),
        PYTHON_SRC_DIR / "wrapper",
    ]:
        if target.exists():
            shutil.rmtree(target)
    pyi_file = PYTHON_SRC_DIR / "__init__.pyi"
    for file in [
        npm_deps_timestamp_file,
        node_lint_timestamp_file,
        Path("./playwright-log.txt"),
        Path("./.coverage"),
        pyi_file,
        Path("./.ruff_cache"),
        Path("./.pytest_cache"),
        PYTHON_SRC_DIR / "rfbrowser.log",
    ]:
        try:
            file.unlink()
        except OSError:
            pass


@task
def protobuf(c, force=False):
    """Compile grpc protobuf files.

    Args:
        force: Force to build protobuf.
    """
    if not python_protobuf_dir.exists():
        python_protobuf_dir.mkdir()
        (python_protobuf_dir / "__init__.py").touch()
    if not node_protobuf_dir.exists():
        node_protobuf_dir.mkdir()
    gen_timestamp_file = python_protobuf_dir / ".generated"
    if _sources_changed(proto_sources, gen_timestamp_file) or force:
        _python_protobuf_gen(c)
        _node_protobuf_gen(c)
        gen_timestamp_file.touch()
    else:
        print("no changes in .proto files, skipping protobuf build")


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
    protoc_plugin = (
        ROOT_DIR
        / "node_modules"
        / ".bin"
        / f"grpc_tools_node_protoc_plugin{plugin_suffix}"
    )
    protoc_ts_plugin = (
        ROOT_DIR / "node_modules" / ".bin" / f"protoc-gen-ts{plugin_suffix}"
    )
    cmd = (
        "npm run grpc_tools_node_protoc -- "
        f"--js_out=import_style=commonjs,binary:{node_protobuf_dir} "
        f"--grpc_out=grpc_js:{node_protobuf_dir} "
        f"--plugin=protoc-gen-grpc={protoc_plugin} "
        "-I ./protobuf protobuf/*.proto"
    )
    c.run(cmd)
    cmd = (
        "npm run grpc_tools_node_protoc -- "
        f"--plugin=protoc-gen-ts={protoc_ts_plugin} "
        f"--ts_out={node_protobuf_dir} "
        "-I ./protobuf protobuf/*.proto"
    )
    c.run(cmd)


@task(protobuf)
def node_build(c):
    c.run("npm run build")
    shutil.rmtree(wrapper_dir / "static", ignore_errors=True)
    shutil.copytree(node_dir / "playwright-wrapper" / "static", wrapper_dir / "static")


@task
def create_test_app(c):
    c.run("npm run build-test-app")


@task(deps, protobuf, node_build, create_test_app)
def build(c):
    c.run("python -m Browser.gen_stub")


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
def clean_atest(c):
    if ATEST_OUTPUT.exists():
        shutil.rmtree(ATEST_OUTPUT)
    _clean_zip_dir()


@task(clean_atest, create_test_app)
def atest(
    c,
    suite=None,
    test=None,
    include=None,
    shard=None,
    zip=None,
    debug=False,
    include_mac=None,
    smoke=False,
    processes=None,
    framed=False,
    exclude=None,
):
    """Runs Robot Framework acceptance tests with pabot.

    Args:
        suite: Select which suite to run.
        test: Select which test to run.
        include: Select test by tag
        shard: Shard tests
        zip: Create zip file from output files.
        debug: Use robotframework-debugger as test listener
        smoke: If true, runs only tests that take less than 500ms.
        include_mac: Does not exclude no-mac-support tags. Should be only used in local testing
    """
    if IS_GITPOD and (not processes or int(processes) > 6):
        processes = "6"

    args = [] if processes is None else ["--processes", processes]

    args.extend(
        [
            "--ordering",
            "atest/atest_order.txt",
            "--pythonpath",
            ".",
        ]
    )
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
    args.extend(["--exclude", "tidy-transformer"])
    ATEST_OUTPUT.mkdir(parents=True, exist_ok=True)

    background_process, port = spawn_node_process(ATEST_OUTPUT / "playwright-log.txt")
    try:
        os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = port
        rc = _run_pabot(args, shard, include_mac)
    finally:
        background_process.kill()

    if zip:
        _clean_zip_dir()
        print(f"Zip file created to: {_create_zip(rc, shard)}")
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


def _create_zip(rc: int, shard: str):
    shard = shard.replace("/", "of")
    zip_dir = ZIP_DIR / "output"
    zip_dir.mkdir(parents=True)
    _clean_pabot_results(rc)
    py_version = platform.python_version()
    node_process = subprocess.run(
        ["node", "--version"], capture_output=True, check=False
    )
    node_version = node_process.stdout.strip().decode("utf-8")
    zip_name = f"{sys.platform}-rf-{rf_version}-py-{py_version}-node-{node_version}-shard-{shard}.zip"
    zip_path = zip_dir / zip_name
    print(f"Creating zip  in: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, "w")
    for file in ATEST_OUTPUT.glob("**/*.*"):
        zip_file = _files_to_zip(zip_file, file, ATEST_OUTPUT)
    for file in UTEST_OUTPUT.glob("*.*"):
        zip_file = _files_to_zip(zip_file, file, UTEST_OUTPUT)
    zip_file.close()
    return zip_path


def _files_to_zip(zip_file, file, relative_to):
    file = PurePath(file)
    arc_name = file.relative_to(str(relative_to))
    zip_file.write(file, arc_name)
    return zip_file


@task()
def copy_xunit(c):
    """Copies local xunit files for flaky test analysis"""
    xunit_dest_dir = FLIP_RATE / "xunit"
    xunit_dest_dir.mkdir(parents=True, exist_ok=True)
    robot_xunit = xunit_dest_dir / f"robot_xunit-{time.monotonic()}.xml"
    try:
        shutil.copy(ATEST_OUTPUT / "robot_xunit.xml", robot_xunit)
    except Exception as error:
        print(f"\nWhen copying robot xunit got error: {error}")
        robot_copy = False
    else:
        robot_copy = True
    pytest_xunit = xunit_dest_dir / f"pytest_xunit-{time.monotonic()}.xml"
    try:
        shutil.copy(UTEST_OUTPUT / "pytest_xunit.xml", pytest_xunit)
    except Exception as error:
        print(f"\nWhen copying pytest xunit got error: {error}")
    else:
        print(f"Copied {pytest_xunit}")
    if robot_copy:
        tree = ET.parse(robot_xunit)
        root = tree.getroot()
        now = datetime.now()
        root.attrib["timestamp"] = now.strftime("%Y-%m-%dT%H:%M:%S.000000")
        new_root = ET.Element("testsuites")
        new_root.insert(0, root)
        ET.ElementTree(new_root).write(robot_xunit)
        print(f"Copied {robot_xunit}")
    else:
        print("Not modifying RF xunit output.")


@task(clean_atest)
def atest_robot(c, zip=None, smoke=False):
    """Run atest with Robot Framework

    Arguments:
        zip: Create zip file from output files.
        smoke: If true, runs only tests that take less than 500ms.
    """
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
    command_args = _add_skips(command_args)
    command_args.append("atest/test")
    env = os.environ.copy()
    process = subprocess.Popen(command_args, env=env)
    process.wait(ATEST_TIMEOUT)
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    if zip:
        _clean_zip_dir()
        print(f"Zip file created to: {_create_zip(rc)}")
    _clean_pabot_results(rc)
    print(f"DONE rc=({rc})")
    sys.exit(rc)


@task(clean_atest)
def atest_global_pythonpath(c):
    rc = _run_pabot(["--variable", "SYS_VAR_CI:True"])
    _clean_pabot_results(rc)
    sys.exit(rc)


# Running failed tests can't clean be cause the old output.xml is required for parsing which tests failed
@task()
def atest_failed(c):
    sys.exit(_run_pabot(["--rerunfailed", "atest/output/output.xml"]))


@task()
def run_tests(c, tests):
    """Run robot with dev Browser.

    Parameter [tests] is the path to tests to run.
    """
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


@task()
def atest_coverage(c):
    """Run atest with robot.run

    To run coverage use:
    coverage run -m invoke utest
    coverage run --append -m invoke atest-coverage
    coverage report
    coverage html
    """
    import robot

    robot_args = {
        "xunit": "robot_xunit.xml",
        "exclude": "not-implementedORtidy-transformer",
        "loglevel": "DEBUG",
        "outputdir": str(ATEST_OUTPUT),
    }
    robot.run("atest/test", **robot_args)


def _run_pabot(extra_args=None, shard=None, include_mac=False):
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
        "DEBUG",
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
    return default_args


@task
def lint_python(c, fix=False):
    print("Run mypy:")
    c.run("mypy --exclude .venv --config-file Browser/mypy.ini Browser/ bootstrap.py")
    print("Run black:")
    c.run(
        "black --config Browser/pyproject.toml tasks.py Browser/ bootstrap.py utest atest"
    )
    print("Run ruff:")
    ruff_cmd = "ruff check --config Browser/pyproject.toml Browser/ bootstrap.py"
    if fix:
        ruff_cmd = f"{ruff_cmd} --fix"
    if IN_CI:
        ruff_cmd = f"{ruff_cmd} --output-format=github"
    c.run(ruff_cmd)


@task
def lint_node(c, force=False):
    """Lint node files

    Args:
        force: When set, lints node files even there is not changes.
    """
    if _sources_changed(node_dir.glob("**/*.ts"), node_lint_timestamp_file) or force:
        c.run("npm run lint")
        node_lint_timestamp_file.touch()
    else:
        print("no changes in .ts files, skipping node lint")


@task
def lint_robot(c):
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    atest_folder = Path("atest/").resolve()
    config_file = Path("Browser/pyproject.toml").resolve()
    base_commnd = ["robotidy", "--config", str(config_file)]
    if IN_CI:
        base_commnd.insert(1, "--check")
        base_commnd.insert(1, "--diff")
    cmd = base_commnd.copy()
    cmd.extend(
        [
            "--extend-exclude",
            '"(11_tidy_transformer\\Snetwork_idle_file\\.robot)|(test\\Skeywords\\.resource)"',
            str(atest_folder),
        ]
    )
    print(cmd)
    c.run(" ".join(cmd))
    # keywords.resource needs resource to be imported before library, but generally
    # that should be avoided.
    base_commnd.insert(1, "--configure")
    base_commnd.insert(
        2, "OrderSettingsSection:imports_order=resource,library,variables"
    )
    base_commnd.append(str(atest_folder.joinpath("test", "keywords.resource")))
    print(base_commnd)
    c.run(" ".join(base_commnd))


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
def run_test_app(c):
    c.run("node node/dynamic-test-app/dist/server.js")


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


@task
def create_package(c):
    shutil.copy(ROOT_DIR / "package.json", ROOT_DIR / "Browser" / "wrapper")
    shutil.copy(ROOT_DIR / "package-lock.json", ROOT_DIR / "Browser" / "wrapper")
    c.run("python -m build")


@task(clean, build, docs, create_package)
def package(c):
    """Build python wheel for release."""


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
    generator = ReleaseNotesGenerator(
        REPOSITORY,
        RELEASE_NOTES_TITLE,
        RELEASE_NOTES_INTRO.replace("REPLACE_PW_VERSION", _get_pw_version()),
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
    setup_py_file = ROOT_DIR / "setup.py"
    _replace_version(setup_py_file, node_version_matcher, f'"version": "{version}"')

    dockerfile = ROOT_DIR / "docker" / "Dockerfile.latest_release"
    docker_version_matcher = re.compile("robotframework-browser==.*")
    _replace_version(
        dockerfile, docker_version_matcher, f"robotframework-browser=={version}"
    )
    # workflow_file = root_dir / ".github" / "workflows" / "python-package.yml"
    # workflow_version_matcher = re.compile("VERSION: .*")
    # _replace_version(workflow_file, workflow_version_matcher, f"VERSION: {version}")


def _replace_version(filepath, matcher, version):
    content = filepath.open().read()
    with open(filepath, "w") as out:
        out.write(matcher.sub(version, content))


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
