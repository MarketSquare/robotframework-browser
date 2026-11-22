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
