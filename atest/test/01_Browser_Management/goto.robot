*** Settings ***
Resource          imports.resource

*** Test Cases ***
No Open Browser Throws
    Run KeyWord and Expect Error    Tried to do playwright action 'goto', but no open page.    GoTo    "about:blank"

Open GoTo GoBack GoForward
    [Setup]    New Page    ${LOGIN_URL}
    Go To    ${WELCOME_URL}
    Get Url    ==    ${WELCOME_URL}
    Go To    ${ERROR_URL}
    Go Back
    Get Url    ==    ${WELCOME_URL}
    Go Back
    Get Url    ==    ${LOGIN_URL}
    Go Forward
    Get Url    ==    ${WELCOME_URL}
    Go Forward
    Get Url    ==    ${ERROR_URL}
    [Teardown]    Close Browser

Timeouting Go To
    New Context
    ${timeout}=  Set Browser Timeout    10ms
    New Page    ${LOGIN_URL}
    Run KeyWord and Expect Error    page.goto: Timeout 10ms exceeded.*    Go To    ${WELCOME_URL}
    Set Browser Timeout    ${timeout}
    Sleep  1s
    [Teardown]    Close Browser
