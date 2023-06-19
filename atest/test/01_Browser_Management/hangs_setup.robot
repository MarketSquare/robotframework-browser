*** Settings ***
Resource            imports.resource

Suite Teardown      Close Browser

*** Variables ***
${ErrorMessage} =       page.goto: Timeout 1ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    [Tags]    slow
    New Page
    Set Browser Timeout    1ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test New Page With Short Default Timeout
    New Context
    Set Browser Timeout    1ms
    Run Keyword And Expect Error    *${ErrorMessage}*    New Page    ${LOGIN_URL}

*** Keywords ***
Setup
    ${original} =    Register Keyword To Run On Failure    ${None}
    Set Suite Variable    $original

Teardown
    Register Keyword To Run On Failure    ${original}
    Close Browser
