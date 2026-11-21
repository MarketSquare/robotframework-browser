*** Settings ***
Resource       imports.resource

Suite Setup    Close Page    ALL

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
    Set Browser Timeout    2ms    scope=Test
    TRY
        Go To    ${WELCOME_URL}
    EXCEPT    TimeoutError: page.goto: Timeout 2ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Close Browser

Timeouting Go To With Custom Timeout
    [Tags]    slow
    New Page    ${LOGIN_URL}
    TRY
        Go To    ${WELCOME_URL}    3 ms
    EXCEPT    TimeoutError: page.goto: Timeout 3ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Close Context

Go Back Stops Waiting At Commit
    New Page    ${STALLED_PAGE}    wait_until=commit
    Go To    ${WELCOME_URL}
    Go Back    timeout=5s    wait_until=commit
    Get Url    ==    ${STALLED_PAGE}
    [Teardown]    Close Context

Go Forward Stops Waiting At Commit
    New Page    ${WELCOME_URL}
    Go To    ${STALLED_PAGE}    wait_until=commit
    Go Back
    Go Forward    timeout=5s    wait_until=commit
    Get Url    ==    ${STALLED_PAGE}
    [Teardown]    Close Context

Go Back Uses Custom Timeout
    New Page    ${STALLED_PAGE}    wait_until=commit
    Go To    ${WELCOME_URL}
    Run Keyword And Expect Error    *Timeout 100ms exceeded*    Go Back    timeout=100ms
    [Teardown]    Close Context

Go Forward Uses Custom Timeout
    New Page    ${WELCOME_URL}
    Go To    ${STALLED_PAGE}    wait_until=commit
    Go Back
    Run Keyword And Expect Error    *Timeout 100ms exceeded*    Go Forward    timeout=100ms
    [Teardown]    Close Context

Go To Sends Referer
    New Page
    Go To    ${REFERER_URL}    referer=https://partner.example.com/campaign
    Get Text    id=referer    ==    https://partner.example.com/campaign
    Go To    ${REFERER_URL}
    Get Text    id=referer    ==    ${EMPTY}
    [Teardown]    Close Context

Context Referer Header Wins Over Go To Referer
    New Context    extraHTTPHeaders={"Referer": "https://context.example.com/"}
    New Page
    Go To    ${REFERER_URL}    referer=https://partner.example.com/campaign
    Get Text    id=referer    ==    https://context.example.com/
    [Teardown]    Close Context
