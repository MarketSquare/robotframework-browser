*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}


*** Test Cases ***
Leaked promise fails test if not rejected
    [Documentation]    FAIL Expected error message
    ${promise}=  Promise To  Get Text

Rejected promise does not fail test
    ${promise}=  Promise To  Get Text
    Reject  ${promise}

