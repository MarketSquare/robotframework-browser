*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL_DIRECT}
Test Setup      Go To    ${WAIT_URL_DIRECT}
Test Timeout    30 sec

*** Test Cases ***
Test Global Scope And Set Test Scope
    Log All Scopes    1000    1000    False    ${EMPTY}
    Timeout Should Be Between    500    1500
    ${global_timeout} =    Set Browser Timeout    2s    scope=Test
    Should Be Equal    ${global_timeout}    1 second
    Timeout Should Be Between    1500    3000

    Go To    ${WAIT_URL_DIRECT}
    Strict Mode Should Be    False
    ${global_strict} =    Set Strict Mode    ${True}    scope=Test
    Should Be Equal    ${global_strict}    ${False}
    Strict Mode Should Be    True

    Go To    ${WAIT_URL_DIRECT}
    Assertion Retry Should Be Between    500    1500
    ${global_retry} =    Set Retry Assertions For    2s    scope=Test
    Should Be Equal    ${global_retry}    1 second
    Assertion Retry Should Be Between    1500    3000

    Go To    ${WAIT_URL_FRAMED}
    ${global_prefix} =    Set Selector Prefix    ${IFRAME_PREFIX}    scope=Test
    Should Be Equal    ${global_prefix}    ${EMPTY}
    Strict Mode Should Be    True

    Log All Scopes    2000    2000    True    ${IFRAME_PREFIX}

Test Removed Test Scope
    Log All Scopes    1000    1000    False    ${EMPTY}
    Timeout Should Be Between    500    1500
    Strict Mode Should Be    ${False}
    Assertion Retry Should Be Between    500    1500

Set Suite Level
    Set Strict Mode    ${True}
    Strict Mode Should Be    True
    Set Browser Timeout    500 ms
    Set Retry Assertions For    500 ms
    Set Selector Prefix    ${IFRAME_PREFIX}
    Log All Scopes    500    500    True    ${IFRAME_PREFIX}

Test Suite Level
    [Setup]    Go To    ${WAIT_URL_FRAMED}
    Log All Scopes    500    500    True    ${IFRAME_PREFIX}
    Strict Mode Should Be    True
    Timeout Should Be Between    100    900
    Assertion Retry Should Be Between    100    900
