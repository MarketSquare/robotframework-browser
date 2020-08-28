*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click Count
    Click With Options    \#clickWithOptions    clickCount=10
    Get Text    \#click_count    ==    10

Click Count with Delay
    Click With Options    \#clickWithOptions    delay=100ms    clickCount=2
    Get Text    \#click_count    ==    2

Delay Click
    Click With Options    \#clickWithOptions    delay=300 ms
    Get Text    \#mouse_delay_time    validate    int(value) >= 300

Second Delay click
    Click With Options    \#clickWithOptions    delay=0.3
    Get Text    \#mouse_delay_time    validate    int(value) >= 300

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
    Get Text    \#coordinatesX    validate    ${x} < float(value)+1 and ${x} > float(value)-1
    Get Text    \#coordinatesY    validate    abs(${y} - float(value)) < 1
