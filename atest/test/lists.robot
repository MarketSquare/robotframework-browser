*** Settings ***
Resource	./resource.robot
Test Setup	Open Form
Test Teardown	Close Browser

*** Test Cases ***
Page Should Contain List
    Page Should Contain List	css=select[name=interests]

List Selection Should Be
    [Documentation]
    ...    LOG 2 Verifying list 'interests' has options [${SPACE*2}] selected.
    ...    LOG 5 Verifying list 'possible_channels' has options [ Email | Telephone ] selected.
    List Selection Should Be    css=select[name=interests]
    List Selection Should Be    preferred_channel    Telephone
    List Selection Should Be    preferred_channel    phone
    List Selection Should Be    possible_channels    Email    Telephone
    List Selection Should Be    possible_channels    Telephone    Email
    List Selection Should Be    possible_channels    phone    email
    Run Keyword And Expect Error
    ...    List 'possible_channels' should have had selection ? Email | Telephone | Direct mail ? but selection was ? Email (email) | Telephone (phone) ?.
    ...    List Selection Should Be    possible_channels    Email    Telephone    Direct mail

Select From Single Selection List
    Select By Label And Verify Selection    preferred_channel    Email    Email
    Select By Label And Verify Selection    preferred_channel    Email    Email
    Select By Value And Verify Selection    preferred_channel    directmail    directmail
    Select From List By Label    preferred_channel    Telephone
    # do something else... anything to ensure the list is really set as the next keyword will pass
    # if list item is highlighted but not selected
    Unselect All From List       possible_channels
    List Selection Should Be     preferred_channel    Telephone
    Select From List By Label    preferred_channel    Direct mail
    List Selection Should Be     preferred_channel    Direct mail


