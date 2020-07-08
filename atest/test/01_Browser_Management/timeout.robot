*** Settings ***
Library           Browser    timeout=1ms
Resource          ../variables.resource
Suite Setup       Open Browser    url=${None}    browser=${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test Overriding With Long
    Set Timeout    10 s
    Go To    ${FORM_URL}
    Go To    about:blank

Test Overriding With Short
    Set Timeout    10 s
    Go To    ${FORM URL}
    Set Timeout    1 ms
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN URL}
    Wait For Elements State    //h1    visible    timeout=2 s
