*** Settings ***
Library           Browser    run_on_failure=None
Resource          imports.resource
Suite Setup       New Browser
Suite Teardown    Close Browser

*** Variables ***
${ErrorMessage}=    page.goto: Timeout 1ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    New Page
    Set Browser Timeout    1ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test Overriding With Long
    New Context
    Set Browser Timeout    10 s
    New Page    ${FORM_URL}
    Go To    about:blank

Test Overriding With Short
    New Context
    Set Browser Timeout    10 s
    New Page    ${FORM_URL}
    Set Browser Timeout    1 ms
    Run Keyword And Expect Error    *${ErrorMessage}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test assertion timeouts
    New Context
    Set Browser Timeout    10 s
    New Page    ${LOGIN_URL}
    ${old} =    Set retry assertions for    0s
    Run Keyword And Expect Error    *    Get title    ==    Wrong title
    Get title    ==    Login Page
    set retry assertions for    ${old}

Set Browser Timeout Should Return Old Value
    New Context
    ${old} =    Set Browser Timeout    1 min
    ${new} =    Set Browser Timeout    ${old}
    Should Be Equal    ${new}    1 minute

Set Browser Timeout Should Fail With Invalid Value And Not Change Existing Value
    New Context
    Run Keyword And Expect Error
    ...    ValueError: Argument 'timeout' got value 'NaN' that cannot be converted to timedelta*
    ...    Set Browser Timeout    NaN
    ${old} =    Set Browser Timeout    1 min
    ${new} =    Set Browser Timeout    ${old}
    Should Not Be Equal    ${old}    Nan
    Should Be Equal    ${new}    1 minute
