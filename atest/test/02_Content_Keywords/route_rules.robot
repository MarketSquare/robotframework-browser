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
    ${journal} =    HTTP Journal    ${path}
    Should Be Empty    ${journal}

Rule With Times Aborts Only The First Requests
    ${path} =    Open HTTP Page Without Sending    /api/echo/times
    Abort Requests    **${path}    times=2
    Send Request    expected_state=error
    Send Request    expected_state=error
    Send Request    expected_state=done
    Get Text    id=request-count    ==    3
    Get Element Count    css=#history li[data-status="200"]    ==    1
    ${journal} =    HTTP Journal    ${path}
    Length Should Be    ${journal}    1

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

Removing A Rule Logs How Many Times It Ran
    [Documentation]
    ...    LOG 5:*    INFO    REGEXP: Removed route rule \\S+\\. It ran 2 times\\.
    ${path} =    Open HTTP Page Without Sending    /api/echo/runs
    ${rule} =    Abort Requests    **${path}
    Send Request    expected_state=error
    Send Request    expected_state=error
    Remove Route Rule    ${rule}

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

Remove All Route Rules Logs How Many Times Each Rule Ran
    [Documentation]
    ...    LOG 5:*    INFO    REGEXP: Removed 1 Context and 1 Page route rules from context \\S+\\.\\nContext route rule \\S+ ran 1 time\\.\\nPage route rule \\S+ ran 0 times\\.
    ${path} =    Open HTTP Page Without Sending    /api/echo/runs-all
    Abort Requests    **${path}
    Send Request    expected_state=error
    Abort Requests    **${path}    on=Page
    Remove All Route Rules

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
    VAR    &{orders} =    count=${2}    status=open
    Mock Responses    **${path}    json=${orders}
    New Page    ${url}
    Get Text    id=status    ==    200
    Get Text    id=response-body    ==    {"count":2,"status":"open"}
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

Binary Body Mock Answers With The Exact Bytes
    ${path} =    Unique HTTP Path    /api/echo/mock-bytes
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    ${image} =    HTTP Fixture Bytes    image.png
    Mock Responses    **${path}    body=${image}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${sha256} =    HTTP Fixture Sha256    image.png
    Get Text    id=response-sha256    ==    ${sha256}
    Get Text    id=response-headers    *=    "content-type": "application/octet-stream"

List Body Mock Answers With JSON
    ${path} =    Unique HTTP Path    /api/echo/mock-list
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    body=${{ [1, {"a": None}] }}
    New Page    ${url}
    Get Text    id=response-body    ==    [1,{"a":null}]
    Get Text    id=response-headers    *=    "content-type": "application/json"

Arrow Function Matcher Gets The URL
    ${path} =    Unique HTTP Path    /api/echo/mock-predicate
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?id=7
    Mock Responses    url => url.pathname === '${path}' && url.searchParams.get('id') === '7'
    ...    body=matched
    New Page    ${url}
    Get Text    id=response-body    ==    matched
    Get Text    id=served-by    ==    not test-app

Invalid RegExp Matcher Fails
    Run Keyword And Expect Error    *Invalid regular expression*
    ...    Mock Responses    /[/    body=never

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
    Get Text    id=response-body    ==    [1,2]
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
    ...    *Header 'X-Gone' must be a string, a Secret, a number or a boolean, got None.*
    ...    Mock Responses    **/api/echo/never    headers=${{ {"X-Gone": None} }}
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
    ...    ValueError: json cannot be sent as JSON: Object of type set is not JSON serializable*
    ...    Mock Responses    **/api/echo/never    json=${{ {1, 2} }}
    Run Keyword And Expect Error
    ...    ValueError: json cannot be sent as JSON: Out of range float values are not JSON compliant*
    ...    Mock Responses    **/api/echo/never    json=${{ {"a": float("nan")} }}

Header Names Differing Only In Case Give One Header
    [Documentation]    Which value the page gets differs between browsers.
    ${path} =    Unique HTTP Path    /api/echo/mock-header-case
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    body=text    headers=${{ {"X-Mock": "upper", "x-mock": "lower"} }}
    New Page    ${url}
    Get Text    id=response-headers    matches    "x-mock": "(upper|lower)"\n

Text File Mock Opened By Navigation Shows UTF-8 Text
    ${path} =    Unique HTTP Path    /api/echo/mock-text-file
    Mock Responses    **${path}    path=${CURDIR}/route_rule_greeting.txt
    New Page    ${{ $ROOT_URL.rstrip("/") + $path }}
    Get Text    body    ==    Hyvää päivää

Secret Body And Header Values Reach The Page
    [Tags]    require-rf-7.4+
    Set Environment Variable    MOCK_TOKEN    secret-token
    VAR    ${token: Secret} =    %{MOCK_TOKEN}
    VAR    &{headers} =    X-Token=${token}
    ${path} =    Unique HTTP Path    /api/echo/mock-secret
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Mock Responses    **${path}    body=${token}    headers=${headers}
    New Page    ${url}
    Get Text    id=response-body    ==    secret-token
    Get Text    id=response-headers    *=    "x-token": "secret-token"

Modified Response Has The New Status And A Merged Header
    ${path} =    Unique HTTP Path    /api/echo/modify-status
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    status=503    headers=${{ {"X-Added": "yes"} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    503
    Get Text    id=response-headers    *=    "x-added": "yes"
    Get Text    id=served-by    matches    ^test-app #\\d+$
    ${journal} =    HTTP Journal    ${path}
    Length Should Be    ${journal}    1

None Header Value Removes A Real Response Header
    ${path} =    Unique HTTP Path    /api/respond/modify-remove-header
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?header=X-Remove:me
    Modify Responses    **${path}*    headers=${{ {"x-remove": None} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-headers    not contains    x-remove
    Get Text    id=served-by    matches    ^test-app #\\d+$

Empty Header Value Sends An Empty Response Header
    ${path} =    Unique HTTP Path    /api/respond/modify-empty-header
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?header=X-Empty:me
    Modify Responses    **${path}*    headers=${{ {"x-empty": ""} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-headers    *=    "x-empty": ""

JSON Patch Changes Nested Fields Of The Real JSON
    ${path} =    Unique HTTP Path    /api/echo/modify-json-patch
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?tag=a&tag=b
    VAR    &{patch} =
    ...    body=${{ {"size": 99, "sha256": None} }}
    ...    query=${{ {"tag": ["c"]} }}
    Modify Responses    **${path}*    json_patch=${patch}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[body][size]    ${99}
    Dictionary Should Not Contain Key    ${echo}[body]    sha256
    Should Be Equal    ${echo}[body][text]    ${EMPTY}
    Should Be Equal    ${echo}[query][tag]    ${{ ["c"] }}
    Should Be Equal    ${echo}[path]    ${path}
    Get Text    id=response-headers    *=    "content-type": "application/json; charset=utf-8"

Text Body Replaces The Real Body And Keeps Its Content Type
    ${path} =    Unique HTTP Path    /api/echo/modify-body
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    body=replaced
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    replaced
    Get Text    id=response-headers    *=    "content-type": "application/json; charset=utf-8"
    Get Text    id=served-by    matches    ^test-app #\\d+$
    ${journal} =    HTTP Journal    ${path}
    Length Should Be    ${journal}    1

JSON Patch On A Compressed Response Drops The Stale Encoding Headers
    ${path} =    Unique HTTP Path    /api/respond/modify-gzip
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?encoding=gzip
    Modify Responses    **${path}*    json_patch=${{ {"patched": True} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[patched]    ${True}
    Should Be Equal    ${echo}[path]    ${path}
    Get Text    id=response-headers    not contains    content-encoding
    Content Length Should Match Response Size

Binary Body Replaces The Real Body With The Exact Bytes
    ${path} =    Unique HTTP Path    /api/echo/modify-bytes
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    ${image} =    HTTP Fixture Bytes    image.png
    Modify Responses    **${path}    body=${image}    headers=${{ {"Content-Type": "image/png"} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${sha256} =    HTTP Fixture Sha256    image.png
    Get Text    id=response-sha256    ==    ${sha256}
    Get Text    id=response-headers    *=    "content-type": "image/png"

Relative Request URL Reaches The New Path And The Page Keeps Its URL
    ${path} =    Unique HTTP Path    /api/echo/modify-relative
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    request_url=${path}/v2
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[path]    ${path}/v2
    Get Text    id=response-url    ==    ${{ $ROOT_URL.rstrip("/") + $path }}

Cross Origin Request URL Gets The Cookies Of The New Host
    ${path} =    Unique HTTP Path    /api/echo/modify-cookie
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Add Cookie    original    localhost    url=${ROOT_URL}
    Add Cookie    other    other-origin    url=${OTHER_ORIGIN_ROOT_URL}
    Modify Responses    **${path}    request_url=${{ $OTHER_ORIGIN_ROOT_URL.rstrip("/") + $path }}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[headers][cookie]    other=other-origin
    Should Be Equal    ${echo}[headers][host]    ${{ $OTHER_ORIGIN_ROOT_URL.split("/")[2] }}

Request Method And Body Change
    ${path} =    Unique HTTP Path    /api/echo/modify-post
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    request_method=POST    request_body=Hyvää päivää
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[method]    POST
    Should Be Equal    ${echo}[body][text]    Hyvää päivää

Binary Request Body Reaches The Server Unchanged
    ${path} =    Unique HTTP Path    /api/echo/modify-post-bytes
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    ${image} =    HTTP Fixture Bytes    image.png
    Modify Responses    **${path}    request_method=POST    request_body=${image}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    ${sha256} =    HTTP Fixture Sha256    image.png
    Should Be Equal    ${echo}[body][sha256]    ${sha256}

Dictionary Request Body Is Sent As JSON
    ${path} =    Unique HTTP Path    /api/echo/modify-post-json
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    request_method=POST    request_body=${{ {"id": 7} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[body][text]    {"id":7}
    Should Start With    ${echo}[body][contentType]    application/json

Changing A POST To GET Sends No Body
    ${path} =    Unique HTTP Path    /api/echo/modify-get
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}    method=POST    bodyMode=text    body=payload
    Modify Responses    **${path}    request_method=GET
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[method]    GET
    Should Be Equal    ${echo}[body][size]    ${0}

Request Headers Merge Onto The Real Request Headers
    ${path} =    Unique HTTP Path    /api/echo/modify-request-headers
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}    headers={"X-Remove": "page"}
    Modify Responses    **${path}    request_headers=${{ {"X-Added": "yes", "x-remove": None, "X-Empty": ""} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[headers][x-added]    yes
    Dictionary Should Not Contain Key    ${echo}[headers]    x-remove
    Should Be Equal    ${echo}[headers][x-empty]    ${EMPTY}
    Dictionary Should Contain Key    ${echo}[headers]    user-agent

Redirect Is Followed And The Page Keeps Its URL
    ${path} =    Unique HTTP Path    /api/respond/modify-redirect
    ${target} =    Unique HTTP Path    /api/echo/modify-redirect-target
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?status=302&header=Location:${target}
    Modify Responses    **${path}**    headers=${{ {"X-Added": "yes"} }}
    New Page    ${url}
    Get Text    id=state    ==    done
    Get Text    id=status    ==    200
    Get Text    id=response-headers    *=    "x-added": "yes"
    ${echo} =    Panel JSON    response-body
    Should Be Equal    ${echo}[path]    ${target}
    Get Text    id=response-url    *=    ${path}?status=302

Unreachable Request URL Fails The Page Request
    ${path} =    Unique HTTP Path    /api/echo/modify-unreachable
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}
    Modify Responses    **${path}    request_url=http://127.0.0.1:1/
    New Page    ${url}
    Get Text    id=state    ==    error

Request Slower Than The Timeout When The Rule Was Added Fails
    ${path} =    Unique HTTP Path    /api/respond/modify-timeout
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?delay=3000
    ${old} =    Set Browser Timeout    1s
    TRY
        Modify Responses    **${path}*    status=200
    FINALLY
        Set Browser Timeout    ${old}
    END
    New Page    ${url}
    Get Text    id=state    ==    error

JSON Patch On A Body That Is Not JSON Fails The Page Request
    ${path} =    Unique HTTP Path    /api/respond/modify-not-json
    ${url} =    HTTP Page Url    ${HTTP_URL}    url=${path}?body=plain
    Modify Responses    **${path}*    json_patch=${{ {"a": 1} }}
    New Page    ${url}
    Get Text    id=state    ==    error

Invalid Modify Responses Fail
    Run Keyword And Expect Error
    ...    ValueError: Modify Responses needs at least one change.
    ...    Modify Responses    **/api/echo/never
    Run Keyword And Expect Error
    ...    ValueError: Give at most one of body, json, path and json_patch, got json and json_patch.
    ...    Modify Responses    **/api/echo/never    json=${1}    json_patch=${{ {"a": 1} }}
    Run Keyword And Expect Error
    ...    ValueError: status must be from 100 to 599, got 99.
    ...    Modify Responses    **/api/echo/never    status=99
    Run Keyword And Expect Error
    ...    ValueError: path ${CURDIR}${/}missing.json is not a file.
    ...    Modify Responses    **/api/echo/never    path=${CURDIR}/missing.json
    Run Keyword And Expect Error
    ...    ValueError: json cannot be sent as JSON: Object of type set is not JSON serializable*
    ...    Modify Responses    **/api/echo/never    json=${{ {1, 2} }}
    Run Keyword And Expect Error
    ...    ValueError: json_patch cannot be sent as JSON: Object of type set is not JSON serializable*
    ...    Modify Responses    **/api/echo/never    json_patch=${{ {"a": {1, 2}} }}
    Run Keyword And Expect Error
    ...    ValueError: json_patch cannot be sent as JSON: Out of range float values are not JSON compliant*
    ...    Modify Responses    **/api/echo/never    json_patch=${{ {"a": float("inf")} }}
    Run Keyword And Expect Error
    ...    *RequestMethod*
    ...    Modify Responses    **/api/echo/never    request_method=FETCH
    Run Keyword And Expect Error
    ...    ValueError: times must be 1 or more, got 0.
    ...    Modify Responses    **/api/echo/never    status=200    times=0
    Run Keyword And Expect Error
    ...    *Tried to add a route rule, but no page was open.*
    ...    Modify Responses    **/api/echo/never    status=200    on=Page

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
