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
import logging
import os
import platform
import re
import sys
from functools import cached_property
from logging.handlers import RotatingFileHandler
from pathlib import Path

INSTALLATION_DIR = Path(__file__).parent.parent / "wrapper"
NODE_MODULES = INSTALLATION_DIR / "node_modules"
IS_WINDOWS = platform.system() == "Windows"
# This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
# But shell=True breaks our linux CI
SHELL = bool(IS_WINDOWS)
ROOT_FOLDER = Path(__file__).resolve().parent.parent
PLAYWRIGHT_BROWSERS_PATH = "PLAYWRIGHT_BROWSERS_PATH"
IS_TERMINAL = sys.stdout.isatty()


class LogWriter:
    """Manages lazy initialization of the logger for CLI commands.

    This class ensures the logger is only initialized when actually needed,
    preventing permission errors in production environments with read-only
    filesystems where log file creation would fail during module import.
    """

    @cached_property
    def logger(self) -> logging.Logger:
        log_file = "rfbrowser.log"
        install_log = ROOT_FOLDER / log_file
        try:
            install_log.touch(exist_ok=True)
        except Exception as error:
            print(f"Could not write to {install_log}, got error: {error}")  # noqa: T201
            install_log = Path.cwd() / log_file
            print(f"Writing install log to: {install_log}")  # noqa: T201

        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        handlers: list[logging.StreamHandler] = [
            RotatingFileHandler(
                install_log,
                maxBytes=2000000,
                backupCount=10,
                mode="a",
                encoding="utf-8",
            ),
        ]
        if not IS_TERMINAL:
            handlers.append(logging.StreamHandler(sys.stdout))
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-8s] %(message)s",
            handlers=handlers,
        )
        return log

    def log(self, message: str, silent_mode: bool = False):
        if silent_mode:
            return
        if os.name == "nt":
            message = re.sub(r"[^\x00-\x7f]", r" ", message)
        try:
            self.logger.info(message.strip("\n"))
            if IS_TERMINAL:
                print(message.strip("\n"), flush=True)  # noqa: T201
        except Exception as error:
            self.logger.info(f"Could not log line, suppress error {error}")

    def info(self, message: str):
        self.logger.info(message)


log_writer = LogWriter()


def log(message: str, silent_mode: bool = False):
    log_writer.log(message, silent_mode)


def write_marker(silent_mode: bool = False):
    log(f"\n{'=' * 70}", silent_mode)


def get_browser_lib():
    from ..browser import Browser, PlaywrightLogTypes  # noqa: PLC0415
    from ..playwright import Playwright  # noqa: PLC0415

    os.environ["ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL"] = "error"
    browser_lib = Browser()
    browser_lib._playwright = Playwright(
        library=browser_lib,
        enable_playwright_debug=PlaywrightLogTypes.library,
        playwright_log=sys.stdout,
    )
    return browser_lib


def get_playwright_browser_path() -> Path:
    pw_env = os.environ.get(PLAYWRIGHT_BROWSERS_PATH)
    if pw_env and pw_env.strip():
        return Path(pw_env)
    return NODE_MODULES / "playwright-core" / ".local-browsers"


def ensure_playwright_browsers_path():
    if not os.environ.get(PLAYWRIGHT_BROWSERS_PATH):
        os.environ[PLAYWRIGHT_BROWSERS_PATH] = str(
            get_playwright_browser_path().resolve()
        )
