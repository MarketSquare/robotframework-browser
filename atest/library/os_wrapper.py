import json
import os
import sys
import time
from datetime import timedelta
from pathlib import Path
from typing import Optional

from robot.api import logger  # type: ignore
from robot.libraries.OperatingSystem import OperatingSystem  # type: ignore
from robot.utils import timestr_to_secs  # type: ignore


def wait_file_count_in_directory(path: str, count: int, pattern: Optional[str] = None, absolute: bool = False, timeout: timedelta = timedelta(seconds=3)):
    wait_time = time.monotonic() + timestr_to_secs(timeout.total_seconds())
    while wait_time > time.monotonic():
        try:
            file_count = len(OperatingSystem().list_files_in_directory(path, pattern, absolute))
        except RuntimeError:
            file_count = None
        logger.info(f"File count in {path} is {file_count}")
        if file_count == count:
            return file_count
        time.sleep(0.42)
    raise AssertionError(f"File count was {file_count}, but should have been {count} within {timeout} seconds")


def wait_until_file_exists(path: Path, timeout: timedelta = timedelta(seconds=3)):
    wait_time = time.monotonic() + timestr_to_secs(timeout.total_seconds())
    while wait_time > time.monotonic():
        if Path(path).exists():
            return
        time.sleep(0.42)
    raise AssertionError(f"File {path} not found within {timeout} seconds")


def glob_files(path: str) -> list:
    """Returns files path.glob(**/*). """
    files = Path(path).glob("**/*")
    find_files = [str(file.absolute()) for file in files if file.is_file()]
    logger.info(f"Files: \"{', '.join(find_files)}\"")
    return find_files


def glob_files_count(path: str) -> int:
    """Returns files count path.glob(**/*)."""
    return len(glob_files(path))


def get_enty_command() -> str:
    """Return correct entry point command."""
    if bool(int(os.environ.get("SYS_VAR_CI_INSTALL_TEST", 0))):
        return "rfbrowser"
    return f"{sys.executable} -m Browser.entry"

def verify_translation(filename: Path) -> dict:
    """Verifies translation file."""
    with filename.open("r") as file:
        data = json.load(file)
    assert data, data
    for kw in data:
        logger.info(kw)
        assert kw == data[kw]["name"], f"{kw} != {data[kw]['name']}"
        assert data[kw]["doc"], data[kw]["doc"]
    return data
