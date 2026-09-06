*** Settings ***
Resource          ../../scope_keywords.resource

Suite Setup       Run Keywords    New Browser    AND    New Context
Suite Teardown    Close Browser    CURRENT
Test Setup        New Page    ${WAIT_URL_FRAMED}

*** Test Cases ***
Test Normal Timeout
    Timeout Should Be    1500

Set Timeout To Test Scope
    Set Browser Timeout    100ms    scope=Test
    Timeout Should Be    100

Verify Removed Scope
    Timeout Should Be    1500

Set Run On Failure To Test Scope
    Register Keyword To Run On Failure    LocalStorage Set Item    test_name    ${TEST_NAME}    scope=Test
    Run Keyword And Ignore Error    Get Title    ==    Wrong Title
    LocalStorage Get Item    test_name    ==    ${TEST_NAME}

Check Run On Failure To Test Scope
    Run Keyword And Ignore Error    Get Title    ==    Wrong Title
    LocalStorage Get Item    test_name    ==    Set Run On Failure To Test Scope
