import pytest

from Browser.locators import LocatorParse


@pytest.fixture
def parse():
    return LocatorParse()


def test_parse_css_locator(parse: LocatorParse):
    assert parse.parse_locator("div") == "css=div"
    assert parse.parse_locator("css:div") == "css=div"
    assert parse.parse_locator("css  :  div") == "css=div"
    assert parse.parse_locator("css:light  :  div") == "css:light=div"


def test_parse_xpath(parse: LocatorParse):
    assert parse.parse_locator("//div") == "xpath=//div"
    assert parse.parse_locator("(//div)[0]") == "xpath=(//div)[0]"
    assert parse.parse_locator("xpath://div") == "xpath=//div"
    assert parse.parse_locator('//div[text="some:text"]') == 'xpath=//div[text="some:text"]'


def test_parse_text(parse: LocatorParse):
    assert parse.parse_locator('text:"foobar"') == 'text="foobar"'
    assert parse.parse_locator(r'text:/^\\s*Login$/i') == r'text=/^\\s*Login$/i'


def test_parse_id(parse: LocatorParse):
    assert parse.parse_locator("id:password") == "id=password"


def test_strategy_index(parse: LocatorParse):
    assert parse._strategy_index('id:password') == 2
    assert parse._strategy_index('password') == -1
    assert parse._strategy_index('css:light:div') == 9
