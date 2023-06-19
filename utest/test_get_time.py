from datetime import timedelta

import pytest

from Browser import Browser


@pytest.fixture(scope="module")
def lib():
    return Browser()


def test_none(lib: Browser):
    assert lib.get_timeout(None) == 10000
    assert Browser(timeout=timedelta(seconds=0.001)).timeout == 1


def test_timedelta(lib: Browser):
    assert lib.get_timeout(timedelta(seconds=1)) == 1000
    assert lib.get_timeout(timedelta(seconds=0)) == 0
    assert lib.get_timeout(timedelta(milliseconds=10)) == 10


def test_rf_time(lib: Browser):
    assert lib.get_timeout("2 s") == 2000  # type: ignore


def test_convert_timeout(lib: Browser):
    assert lib.convert_timeout(0.1) == 100
    assert lib.convert_timeout(0.1, False) == 0.1


def test_millisecs_to_timestr(lib: Browser):
    assert lib.millisecs_to_timestr(1000) == "1 second"
    assert lib.millisecs_to_timestr(1) == "1 millisecond"
    assert lib.millisecs_to_timestr(3600000) == "1 hour"
