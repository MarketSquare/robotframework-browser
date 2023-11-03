import Browser


def test_output_dir():
    browser = Browser.Browser()
    assert browser.outputdir == "."
    browser.outputdir = "/foo/bar"
    assert browser.outputdir == "/foo/bar"
