*** Settings ***
Resource          ./keywords.resource
Test Setup        Open Browser    ${FORM_URL}
Test Teardown     Close Browser
Test Timeout      10s

*** Keywords ***
Select Labels And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select Option By    label    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}

Select Values And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select Option By    value    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}

*** Test Cases ***
Page Should Contain List
    Page Should Have    select[name=interests]

List Selection Should Be
    [Documentation]
    ...    Verifying list 'interests' has no options selected.
    ...    Verifying list 'preferred_channel' has options [Telephone] selected.
    ...    Verifying list 'select[name=possible_channels]' has options [ Email | Telephone ] selected.
    List Selection Should Be    select[name=interests]
    List Selection Should Be    select[name=preferred_channel]    Telephone
    List Selection Should Be    select[name=preferred_channel]    phone
    List Selection Should Be    select[name=possible_channels]    Email    Telephone
    List Selection Should Be    select[name=possible_channels]    Telephone    Email
    List Selection Should Be    select[name=possible_channels]    phone    email
    Run Keyword And Expect Error    * options *'Direct mail'* should have been selected.
    ...    List Selection Should Be    select[name=possible_channels]    Email    Telephone    Direct mail

Small Select From List
    Select Option By    label    select[name=preferred_channel]    Direct mail

Select From List
    List Selection Should Be    select[name=preferred_channel]    Telephone
    Select Option By    label    select[name=preferred_channel]    Email
    List Selection Should Be    select[name=preferred_channel]    Email
    Select Labels And Verify Selection    select[name=preferred_channel]    Email    Email
    Select Values And Verify Selection    select[name=preferred_channel]    directmail    directmail
    Select Labels And Verify Selection    select[name=preferred_channel]    Telephone    Telephone

Multiselect From List
    List Selection Should Be    select[name=possible_channels]    Email    Telephone
    Select Option By    label    select[name=possible_channels]    Email    Telephone
    # FIXME: There's some weird behaviour with trying to unselect fields with page.select.
    # More details at
    Run Keyword And Expect Error    *
    ...    List Selection Should Be    select[name=possible_channels]
    Select Option By    label    select[name=possible_channels]    Email    Telephone    Direct mail
    List Selection Should Be    select[name=possible_channels]    Email    Telephone    Direct mail
