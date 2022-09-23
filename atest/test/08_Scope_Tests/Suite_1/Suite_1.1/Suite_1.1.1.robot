*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL}
Test Setup      Go To    ${WAIT_URL}
Test Timeout    200 sec

*** Test Cases ***
Test Global Scope And Set Test Scope
    Timeout Should Be Between    500    1500
    ${global_timeout} =    Set Browser Timeout    2s    scope=Test
    Should Be Equal    ${global_timeout}    1 second 1 millisecond
    Timeout Should Be Between    1500    3000

    Go To    ${WAIT_URL}
    Strict Mode Should Be    False
    Set Strict Mode    ${True}    scope=Test
    Strict Mode Should Be    True

    Go To    ${WAIT_URL}
    Assertion Retry Should Be Between    500    1500
    ${global_retry} =    Set Retry Assertions For    2s    scope=Test
    Should Be Equal    ${global_retry}    1 second 1 millisecond
    Assertion Retry Should Be Between    1500    3000

Test Removed Test Scope
    Timeout Should Be Between    500    1500
    Strict Mode Should Be    ${False}
    Assertion Retry Should Be Between    500    1500

Set Suite Level
    Set Strict Mode    ${True}
    Strict Mode Should Be    True
    Set Browser Timeout    500 ms
    Set Retry Assertions For    500 ms

Test Suite Level
    Strict Mode Should Be    True
    Timeout Should Be Between    100    900
    Assertion Retry Should Be Between    100    900
