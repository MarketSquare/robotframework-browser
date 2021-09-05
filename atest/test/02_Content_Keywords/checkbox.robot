*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${FORM_URL}

*** Test Cases ***
Get Checkbox State Checked
    Get Checkbox State    [name=can_send_email]    ==    checked

Get Checkbox State Unchecked
    Get Checkbox State    [name=can_send_sms]    ==    UnChecked

Get Checkbox State With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 12 elements.*
    ...    Get Checkbox State    //input
    ${state} =    Get Checkbox State    //input    strict=False
    Should Not Be True    ${state}

Get Checkbox State Default Error
    Run Keyword And Expect Error
    ...    Checkbox ?name=can_send_email? is 'True' (bool) should be 'False' (bool)
    ...    Get Checkbox State    [name=can_send_email]    ==    unchecked

Get Checkbox State Custom Error
    Run Keyword And Expect Error
    ...    Kala False bool
    ...    Get Checkbox State    [name=can_send_email]    ==    unchecked    Kala {expected} {expected_type}

Check Checkbox
    ${state} =    Get Checkbox State    [name=can_send_sms]    ==    off
    Should Not Be True    ${state}
    Check Checkbox    [name=can_send_sms]
    ${state} =    Get Checkbox State    [name=can_send_sms]    ==    on
    Should Be True    ${state}

Uncheck Checkbox
    Get Checkbox State    [name=can_send_email]    ==    ${True}
    Uncheck Checkbox    [name=can_send_email]
    Get Checkbox State    [name=can_send_email]    ==    ${False}

Uncheck Checkbox With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 12 elements.*
    ...    Uncheck Checkbox   //input
    Run Keyword And Expect Error
    ...    *Not a checkbox or radio button*
    ...    Uncheck Checkbox   //input    strict=False

Get Checkbox State With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "xpath=//notamatch"*
    ...    Get Checkbox State    xpath=//notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}
