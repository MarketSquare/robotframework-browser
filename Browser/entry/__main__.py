# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
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
from typing import TYPE_CHECKING, List, Optional

import click

from .translation import compare_translatoin, get_library_translaton

if TYPE_CHECKING:
    from ..browser import Browser

INSTALLATION_DIR = Path(__file__).parent.parent / "wrapper"
NODE_MODULES = INSTALLATION_DIR / "node_modules"
TIDY_TRANSFORMER_DIR = Path(__file__).parent.parent / "tidy_transformer"
# This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
# But shell=True breaks our linux CI
SHELL = bool(platform.platform().startswith("Windows"))
ROOT_FOLDER = Path(__file__).resolve().parent.parent
log_file = "rfbrowser.log"
INSTALL_LOG = ROOT_FOLDER / log_file
PLAYWRIGHT_BROWSERS_PATH = "PLAYWRIGHT_BROWSERS_PATH"
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
    if os.name == "nt":
        message = re.sub(r"[^\x00-\x7f]", r" ", message)
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
    elif not os.environ.get(PLAYWRIGHT_BROWSERS_PATH):
        os.environ[PLAYWRIGHT_BROWSERS_PATH] = "0"

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

        pw_browser_path = os.environ.get(PLAYWRIGHT_BROWSERS_PATH)
        with contextlib.suppress(ValueError):
            pw_browser_path = int(pw_browser_path)  # type: ignore
        install_dir = pw_browser_path if pw_browser_path else INSTALLATION_DIR
        _log(
            f"Installing browser {browser_as_str}binaries to {install_dir}",
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


def _log_install_dir(error_msg=True):
    if error_msg:
        logging.info(
            f"Installation directory `{INSTALLATION_DIR!s}` does not contain the required files for. "
            "unknown reason. Investigate the npm output and fix possible problems."
            "\nPrinting contents:\n"
        )
    for line in _walk_install_dir():
        logging.info(line)
    _write_marker()


def get_rf_version():
    process = subprocess.run(
        [sys.executable, "-m", "robot", "--version"], capture_output=True, check=False
    )
    return process.stdout.decode("utf-8").split(" ")[2]


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    _write_marker()
    version_file = ROOT_FOLDER / "version.py"
    version_text = version_file.read_text()
    match = re.search(r"\"\d+\.\d+.\d+\"", version_text)
    browser_lib_version = match.group(0) if match else "unknown"
    package_json = INSTALLATION_DIR / "package.json"
    package_json_data = json.loads(package_json.read_text())
    match = re.search(r"\d+\.\d+\.\d+", package_json_data["dependencies"]["playwright"])
    pw_version = match.group(0) if match else "unknown"
    logging.info(f"Installed Browser library version is: {browser_lib_version}")
    logging.info(f'Robot Framework version: "{get_rf_version()}"')
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
    launch-browser-server
    transform
    translation

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

    launch-browser-server will launch a playwright browser server.

    transform will run Robotidy with Browser library transformer and handle keyword deprecations.

    translation will generate detaul tranlsation json file from library keywords.

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
    _log_install_dir(False)
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


@cli.command()
@click.argument(
    "browser",
    type=click.Choice(("chromium", "firefox", "webkit"), case_sensitive=False),
    default="chromium",
)
@click.argument("options", nargs=-1)
def launch_browser_server(browser, options):
    """Launches a playwright browser server.

    \b
    Example:
      rfbrowser launch-browser-server chromium headless=True "timeout=10 sec"

    The browser server is started in the background and will be closed when the
    process is terminated. i.e. when users hits Ctrl-C.

    == Arguments ==

    The browser type is the first positional argument and can be one of `chromium`, `firefox` or `webkit`.

    Specific browser server arguments are `port` and `wsPath`, which be used to define
    the tcp port and the path to the websocket endpoint, so that the connection string is static.
    By default port and wsPath are randomly generated.

    \b
    Example:
      rfbrowser launch-browser-server chromium headless=No port=8282 wsPath=chromium/1

    \b
    Which results in:
      ws://127.0.0.1:8282/chromium/1

    \b
    Which can be connected with Robot Framework like:
      Connect To Browser    ws://127.0.0.1:8282/chromium/1

    The browser server can be started with additional options, which are passed as named arguments
    to the keyword `Launch Browser Server`. Arguments must be in the form of `argument_name=value`.
    See the keyword documentation for more details on the available options.

    == Connecting to a randomly generated websocket ==

    When the browser server is started, the generated wsEndpoint is printed to the console.
    This can be used to connect to the browser server with the keyword `Connect To Browser`.
    The wsEndpoint will be in the for of `ws://<ip-addr>:<port>/<token>`.

    \b
    Example: ws://127.0.0.1:55420/df86c0cf4ec85cc8f21fe12d264bb6c1

    It can be parsed from the console output with the following regular expression: `ws://.*`
    This example will return the wsEndpoint as a string form a multiline string `console_output`.

    \b
    Example: re.search(r"ws://.*", console_output).group()
    """
    from ..browser import Browser, SupportedBrowsers

    logging.getLogger().setLevel(logging.INFO)

    browser_lib = Browser()
    params = convert_options_types(options, browser_lib)
    wsEndpoint = browser_lib.launch_browser_server(
        browser=SupportedBrowsers[browser], **params
    )
    logging.info(f"Browser server started at:\n\n\n{wsEndpoint}\n\n")
    logging.info("Press Ctrl-C to stop the server")
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        logging.info("Stopping browser server by user request")
    except Exception as err:
        logging.info(f"Stopping browser server due to error: {err}")
        traceback.print_exc()
    finally:
        with contextlib.suppress(Exception):
            browser_lib._playwright_state.close_browser_server("ALL")
        logging.info("Browser server stopped")


def convert_options_types(options: List[str], browser_lib: "Browser"):
    from Browser.utils.data_types import RobotTypeConverter

    keyword_types = browser_lib.get_keyword_types("launch_browser_server")

    params = {}
    for option in options:
        if "=" not in option:
            raise RuntimeError(
                f"Invalid option {option}. Options must be in the form of argument_name=value"
            )
        key, value = option.split("=", maxsplit=1)
        if key not in keyword_types:
            raise RuntimeError(
                f"Invalid argument name {key}. Argument names must be one of {', '.join(keyword_types.keys())}"
            )
        params[key] = RobotTypeConverter.converter_for(keyword_types[key]).convert(
            name=key, value=value
        )
    return params


@cli.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    required=True,
    nargs=-1,
)
@click.option(
    "--wait-until-network-is-idle",
    is_flag=True,
    help="If set will convert Wait Until Network Is Idle keyword to Wait For Load State keyword.",
    default=False,
)
def transform(path: Path, wait_until_network_is_idle: bool):
    """Runs Robotidy with Browser library transofrormer.

    This will help users to convert automatically deprecated to new ones. Conversion
    is not allways possible and to perform automatically and always reguires human
    inspection to verify that correct result is acheived.

    The path argument is always required and should point to folder which contains
    Robot Framework test data where conversion is done.

    Example: rfbrowser transform --wait-until-network-is-idle /path/to/test
    will convert Wait Until Network Is Idle keyword to Wait For Load State keyword
    from all test data files in /path/to/test folder
    """
    if not wait_until_network_is_idle:
        logging.info("No transformer defined, exiting.")
        return
    cmd = ["robotidy"]
    if wait_until_network_is_idle:
        wait_until_network_is_idle_file = TIDY_TRANSFORMER_DIR / "network_idle.py"
        cmd.append("--transform")
        cmd.append(str(wait_until_network_is_idle_file))
    cmd.extend([str(item) for item in path])  # type: ignore
    subprocess.run(cmd, check=False)


@cli.command()
@click.argument(
    "filename",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    required=True,
)
@click.option(
    "--plugings",
    help="Same as plugins argument in the library import.",
    default=None,
    type=str,
)
@click.option(
    "--jsextension",
    help="Same as jsextension argument in the library import.",
    default=None,
    type=str,
)
@click.option(
    "--compare",
    help="Compares the translation file sha256 sum to library documentation.",
    default=False,
    is_flag=True,
    show_default=True,
)
def translation(
    filename: Path,
    plugings: Optional[str] = None,
    jsextension: Optional[str] = None,
    compare: bool = False,
):
    """Default translation file from library keywords.

    This will help users to create their own translation as Python plugins. Command
    will populate json file with english language. To create proper translation
    file, users needs to translate the keyword name and doc arguments values in
    json file.

    The filename argument will tell where the default json file is saved.

    The --pluging argument is same as plugins argument in the library import.
    If you use plugins, it is also get default translation json file also witht
    the plugin keyword included in the library.

    The --jsextension argument is same as jsextension argument in the library
    import. If you use jsextension, it is also get default translation json
    file also witht the jsextension keywords included in the library.

    If the --compare flag is set, then command does not generate template
    translation file. Then it compares sha256 sums from the filenane
    to ones read from the library documenentation. It will print out a list
    of keywords which documentation sha256 does not match. This will ease
    translation projects to identify keywords which documentation needs updating.
    """
    translation = get_library_translaton(plugings, jsextension)
    if compare:
        if table := compare_translatoin(filename, translation):
            logging.info(
                "Found differences between translation and library, see below for details."
            )
            for line in table:
                logging.info(line)
        else:
            logging.info("Translation is valid, no updated needed.")
    else:
        with filename.open("w") as file:
            json.dump(translation, file, indent=4)
        logging.info(f"Translation file created in {filename.absolute()}")


if __name__ == "__main__":
    cli()
