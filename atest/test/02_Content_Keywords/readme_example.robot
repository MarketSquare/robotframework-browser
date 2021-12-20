*** Settings ***
Library             Browser
Resource            imports.resource

Suite Teardown      Close Page

*** Test Cases ***
Example
    ${old_timeout} =    Set Browser Timeout    60 seconds
    New Page    https://playwright.dev
    Get Text    h1    contains    Playwright
    Set Browser Timeout    ${old_timeout}
