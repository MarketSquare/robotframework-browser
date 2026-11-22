*** Settings ***
Library          ../../library/http_test_page.py
Resource         imports.resource

Test Setup       New Context
Test Teardown    Close Context    ALL

Test Tags        no-iframe

*** Test Cases ***
Aborted Request Shows An Error And Never Reaches The Server
    ${path} =    Unique HTTP Path    /api/echo/abort
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Abort Requests    **${path}
    New Page    ${url}
    Get Text    id=state    ==    error
    ${count} =    HTTP Echo Count    ${path}
    Should Be Equal    ${count}    ${0}

Rule With Times Aborts Only The First Requests
    ${path} =    Open HTTP Page Without Sending    /api/echo/times
    Abort Requests    **${path}    times=2
    Send Request    expected_state=error
    Send Request    expected_state=error
    Send Request    expected_state=done
    Get Text    id=request-count    ==    3
    Get Element Count    css=#history li[data-status="200"]    ==    1
    ${count} =    HTTP Echo Count    ${path}
    Should Be Equal    ${count}    ${1}

Removing A Rule Ends The Outage
    ${path} =    Open HTTP Page Without Sending    /api/echo/outage
    ${rule} =    Abort Requests    **${path}
    Send Request    expected_state=error
    Remove Route Rule    ${rule}
    Send Request    expected_state=done
    Get Text    id=status    ==    200

Removing An Ended Rule Passes
    ${path} =    Open HTTP Page Without Sending    /api/echo/ended
    ${removed} =    Abort Requests    **${path}
    Remove Route Rule    ${removed}
    Remove Route Rule    ${removed}
    ${used_up} =    Abort Requests    **${path}    times=1
    Send Request    expected_state=error
    Remove Route Rule    ${used_up}
    Send Request    expected_state=done

Context Rule Applies To A Page Opened Later And Survives Navigation
    ${path} =    Unique HTTP Path    /api/echo/context-rule
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    New Page    ${HTTP_URL}
    Abort Requests    **${path}
    New Page    ${url}
    Get Text    id=state    ==    error
    Go To    ${url}
    Get Text    id=state    ==    error

Page Rule Stays On Its Page
    ${path} =    Unique HTTP Path    /api/echo/page-rule
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    ${first} =    New Page    ${HTTP_URL}
    Abort Requests    **${path}    on=Page
    Go To    ${url}
    Get Text    id=state    ==    error
    New Page    ${url}
    Get Text    id=state    ==    done
    Switch Page    ${first}
    Send Request    expected_state=error

Remove All Route Rules Clears The Active Context Only
    ${path} =    Unique HTTP Path    /api/echo/remove-all
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    url=${path}
    ${other} =    New Context
    New Page    ${url}
    Abort Requests    **${path}
    New Context
    ${first} =    New Page    ${url}
    Abort Requests    **${path}
    Abort Requests    **${path}    on=Page
    New Page    ${url}
    Abort Requests    **${path}    on=Page
    Remove All Route Rules
    Send Request    expected_state=done
    Switch Page    ${first}
    Send Request    expected_state=done
    Switch Context    ${other}
    Send Request    expected_state=error

Invalid Abort Requests Fail
    Run Keyword And Expect Error
    ...    ValueError: times must be 1 or more, got 0.
    ...    Abort Requests    **/api/echo/never    times=0
    Run Keyword And Expect Error
    ...    *AbortErrorCode*
    ...    Abort Requests    **/api/echo/never    errorCode=nosuchcode
    Run Keyword And Expect Error
    ...    *Invalid regular expression*
    ...    Abort Requests    /api/echo/[/
    Run Keyword And Expect Error
    ...    *Tried to add a route rule, but no page was open.*
    ...    Abort Requests    **/api/echo/never    on=Page
    Close Context    ALL
    Run Keyword And Expect Error
    ...    *Tried to add a route rule, but no context was open.*
    ...    Abort Requests    **/api/echo/never

Removing Rules Without A Context Passes
    Close Context    ALL
    Remove Route Rule    00000000-0000-0000-0000-000000000000
    Remove All Route Rules

Every Abort Error Code Aborts The Request
    [Tags]    chromium-only
    [Template]    Request Aborted With Error Code Fails
    aborted
    accessdenied
    addressunreachable
    blockedbyclient
    blockedbyresponse
    connectionaborted
    connectionclosed
    connectionfailed
    connectionrefused
    connectionreset
    internetdisconnected
    namenotresolved
    timedout
    failed

Body Mock Answers With Its Status, Header And Body
    ${path} =    Unique HTTP Path    /api/echo/mock-body
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    status=201    body=mocked text    headers=${{ {"X-Mock": "yes"} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    201
    Get Text    id=response-body    ==    mocked text
    Get Text    id=response-headers    *=    "x-mock": "yes"
    Get Text    id=response-headers    *=    "content-type": "text/plain; charset=utf-8"
    Get Text    id=served-by    ==    not test-app
    ${journal} =    HTTP Journal    ${path}
    Should Be Empty    ${journal}

JSON Mock Answers With An Encoded Body And JSON Content Type
    ${path} =    Unique HTTP Path    /api/echo/mock-json
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    VAR    &{orders}    count=${2}    status=open
    Mock Responses    **${path}    json=${orders}
    New Page    ${url}
    Get Text    id=status    ==    200
    Get Text    id=response-body    ==    {"count": 2, "status": "open"}
    Get Text    id=response-headers    *=    "content-type": "application/json"

File Mock Answers With The File And A Content Type From Its Extension
    ${image_path} =    Unique HTTP Path    /api/echo/mock-image
    ${json_path} =    Unique HTTP Path    /api/echo/mock-file
    ${image} =    HTTP Fixture Path    image.png
    Mock Responses    **${image_path}    path=${image}
    Mock Responses    **${json_path}    path=${CURDIR}/route_rule_orders.json
    ${image_url} =    HTTP Page Url    ${HTTP_URL}    kind=img    url=${image_path}
    New Page    ${image_url}
    Get Text    id=response-body    ==    image 64x48
    ${json_url} =    HTTP Page Url    ${HTTP_URL}    url=${json_path}
    New Page    ${json_url}
    Get Text    id=response-body    ==    {"orders": []}
    Get Text    id=response-headers    *=    "content-type": "application/json"

Mock Without A Payload Has An Empty Body
    ${path} =    Unique HTTP Path    /api/echo/mock-empty
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    status=204
    New Page    ${url}
    Get Text    id=status    ==    204
    Get Text    id=response-size    ==    0

Mock Without A Payload Has No Content Type
    [Documentation]    WebKit reports application/octet-stream for a fulfilled response without one.
    [Tags]    known-bug-webkit
    ${path} =    Unique HTTP Path    /api/echo/mock-no-content-type
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    status=204
    New Page    ${url}
    Get Text    id=status    ==    204
    Get Text    id=response-headers    not contains    content-type

Content Type In Headers Wins Over The JSON Default
    ${path} =    Unique HTTP Path    /api/echo/mock-content-type
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    json=${{ [1, 2] }}    headers=${{ {"content-type": "application/vnd.orders+json"} }}
    New Page    ${url}
    Get Text    id=response-body    ==    [1, 2]
    Get Text    id=response-headers    *=    "content-type": "application/vnd.orders+json"

Mock With Times Answers Once And Then The Server Answers
    ${path} =    Open HTTP Page Without Sending    /api/echo/mock-once
    Mock Responses    **${path}    status=500    body=down    times=1
    Send Request    expected_state=done
    Get Text    id=status    ==    500
    Get Text    id=served-by    ==    not test-app
    Send Request    expected_state=done
    Get Text    id=status    ==    200
    Get Text    id=served-by    matches    ^test-app #\\d+$
    ${journal} =    HTTP Journal    ${path}
    Length Should Be    ${journal}    1

Newest Rule Wins And A Page Rule Wins Over A Context Rule
    ${path} =    Open HTTP Page Without Sending    /api/echo/mock-order
    Abort Requests    **${path}
    ${newest} =    Mock Responses    **${path}    body=newest
    Send Request    expected_state=done
    Get Text    id=response-body    ==    newest
    Remove Route Rule    ${newest}
    Send Request    expected_state=error
    Mock Responses    **${path}    body=page    on=Page
    Mock Responses    **${path}    body=context
    Send Request    expected_state=done
    Get Text    id=response-body    ==    page

Cross Origin Mock Without CORS Headers Reaches The Page
    ${path} =    Unique HTTP Path    /api/echo/mock-cors
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${{ $OTHER_ORIGIN_ROOT_URL.rstrip("/") + $path }}
    Mock Responses    **${path}    body=cross origin
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    cross origin

Invalid Mock Responses Fail
    Run Keyword And Expect Error
    ...    ValueError: Give at most one of body, json and path, got body and json.
    ...    Mock Responses    **/api/echo/never    body=text    json=${1}
    Run Keyword And Expect Error
    ...    ValueError: status must be from 100 to 599, got 99.
    ...    Mock Responses    **/api/echo/never    status=99
    Run Keyword And Expect Error
    ...    ValueError: status must be from 100 to 599, got 600.
    ...    Mock Responses    **/api/echo/never    status=600
    Run Keyword And Expect Error
    ...    ValueError: path ${CURDIR}${/}missing.json is not a file.
    ...    Mock Responses    **/api/echo/never    path=${CURDIR}/missing.json
    Run Keyword And Expect Error
    ...    TypeError: Object of type set is not JSON serializable
    ...    Mock Responses    **/api/echo/never    json=${{ {1, 2} }}

Header Names Differing Only In Case Give One Header
    [Documentation]    Which value the page gets differs between browsers.
    ${path} =    Unique HTTP Path    /api/echo/mock-header-case
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    body=text    headers=${{ {"X-Mock": "upper", "x-mock": "lower"} }}
    New Page    ${url}
    Get Text    id=response-headers    matches    "x-mock": "(upper|lower)"\n

*** Keywords ***
Open HTTP Page Without Sending
    [Arguments]    ${prefix}
    ${path} =    Unique HTTP Path    ${prefix}
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    url=${path}
    New Page    ${url}
    RETURN    ${path}

Send Request
    [Arguments]    ${expected_state}
    ${sent} =    Get Element Count    css=#history li
    Click    id=send
    Get Element Count    css=#history li    ==    ${sent + 1}
    Get Text    id=state    ==    ${expected_state}

Request Aborted With Error Code Fails
    [Arguments]    ${error_code}
    ${path} =    Open HTTP Page Without Sending    /api/echo/code-${error_code}
    Abort Requests    **${path}    errorCode=${error_code}
    Send Request    expected_state=error
