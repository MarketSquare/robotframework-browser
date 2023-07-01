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
import argparse
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
from subprocess import DEVNULL, PIPE, STDOUT, CalledProcessError, Popen
from typing import List

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
    print(f"Cound not wwrite to {INSTALL_LOG}, got error: {error}")  # noqa: T201
    INSTALL_LOG = Path.cwd() / log_file
    print(f"Writing install log to: {INSTALL_LOG}")  # noqa: T201

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
IS_PYTHON_37 = (sys.version_info.major, sys.version_info.minor) == (3, 7)
PYTHON_37_EOL = (
    "The end of life for Python 3.7 was 2023-06-27.\n"
    "Support for Python 3.7 has been deprecated and\n"
    "will be removed in version 16.4 of Robot Framework Browser.\n"
    "Users are strongly recommended to upgrade to a version supported by the Python community."
)


def _write_marker(silent_mode: bool = False):
    if silent_mode:
        return
    logging.info("=" * 110)


def rfbrowser_init(skip_browser_install: bool, silent_mode: bool):
    _write_marker(silent_mode)
    try:
        _rfbrowser_init(skip_browser_install, silent_mode)
        _write_marker(silent_mode)
    except Exception as error:
        _write_marker(silent_mode)
        logging.info(traceback.format_exc())
        _python_info()
        _node_info()
        _log_install_dir()
        raise error


def _log_install_dir():
    logging.info(
        f"Installation directory `{INSTALLATION_DIR!s}` does not contain the required files for."
        "unknown reason. Investigate the npm output and fix possible problems."
        "\nPrinting contents:\n"
    )
    for line in _walk_install_dir():
        logging.info(line)
    _write_marker()


def _node_info():
    process = subprocess.run(
        ["npm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=SHELL
    )
    logging.info("npm version is:n")
    logging.info(process.stdout.decode("UTF-8"))
    _write_marker()


def _python_info():
    _write_marker()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    logging.info(f"Used Python is: {sys.executable}\nVersion: {python_version}")
    _write_marker()
    logging.info("pip freeze output:\n\n")
    process = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        timeout=60,
    )
    logging.info(process.stdout.decode("UTF-8"))
    _write_marker()


def _walk_install_dir():
    lines = []
    for root, _dirs, files in os.walk(INSTALLATION_DIR):
        level = root.replace(INSTALLATION_DIR.__str__(), "").count(os.sep)
        indent = " " * 4 * (level)
        lines.append(f"{indent}{Path(root).name}/\n")
        subindent = " " * 4 * (level + 1)
        for file in files:
            lines.append(f"{subindent}{file}\n")
    return lines


def _check_npm():
    try:
        subprocess.run(["npm", "-v"], stdout=DEVNULL, check=True, shell=SHELL)
    except (CalledProcessError, FileNotFoundError, PermissionError) as exception:
        logging.info(
            "Couldn't execute npm. Please ensure you have node.js and npm installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        raise exception


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


def _log(message: str, silent_mode: bool = False):
    if silent_mode:
        return
    logging.info(message)


def _rfbrowser_init(skip_browser_install: bool, silent_mode: bool):
    _log("Installing node dependencies...", silent_mode)
    _check_files_and_access()
    _check_npm()
    _log(f"Installing rfbrowser node dependencies at {INSTALLATION_DIR}", silent_mode)
    if skip_browser_install:
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    elif not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

    process = Popen(
        "npm ci --production --parseable true --progress false",
        shell=True,
        cwd=INSTALLATION_DIR,
        stdout=PIPE,
        stderr=STDOUT,
    )

    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("UTF-8")
            try:
                _log(output, silent_mode)
            except Exception as error:
                logging.info(f"While writing log file, got error: {error}")

    if process.returncode != 0:
        raise RuntimeError(
            "Problem installing node dependencies."
            f"Node process returned with exit status {process.returncode}"
        )
    _log("rfbrowser init completed", silent_mode)
    if IS_PYTHON_37:
        logging.warning(PYTHON_37_EOL)


def rfbrowser_clean_node():
    if not NODE_MODULES.is_dir():
        logging.info(f"Could not find {NODE_MODULES}, nothing to delete.")
        return
    logging.info("Delete library node dependencies...")
    shutil.rmtree(NODE_MODULES)


def show_trace(file: str):
    absolute_file = Path(file).resolve(strict=True)
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
    subprocess.run(trace_arguments, env=env, shell=SHELL, cwd=INSTALLATION_DIR)


def show_versions():
    _write_marker()
    version_file = CURRENT_FOLDER / "version.py"
    version_text = version_file.read_text()
    match = re.search(r"\"\d+\.\d+.\d+\"", version_text)
    browser_lib_version = match.group(0) if match else "unknown"
    package_json = INSTALLATION_DIR / "package.json"
    package_json_data = json.loads(package_json.read_text())
    match = re.search(r"\d+\.\d+\.\d+", package_json_data["dependencies"]["playwright"])
    pw_version = match.group(0) if match else "unknown"
    logging.info(
        f'Installed Browser library version is: {browser_lib_version} with RF "{rf_version.VERSION}"'
    )
    logging.info(f'Installed Playwright is: "{pw_version}"')
    _write_marker()


# Based on: https://stackoverflow.com/questions/3853722/how-to-insert-newlines-on-argparse-help-text
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith("Possible commands are:"):
            parts: List[str] = []
            for part in text.splitlines():
                parsed_part = argparse.HelpFormatter._split_lines(self, part, width)
                parts.extend(parsed_part if parsed_part else "\n")
            return parts
        return argparse.HelpFormatter._split_lines(self, text, width)


def runner(command, skip_browsers, trace_file, silent_mode: bool):
    if command == "init":
        rfbrowser_init(skip_browsers, silent_mode)
    elif command == "clean-node":
        rfbrowser_clean_node()
    elif command == "show-trace":
        if not trace_file:
            raise Exception("show-trace needs also --file argument")
        show_trace(trace_file)
    elif command == "version":
        show_versions()
    else:
        raise Exception(
            f"Command should be init, clean-node or show-trace, but it was {command}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Robot Framework Browser library command line tool. If there is error during command, debug "
        "information is saved to <install dir>/Browser/rfbrowser.log file.",
        formatter_class=SmartFormatter,
    )
    parser.add_argument(
        "command",
        help=(
            "Possible commands are:\ninit\nclean-node\nshow-trace\nversion\n\ninit command will install the required node "
            "dependencies. init command is needed when library is installed or updated.\n\nclean-node is used to delete"
            "node side dependencies and installed browser binaries from the library default installation location. "
            "When upgrading browser library, it is recommended to clean old node side binaries after upgrading the "
            "Python side. Example:\n1) pip install -U robotframework-browser\n2) rfbrowser clean-node\n3)rfbrowser "
            "init.\nRun rfbrowser clean-node command also before uninstalling the library with pip. This makes sure "
            "that playwright browser binaries are not left in the disk after the pip uninstall command."
            "\n\nshow-trace command will start the Playwright trace viewer tool.\n\nversion command displays the "
            "installed Browser library, Robot Framework and Playwright versions.\n\nSee the each command argument "
            "group for more details what (optional) arguments that command supports."
        ),
        type=str,
    )
    install = parser.add_argument_group("init options")
    install.add_argument(
        "--skip-browsers",
        help="If defined skips the Playwright browser installation. Argument is optional",
        default=False,
        action="store_true",
    )
    install.add_argument(
        "--silent",
        help="Does not log anything, not even in the log file. Argument is optional",
        default=False,
        action="store_true",
    )
    trace = parser.add_argument_group("show-trace options")
    trace.add_argument(
        "--file",
        "-F",
        help=(
            "Full path to trace zip file. See New Context keyword for more details how to "
            "create trace file. Argument is mandatory."
        ),
        default=False,
    )
    args = parser.parse_args()
    command = args.command.lower()
    skip_browsers = args.skip_browsers
    trace_file = args.file
    silent_mode = args.silent
    runner(command, skip_browsers, trace_file, silent_mode)


if __name__ == "__main__":
    main()
