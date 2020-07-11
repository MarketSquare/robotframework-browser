from robot.utils import timestr_to_secs


def timestr_to_millisecs(time_str: str) -> float:
    return timestr_to_secs(time_str) * 1000
