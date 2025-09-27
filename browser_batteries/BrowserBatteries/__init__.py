# Copyright 2025-     Robot Framework Foundation
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


import os
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import TextIO

from robot.api import logger

from Browser.entry.constant import PLAYWRIGHT_BROWSERS_PATH
from Browser.utils.data_types import PlaywrightLogTypes


def start_grpc_server(
    logfile: TextIO,
    host: str,
    port: str,
    enable_playwright_debug: "PlaywrightLogTypes | bool",
) -> Popen:
    """Run the prebuilt gRPC server."""
    current_dir = Path(__file__).parent
    grpc_server = "grpc_server.exe" if os.name == "nt" else "grpc_server"
    playwright_script = current_dir / "bin" / grpc_server
    logger.info(f"Starting GRPC process {playwright_script} using at {host}:{port}")
    args = [str(playwright_script), host, port]
    workdir = current_dir / "bin"
    if enable_playwright_debug == PlaywrightLogTypes.playwright:
        logger.trace("Enabling Playwright debug logging")
        os.environ["DEBUG"] = "pw:api"
    if os.environ.get("ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS"):
        logger.trace(
            "it is not possible to define ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS for BrowserBatteries"
        )
    if not os.environ.get(PLAYWRIGHT_BROWSERS_PATH):
        logger.trace(f"Setting {PLAYWRIGHT_BROWSERS_PATH} to '0'")
        os.environ[PLAYWRIGHT_BROWSERS_PATH] = "0"
    logger.trace(f"GRPC startup parameters: {args}")
    return Popen(
        args,
        cwd=workdir,
        env=os.environ,
        stdout=logfile,
        stderr=STDOUT,
    )
