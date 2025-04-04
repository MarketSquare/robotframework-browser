*** Settings ***
Resource        imports.resource

Suite Setup     Ensure Open Page    ${FORM_URL}

*** Test Cases ***
Get Checkbox State Checked
    Get Checkbox State    [name=can_send_email]    ==    checked

Get Checkbox State Unchecked
    Get Checkbox State    [name=can_send_sms]    ==    UnChecked

Get Checkbox State With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 12 elements*
    ...    Get Checkbox State    //input
    Set Strict Mode    False
    ${state} =    Get Checkbox State    //input
    Should Not Be True    ${state}
    [Teardown]    Set Strict Mode    True

Get Checkbox State Default Error
    [Tags]    slow
    Run Keyword And Expect Error
    ...    Checkbox ${SELECTOR_PREFIX_SPACED}?name=can_send_email? is 'True' (bool) should be 'False' (bool)
    ...    Get Checkbox State    [name=can_send_email]    ==    unchecked

Get Checkbox State Custom Error
    [Tags]    slow
    Run Keyword And Expect Error
    ...    Kala False bool
    ...    Get Checkbox State    [name=can_send_email]    ==    unchecked    Kala {expected} {expected_type}

Check Checkbox
    [Documentation]
    ...    LOG 3:*    DEBUG    REGEXP: Checked checkbox: .*?\\[name=can_send_sms\\] with force: false
    ${state} =    Get Checkbox State    [name=can_send_sms]    ==    off
    Should Not Be True    ${state}
    Check Checkbox    [name=can_send_sms]
    ${state} =    Get Checkbox State    [name=can_send_sms]    ==    on
    Should Be True    ${state}

Check Checkbox With Force
    [Documentation]
    ...    LOG 1:*    DEBUG    REGEXP: Checked checkbox: .*?\\[name=can_send_sms\\] with force: true
    Check Checkbox    [name=can_send_sms]    True
    ${state} =    Get Checkbox State    [name=can_send_sms]    ==    on

Check Checkbox With Strict
    # TODO: Change: "*2" to correct value after PW update
    Run Keyword And Expect Error    *strict mode violation*//input[@type*resolved to 2 elements*    Check Checkbox
    ...    //input[@type="checkbox"]
    Set Strict Mode    False
    Check Checkbox    //input[@type="checkbox"]
    [Teardown]    Set Strict Mode    True

Uncheck Checkbox
    Get Checkbox State    [name=can_send_email]    ==    ${True}
    Uncheck Checkbox    [name=can_send_email]
    Get Checkbox State    [name=can_send_email]    ==    ${False}

Uncheck Checkbox With Force
    [Documentation]
    ...    LOG 1:*    DEBUG    REGEXP: Unchecked checkbox: .*?\\[name=can_send_email\\] with force: true
    Uncheck Checkbox    [name=can_send_email]    True
    Get Checkbox State    [name=can_send_email]    ==    ${False}

Uncheck Checkbox With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation*//input*resolved to 12 elements*
    ...    Uncheck Checkbox    //input
    Set Strict Mode    False
    Run Keyword And Expect Error
    ...    *Not a checkbox or radio button*
    ...    Uncheck Checkbox    //input
    [Teardown]    Set Strict Mode    True

Get Checkbox State With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.elementHandle: Timeout 50ms exceeded.*waiting for locator('//notamatch')*
    ...    Get Checkbox State    xpath=//notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Check Checkbox With Waiting
    [Tags]    slow
    New Page    ${WAIT_URL}
    Select Options By    \#dropdown    value    True    attached-unchecked
    Click With Options    \#submit    noWaitAfter=True
    Check Checkbox    \#victim
    Get Checkbox State    \#victim    ==    ${True}

Uncheck Checkbox With Waiting
    [Tags]    slow
    New Page    ${WAIT_URL}
    Select Options By    \#dropdown    value    True    attached-checked
    Click With Options    \#submit    noWaitAfter=True
    Uncheck Checkbox    \#victim
    Get Checkbox State    \#victim    ==    ${False}
