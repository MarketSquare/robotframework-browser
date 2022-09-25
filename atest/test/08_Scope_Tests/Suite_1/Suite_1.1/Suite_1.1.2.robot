*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL_DIRECT}
Test Setup      Go To    ${WAIT_URL_DIRECT}

*** Test Cases ***
Test Suite Level Removed
    Log All Scopes    1000    1000    False    ${EMPTY}
    Strict Mode Should Be    False
    Timeout Should Be Between    500    1500
    Assertion Retry Should Be Between    500    1500

Set Global Scope
    Log All Scopes    1000    1000    False    ${EMPTY}
    Set Browser Timeout    1500 ms    scope=Global
    Set Retry Assertions For    1500 ms    scope=Global
    Set Strict Mode    True    scope=Global
    Set Selector Prefix    ${IFRAME_PREFIX}    scope=Global
    Log All Scopes    1500    1500    True    ${IFRAME_PREFIX}
