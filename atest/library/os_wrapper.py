import json
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from robot.api import logger  # type: ignore
from robot.libraries.OperatingSystem import OperatingSystem  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robot.utils import timestr_to_secs  # type: ignore


def wait_file_count_in_directory(
    path: str,
    count: int,
    pattern: Optional[str] = None,
    absolute: bool = False,
    timeout: timedelta = timedelta(seconds=3),
):
    wait_time = time.monotonic() + timestr_to_secs(timeout.total_seconds())
    while wait_time > time.monotonic():
        try:
            file_count = len(
                OperatingSystem().list_files_in_directory(path, pattern, absolute)
            )
        except RuntimeError:
            file_count = None
        logger.info(f"File count in {path} is {file_count}")
        if file_count == count:
            return file_count
        time.sleep(0.42)
    raise AssertionError(
        f"File count was {file_count}, but should have been {count} within {timeout} seconds"
    )


def wait_until_file_exists(path: Path, timeout: timedelta = timedelta(seconds=3)):
    wait_time = time.monotonic() + timestr_to_secs(timeout.total_seconds())
    while wait_time > time.monotonic():
        if Path(path).exists():
            return
        time.sleep(0.42)
    raise AssertionError(f"File {path} not found within {timeout} seconds")


def glob_files(path: str) -> list:
    """Returns files path.glob(**/*)."""
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
        assert data[kw]["sha256"]
    return data


def modify_sha256(filename: Path, *kw_names):
    with filename.open("r") as file:
        data = json.load(file)
    for kw in data:
        if kw in kw_names:
            logger.info(f"Modify keyword {kw} sha256 value")
            data[kw]["sha256"] = str(random.randint(1, 1000))
    with filename.open("w") as file:
        json.dump(data, file, indent=4)


def remove_sha256(filename: Path, *kw_names):
    with filename.open("r") as file:
        data = json.load(file)
    for kw in data:
        if kw in kw_names:
            logger.info(f"Remove keyword {kw} sha256 value")
            kw_data = data[kw]
            kw_data.pop("sha256", None)
    with filename.open("w") as file:
        json.dump(data, file, indent=4)


def remoe_kw(filename: Path, *kw_names):
    with filename.open("r") as file:
        data = json.load(file)
    for kw in kw_names:
        logger.info(f"Remove {kw}")
        data.pop(kw, None)
    with filename.open("w") as file:
        json.dump(data, file, indent=4)


def add_kw(filename: Path, *kw_names):
    with filename.open("r") as file:
        data = json.load(file)
    for kw in kw_names:
        kw_data = {
            "name": kw,
            "doc": str(random.randint(1, 1000)),
            "sha256": str(random.randint(1, 1000)),
        }
        logger.info(f"Add keyword {kw_data}")
        data[kw] = kw_data
    with filename.open("w") as file:
        json.dump(data, file, indent=4)


def is_macos() -> bool:
    return sys.platform == "darwin"


def get_python_binary_path() -> str:
    return sys.executable


def _parse_fi_date(date: str) -> datetime:
    if not date:
        # 2000-01-01 because of Windos raising OsError
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp
        return datetime.fromtimestamp(946688461)
    try:
        return datetime.strptime(date, "%d.%m.%Y klo %H.%M.%S")
    except ValueError:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


ROBOT_LIBRARY_CONVERTERS = {datetime: _parse_fi_date}


def delta_time_is_less_than(
    expected_time: datetime,
    locator: str,
    max_difference: timedelta = timedelta(seconds=30),
    timeout: timedelta = timedelta(seconds=30),
):
    """Fail if the difference between time and time in selector is greater than difference within timeout."""
    browser = BuiltIn().get_library_instance("Browser")
    time_page = _parse_fi_date(browser.get_text(locator))
    wait_time = time.monotonic() + int(timestr_to_secs(timeout.total_seconds()))
    while not _delta_time_is_less_than(time_page, expected_time, max_difference):
        time_page = _parse_fi_date(browser.get_text(locator))
        if wait_time < time.monotonic():
            BuiltIn().run_keyword("Take Screenshot")
            raise AssertionError(f"Time difference is greater than {max_difference}")
        time.sleep(0.42)


def _delta_time_is_less_than(
    time1: datetime, time2: datetime, max_difference: timedelta = timedelta(seconds=30)
) -> bool:
    """Fail if the difference between time1 and time2 is greater than difference."""
    logger.info(
        f"time1: {time1}, time2: {time2}, max difference: {max_difference.seconds}"
    )
    time_difference = abs(time1.timestamp() - time2.timestamp())
    if time_difference > max_difference.seconds:
        logger.info(
            f"Time difference {time_difference} is greater than {max_difference.seconds}"
        )
        return False
    return True


def time1_is_less_than_time2(time1: datetime, time2: datetime) -> bool:
    """Fail if time1 is greater than time2."""
    logger.info(f"Time1 is {time1} and time2 is {time2}")
    if time1.timestamp() > time2.timestamp():
        logger.info(f"Time1 {time1} is greater than time2 {time2}")
        raise ValueError(f"Time1 {time1} is greater than time2 {time2}")
    return True


def dates_are_equal(date1: datetime, date2: datetime) -> bool:
    """Fail if time1 is not equal to time2."""
    logger.info(f"Time1 is {date1} and time2 is {date2}")
    if date1.timestamp() != date2.timestamp():
        logger.info(f"Time1 {date1} is not equal to time2 {date2}")
        raise ValueError(f"Time1 {date1} is not equal to time2 {date2}")
    return True


def file_as_uri(path: str) -> Path:
    """Return file as uri."""
    return Path(path).as_uri()


def get_parent(path: str) -> Path:
    """Return parent of the path."""
    return Path(path).parent


def relative_to(path1: Path, path2: Path) -> str:
    """Return relative path."""
    return path1.relative_to(path2)
