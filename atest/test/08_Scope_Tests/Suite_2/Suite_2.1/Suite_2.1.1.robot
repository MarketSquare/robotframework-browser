*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL_DIRECT}
Test Setup      Go To    ${WAIT_URL_DIRECT}

*** Test Cases ***
Test Suite Level Removed
    Log All Scopes    1000    1000    False    ${EMPTY}
    Strict Mode Should Be    False
    Timeout Should Be Between    600    1500
    Assertion Retry Should Be Between    600    1500
