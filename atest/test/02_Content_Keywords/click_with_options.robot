*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click Count
    Click With Options    \#clickWithOptions    click_count=10
    Get Text    \#click_count    ==    10
# When delay is set raises Could not find element with selector `#clickWithOptions` within timeout. error

Delay Click
    [Tags]    Not-Implemented
    Click With Options    \#clickWithOptions    delay=1100
    Get Text    \#mouse_delay_time    validate    int(value) > 1000

Second Delay click
    [Tags]    Not-Implemented
    Click With Options    \#clickWithOptions    delay=1
    Get Text    \#mouse_delay_time    validate    int(value) > 1000
    Fail

Left Right and Middle Click
    Click With Options    \#clickWithOptions    right
    Get Text    \#mouse_button    ==    right
    Click With Options    \#clickWithOptions    middle
    Get Text    \#mouse_button    ==    middle
    Click With Options    \#clickWithOptions    left
    Get Text    \#mouse_button    ==    left
# Invalid usage since coordinates are usually return as centre.
# When we go to x=1, y=1 we are at top left of element, not 1, 1 pixels off the centre

Click with Coordinates
    [Tags]    Not-Implemented
    Click With Options    \#clickWithOptions
    ${x}=    Get Text    \#coordinatesX
    ${y}=    Get Text    \#coordinatesY
    Click With Options    \#clickWithOptions    position_x=1    position_y=1
    Get Text    \#coordinatesX    validate    int(${x}+1)==int(value)
    Get Text    \#coordinatesY    validate    int(${y}+1)==int(value)
