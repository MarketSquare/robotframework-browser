*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL}
Test Setup      Go To    ${WAIT_URL}


*** Test Cases ***
Test Suite Level Removed
    Strict Mode should be    False
    Timeout Should Be Between    600   1500
    Assertion Retry Should Be Between    600    1500

