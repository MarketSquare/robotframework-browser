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
import os
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import click
import seedir  # type: ignore

from .constant import (
    INSTALLATION_DIR,
    IS_TERMINAL,
    NODE_MODULES,
    PLAYWRIGHT_BROWSERS_PATH,
    SHELL,
    log,
    write_marker,
)
from .coverage_combine import combine
from .get_versions import print_version
from .transform import transform as tidy_transform
from .translation import compare_translation, get_library_translation

if TYPE_CHECKING:
    from ..browser import Browser
try:
    import pty

    has_pty = True
except ImportError:
    has_pty = False

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", flags=re.IGNORECASE)
PROGRESS_MATCHER = re.compile(
    r"(?P<size>\d+(?:\.\d+)*\s\w*B)\s\[\]\s(?P<percent>\d+)(?P<time>%\s.+)"
)
PROGRESS_SIZE = 50


def _process_poller(process: subprocess.Popen, silent_mode: bool):
    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("UTF-8")
            log(output, silent_mode)

    if process.returncode != 0:
        raise RuntimeError(
            "Problem installing node dependencies."
            f"Node process returned with exit status {process.returncode}"
        )


def _python_info():
    write_marker()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    log(f"Used Python is: {sys.executable}\nVersion: {python_version}")
    write_marker()
    log("pip freeze output:\n\n")
    process = subprocess.run(  # noqa: PLW1510
        [sys.executable, "-m", "pip", "freeze"],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        timeout=60,
    )
    log(process.stdout.decode("UTF-8"))
    write_marker()


def _check_files_and_access():
    if not (INSTALLATION_DIR / "package.json").is_file():
        log(
            f"Installation directory `{INSTALLATION_DIR}` does not contain the required package.json "
            "\nPrinting contents:\n"
        )
        log(f"\n{_walk_install_dir()}")
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
        log(
            "Couldn't execute npm. Please ensure you have node.js and npm installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        raise exception


def _unix_process_executor_with_bar(command, cwd=None, silent_mode=False):
    if not has_pty:
        return
    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=slave_fd,
        stderr=slave_fd,
        stdin=subprocess.PIPE,
        close_fds=True,
    )
    os.close(slave_fd)
    last_file_msg = ""

    while True:
        try:
            output = os.read(master_fd, 1024)
            if not output:  # End of output
                break
            if silent_mode:
                continue
            with contextlib.suppress(UnicodeDecodeError):
                message = output.decode("utf-8", errors="backslashreplace")
            if os.name == "nt":
                message = re.sub(r"[^\x00-\x7f]", r" ", message)
            last_file_msg = log_progress_update(last_file_msg, message)
        except OSError:
            break
    os.close(master_fd)
    process.wait()

    if process.returncode != 0:
        raise RuntimeError(
            f"Problem installing node dependencies. "
            f"Process returned with exit status {process.returncode}"
        )


def log_progress_update(last_file_msg, message):
    try:
        message, file_msg = format_progress_bar(message)
        if IS_TERMINAL:
            print(message, end="", flush=True)  # noqa: T201
        if file_msg.strip() and last_file_msg.split("%")[0] != file_msg.split("%")[0]:
            log(file_msg.strip("\n"))
            return file_msg
        return last_file_msg
    except Exception as error:
        log(f"Could not log line, suppress error {error}")


def format_progress_bar(message: str) -> tuple[str, str]:
    progress_match = PROGRESS_MATCHER.search(message)
    if progress_match:
        size = progress_match.group("size")
        percent = progress_match.group("percent")
        time = progress_match.group("time")
        with contextlib.suppress(Exception):
            file_msg = ANSI_ESCAPE.sub(
                "",
                (
                    f"total: {size}, progress: {percent}{time}"
                    if int(percent) % 20 == 0
                    else ""
                ),
            )
            bar = "=" * (int(percent) // (100 // PROGRESS_SIZE))
            message = message.replace(
                " [] ", f" [{bar}{' ' * (PROGRESS_SIZE - len(bar))}] ", 1
            )
    else:
        file_msg = ANSI_ESCAPE.sub("", message)
    return message, file_msg


def _rfbrowser_init(
    skip_browser_install: bool, silent_mode: bool, with_deps: bool, browser: list
):
    log("Installing node dependencies...", silent_mode)
    _check_files_and_access()
    _check_npm()
    log(f"Installing rfbrowser node dependencies at {INSTALLATION_DIR}", silent_mode)
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
        log(
            f"Installing browser {browser_as_str}binaries to {install_dir}",
            silent_mode,
        )
        log(cmd, silent_mode)
        if has_pty:
            _unix_process_executor_with_bar(
                cmd,
                cwd=INSTALLATION_DIR,
                silent_mode=silent_mode,
            )
        else:
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=INSTALLATION_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            _process_poller(process, silent_mode)
    log("rfbrowser init completed", silent_mode)


def _walk_install_dir():
    return seedir.seedir(
        INSTALLATION_DIR,
        indent=4,
        printout=False,
        exclude_folders=["__pycache__", ".git"],
        depthlimit=4,
        itemlimit=(None, 5),
    )


def _node_info():
    process = subprocess.run(  # noqa: PLW1510
        ["npm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=SHELL
    )
    log("npm version is:n")
    log(process.stdout.decode("UTF-8"))
    write_marker()


def _log_install_dir(error_msg=True):
    if error_msg:
        log(
            f"Installation directory `{INSTALLATION_DIR!s}` does not contain the required files for. "
            "unknown reason. Investigate the npm output and fix possible problems."
            "\nPrinting contents:\n"
        )
    log(f"\n{_walk_install_dir()}")
    write_marker()


def get_rf_version():
    process = subprocess.run(
        [sys.executable, "-m", "robot", "--version"], capture_output=True, check=False
    )
    return process.stdout.decode("utf-8").split(" ")[2]


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
    coverage
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

    coverage command will combine the coverage reports from the pages and create a single report.

    show-trace command will start the Playwright trace viewer tool.

    launch-browser-server will launch a playwright browser server.

    transform will run Robotidy with Browser library transformer and handle keyword deprecations.

    translation will generate default translation json file from library keywords.

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
    type=click.Choice(
        [
            "chromium",
            "chrome",
            "chrome-beta",
            "msedge",
            "msedge-beta",
            "msedge-dev",
            "firefox",
            "webkit",
        ],
        case_sensitive=False,
    ),
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

    It is possible to install only selected browser binaries: chromium, chrome, chrome-beta, msedge, msedge-beta,
    msedge-dev, firefox or webkit. Example: `rfbrowser init webkit` will install only webkit binaries and
    `rfbrowser init chromium firefox` will install both chromium firefox binaries.
    """
    silent_mode = ctx.obj["SILENT"]
    if browser and skip_browsers:
        raise click.UsageError(
            f"Both --skip-browsers and {', '.join(browser)} provided, but only should be used."
        )
    write_marker(silent_mode)
    try:
        _rfbrowser_init(skip_browsers, silent_mode, with_deps, browser)
        write_marker(silent_mode)
    except Exception as err:
        write_marker(silent_mode)
        log(traceback.format_exc())
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
    write_marker()
    _python_info()
    _node_info()
    _log_install_dir(False)
    write_marker()

    if not NODE_MODULES.is_dir():
        log(f"Could not find {NODE_MODULES}, nothing to delete.")
        return
    log(f"Delete library node dependencies from {NODE_MODULES}")
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
    log(f"Opening file: {absolute_file}")
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

    browser_lib = Browser()
    params = convert_options_types(options, browser_lib)
    wsEndpoint = browser_lib.launch_browser_server(
        browser=SupportedBrowsers[browser], **params
    )
    log(f"Browser server started at:\n\n\n{wsEndpoint}\n\n")
    log("Press Ctrl-C to stop the server")
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        log("Stopping browser server by user request")
    except Exception as err:
        log(f"Stopping browser server due to error: {err}")
        traceback.print_exc()
    finally:
        with contextlib.suppress(Exception):
            browser_lib._playwright_state.close_browser_server("ALL")
        log("Browser server stopped")


def convert_options_types(options: list[str], browser_lib: "Browser"):
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
    """Runs Robotidy with Browser library transformer.

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
        log("No transformer defined, exiting.")
        return
    tidy_transform(path, wait_until_network_is_idle)


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
    translation = get_library_translation(plugings, jsextension)
    if compare:
        if table := compare_translation(filename, translation):
            log(
                "Found differences between translation and library, see below for details."
            )
            for line in table:
                log(line)
        else:
            log("Translation is valid, no updated needed.")
    else:
        with filename.open("w", encoding="utf-8") as file:
            json.dump(translation, file, indent=4)
        log(f"Translation file created in {filename.absolute()}")


@cli.command()
@click.argument(
    "input",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    required=True,
)
@click.argument(
    "output",
    type=click.Path(exists=False, dir_okay=True, path_type=Path),
    required=True,
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Optional path to monocart-coverage-reports options file.",
)
@click.option(
    "--name",
    help="Report name for title in the report.",
)
@click.option(
    "--reports",
    help="Comma separted list of reports to create. Default is 'v8'.",
    default="v8",
)
def coverage(
    input: Path,  # noqa: A002
    output: Path,
    config: Optional[Path] = None,
    name: Optional[str] = None,
    reports: str = "v8",
):
    """Combine coverage reports from the pages and create a single report.

    Coverage report should have raw data available in the input folder. The
    raw is collected when Stop Coverage keyword is called with config file
    and it has:

    module.exports = {
        reports: [['raw']]
    }

    Note this will only save raw data, if you need to also save coverage
    report for each page, use:

    module.exports = {
        reports: [['raw'], ['v8']]
    }


    The input argument is the base folder where the coverage reports are
    located. Command will look into each subfolder and if the subfolder
    contains "raw" folder, it will use data from the "raw" folder for
    combined reports

    The output argument is the folder where the combined report is saved.
    If folder does not exist, it is created. If folder exists, it's content
    is deleted before report is created.

    The config argument is optional and can be used to provide a path to a
    monocart-coverage-reports options file. For more details see:
    https://www.npmjs.com/package/monocart-coverage-reports#config-file

    The name argument is optional and can be used to provide a name for the
    report.

    The reports argument is optional and can be used to provide a list of
    reporters to create. Default is 'v8'. If you want to create multiple
    provide a comma separated list. Example: 'v8,html'
    """
    combine(input, output, config, name, reports)


if __name__ == "__main__":
    cli()
