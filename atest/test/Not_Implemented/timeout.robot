*** Settings ***
Library           Browser    timeout=1ms
Suite Setup       Open Browser    url=${None}    browser=${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser
Force Tags        Not-Implemented
Resource          keywords.resource

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN_URL}

Test Overriding With Long
    Set Timeout    10 s
    Go To    ${FORM_URL}

Test Overriding With Short
    Set Timeout    10 s
    Go To    ${ERROR URL}
    Set Timeout    1 ms
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN URL}
