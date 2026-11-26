import os
import platform
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from invoke import Exit, task

from tasks.building import create_test_app, node_build
from tasks.shared import (
    ATEST_LIB_DIR,
    ATEST_OUTPUT,
    BROWSER_BATTERIES_DIR,
    IS_GITPOD,
    NODE_MODULES,
    ROOT_DIR,
    clean_zip_dir,
)

ATEST_TIMEOUT = 900
ATEST_ROBOT_TIMEOUT = 1500
cpu_count = os.cpu_count() or 1
EXECUTOR_COUNT = str(cpu_count - 1 or 1)


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
    import pytest

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
    clean_zip_dir()


def _batteries(batteries: bool):
    batteries_dir = str(BROWSER_BATTERIES_DIR)
    if batteries:
        print("Running with BrowserBatteries")
        sys.path.append(batteries_dir)
        browser_path = NODE_MODULES / "playwright-core" / ".local-browsers"
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_path)
    return batteries_dir


ATEST_ORDER_AND_PYTHONPATH = [
    "--ordering",
    "atest/atest_order.data",
    "--pythonpath",
    ".",
]


def _get_listener_args():
    return [
        "--listener",
        str(ATEST_LIB_DIR / "test_app_listener.py"),
    ]


ATEST_BROWSERS = ("chromium", "firefox", "webkit")


def _browser_args(browser: str | None) -> list[str]:
    """Run the acceptance tests in ``browser``, leaving out its known bugs and
    the tests that only other browsers can run."""
    if browser is None:
        return []
    if browser not in ATEST_BROWSERS:
        raise Exit(
            f"--browser must be one of {', '.join(ATEST_BROWSERS)}, got {browser!r}."
        )
    args = ["--variable", f"BROWSER:{browser}", "--exclude", f"known-bug-{browser}"]
    for other in ATEST_BROWSERS:
        if other != browser:
            args.extend(["--exclude", f"{other}-only"])
    return args


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
    browser=None,
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
        browser: chromium, firefox or webkit. Default: ${BROWSER} of
            atest/test/variables.resource. Leaves out the tests tagged
            known-bug-<browser> and those tagged <other browser>-only.
    """
    if IS_GITPOD and (not processes or int(processes) > 6):
        processes = "6"

    args = [] if processes is None else ["--processes", processes]

    args.extend(ATEST_ORDER_AND_PYTHONPATH)
    args.extend(_get_listener_args())
    args.extend(_browser_args(browser))
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


def _clean_pabot_results(rc: int):
    if rc == 0:

        def on_error(function, path, excinfo):
            print(f"Could not delete {path} with excinfo: {excinfo}")

        pabot_results = ATEST_OUTPUT / "pabot_results"
        shutil.rmtree(pabot_results, onerror=on_error)
    else:
        print("Not deleting pabot_results on error")


@task(clean_atest)
def atest_robot(
    c, smoke=False, suite=None, batteries=False, parallel=False, browser=None
):
    """Run atest with Robot Framework, each run starting its own Node.js process

    Unlike `inv atest`, no Node.js process is shared: the library starts one
    the way it does for a user, which is what the install tests check.

    Arguments:
        smoke: If true, runs only tests that take less than 500ms.
        suite: Select which suite to run.
        batteries: If true, includes BrowserBatteries in the test run.
        parallel: If true, runs the suites with pabot, one process per CPU but
            one, and every pabot process starts its own Node.js process.
        browser: chromium, firefox or webkit, as for `inv atest`.
    """
    browser_args = _browser_args(browser)
    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "debug"
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    sys_var_ci = int(os.environ.get("SYS_VAR_CI_INSTALL_TEST", 0))
    sys_var_cmd = (
        "SYS_VAR_CI_INSTALL_TEST:True"
        if sys_var_ci
        else "SYS_VAR_CI_INSTALL_TEST:False"
    )
    if parallel:
        args = [*ATEST_ORDER_AND_PYTHONPATH, "--variable", sys_var_cmd, *browser_args]
        args.extend(["--exclude", "slow"] if smoke else [])
        args.extend(_get_listener_args())
        if suite:
            args.extend(["--suite", suite])
        if batteries:
            args.extend(["--pythonpath", _batteries(batteries)])
        rc = _run_pabot(args)
        _clean_pabot_results(rc)
        sys.exit(rc)
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
    command_args.extend(browser_args)
    if suite:
        command_args.extend(["--suite", suite])
    if batteries:
        batteries_dir = _batteries(batteries)
        command_args.extend(["--pythonpath", batteries_dir])
    import robotstatuschecker
    from robot import rebot_cli

    command_args = _add_skips(command_args)
    command_args.append("atest/test")
    env = os.environ.copy()
    process = subprocess.Popen(command_args, env=env)
    process.wait(ATEST_ROBOT_TIMEOUT)
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    _clean_pabot_results(rc)
    print(f"DONE rc=({rc})")
    sys.exit(rc)


@task()
def atest_failed(c, browser=None):
    """Reruns the acceptance tests that failed in the last run.

    Args:
        browser: chromium, firefox or webkit. output.xml does not record the
            browser, so pass the one the last run used.
    """
    args = ["--rerunfailed", "atest/output/output.xml"]
    args.extend(_get_listener_args())
    args.extend(_browser_args(browser))
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
    batteries=False,
    browser=None,
):
    """Run acceptance tests with pabot, measuring Python and Node.js coverage.

    Builds the Node.js wrapper with source maps, runs the acceptance tests under
    `coverage run -m pabot.pabot` and stops the shared Node.js process with
    SIGTERM, so it writes its V8 coverage. The task fails when Node.js does not
    write it.

    Args:
        suite:    Select which suite to run.
        test:     Select which test to run.
        include:  Select tests by tag.
        debug:    Use robotframework-debugger as test listener.
        exclude:  Exclude tests by tag.
        loglevel: Set log level for robot framework.
        batteries: Run the shared Node.js process from BrowserBatteries. Assumes
            the NodeJS side was assembled with
            ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE=1, see `inv build-nodejs`.
        browser:  chromium, firefox or webkit, as for `inv atest`.

    Python: every pabot worker writes its own `.coverage.*` file. Run
    `inv utest` first, because pytest-cov erases `.coverage.*` files.
    `inv coverage` runs every suite in that order and merges the results.

    Node.js: atest/output/node-coverage-report/ has an HTML report and
    lcov.info, with one record per wrapper `.ts` file, at the same paths Jest
    uses. V8 data goes to NODE_V8_COVERAGE when it is set, otherwise to
    atest/output/browser/node-v8-coverage/.

    Node.js coverage is not collected on Windows.
    """
    browser_args = _browser_args(browser)
    from Browser.utils import spawn_node_process

    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "debug"
    os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE"] = "1"
    node_build(c)
    clean_atest(c)
    create_test_app(c)
    ATEST_OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in ROOT_DIR.glob(".coverage.*"):
        stale.unlink()

    node_coverage = sys.platform != "win32"
    if node_coverage:
        v8_coverage_dir = Path(
            os.environ.setdefault(
                "NODE_V8_COVERAGE",
                str(ATEST_OUTPUT / "browser" / "node-v8-coverage"),
            )
        )
        v8_coverage_dir.mkdir(parents=True, exist_ok=True)
    else:
        print("Node.js V8 coverage is not supported on Windows.")

    args = ATEST_ORDER_AND_PYTHONPATH + _get_listener_args() + browser_args
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
    args.extend(["--exclude", "no-coverage-support"])

    _batteries(batteries)
    node_started = time.time()
    background_process, port = spawn_node_process(ATEST_OUTPUT / "playwright-log.txt")
    try:
        os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = port
        rc = _run_pabot(args, loglevel=loglevel or "DEBUG", coverage=True)
    finally:
        if node_coverage:
            _stop_node_flushing_coverage(background_process)
        else:
            background_process.kill()

    if node_coverage:
        _require_v8_coverage_written_since(v8_coverage_dir, node_started)
        c.run(f'node node/process-coverage.mjs "{v8_coverage_dir}"')
    print("\nMerge all coverage into one report: inv coverage-report")
    sys.exit(rc)


NODE_COVERAGE_FLUSH_TIMEOUT = 10


def _stop_node_flushing_coverage(process: subprocess.Popen):
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=NODE_COVERAGE_FLUSH_TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise Exit(
            f"Node.js did not exit within {NODE_COVERAGE_FLUSH_TIMEOUT} s of "
            "SIGTERM and was killed, so its V8 coverage was not written.",
            code=1,
        ) from None
    if process.returncode != 0:
        raise Exit(
            f"Node.js exited with {process.returncode} after SIGTERM, so its "
            "V8 coverage may not have been written.",
            code=1,
        )
    print("Node.js exited after SIGTERM")


def _require_v8_coverage_written_since(v8_coverage_dir: Path, since: float):
    if not any(
        data.stat().st_mtime >= since for data in v8_coverage_dir.glob("*.json")
    ):
        raise Exit(
            f"Node.js wrote no V8 coverage to {v8_coverage_dir} during this run.",
            code=1,
        )


def _make_pabot_workers_use_this_python():
    this_python_bin = str(Path(sys.executable).parent)
    os.environ["PATH"] = this_python_bin + os.pathsep + os.environ.get("PATH", "")


def _run_pabot(
    extra_args=None, shard=None, include_mac=False, loglevel="DEBUG", coverage=False
):
    import robotstatuschecker
    from robot import rebot_cli

    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    launcher = (
        [sys.executable, "-m", "coverage", "run"] if coverage else [sys.executable]
    )
    if coverage:
        _make_pabot_workers_use_this_python()
    pabot_args = (
        launcher
        + [
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
        ]
        + (["--shard", shard] if shard else [])
    )
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
    from robot import version as robot_version_module

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
