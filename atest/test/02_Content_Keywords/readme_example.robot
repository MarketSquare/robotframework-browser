*** Settings ***
Resource            imports.resource

Suite Teardown      Close Page

Test Tags           no-iframe    need-inet    no-docker-pr

*** Test Cases ***
Example
    ${old_timeout} =    Set Browser Timeout    60 seconds
    New Page    https://playwright.dev
    Get Text    h1    contains    Playwright
    Set Browser Timeout    ${old_timeout}
