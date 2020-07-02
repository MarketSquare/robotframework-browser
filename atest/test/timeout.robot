*** Settings ***
Library           Browser    timeout=1ms
Resource          keywords.resource
Test Setup        Open Browser
Test Teardown     Close Browser
Resource          keywords.resource

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN_URL}

Test Overriding With Short
    Set Timeout    1ms
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN_URL}

Test Overriding With Long
    Set Timeout    10s
    Go To    ${LOGIN_URL}
