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

Set Timeout Should Return Old Value
    New Context
    ${old} =    Set Timeout    1 min
    ${new} =    Set Timeout    ${old}
    Should Be Equal    ${new}    1 min

Set Timeout Should Fail With Invalid Value And Not Change Existing Value
    New Context
    Run Keyword And Expect Error
    ...    ValueError: cannot convert float NaN to integer
    ...    Set Timeout    NaN
    ${old} =    Set Timeout    1 min
    ${new} =    Set Timeout    ${old}
    Should Not Be Equal    ${old}    Nan
    Should Be Equal    ${new}    1 min
