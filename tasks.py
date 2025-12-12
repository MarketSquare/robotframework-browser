import json
import os
import platform
import re
import shutil
import subprocess
import sys
import sysconfig
import time
import traceback
import zipfile
from collections.abc import Iterable
from pathlib import Path, PurePath

from invoke import Exit, task
from invoke.context import Context

try:
    import bs4
    import pytest
    import robotstatuschecker
    from rellu import ReleaseNotesGenerator, Version
    from robot import __version__ as rf_version
    from robot import rebot_cli
    from robot.libdoc import libdoc
except ModuleNotFoundError:
    traceback.print_exc()
    print('Assuming that this is for "inv deps" command and ignoring error.')

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST_OUTPUT = ROOT_DIR / "atest" / "output"
UTEST_OUTPUT = ROOT_DIR / "utest" / "output"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
BROWSER_BATTERIES_DIR = ROOT_DIR / "browser_batteries"
BROWSER_BATTERIES_BIN_DIR = BROWSER_BATTERIES_DIR / "BrowserBatteries" / "bin"
proto_sources = (ROOT_DIR / "protobuf").glob("*.proto")
PYTHON_SRC_DIR = ROOT_DIR / "Browser"
python_protobuf_dir = PYTHON_SRC_DIR / "generated"
WRAPPER_DIR = PYTHON_SRC_DIR / "wrapper"
node_protobuf_dir = ROOT_DIR / "node" / "playwright-wrapper" / "generated"
node_dir = ROOT_DIR / "node"
NODE_MODULES = ROOT_DIR / "node_modules"
npm_deps_timestamp_file = NODE_MODULES / ".installed"

node_lint_timestamp_file = node_dir / ".linted"
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
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright REPLACE_PW_VERSION

"""


def _node_deps(context: Context):
    arch = " --target_arch=x64" if platform.processor() == "arm" else ""
    context.run(
        f"npm install{arch} --parseable true --progress false",
        env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
    )
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
    ]:
        if target.exists():
            shutil.rmtree(target)
    pyi_file = PYTHON_SRC_DIR / "__init__.pyi"
    for file in [
        npm_deps_timestamp_file,
        node_lint_timestamp_file,
        Path("./.coverage"),
        pyi_file,
        Path("./.ruff_cache"),
        Path("./.pytest_cache"),
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
        NODE_MODULES / ".bin" / f"grpc_tools_node_protoc_plugin{plugin_suffix}"
    )
    protoc_ts_plugin = NODE_MODULES / ".bin" / f"protoc-gen-ts{plugin_suffix}"
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


def _build_nodejs(c: Context, architecture: str):
    """Build NodeJS binary for GRPC server."""
    print(
        f"Build NodeJS binary to '{BROWSER_BATTERIES_BIN_DIR}' with architecture '{architecture}'."
    )
    _copy_package_files()
    target = f"node22-{_os_platform()}-{architecture}"
    print(f"Target: {target}")
    grpc_server_bin = "grpc_server.exe" if os.name == "nt" else "grpc_server"
    grpc_server = BROWSER_BATTERIES_BIN_DIR.joinpath(grpc_server_bin)
    cmd = [
        "node",
        "node_modules/@yao-pkg/pkg/lib-es5/bin.js",
        "--public",
        "--targets",
        target,
        "--output",
        str(grpc_server),
        ".",
    ]
    c.run(" ".join(cmd))
    if grpc_server.exists():
        print(f"GRPC server binary created at '{grpc_server}'.")
    else:
        print(f"Failed to create GRPC server binary at '{grpc_server}'.")
        sys.exit(1)


@task(clean, build)
def build_nodejs(c: Context, architecture: str):
    """Build GRPC server binary from NodeJS side."""
    _build_nodejs(c, architecture)


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


def _batteries(batteries: bool):
    batteries_dir = str(BROWSER_BATTERIES_DIR)
    if batteries:
        print("Running with BrowserBatteries")
        sys.path.append(batteries_dir)
        browser_path = NODE_MODULES / "playwright-core" / ".local-browsers"
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_path)
    return batteries_dir


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
        batteries: Run test with BrowserBatteries. Assumes that GRPC server is build.
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
    rc = _run_pabot(["--variable", "SYS_VAR_CI:True"])
    _clean_pabot_results(rc)
    sys.exit(rc)


# Running failed tests can't clean be cause the old output.xml is required for parsing which tests failed
@task()
def atest_failed(c):
    sys.exit(_run_pabot(["--rerunfailed", "atest/output/output.xml"]))


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
    ]
    ruff_cmd_check = [
        "ruff",
        "check",
        "--config",
        "pyproject.toml",
        "Browser/",
        "browser_batteries/",
        "bootstrap.py",
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
    ]
    c.run(" ".join(mypy_cmd))


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


def _get_architectures() -> str:
    if sysconfig.get_platform() == "win-amd64":
        return "x64"
    machine = platform.machine().lower()
    if machine == "aarch64":
        return "arm64"
    return machine


@task(clean_mini, build)
def package_nodejs(c: Context, architecture=None):
    """Build Python wheel from BrowserBattiers release."""
    pw_browser_bin = NODE_MODULES / "playwright-core" / ".local-browsers"
    print(f"Removing existing Playwright browsers in {pw_browser_bin}")
    shutil.rmtree(pw_browser_bin, ignore_errors=True)
    architecture = architecture or _get_architectures()
    _build_nodejs(c, architecture)
    with c.cd(BROWSER_BATTERIES_DIR):
        print(f"Building Browser Batteries package in {BROWSER_BATTERIES_DIR}")
        c.run("python -m build")
    _os_platform = sysconfig.get_platform()
    print(f"Current os platform: {_os_platform}")
    _os_platform = _os_platform.replace("-", "_").replace(".", "_").replace(" ", "_")
    if _os_platform.startswith("macosx") and platform.machine().lower() == "x86_64":
        _os_platform = _os_platform.replace("universal2", platform.machine().lower())
    elif sysconfig.get_platform().lower() == "linux-x86_64":
        _os_platform = f"manylinux_2_17_{architecture}"
    elif sysconfig.get_platform().lower() == "linux-aarch64":
        _os_platform = "manylinux_2_17_aarch64.manylinux2014_aarch64"
    dist_dir = BROWSER_BATTERIES_DIR.joinpath("dist")
    wheel_pkg = dist_dir.glob("*.whl")
    wheel_pkg = list(wheel_pkg)[0]
    wheel_pkg_os_platform = wheel_pkg.name.replace("any", _os_platform)
    wheel_pkg_os_platform = dist_dir / wheel_pkg_os_platform
    print(f"Renaming {wheel_pkg} to have platform tag {wheel_pkg_os_platform}")
    wheel_pkg.rename(wheel_pkg_os_platform)
    tar_gz_pkg = dist_dir.glob("*.tar.gz")
    tar_gz_pkg = list(tar_gz_pkg)[0]
    print(f"Deleting tar.gz package {tar_gz_pkg}")
    tar_gz_pkg.unlink()


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
