*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click Count
    Click With Options    \#clickWithOptions    click_count=10
    Get Text              \#click_count    ==    10

Delay Click
    Click With Options    \#clickWithOptions    delay=1100
    Get Text              \#mouse_delay_time    >    1000

Left Right and Middle Click
    Browser.Click With Options    \#clickWithOptions    right
    Get Text    \#mouse_button    ==    right
    Browser.Click With Options    \#clickWithOptions    middle
    Get Text    \#mouse_button    ==    middle
    Browser.Click With Options    \#clickWithOptions    left
    Get Text    \#mouse_button    ==    left

Click with Coordinates
    Browser.Click With Options    \#clickWithOptions
    ${x}=    Get Text    coordinatesX
    ${y}=    Get Text    coordinatesY
    Browser.Click With Options    \#clickWithOptions    position_x=1    position_y=1
    Get Text    coordinatesX    validate    int(${x}+1)==int(value)
    Get Text    coordinatesY    validate    int(${y}+1)==int(value)
    
    