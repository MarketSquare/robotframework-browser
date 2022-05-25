*** Settings ***
Resource        imports.resource

Suite Setup     Close Page    ALL

*** Test Cases ***
No Open Browser Throws
    Run KeyWord And Expect Error
    ...    Error: No page open.
    ...    GoTo    "about:blank"

Open GoTo GoBack GoForward
    [Tags]    slow
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
    [Teardown]    Close Context

Timeouting Go To
    New Page    ${LOGIN_URL}
    ${timeout} =    Set Browser Timeout    7ms
    Run KeyWord And Expect Error
    ...    TimeoutError: page.goto: Timeout 7ms exceeded.*
    ...    Go To    ${WELCOME_URL}
    [Teardown]    Teardown For Timeouting Go To    ${timeout}

Timeouting Go To With Custom Timeout
    [Tags]    slow
    New Page    ${LOGIN_URL}
    Run KeyWord And Expect Error
    ...    TimeoutError: page.goto: Timeout 10ms exceeded.*
    ...    Go To    ${WELCOME_URL}    10 ms
    [Teardown]    Close Context

*** Keywords ***
Teardown For Timeouting Go To
    [Arguments]    ${timeout}
    Set Browser Timeout    ${timeout}
    Close Browser
