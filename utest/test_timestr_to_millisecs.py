from Browser.utils.time_conversion import timestr_to_millisecs


def test_timestring_to_millisecs():
    assert timestr_to_millisecs("1s") == 1000
    assert timestr_to_millisecs(1) == 1000
    assert timestr_to_millisecs(1.0) == 1000
    assert timestr_to_millisecs("1 hour") == 3600 * 1000
