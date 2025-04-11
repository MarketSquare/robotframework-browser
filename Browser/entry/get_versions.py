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
import json
import re
import subprocess
import sys

from .constant import INSTALLATION_DIR, ROOT_FOLDER, log, write_marker


def get_rf_version():
    process = subprocess.run(
        [sys.executable, "-m", "robot", "--version"], capture_output=True, check=False
    )
    return process.stdout.decode("utf-8").split(" ")[2]


def get_pw_version() -> str:
    process = subprocess.run(
        ["npm", "list", "playwright"],
        capture_output=True,
        check=False,
        shell=True,
        cwd=INSTALLATION_DIR,
    )
    std_out = process.stdout.decode("utf-8")
    match = re.search(r"((?:@[^@]*))$", std_out)

    if match:
        version_string = match.group(0)
        version_string = version_string.replace("@", "")
        return version_string.replace("\r", "").replace("\n", "")
    log(
        f"Could not get Playwright version, got: {std_out}, reading it from package.json"
    )
    package_json = INSTALLATION_DIR / "package.json"
    package_json_data = json.loads(package_json.read_text())
    match = re.search(r"\d+\.\d+\.\d+", package_json_data["dependencies"]["playwright"])
    return match.group(0) if match else "unknown"


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    write_marker()
    version_file = ROOT_FOLDER / "version.py"
    version_text = version_file.read_text()
    match = re.search(r"\"\d+\.\d+.\d+\"", version_text)
    browser_lib_version = match.group(0) if match else "unknown"
    pw_version = get_pw_version()
    log(f"Installed Browser library version is: {browser_lib_version}")
    log(f'Robot Framework version: "{get_rf_version()}"')
    log(f'Installed Playwright is: "{pw_version}"')
    write_marker()
