*** Settings ***
Library           Browser    timeout=1ms    run_on_failure=None
Resource          imports.resource
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${ErrorMessage}=    page.goto: Timeout 1ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    New Page
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s
