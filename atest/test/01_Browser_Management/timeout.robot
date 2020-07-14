*** Settings ***
Library           Browser    timeout=1ms
Resource          imports.resource
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${ErrorMessage}=    Timeout 1ms exceeded during

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test Overriding With Long
    Set Timeout    10 s
    Go To    ${FORM_URL}
    Go To    about:blank

Test Overriding With Short
    Set Timeout    10 s
    Go To    ${FORM_URL}
    Set Timeout    1 ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s
