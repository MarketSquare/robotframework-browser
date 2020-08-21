*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click Count
    Click With Options    \#clickWithOptions    click_count=10
    Get Text    \#click_count    ==    10

Click Count with Delay
    [Tags]    Not-Implemented
    Click With Options    \#clickWithOptions    delay=100    click_count=10
    Get Text    \#click_count    ==    10

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

Click with Coordinates
    [Tags]    Not-Implemented
    ${xy}    Get Boundingbox    \#clickWithOptions    x    y
    ${x}    Evaluate    ${xy}[x]+1
    ${y}    Evaluate    ${xy}[y]+1
    Click With Options    \#clickWithOptions    position_x=1    position_y=1
    Get Text    \#coordinatesX    validate    int(${x})==int(value)
    Get Text    \#coordinatesY    validate    int(${y})==int(value)
