import pytest

from Browser.locators import LocatorParse


@pytest.fixture
def parse():
    return LocatorParse()


def test_parse_css_locator(parse: LocatorParse):
    assert parse.parse_locator("div") == "css=div"
    assert parse.parse_locator("css:div") == "css=div"
    assert parse.parse_locator("css  :  div") == "css=div"


def test_parse_xpath(parse: LocatorParse):
    assert parse.parse_locator("//div") == "xpath=//div"
    assert parse.parse_locator("(//div)[0]") == "xpath=(//div)[0]"
    assert parse.parse_locator("xpath://div") == "xpath=//div"


def test_parse_id(parse: LocatorParse):
    assert parse.parse_locator("id:password") == "id=password"
