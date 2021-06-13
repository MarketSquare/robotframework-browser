import time
from pathlib import Path
from typing import Optional, Union

from robot.api import logger  # type: ignore
from robot.libraries.OperatingSystem import OperatingSystem  # type: ignore
from robot.utils import timestr_to_secs  # type: ignore


def wait_file_count_in_directory(path: str, count: int, pattern: Optional[str] = None, absolute: bool = False, timeout: Union[int, str] = 3):
    wait_time = time.monotonic() + timestr_to_secs(timeout)
    while wait_time > time.monotonic():
        file_count = len(OperatingSystem().list_files_in_directory(path, pattern, absolute))
        logger.info(f"File count in {path} is {file_count}")
        if file_count == count:
            return file_count
        time.sleep(0.42)
    raise AssertionError(f"File count was {file_count}, but should have been {count} within {timeout}")


def glob_files(path: str) -> list:
    """Returns files path.glob(**/*). """
    path = Path(path)
    files = path.glob("**/*")
    find_files = [str(file.absolute()) for file in files if file.is_file()]
    logger.info(f"Files: \"{', '.join(find_files)}\"")
    return find_files


def glob_files_count(path: str) -> int:
    """Returns files count path.glob(**/*)."""
    return len(glob_files(path))
