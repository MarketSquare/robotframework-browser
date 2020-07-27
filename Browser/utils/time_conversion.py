from robot.utils import timestr_to_secs  # type: ignore


def timestr_to_millisecs(time_str: str) -> int:
    return int(timestr_to_secs(time_str) * 1000)
