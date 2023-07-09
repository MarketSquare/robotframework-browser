*** Settings ***
Resource            ../../scope_keywords.resource

Suite Setup         Run Keywords    New Browser    AND    New Context
Suite Teardown      Close Browser    CURRENT
Test Setup          New Page    ${WAIT_URL_FRAMED}

*** Test Cases ***
Test Normal Timeout
    Select Options By    \#dropdown    value    enabled
    Click With Options    \#submit    noWaitAfter=True
    Click    "victim"

Set Timeout To Test Scope
    Select Options By    \#dropdown    value    enabled
    Click With Options    \#submit    noWaitAfter=True
    Set Browser Timeout    100ms    scope=Test
    Run Keyword And Expect Error    *Timeout 100ms exceeded.*    Click    "victim"

Verify Removed Scope
    Select Options By    \#dropdown    value    enabled
    Click With Options    \#submit    noWaitAfter=True
    Click    "victim"

Set Run On Failure To Test Scope
    Register Keyword To Run On Failure    LocalStorage Set Item    test_name    ${TEST_NAME}    scope=Test
    Run Keyword And Ignore Error    Get Title    ==    Wrong Title
    LocalStorage Get Item    test_name    ==    ${TEST_NAME}

Check Run On Failure To Test Scope
    Run Keyword And Ignore Error    Get Title    ==    Wrong Title
    LocalStorage Get Item    test_name    ==    Set Run On Failure To Test Scope
