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
import subprocess
import sys
from pathlib import Path

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


def rfbrowser_init(skip_browser_install: bool):
    print("Downloading and extracting playwright browsers")
    try:
        if skip_browser_install:
            print("Skipping browser install")
            os.putenv("PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD", "1")

        installation_dir = Path(__file__).parent / "wrapper"

        # We don't want to download browsers to Browser/wrapper in development setup
        if not os.environ.get("RFBROWSER_DEVELOPMENT"):
            os.putenv(
                "PLAYWRIGHT_BROWSERS_PATH", str(installation_dir / "browser_binaries")
            )
        subprocess.run(["python", "-m", "playwright", "install"], capture_output=True)

    except Exception as err:
        raise RuntimeError("Problem installing node dependencies." + f"{err}")

    print("rfbrowser init completed")
