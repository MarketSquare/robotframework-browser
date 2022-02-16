*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    ${assert_timeout}

*** Test Cases ***
Get Element States Checkboxes and RadioButton checked
    Wait For Elements State    [name='can_send_sms']
    Get Element States    [name='can_send_sms']    *=    unchecked
    Get Element States    [name='can_send_email']    *=    checked
    Get Element States    [name='can_send_email']    not contains    unchecked
    Get Element States    [name='can_send_sms']    not contains    checked
    Get Element States    [name="sex"][value="female"]    contains    checked
    Get Element States    [name="sex"][value="male"]    not contains    checked

Get Element States Focused
    Wait For Elements State    textarea[name="comment"]
    Focus    textarea[name="comment"]
    Get Element States    textarea[name="comment"]    contains    focused
    Get Element States    textarea[name="comment"]    not contains    defocused
    Get Element States    [name='can_send_sms']    contains    defocused
    Get Element States    [name='can_send_sms']    not contains    focused
    Focus    [name='can_send_sms']
    Get Element States    textarea[name="comment"]    contains    defocused
    Get Element States    textarea[name="comment"]    not contains    focused
    Get Element States    [name='can_send_sms']    contains    focused
    Get Element States    [name='can_send_sms']    not contains    defocused

Get Element States readonly disabled
    Ensure URL    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    Get Element States    [name="enabled_input"]
    Get Element States    [name="enabled_input"]    contains    enabled    editable
    Get Element States    [name="readonly_input"]    contains    enabled    readonly
    Get Element States    [name="disabled_input"]    contains    disabled    readonly
    Get Element States    [name="enabled_input_button"]    contains    enabled    editable
    Get Element States    [name="disabled_input_button"]    contains    disabled    readonly
    Get Element States    [name="select"]    contains    enabled    editable
    Get Element States    id=enabled_option    contains    selected
    Get Element States    id=disabled_option    contains    deselected
    Get Element States    [name='disabled_button']    contains    disabled    readonly
    Get Element States    [name='disabled_only']    contains    disabled    readonly

Get Element States Then Flag Operations
    Ensure URL    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${filtered} =    Get Element States    [name="enabled_input"]    evaluate    value & (visible | attached)
    ${exp} =    Create List    attached    visible
    Lists Should Be Equal    ${filtered}    ${exp}

Get Element States Validate Flag Operations
    Ensure URL    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    Get Element States    [name="enabled_input"]    validate    value | (visible | attached)

Get Element States Return single element
    Ensure URL    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${visibility} =    Get Element States    [name="enabled_input"]    then    value & visible
    Should Be Equal    visible    @{visibility}
    ${hiddibility} =    Get Element States    [name="enabled_input"]    then    value & hidden
    Should Be Equal    ${{[]}}    ${hiddibility}

Get Element States Return Flags
    Ensure URL    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${flags} =    Get Element States    [name="enabled_input"]    return_names=False
    Evaluate    $flags & (type($flags).attached | type($flags).visible) == 5
    Wait For Elements State    [name="enabled_input"]    stable
    ${input_state} =    Get Element States    [name="enabled_input"]    return_names=False
    Wait For Elements State    [name="enabled_password"]    stable
    ${pwd_state} =    Get Element States    [name="enabled_password"]    return_names=False
    Should Be Equal    ${input_state}    ${pwd_state}

*** Keywords ***
Setup
    Close Page    ALL
    New Page    ${FORM_URL}
    ${assert_timeout} =    Set Retry Assertions For    2 sec
    Set Suite Variable    $assert_timeout

Ensure URL
    [Arguments]    ${url}
    ${cur} =    Get Url
    IF    $cur != $url
        Go To    ${url}
    END
