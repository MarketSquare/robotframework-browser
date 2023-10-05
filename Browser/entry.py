import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import traceback
from logging.handlers import RotatingFileHandler
from pathlib import Path

import click
from robot import version as rf_version

INSTALLATION_DIR = Path(__file__).parent / "wrapper"
NODE_MODULES = INSTALLATION_DIR / "node_modules"
# This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
# But shell=True breaks our linux CI
SHELL = bool(platform.platform().startswith("Windows"))
CURRENT_FOLDER = Path(__file__).resolve().parent
log_file = "rfbrowser.log"
INSTALL_LOG = CURRENT_FOLDER / log_file
try:
    INSTALL_LOG.touch(exist_ok=True)
except Exception as error:
    print(f"Could not write to {INSTALL_LOG}, got error: {error}")  # noqa: T201
    INSTALL_LOG = Path.cwd() / log_file
    print(f"Writing install log to: {INSTALL_LOG}")  # noqa: T201

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    handlers=[
        RotatingFileHandler(
            INSTALL_LOG, maxBytes=2000000, backupCount=10, mode="a", encoding="utf-16"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)


def _write_marker(silent_mode: bool = False):
    if silent_mode:
        return
    logging.info("=" * 110)


def _log(message: str, silent_mode: bool = False):
    if silent_mode:
        return
    try:
        logging.info(message.strip("\n"))
    except UnicodeEncodeError as error:
        logging.info(f"Could not log line, suppress error {error}")


def _process_poller(process: subprocess.Popen, silent_mode: bool):
    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("UTF-8")
            try:
                _log(output, silent_mode)
            except Exception as err:
                logging.info(f"While writing log file, got error: {err}")

    if process.returncode != 0:
        raise RuntimeError(
            "Problem installing node dependencies."
            f"Node process returned with exit status {process.returncode}"
        )


def _python_info():
    _write_marker()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    logging.info(f"Used Python is: {sys.executable}\nVersion: {python_version}")
    _write_marker()
    logging.info("pip freeze output:\n\n")
    process = subprocess.run(  # noqa: PLW1510
        [sys.executable, "-m", "pip", "freeze"],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        timeout=60,
    )
    logging.info(process.stdout.decode("UTF-8"))
    _write_marker()


def _check_files_and_access():
    if not (INSTALLATION_DIR / "package.json").is_file():
        logging.info(
            f"Installation directory `{INSTALLATION_DIR}` does not contain the required package.json ",
            "\nPrinting contents:\n",
        )
        for line in _walk_install_dir():
            logging.info(line)
        raise RuntimeError("Could not find robotframework-browser's package.json")
    if not os.access(INSTALLATION_DIR, os.W_OK):
        sys.tracebacklimit = 0
        raise RuntimeError(
            f"`rfbrowser init` needs write permissions to {INSTALLATION_DIR}"
        )


def _check_npm():
    try:
        subprocess.run(
            ["npm", "-v"], stdout=subprocess.DEVNULL, check=True, shell=SHELL
        )
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        PermissionError,
    ) as exception:
        logging.info(
            "Couldn't execute npm. Please ensure you have node.js and npm installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        raise exception


def _rfbrowser_init(
    skip_browser_install: bool, silent_mode: bool, with_deps: bool, browser: list
):
    _log("Installing node dependencies...", silent_mode)
    _check_files_and_access()
    _check_npm()
    _log(f"Installing rfbrowser node dependencies at {INSTALLATION_DIR}", silent_mode)
    if skip_browser_install:
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    elif not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

    process = subprocess.Popen(
        "npm ci --production --parseable true --progress false",
        shell=True,
        cwd=INSTALLATION_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    _process_poller(process, silent_mode)

    if not skip_browser_install:
        cmd = "npx --quiet playwright install"
        browser_as_str = " ".join(browser)
        if browser_as_str:
            browser_as_str = f"{browser_as_str} "
            cmd = f"{cmd} {browser_as_str}"
        if with_deps:
            cmd = f"{cmd.strip(' ')} --with-deps"
        _log(
            f"Installing browser {browser_as_str}binaries to {INSTALLATION_DIR}",
            silent_mode,
        )
        _log(cmd)
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=INSTALLATION_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        _process_poller(process, silent_mode)
    _log("rfbrowser init completed", silent_mode)


def _walk_install_dir():
    for file in INSTALLATION_DIR.glob("**/*"):
        level = len(file.parent.parts)
        if file.is_dir():
            indent = " " * 4 * level
            tree = f"{indent}{file.name}/\n"
        else:
            indent = " " * 4 * (level + 1)
            tree = f"{indent}{file.resolve()}"
        yield tree


def _node_info():
    process = subprocess.run(  # noqa: PLW1510
        ["npm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=SHELL
    )
    logging.info("npm version is:n")
    logging.info(process.stdout.decode("UTF-8"))
    _write_marker()


def _log_install_dir():
    logging.info(
        f"Installation directory `{INSTALLATION_DIR!s}` does not contain the required files for. "
        "unknown reason. Investigate the npm output and fix possible problems."
        "\nPrinting contents:\n"
    )
    for line in _walk_install_dir():
        logging.info(line)
    _write_marker()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    _write_marker()
    version_file = CURRENT_FOLDER / "version.py"
    version_text = version_file.read_text()
    match = re.search(r"\"\d+\.\d+.\d+\"", version_text)
    browser_lib_version = match.group(0) if match else "unknown"
    package_json = INSTALLATION_DIR / "package.json"
    package_json_data = json.loads(package_json.read_text())
    match = re.search(r"\d+\.\d+\.\d+", package_json_data["dependencies"]["playwright"])
    pw_version = match.group(0) if match else "unknown"
    logging.info(f"Installed Browser library version is: {browser_lib_version}")
    logging.info(f'Robot Framework version: "{rf_version.VERSION}"')
    logging.info(f'Installed Playwright is: "{pw_version}"')
    _write_marker()


@click.group(
    invoke_without_command=True, context_settings=CONTEXT_SETTINGS, no_args_is_help=True
)
@click.option(
    "--version",
    is_flag=True,
    help="Prints versions and exits",
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--silent", is_flag=True, help="Does not log anything, not even in the log file."
)
@click.pass_context
def cli(ctx, silent):
    """Robot Framework Browser library command line tool.

    When commands are run, output is also saved to: <install_dir>/Browser/rfbrowser.log file.

    \b
    Possible commands are:
    init
    clean-node
    show-trace

    init command will install the required node dependencies. The command is needed to run after when library is
    installed or updated. Example after first installation:

    \b
    1) pip install robotframework-browser
    2) rfbrowser init.

    clean-node command is used to delete node side dependencies and installed browser binaries from the library
    default installation location. When upgrading browser library, it is recommended to clean old node side
    binaries after upgrading the Python side. Example:

    \b
    1) pip install -U robotframework-browser
    2) rfbrowser clean-node
    3) rfbrowser init.

    Run rfbrowser clean-node command also before uninstalling the library with pip. This makes sure that playwright
    browser binaries are not left in the disk after the pip uninstall command.

    show-trace command will start the Playwright trace viewer tool.

    See each command argument help for more details what (optional) arguments that command supports.
    """
    ctx.ensure_object(dict)
    ctx.obj["SILENT"] = silent


@cli.command()
@click.pass_context
@click.option(
    "--skip-browsers",
    is_flag=True,
    help="If defined skips the Playwright browser installation. Argument is optional",
    default=False,
)
@click.option(
    "--with-deps",
    is_flag=True,
    help="If set system dependencies are installed automatically. This is useful for CI environments.",
    default=False,
)
@click.argument(
    "browser",
    type=click.Choice(["chromium", "firefox", "webkit"], case_sensitive=False),
    nargs=-1,
)
def init(ctx, skip_browsers, with_deps, browser):
    """Install node dependencies.

    init command is needed when library is installed or updated. When installing first time, run

    \b
    1) pip install robotframework-browser
    2) rfbrowser init

    When updating library to new version, run:

    \b
    1) pip install -U robotframework-browser
    2) rfbrowser clean-node
    3) rfbrowser init

    If you want to skip browser binary installation, provide --skip argument. In this case it is users responsibility
    to install browser binaries and use PLAYWRIGHT_BROWSERS_PATH environment variable to define where browser
    binaries are located.

    It is possible to install only selected browser binaries: chromium, firefox or webkit. Example:
    `rfbrowser init webkit` will install only webkit binaries and `rfbrowser init chromium firefox` will
    install both chromium firefox binaries.
    """
    silent_mode = ctx.obj["SILENT"]
    if browser and skip_browsers:
        raise click.UsageError(
            f"Both --skip-browsers and {', '.join(browser)} provided, but only should be used."
        )
    _write_marker(silent_mode)
    try:
        _rfbrowser_init(skip_browsers, silent_mode, with_deps, browser)
        _write_marker(silent_mode)
    except Exception as err:
        _write_marker(silent_mode)
        logging.info(traceback.format_exc())
        _python_info()
        _node_info()
        _log_install_dir()
        raise err


@cli.command()
def clean_node():
    """Delete node side dependencies.

    Removes node dependencies and installed browser binaries from the library default installation location.
    Should be used after upgrading the library and before uninstalling the library.
    """
    _write_marker()
    _python_info()
    _node_info()
    _log_install_dir()
    _write_marker()

    if not NODE_MODULES.is_dir():
        logging.info(f"Could not find {NODE_MODULES}, nothing to delete.")
        return
    logging.info(f"Delete library node dependencies from {NODE_MODULES}")
    shutil.rmtree(NODE_MODULES)


@cli.command(epilog="")
@click.argument(
    "file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
def show_trace(file: Path):
    """Start the Playwright trace viewer tool.

    Provide path to trace zip FILE.

    See New Context keyword documentation for more details how to create trace file:
    https://marketsquare.github.io/robotframework-browser/Browser.html#New%20Contex
    """
    absolute_file = file.resolve(strict=True)
    logging.info(f"Opening file: {absolute_file}")
    playwright = NODE_MODULES / "playwright-core"
    local_browsers = playwright / ".local-browsers"
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(local_browsers)
    trace_arguments = [
        "npx",
        "playwright",
        "show-trace",
        str(absolute_file),
    ]
    subprocess.run(  # noqa: PLW1510
        trace_arguments, env=env, shell=SHELL, cwd=INSTALLATION_DIR
    )


if __name__ == "__main__":
    cli()
