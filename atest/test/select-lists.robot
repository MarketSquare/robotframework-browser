*** Settings ***
Resource          ./keywords.resource
Test Setup        Open Browser    ${FORM_URL}
Test Teardown     Close Browser

*** Keywords ***
Select By Label And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select From List By Label    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}

Select By Value And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select From List By Value    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}

*** Test Cases ***
Page Should Contain List
    Page Should Have  css=select[name=interests]

List Selection Should Be
    [Documentation]
    ...    Verifying list 'interests' has no options selected.
    ...    Verifying list 'preferred_channel' has options [Telephone] selected.
    ...    Verifying list 'css=select[name=possible_channels]' has options [ Email | Telephone ] selected.
    List Selection Should Be    css=select[name=interests]
    List Selection Should Be    css=select[name=preferred_channel]    Telephone
    List Selection Should Be    css=select[name=preferred_channel]    phone
    List Selection Should Be    css=select[name=possible_channels]    Email    Telephone
    List Selection Should Be    css=select[name=possible_channels]    Telephone    Email
    List Selection Should Be    css=select[name=possible_channels]    phone    email
    Run Keyword And Expect Error    * options *'Direct mail'* should have been selected.
    ...    List Selection Should Be    css=select[name=possible_channels]    Email    Telephone    Direct mail

Small Select From List
    Select From List By Label    css=select[name=preferred_channel]    Direct mail

Select From List
    List Selection Should Be    css=select[name=preferred_channel]    Telephone
    Select From List By Label    css=select[name=preferred_channel]    Email
    List Selection Should Be    css=select[name=preferred_channel]    Email
    Select By Label And Verify Selection    css=select[name=preferred_channel]    Email    Email
    Select By Value And Verify Selection    css=select[name=preferred_channel]    directmail    directmail
    Select By Label And Verify Selection    css=select[name=preferred_channel]    Telephone

Multiselect From List
    List Selection Should Be    css=select[name=possible_channels]    Email    Telephone
    Select From List By Label    css=select[name=possible_channels]    Email    Telephone
    List Selection Should Be    css=select[name=possible_channels]
    Select From List By Label    css=select[name=possible_channels]    Email    Telephone    Direct mail
    List Selection Should Be    css=select[name=possible_channels]    Email    Telephone    Direct mail
