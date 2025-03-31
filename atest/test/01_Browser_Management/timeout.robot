*** Settings ***
Library             Browser    run_on_failure=None    enable_playwright_debug=${True}
Resource            imports.resource

Suite Setup         New Browser    headless=${HEADLESS}
Suite Teardown      Close Browser

Test Tags           timeout    no-iframe

*** Variables ***
${err_goto} =       page.goto: Timeout 1ms exceeded.
${err_click} =      SEPARATOR=
...                 locator.click: Timeout 100ms exceeded.

*** Test Cases ***
Test GoTo With Short Default Timeout
    New Page
    Set Browser Timeout    1ms
    Run Keyword And Expect Error    *${err_goto}*    Go To    ${LOGIN_URL}
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
    Run Keyword And Expect Error    *${err_goto}*    Go To    ${LOGIN_URL}
    Wait For Elements State    //h1    visible    timeout=2 s

Test Assertion Timeouts
    New Context
    Set Browser Timeout    10 s
    New Page    ${LOGIN_URL}
    ${old} =    Set Retry Assertions For    0s
    Run Keyword And Expect Error    *    Get Title    ==    Wrong title
    Get Title    ==    Login Page
    Set Retry Assertions For    ${old}

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

Calling Set Browser Timeout Without Open Context Should Not Fail
    Set Browser Timeout    1s
    Close Browser    ALL
    Set Browser Timeout    1s

Check Timeout Tips
    New Page    ${LOGIN_URL}
    Set Browser Timeout    0.1s
    Run Keyword And Expect Error    *${err_click}*    Click    nothing
