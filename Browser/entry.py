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

import os
import platform
import subprocess
import sys
from pathlib import Path
from subprocess import DEVNULL, PIPE, STDOUT, CalledProcessError, Popen

USAGE = """USAGE
  rfbrowser [command]
AVAILABLE COMMANDS
  init  Install required nodejs dependencies
    OPTIONS:
        --skip-browsers

"""


def run():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init":
        arg2 = sys.argv[2] if len(sys.argv) >= 3 else ""
        rfbrowser_init(arg2 == "--skip-browsers")
    else:
        print(f"Invalid command `{cmd}`")
        print(USAGE)
        sys.exit(64)


def rfbrowser_init(skip_browser_install: bool):
    print("Installing node dependencies...")
    installation_dir = Path(__file__).parent / "wrapper"

    if not (installation_dir / "package.json").is_file():
        print(
            f"Installation directory `{installation_dir}` does not contain the required package.json "
            + "\nPrinting contents:"
        )
        for root, _dirs, files in os.walk(installation_dir):
            level = root.replace(installation_dir.__str__(), "").count(os.sep)
            indent = " " * 4 * (level)
            print("{}{}/".format(indent, os.path.basename(root)))
            subindent = " " * 4 * (level + 1)
            for f in files:
                print("{}{}".format(subindent, f))
        raise RuntimeError("Could not find robotframework-browser's package.json")
    if not os.access(installation_dir, os.W_OK):
        sys.tracebacklimit = 0
        raise RuntimeError(
            f"`rfbrowser init` needs write permissions to {installation_dir}"
        )

    print("Installing rfbrowser node dependencies at {}".format(installation_dir))

    try:
        # This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
        # But shell=True breaks our linux CI
        shell = True if platform.platform().startswith("Windows") else False
        subprocess.run(["npm", "-v"], stdout=DEVNULL, check=True, shell=shell)
    except (CalledProcessError, FileNotFoundError, PermissionError) as exception:
        print(
            "Couldn't execute npm. Please ensure you have node.js and npm installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        sys.exit(exception)

    if skip_browser_install:
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    else:
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

    process = Popen(
        "npm install --production",
        shell=True,
        cwd=installation_dir,
        stdout=PIPE,
        stderr=STDOUT,
    )

    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline()
            print(output.decode("utf-8"))

    if process.returncode != 0:
        raise RuntimeError(
            "Problem installing node dependencies."
            + f"Node process returned with exit status {process.returncode}"
        )

    print("rfbrowser init completed")


if __name__ == "__main__":
    run()
