import sys
from datetime import datetime, timezone

import pytest

from Browser.keywords import Cookie


@pytest.fixture(scope="module")
def cookie():
    return Cookie(None)


def test_cookie_as_dot_dict_expiry(cookie: Cookie):
    epoch = 1604698517
    data = cookie._cookie_as_dot_dict({"expires": epoch})
    assert data.expires == datetime.fromtimestamp(epoch, tz=timezone.utc)


def test_cookie_as_dot_dict_negative_expiry(cookie: Cookie):
    epoch = -1
    data = cookie._cookie_as_dot_dict({"expires": epoch})
    assert data.expires == datetime.fromtimestamp(epoch, tz=timezone.utc)
