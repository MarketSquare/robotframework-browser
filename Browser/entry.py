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
import shutil
import subprocess
import stat
import sys
from pathlib import Path
from subprocess import DEVNULL, PIPE, STDOUT, CalledProcessError, Popen

from clint.textui import progress  # type: ignore
import requests

from .version import bin_archive_filename, bin_archive_filename_with_ext, __version__

USAGE = """USAGE
  rf-browser [command]
AVAILABLE COMMANDS
  init  Install required nodejs dependencies
"""


def run():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init":
        rfbrowser_init()
    else:
        print(f"Invalid command `{cmd}`")
        print(USAGE)


def rfbrowser_init():
    def request_with_progress_bar(url: str, path: Path):
        r = requests.get(url, stream=True)
        with open(path, "wb") as f:
            total_length = int(r.headers.get("content-length"))
            for chunk in progress.bar(
                r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()

    installation_dir = Path(__file__).parent / "wrapper"

    print(f"Downloading and extracting rfbrowser data at {installation_dir}")

    try:
        # base_url = "https://github.com/MarketSquare/robotframework-browser/archive/"
        base_url = f"https://github.com/MarketSquare/robotframework-browser/releases/download/v{__version__}/"
        url = base_url + bin_archive_filename_with_ext
        print(f"Downloading rfbrowser data from {url}")
        request_with_progress_bar(url, bin_archive_filename_with_ext)
        print("Decompressing")
        shutil.unpack_archive(bin_archive_filename_with_ext, installation_dir)
        os.remove(bin_archive_filename_with_ext)

    except Exception as err:
        raise RuntimeError("Problem installing node dependencies." + f"{err}")

    print("rfbrowser init completed")
