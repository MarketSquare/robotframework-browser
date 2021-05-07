*** Settings ***
Resource          ../keywords.resource

*** Test Cases ***
Crawling
    New Browser
    New Context
    Set Browser Timeout    10s
    ${urls}=    Crawl site    https://www.reaktor.com
    [Teardown]    Close Browser
