*** Settings ***
Resource        imports.resource

Test Setup      Ensure Location    ${LOGIN_URL}

*** Test Cases ***
Wait For Fails If No Success
    Run Keyword And Expect Error
    ...    GLOB:*Timeout 100ms exceeded while waiting for event "request"*
    ...    Wait For Request
    ...    /api/get/json
    ...    timeout=100ms

Wait For Request Synchronous
    Click    \#delayed_request
    Wait For Request    timeout=1s

Wait For Request Async
    ${promise} =    Promise To    Wait For Request    matcher=    timeout=3s
    Click    \#delayed_request
    Wait For    ${promise}

Wait For Request Url
    Click    \#delayed_request
    Wait For Request    matcher=${ROOT_URL}/api/get/json    timeout=1s

Wait For Request Regex
    Click    \#delayed_request
    Wait For Request    matcher=\\/\\/local\\w+\\:\\d+\\/api    timeout=1s

Wait For Request Predicate
    Click    \#delayed_request
    Wait For Request    matcher=request => request.url().endsWith('api/get/json') && request.method() === 'GET'
    ...    timeout=1s

Wait For Response Synchronous
    Click    \#delayed_request
    Wait For Response    timeout=1s

Wait For Response Synchronous With Default Timeout
    Click    \#delayed_request
    Wait For Response

Wait For Response Synchronous With Regex Matcher
    Click    \#delayed_request
    Wait For Response    matcher=\\/\\/local\\w+\\:\\d+\\/api

Wait For Response Synchronous With Predicate
    Click    \#delayed_request
    Wait For Response    response => response.url().endsWith('json') && response.request().method() === 'GET'

Wait For Response Async
    ${promise} =    Promise To    Wait For Response    matcher=    timeout=3s
    Click    \#delayed_request
    ${body} =    Wait For    ${promise}

Wait Until Network Is Idle Works
    [Tags]    slow
    Go To    ${ROOT_URL}/delayed-load.html
    Get Text    \#server_delayed_response    ==    Server response after 400ms
    Wait Until Network Is Idle    timeout=3s
    Get Text    \#server_delayed_response    ==    after some time I respond

Wait For Navigation Works
    [Tags]    slow
    Go To    ${ROOT_URL}/redirector.html
    Wait For Navigation    ${ROOT_URL}/posted.html
    Get Url    ==    ${ROOT_URL}/posted.html

Wait For Navigation Works With Regex
    [Tags]    slow
    Go To    ${ROOT_URL}/redirector.html
    Wait For Navigation    /p[\\w]{4}d/i
    Get Url    contains    posted

Wait For Navigation Fails With Wrong Regex
    [Tags]    slow
    Go To    ${ROOT_URL}/redirector.html
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error    *TimeoutError*    Wait for navigation    foobar
    Set Browser Timeout    ${timeout}
    Get Url    not contains    foobar

Wait For Navigation Fails With Wrong Wait_until
    [Tags]    slow
    Go To    ${ROOT_URL}/redirector.html
    Run Keyword And Expect Error
    ...    *PageLoadStates does not have member 'foobar'. Available: 'commit', 'domcontentloaded', 'load' and 'networkidle'*
    ...    Wait for navigation
    ...    ${ROOT_URL}/posted.html
    ...    wait_until=foobar

Wait For Navigation Works With Wait_until
    [Tags]    slow
    ${old timeout} =    Set Browser Timeout    4s
    FOR    ${wait_until}    IN    domcontentloaded    networkidle    load    commit
        Go To    ${ROOT_URL}/redirector.html
        Wait For Navigation    ${ROOT_URL}/posted.html    wait_until=${wait_until}
        Get Url    contains    posted
    END
    [Teardown]    Set Browser Timeout    ${old timeout}
