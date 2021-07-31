*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${FORM_URL}
Test Timeout    10s

*** Test Cases ***
Page Should Contain List
    Get Element Count    select[name=interests]    ==    1

Get Select Options
    Get Select Options    select[name=preferred_channel]    validate    len(value) == 3
    Get Select Options    select[name=preferred_channel]    validate    value[0]['index'] == 0
    Get Select Options    select[name=preferred_channel]    validate    value[2]['label'] == 'Direct mail'
    ${options} =    Get Select Options    select[name=possible_channels]
    Should be equal    ${options}[0][label]    Email
    Should be equal    ${options}[1][value]    phone

Get Selected Options
    [Documentation]
    ...    Verifying list 'preferred_channel' has options [Telephone] selected.
    ...    Verifying list 'possible_channels' has options [ Email | Telephone ] selected.
    ...    Verifying list 'interests' has no options selected.
    ...    Verifying list 'possible_channels' fails if assert all options selected.
    ${selection} =    Get Selected Options    select[name=preferred_channel]    label    ==    Telephone
    Log    ${selection}
    Should Be Equal    ${selection}    Telephone
    Get Selected Options    select[name=preferred_channel]    value    ==    phone
    Get Selected Options    select[name=possible_channels]    text    ==    Email    Telephone
    Get Selected Options    select[name=possible_channels]    text    validate    len(value) == 2
    Get Selected Options    select[name=possible_channels]    label    ==    Telephone    Email
    ${selection} =    Get Selected Options    select[name=possible_channels]    value    ==    phone    email
    Should Be Equal    ${selection}[0]    email
    Should Be Equal    ${selection}[1]    phone
    Get Selected Options    select[name=interests]    label    ==
    ${selection} =    Get Selected Options    select[name=interests]    label    ==
    Should Be Equal    ${selection}    ${None}
    Run Keyword And Expect Error    *
    ...    Get Selected Options    select[name=possible_channels]    label    ==    Email    Telephone    Direct mail

Get Selected Options with xpath
    ${selection} =    Get Selected Options    //html/body/form/table/tbody/tr[8]/td[2]/select    label    ==
    ...    Telephone
    Should Be Equal    ${selection}    Telephone

Get Selected Options With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Get Selected Options
    ...    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Select Option By label
    Select Option And Verify Selection    label    select[name=preferred_channel]    Direct mail

Select Options By value
    Select Option And Verify Selection    value    select[name=interests]    males    females    others

Select Options By index
    Select Option And Verify Selection    index    select[name=possible_channels]    0    2

Select Options By text
    Select Option And Verify Selection    text    select[name=interests]    Males    Females

Select Options By With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Select Options By
    ...    notamatch    label    Label
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Deselect Options Implicitly
    Select Option And Verify Selection    text    select[name=possible_channels]

Deselect Options Explicitly
    Deselect Options    select[name=possible_channels]
    Get Selected Options    select[name=possible_channels]    text    ==

Deselect Options With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Deselect Options
    ...    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

*** Keywords ***
Select Option And Verify Selection
    [Arguments]    ${attribute}    ${list_id}    @{selection}
    Select Options By    ${list_id}    ${attribute}    @{selection}
    Get Selected Options    ${list_id}    ${attribute}    ==    @{selection}
