*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Fails if no success
    Run Keyword And Expect Error    STARTS:    Timeout while waiting for event "request"    Wait For Request    /api/get/json    timeout=100ms

Wait For Request synchronous
    Click    \#delayed_request
    Wait For Request    timeout=1s

Wait For Request async
    ${promise}=    Promise To    Wait For Request    matcher=    timeout=3s
    # Go To    http://localhost:7272/api/get/json
    Click    \#delayed_request
    Wait For    ${promise}

Wait For Response synchronous
    Click    \#delayed_request
    Wait For Response    timeout=1s

Wait For Response synchronous with default timeout
    Click    \#delayed_request
    Wait For Response

Wait For Response async
    ${promise}=    Promise To    Wait For Response    matcher=    timeout=3s
    Click    \#delayed_request
    ${body}=    Wait For    ${promise}

Wait Until Network Is Idle Works
    Go To    ${ROOT_URL}/delayed-load.html
    Get text    \#server_delayed_response    ==    Server response after 400ms
    Wait until network is idle    timeout=3s
    Get text    \#server_delayed_response    ==    after some time I respond

Wait For Navigation Works
    Go To    ${ROOT_URL}/redirector.html
    Wait for navigation    ${ROOT_URL}/posted.html
    Get Url    ==    ${ROOT_URL}/posted.html

Wait For Navigation Works With Regex
    Go To    ${ROOT_URL}/redirector.html
    Wait for navigation    /p[\\w]{4}d/i
    Get Url    contains    posted

Wait For Navigation Fails With Wrong Regex
    Go To    ${ROOT_URL}/redirector.html
    Run Keyword And Expect Error    *TimeoutError*    Wait for navigation    foobar
    Get Url    not contains    foobar

Wait For Navigation Fails With Wrong wait_until
    Go To    ${ROOT_URL}/redirector.html
    Run Keyword And Expect Error
    ...    *PageLoadStates does not have member 'foobar'. Available: 'domcontentloaded', 'load' and 'networkidle'*
    ...    Wait for navigation    ${ROOT_URL}/posted.html    wait_until=foobar

Wait For Navigation Works With wait_until
    FOR    ${wait_until}    IN    domcontentloaded    load    networkidle
        Go To    ${ROOT_URL}/redirector.html
        Wait for navigation    ${ROOT_URL}/posted.html    wait_until=${wait_until}
        Get Url    contains    postaaa
    END
