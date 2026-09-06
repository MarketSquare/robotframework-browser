*** Settings ***
Resource       ../../scope_keywords.resource

Suite Setup    Ensure Open Framed Page

*** Test Cases ***
Test Suite Level Removed
    Log All Scopes    1500    1500    True    ${IFRAME_PREFIX}
    Strict Mode Should Be    True
    Timeout Should Be    1500
    Assertion Retry Should Be    1500
