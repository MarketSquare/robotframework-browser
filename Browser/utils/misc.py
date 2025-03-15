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
import inspect
import os
import socket
import string
import subprocess
from pathlib import Path
from typing import Any, Union

from robot.libraries.BuiltIn import BuiltIn

from Browser.utils.data_types import DownloadInfo

get_variable_value = BuiltIn().get_variable_value


def find_free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def spawn_node_process(output_dir: Path) -> tuple[subprocess.Popen, str]:
    """
    Spawn an rfbrowser node process, that can be shared between library instances.

    Usage example:

    rc = 1
    background_process, port = spawn_node_process(ATEST_OUTPUT / "playwright-log.txt")
    try:
        os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = port
        rc = _run_pabot(args)
    finally:
        background_process.kill()


    """
    logfile = output_dir.open("w", encoding="utf-8")
    os.environ["DEBUG"] = "pw:api"
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
    port = str(find_free_port())
    process = subprocess.Popen(
        [
            "node",
            "Browser/wrapper/index.js",
            port,
        ],
        stdout=logfile,
        stderr=subprocess.STDOUT,
    )
    return process, port


def is_same_keyword(first: str, second: str) -> bool:
    if isinstance(first, str) and isinstance(second, str):
        return get_normalized_keyword(first) == get_normalized_keyword(second)
    return False


def get_normalized_keyword(keyword: str) -> str:
    if " " not in keyword:
        for index, char in enumerate(keyword):
            if index == 0:
                new_keyword = char.lower()
            elif char in string.ascii_uppercase and keyword[index - 1] != " ":
                new_keyword = f"{new_keyword} {char.lower()}"
            else:
                new_keyword = f"{new_keyword}{char}"
    else:
        new_keyword = keyword
    return new_keyword.lower().replace(" ", "_")


def keyword(name: Any = None, tags: tuple = (), types: tuple = ()):
    if inspect.isroutine(name):
        return keyword()(name)

    def decorator(func):
        func.robot_name = name
        func.robot_tags = tags
        func.robot_types = types
        return func

    return decorator


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()


def get_download_id(download: Union[DownloadInfo, str]) -> str:
    if isinstance(download, str):
        return download
    if isinstance(download, dict):
        download_id = download.get("downloadID", None)
        if download_id:
            return download_id
        raise ValueError(
            "Dictionary must contain a key 'downloadID' with a valid download id."
        )
    raise ValueError(
        "Argument must be either a dictionary with a key 'downloadID' or a string with a valid download id."
    )
