*** Settings ***
Resource          ./keywords.resource
Test Setup        Open Browser    ${FORM_URL}
Test Teardown     Close Browser
Test Timeout      10s

*** Keywords ***
Select Labels And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select Options By    label    ${list_id}    ${selection}
    Get Selected Options    ${list_id}    label    ==    @{exp_selection}

Select Values And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select Options By    value    ${list_id}    ${selection}
    Get Selected Options    ${list_id}    value    ==    @{exp_selection}

*** Test Cases ***
Page Should Contain List
    Page Should Have    select[name=interests]

Get Selected Options
    [Documentation]
    ...    Verifying list 'interests' has no options selected.
    ...    Verifying list 'preferred_channel' has options [Telephone] selected.
    ...    Verifying list 'select[name=possible_channels]' has options [ Email | Telephone ] selected.
    Get Selected Options    select[name=interests]    label    ==
    Get Selected Options    select[name=preferred_channel]    label    ==    Telephone
    Get Selected Options    select[name=preferred_channel]    value    ==    phone
    Get Selected Options    select[name=possible_channels]    text    ==    Email    Telephone
    Get Selected Options    select[name=possible_channels]    label    ==    Telephone    Email
    Get Selected Options    select[name=possible_channels]    value    ==    phone    email
    Run Keyword And Expect Error    *
    ...    Get Selected Options    select[name=possible_channels]    label    ==    Email    Telephone    Direct mail

Small Select From List
    Select Options By    label    select[name=preferred_channel]    Direct mail

Select From List
    Get Selected Options    select[name=preferred_channel]    label    ==    Telephone
    Select Options By    label    select[name=preferred_channel]    Email
    Get Selected Options    select[name=preferred_channel]    label    ==    Email
    Select Labels And Verify Selection    select[name=preferred_channel]    Email    Email
    Select Values And Verify Selection    select[name=preferred_channel]    directmail    directmail
    Select Labels And Verify Selection    select[name=preferred_channel]    Telephone    Telephone

Multiselect From List
    Get Selected Options    select[name=possible_channels]    label    ==    Email    Telephone
    Select Options By    label    select[name=possible_channels]
    Get Selected Options    select[name=possible_channels]    label    ==
    Select Options By    label    select[name=possible_channels]    Email    Telephone    Direct mail
    Get Selected Options    select[name=possible_channels]    label    ==    Email    Telephone    Direct mail
