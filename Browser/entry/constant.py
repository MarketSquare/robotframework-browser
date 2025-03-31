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
from logging.handlers import RotatingFileHandler
from pathlib import Path

INSTALLATION_DIR = Path(__file__).parent.parent / "wrapper"
NODE_MODULES = INSTALLATION_DIR / "node_modules"
IS_WINDOWS = platform.system() == "Windows"
# This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
# But shell=True breaks our linux CI
SHELL = bool(IS_WINDOWS)
ROOT_FOLDER = Path(__file__).resolve().parent.parent
LOG_FILE = "rfbrowser.log"
INSTALL_LOG = ROOT_FOLDER / LOG_FILE
PLAYWRIGHT_BROWSERS_PATH = "PLAYWRIGHT_BROWSERS_PATH"
IS_TERMINAL = sys.stdout.isatty()
try:
    INSTALL_LOG.touch(exist_ok=True)
except Exception as error:
    print(f"Could not write to {INSTALL_LOG}, got error: {error}")  # noqa: T201
    INSTALL_LOG = Path.cwd() / LOG_FILE
    print(f"Writing install log to: {INSTALL_LOG}")  # noqa: T201

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handlers: list[logging.StreamHandler] = [
    RotatingFileHandler(
        INSTALL_LOG, maxBytes=2000000, backupCount=10, mode="a", encoding="utf-8"
    ),
]
if not IS_TERMINAL:
    handlers.append(logging.StreamHandler(sys.stdout))
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    handlers=handlers,
)


def log(message: str, silent_mode: bool = False):
    if silent_mode:
        return
    if os.name == "nt":
        message = re.sub(r"[^\x00-\x7f]", r" ", message)
    try:
        logger.info(message.strip("\n"))
        if IS_TERMINAL:
            print(message.strip("\n"), flush=True)  # noqa: T201
    except Exception as error:
        logger.info(f"Could not log line, suppress error {error}")


def write_marker(silent_mode: bool = False):
    log(f"\n{'=' * 70}", silent_mode)
