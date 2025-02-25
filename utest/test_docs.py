import Browser


def test_all_keywords_have_docs():
    browser = Browser.Browser()
    for name in browser.get_keyword_names():
        assert len(browser.get_keyword_documentation(name)) > 1, (
            f"Keyword '{name}' is missing docs"
        )
