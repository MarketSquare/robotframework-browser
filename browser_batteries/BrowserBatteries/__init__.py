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
from subprocess import Popen
from typing import TextIO

from Browser.playwright import spawn_wrapper_process
from Browser.utils.data_types import PlaywrightLogTypes


def start_grpc_server(
    logfile: TextIO,
    host: str,
    port: str,
    enable_playwright_debug: "PlaywrightLogTypes | bool",
    coverage_output: "Path | None" = None,
) -> Popen:
    """Run the gRPC server on the NodeJS shipped inside this package.

    All this package contributes is the two paths below. Starting the process is
    the same work whichever NodeJS runs it, so it is done by the Browser library
    for both, and this package no longer has its own copy to keep in step.
    """
    bin_dir = Path(__file__).parent / "bin"
    node = "node.exe" if os.name == "nt" else "node"
    wrapper_dir = bin_dir / "wrapper"
    return spawn_wrapper_process(
        node_executable=bin_dir / node,
        script=wrapper_dir / "index.js",
        cwd=wrapper_dir,
        logfile=logfile,
        host=host,
        port=port,
        enable_playwright_debug=enable_playwright_debug,
        coverage_output=coverage_output,
    )
