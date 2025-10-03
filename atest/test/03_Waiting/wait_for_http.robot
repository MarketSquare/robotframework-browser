*** Settings ***
Resource        imports.resource

Test Setup      Ensure Location    ${LOGIN_URL}

Force Tags      no-iframe

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
    Wait For Request    matcher=${ROOT_URL}api/get/json    timeout=1s

Wait For Request Regex
    [Tags]    no-docker-pr
    Click    \#delayed_request
    Wait For Request    matcher=/\\/\\/local\\w+\\:\\d+\\/api/    timeout=1s

Wait For Request Predicate
    Click    \#delayed_request
    Wait For Request    matcher=request => request.url().endsWith('api/get/json') && request.method() === 'GET'
    ...    timeout=1s

Wait For Response Synchronous
    Click    \#delayed_request
    ${data} =    Wait For Response    timeout=1s
    ${body} =    Set Variable    ${data.body}
    ${expected_body} =    Create Dictionary    greeting=HELLO
    Dictionaries Should Be Equal    ${body}    ${expected_body}

Wait For Request Async Big
    Click    id=delayed_request_big
    ${data} =    Wait For Response    timeout=15s
    ${body} =    Set Variable    ${data.body}
    ${keys} =    Create List
    ...    long1
    ...    long2
    ...    long3
    ...    long4
    ...    long5
    ...    long6
    ...    long7
    ...    long8
    ...    long9
    ...    long10
    ...    long11
    ...    long12
    ...    long13
    ...    long14
    ...    long15
    ...    long16
    ...    long17
    ...    long18
    ...    long19
    ...    long20
    FOR    ${key}    IN    @{keys}
        Dictionary Should Contain Key    ${body}    ${key}
    END

Wait For Response Synchronous With Default Timeout
    Click    \#delayed_request
    Wait For Response

Wait For Response Synchronous With Regex Matcher
    [Tags]    no-docker-pr
    Click    \#delayed_request
    Wait For Response    matcher=/\\/\\/local\\w+\\:\\d+\\/api/

Wait For Response Synchronous With Predicate
    Click    \#delayed_request
    Wait For Response    response => response.url().endsWith('json') && response.request().method() === 'GET'

Wait For Response Async
    ${promise} =    Promise To    Wait For Response    matcher=    timeout=3s
    Click    \#delayed_request
    ${body} =    Wait For    ${promise}

Wait For Response With OPTIONS Request
    Go To    ${ROOT_URL}
    ${prom} =    Promise To    Wait For Response    /.*options/    # ΔT: 0.028s
    ${res} =    Evaluate JavaScript
    ...    ${None}
    ...    () => fetch('api/options', {method: 'OPTIONS'}).then(resp => resp.status)
    ${res2} =    Wait For    ${prom}
    Should Be Equal As Numbers    ${res}    204
    Should Be Equal As Numbers    ${res2.status}    204
    Should Be Equal    ${res2.body}    ${None}

Wait Until Network Is Idle Works
    [Tags]    slow
    Go To    ${ROOT_URL}delayed-load.html
    Get Text    \#server_delayed_response    ==    Server response after 400ms
    Wait Until Network Is Idle    timeout=3s
    Get Text    \#server_delayed_response    ==    after some time I respond

Wait For Navigation Works
    [Tags]    slow
    Go To    ${ROOT_URL}redirector.html
    Wait For Navigation    ${ROOT_URL}posted.html
    Get Url    ==    ${ROOT_URL}posted.html

Wait For Navigation Works With Regex
    [Tags]    slow
    Go To    ${ROOT_URL}redirector.html
    Wait For Navigation    /p[\\w]{4}d/i
    Get Url    contains    posted

Wait For Navigation Fails With Wrong Regex
    [Tags]    slow
    Go To    ${ROOT_URL}redirector.html
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error    *Error*    Wait For Navigation    foobar
    Set Browser Timeout    ${timeout}
    Get Url    not contains    foobar

Wait For Navigation Fails With Wrong Wait_until
    [Tags]    slow
    Go To    ${ROOT_URL}redirector.html
    Run Keyword And Expect Error
    ...    *PageLoadStates does not have member 'foobar'. Available: 'commit', 'domcontentloaded', 'load' and 'networkidle'*
    ...    Wait For Navigation
    ...    ${ROOT_URL}posted.html
    ...    wait_until=foobar

Wait For Navigation Works With Wait_until
    [Tags]    slow
    ${old timeout} =    Set Browser Timeout    4s
    FOR    ${wait_until}    IN    domcontentloaded    networkidle    load    commit
        Go To    ${ROOT_URL}redirector.html
        Wait For Navigation    ${ROOT_URL}posted.html    wait_until=${wait_until}
        Get Url    contains    posted
    END
    [Teardown]    Set Browser Timeout    ${old timeout}

Go To Works With Wait_until
    [Tags]    slow
    ${old timeout} =    Set Browser Timeout    4s
    FOR    ${wait_until}    IN    domcontentloaded    networkidle    load    commit
        Go To    ${ROOT_URL}redirector.html    wait_until=${wait_until}
        Get Url    contains    posted
    END
    [Teardown]    Set Browser Timeout    ${old timeout}

New Page Works With Wait_until
    [Tags]    slow
    [Setup]    NONE
    ${old timeout} =    Set Browser Timeout    4s
    FOR    ${wait_until}    IN    domcontentloaded    networkidle    load    commit
        New Page    ${ROOT_URL}redirector.html    wait_until=${wait_until}
        Get Url    contains    posted
        Close Page
    END
    [Teardown]    Set Browser Timeout    ${old timeout}

Promise To Wait For Navigation With Wait_until
    ${old timeout} =    Set Browser Timeout    4s
    Go To    ${ROOT_URL}redirector.html
    ${page_navigation} =    Promise To    Wait For Navigation    url=${ROOT_URL}posted.html    wait_until=networkidle
    Wait For    ${page_navigation}
    [Teardown]    Set Browser Timeout    ${old timeout}
