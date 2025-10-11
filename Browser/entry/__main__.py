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
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import click

from Browser.utils.data_types import (
    AutoClosingLevel,
    InstallableBrowser,
    InstallationOptions,
    InstallationOptionsHelp,
    SupportedBrowsers,
)

from .constant import (
    INSTALLATION_DIR,
    NODE_MODULES,
    SHELL,
    ensure_playwright_browsers_path,
    get_browser_lib,
    log,
    write_marker,
)
from .coverage_combine import combine
from .get_versions import print_version
from .rfbrowser_init import log_install_dir, rfbrowser_init
from .transform import transform as tidy_transform
from .translation import compare_translation, get_library_translation

if TYPE_CHECKING:
    from ..browser import Browser


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


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


def _node_info():
    process = subprocess.run(  # noqa: PLW1510
        ["npm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=SHELL
    )
    log("npm version is:n")
    log(process.stdout.decode("UTF-8"))
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
    install
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

    install command will install the Playwright browsers. This command is needed when you install both Browser and
    BrowserBatteries libraries. Example:
    \b
    1) pip install robotframework-browser robotframework-browser-batteries
    2) rfbrowser install

    clean-node command is used to delete node side dependencies and installed browser binaries from the library
    default installation location. When upgrading browser library, it is recommended to clean old node side
    binaries after upgrading the Python side. Example:

    \b
    1) pip install -U robotframework-browser
    2) rfbrowser clean-node
    3) rfbrowser init.

    Example with BrowserBatteries library:

    \b
    1) pip install -U robotframework-browser robotframework-browser-batteries
    2) rfbrowser clean-node
    3) rfbrowser install

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
        rfbrowser_init(skip_browsers, silent_mode, with_deps, browser)
        write_marker(silent_mode)
    except Exception as err:
        write_marker(silent_mode)
        log(traceback.format_exc())
        _python_info()
        _node_info()
        log_install_dir()
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
    log_install_dir(False)
    write_marker()

    if not NODE_MODULES.is_dir():
        log(f"Could not find {NODE_MODULES}, nothing to delete.")
        return
    log(f"Delete library node dependencies from {NODE_MODULES}")
    shutil.rmtree(NODE_MODULES)


def _is_url(value: str) -> bool:
    p = urlparse(value)
    return p.scheme in {"http", "https"} and bool(p.netloc)


def _normalize_traces(item: str) -> str:
    """Return a list of absolute file paths (for locals) and URLs (unchanged)."""
    if _is_url(item):
        return item
    p = Path(item)
    if not p.exists() or not p.is_file():
        raise click.BadParameter(f"not a file or does not exist: {item!r}")
    return str(p.resolve(strict=True))


@cli.command(epilog="")
@click.argument(
    "file",
    type=str,  # allow URLs and paths; we validate ourselves
    required=False,
)
@click.option(
    "--browser",
    "-b",
    type=click.Choice(tuple(SupportedBrowsers._member_names_), case_sensitive=False),
    default=None,
    help="Browser to use, one of chromium, firefox, webkit.",
)
@click.option(
    "--host",
    "-h",
    type=str,
    default=None,
    help="Host to serve trace on; specifying this opens the trace in a browser tab.",
)
@click.option(
    "--port",
    "-p",
    type=click.IntRange(0, 65535),
    default=None,
    help="Port to serve trace on (0 for any free port); specifying this opens a browser tab.",
)
@click.option(
    "--stdin",
    is_flag=True,
    default=False,
    help="Accept trace URLs over stdin to update the viewer.",
)
def show_trace(
    file: str, browser: str, host: str | None, port: int | None, stdin: bool
):
    """Start the Playwright trace viewer.

    Accepts paths to trace .zip files and/or HTTP(S) URLs. Example:

        show-trace trace1.zip trace2.zip https://example.com/trace.zip

    If using Browser Batteries, only --browser argument is supported.

    To stream more traces dynamically, use --stdin and write newline-separated URLs to stdin.

    See the "New Context" keyword docs for creating traces:
    https://marketsquare.github.io/robotframework-browser/Browser.html#New%20Context
    """
    try:
        normalized_trace = _normalize_traces(file) if file else ""
    except click.BadParameter as e:
        raise click.UsageError(str(e)) from e
    if not _is_url(normalized_trace):
        log(f"Opening file: {normalized_trace}")
    ensure_playwright_browsers_path()
    try:
        _show_trace_via_npx(browser, host, port, stdin, normalized_trace)
    except Exception:
        _show_trace_via_grpc(browser, normalized_trace)


def _show_trace_via_npx(browser, host, port, stdin, normalized_trace):
    trace_arguments = ["npx", "playwright", "show-trace"]
    if browser:
        trace_arguments.extend(["--browser", browser])
    if host is not None:
        trace_arguments.extend(["--host", host])
    if port is not None:
        trace_arguments.extend(["--port", str(port)])
    if stdin:
        trace_arguments.append("--stdin")
    if normalized_trace:
        trace_arguments.append(str(normalized_trace))
    subprocess.run(  # noqa: PLW1510
        trace_arguments, shell=SHELL, cwd=INSTALLATION_DIR
    )


def _show_trace_via_grpc(browser, normalized_trace):
    args: list[str] = []
    if browser is not None:
        args += ["--browser", browser]
    if normalized_trace:
        args += [normalized_trace]
    browser_lib = get_browser_lib()
    browser_lib._auto_closing_level = AutoClosingLevel.KEEP
    browser_lib.execute_npx_playwright("show-trace", *args)


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
    from ..browser import Browser, SupportedBrowsers  # noqa: PLC0415

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
    from Browser.utils.data_types import RobotTypeConverter  # noqa: PLC0415

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
    "browser",
    type=click.Choice([b.value for b in InstallableBrowser]),
    required=False,
    default=None,
)
def install(browser: str | None = None, **flags):
    """Install Playwright Browsers binaries.

    It installs the specified browser by executing 'npx playwright install' command.

    You should only run this command if you have both Browser and BrowserBatteries
    libraries installed. Also you do not need to run `rfbrowser init` when after or
    before this command.

    Also not run this command if you have only installed Browser library. When Browser
    library is installed, run only the `rfbrowser init` command.
    """
    browser_enum = InstallableBrowser(browser) if browser else None
    selected = []
    for name, enabled in flags.items():
        if enabled:
            key = name.replace("_", "-")  # e.g. with_deps -> with-deps
            selected.append(InstallationOptions[key])
    ensure_playwright_browsers_path()
    browser_lib = get_browser_lib()
    options = [opt.value for opt in selected]
    if browser_enum:
        options.append(browser_enum.value)
    with contextlib.suppress(Exception):
        browser_lib.execute_npx_playwright("install", *options)


for opt in InstallationOptions:
    param_name = opt.name.replace("-", "_")
    install = click.option(
        opt.value, param_name, is_flag=True, help=InstallationOptionsHelp[opt.name]
    )(install)


@cli.command()
@click.option(
    "--all",
    is_flag=True,
    help="Removes all browsers used by Robot Framework Browser installation.",
)
def uninstall(all: bool):  # noqa: A002
    """Uninstall Playwright Browsers binaries.

    It uninstalls browsers by executing 'npx playwright uninstall' command.

    This command removes browsers used by this installation of Robot Framework Browser from the system
    (chromium, firefox, webkit, ffmpeg). This does not include branded channels.

    If --all option is provided, it removes all browsers used by any Robot Framework Browser installation
    from the system.
    """
    ensure_playwright_browsers_path()
    browser_lib = get_browser_lib()
    with contextlib.suppress(Exception):
        args = ["--all"] if all else []
        browser_lib.execute_npx_playwright("uninstall", *args)


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
    plugings: str | None = None,
    jsextension: str | None = None,
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
    config: Path | None = None,
    name: str | None = None,
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
