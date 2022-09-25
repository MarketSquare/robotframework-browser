*** Settings ***
Resource        ../../scope_keywords.resource

Suite Setup     Ensure Open Page    ${WAIT_URL_FRAMED}

*** Test Cases ***
Test Suite Level Removed
    Log All Scopes    1500    1500    True    ${IFRAME_PREFIX}
    Strict Mode Should Be    True
    Timeout Should Be Between    1000    2000
    Assertion Retry Should Be Between    1000    2000
