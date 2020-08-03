*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${FORM_URL}

*** Test Cases ***
Get Checkbox State Checked
    Get Checkbox State    [name=can_send_email]    ==    checked

Get Checkbox State Unchecked
    Get Checkbox State    [name=can_send_sms]    ==    UnChecked

Check Checkbox
    ${state}=    Get Checkbox State    [name=can_send_sms]    ==    off
    Should Not Be True    ${state}
    Check Checkbox    [name=can_send_sms]
    ${state}=    Get Checkbox State    [name=can_send_sms]    ==    on
    Should Be True    ${state}

Uncheck Checkbox
    Get Checkbox State    [name=can_send_email]    ==    ${True}
    Uncheck Checkbox    [name=can_send_email]
    Get Checkbox State    [name=can_send_email]    ==    ${False}

Get Checkbox State With Nonmatching Selector
    Set Timeout    50ms
    Run Keyword And Expect Error    Could not find element with selector `xpath=//notamatch` within timeout.    Get Checkbox State    xpath=//notamatch
    [Teardown]    Set Timeout    ${PLAYWRIGHT_TIMEOUT}
