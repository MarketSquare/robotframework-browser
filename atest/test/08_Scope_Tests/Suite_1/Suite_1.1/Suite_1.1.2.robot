*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL}
Test Setup      Go To    ${WAIT_URL}

*** Test Cases ***
Test Suite Level Removed
    Strict Mode Should Be    False
    Timeout Should Be Between    500    1500
    Assertion Retry Should Be Between    500    1500

Set Global Scope
    Set Browser Timeout    400 ms    scope=Global
    Set Retry Assertions For    400 ms    scope=Global
    Set Strict Mode    True    scope=Global
