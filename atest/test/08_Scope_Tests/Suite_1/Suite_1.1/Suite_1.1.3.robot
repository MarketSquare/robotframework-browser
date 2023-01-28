*** Settings ***
Resource            ../../scope_keywords.resource

Suite Setup         Run Keywords    New Browser    AND    New Context
Suite Teardown      Close Browser    CURRENT
Test Setup          New Page    ${WAIT_URL_FRAMED}

*** Test Cases ***
Test 1
    Select Options By    \#dropdown    value    enabled
    Click    \#submit    noWaitAfter=True
    Click    "victim"

Test 2
    Set Browser Timeout    100ms    scope=Test
    Select Options By    \#dropdown    value    enabled
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *Timeout 100ms exceeded.*    Click    "victim"

Test 3
    Select Options By    \#dropdown    value    enabled
    Click    \#submit    noWaitAfter=True
    Click    "victim"
