*** Settings ***
Library           Browser    timeout=1ms
Resource          imports.resource
Suite Setup       New Browser
Suite Teardown    Close Browser

*** Variables ***
${ErrorMessage}=    page.goto: Timeout 1ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    New Page
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test Overriding With Long
    New Context
    Set Timeout    10 s
    New Page    ${FORM_URL}
    Go To    about:blank

Test Overriding With Short
    New Context
    Set Timeout    10 s
    New Page    ${FORM_URL}
    Set Timeout    1 ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s
