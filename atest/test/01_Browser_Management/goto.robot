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
    ${status} =    Go To    ${WELCOME_URL}
    Should Be Equal    ${status}    ${200}
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

Go To 404 URL
    [Tags]    slow
    New Page    ${LOGIN_URL}
    ${status} =    Go To    ${WELCOME_URL}_404
    Should Be Equal    ${status}    ${404}
    [Teardown]    Close Context

Timeouting Go To
    New Page    ${LOGIN_URL}
    ${timeout} =    Set Browser Timeout    2ms
    TRY
        Go To    ${WELCOME_URL}
    EXCEPT    TimeoutError: page.goto: Timeout 2ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Teardown For Timeouting Go To    ${timeout}

Timeouting Go To With Custom Timeout
    [Tags]    slow
    New Page    ${LOGIN_URL}
    TRY
        Go To    ${WELCOME_URL}    3 ms
    EXCEPT    TimeoutError: page.goto: Timeout 3ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Close Context

*** Keywords ***
Teardown For Timeouting Go To
    [Arguments]    ${timeout}
    Set Browser Timeout    ${timeout}
    Close Browser
