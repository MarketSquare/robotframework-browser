*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL}
Test Setup      Go To    ${WAIT_URL}

*** Test Cases ***
Test Suite Level Removed
    Strict Mode Should Be    True
    Timeout Should Be Between    100    800
    Assertion Retry Should Be Between    100    800
