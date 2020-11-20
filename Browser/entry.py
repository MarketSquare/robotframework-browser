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
import shutil
import sys
from pathlib import Path
from typing import Union

import requests
from clint.textui import progress  # type: ignore

from .version import __version__, bin_archive_filename_with_ext

USAGE = """USAGE
  rf-browser [command]
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


def _request_with_progress_bar(url: str, path: Union[str, Path]):
    r = requests.get(url, stream=True)
    if r.status_code == 404:
        raise RuntimeError(
            "Problem downloading binary dependencies."
            f"Artifact {url} was not found on server"
        )
    with open(path, "wb") as f:
        header_length = r.headers.get("content-length")
        total_length = int(header_length) if header_length else 0
        for chunk in progress.bar(
            r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
        ):
            if chunk:
                f.write(chunk)
                f.flush()


def rfbrowser_init(skip_browser_install: bool):

    print("Installing node dependencies...")
    # FIXME: do something with this
    if skip_browser_install:
        os.putenv("PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD", "1")

    installation_dir = Path(__file__).parent / "wrapper"

    print(f"Downloading and extracting rfbrowser data at {installation_dir}")

    try:
        # base_url = "https://github.com/MarketSquare/robotframework-browser/archive/"
        base_url = f"https://github.com/MarketSquare/robotframework-browser/releases/download/v{__version__}/"
        url = base_url + bin_archive_filename_with_ext
        print(f"Downloading rfbrowser data from {url}")
        _request_with_progress_bar(url, bin_archive_filename_with_ext)
        print("Decompressing")
        shutil.unpack_archive(bin_archive_filename_with_ext, installation_dir)
        os.remove(bin_archive_filename_with_ext)

    except Exception as err:
        raise RuntimeError("Problem installing node dependencies." + f"{err}")

    print("rfbrowser init completed")
