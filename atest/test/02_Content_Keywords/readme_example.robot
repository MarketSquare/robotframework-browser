*** Settings ***
Resource          imports.resource

Suite Teardown    Close Page

Test Tags         no-iframe    need-inet    no-docker-pr

*** Test Cases ***
Example
    Set Browser Timeout    60 seconds    scope=Test
    New Page    https://playwright.dev
    Get Text    h1    contains    Playwright
