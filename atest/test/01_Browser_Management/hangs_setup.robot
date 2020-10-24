*** Settings ***
Library           Browser    run_on_failure=None
Resource          imports.resource
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${ErrorMessage}=    page.goto: Timeout 1ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    New Page
    set browser timeout    1ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test New Page with short Default Timeout
    new context
    set browser timeout    1ms
    Run Keyword And Expect Error    *${ErrorMessage}*    New Page    ${LOGIN_URL}
