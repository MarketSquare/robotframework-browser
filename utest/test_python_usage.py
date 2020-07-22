import pytest
import sys


def test_import():
    # Browser = __import__('Browser')
    import Browser

    # del sys.modules['robotframework']
    browser = Browser.Browser()
    print(Browser)
    browser.new_page()
    assert False
