from datetime import datetime, timezone

import pytest

from Browser.keywords import Cookie


@pytest.fixture
def cookie():
    return Cookie(None)


def test_one_cookie_as_string(cookie: Cookie):
    as_string = cookie._format_cookies_as_string(
        [{"name": "tidii", "value": 1111, "expires": -1}]
    )
    assert as_string == "tidii=1111"


def test_many_cookies_as_string(cookie: Cookie):
    cookies = [
        {"name": "tidii", "value": 1111, "httpOnly": False},
        {"name": "foo", "value": "bar", "httpOnly": True},
    ]
    as_string = cookie._format_cookies_as_string(cookies)
    assert as_string == "tidii=1111; foo=bar"


def test_as_dot_dict(cookie: Cookie):
    dot_dict = cookie._format_cookies_as_dot_dict(
        [{"name": "tidii", "value": 1111, "expires": -1}]
    )
    assert dot_dict[0].name == "tidii"
    assert dot_dict[0].value == 1111
    assert dot_dict[0].expires == datetime.fromtimestamp(-1, tz=timezone.utc)
