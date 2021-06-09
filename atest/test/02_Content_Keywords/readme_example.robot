*** Settings ***
Library           Browser
Resource          imports.resource
Suite Teardown    Close Page

*** Test Cases ***
Example
    New Page    https://playwright.dev
    Get Text    h1    contains    Selenium
