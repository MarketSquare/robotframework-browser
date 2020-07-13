from typing import Union

from robot.utils import timestr_to_secs  # type: ignore


def timestr_to_millisecs(time_str: Union[Union[int, str], float]) -> int:
    return timestr_to_secs(time_str) * 1000
