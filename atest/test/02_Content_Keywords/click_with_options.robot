*** Settings ***
Resource        imports.resource

Suite Setup     Ensure Open Browser
Test Setup      Ensure Open Page    ${LOGIN_URL}

*** Test Cases ***
Click Count
    Click    \#clickWithOptions    clickCount=10
    Get Text    \#click_count    ==    10

Click Count With Delay
    Click    \#clickWithOptions    delay=100ms    clickCount=2
    Get Text    \#click_count    ==    2

Delay Click
    Click    \#clickWithOptions    delay=200 ms
    Get Text    \#mouse_delay_time    validate    int(value) >= 200

Second Delay Click
    Click    \#clickWithOptions    delay=0.2
    Get Text    \#mouse_delay_time    validate    int(value) >= 200

Left Right And Middle Click
    Click    \#clickWithOptions    right
    Get Text    \#mouse_button    ==    right
    Click    \#clickWithOptions    middle
    Get Text    \#mouse_button    ==    middle
    Click    \#clickWithOptions    left
    Get Text    \#mouse_button    ==    left

Click With Coordinates
    ${xy} =    Get Boundingbox    \#clickWithOptions
    ${x} =    Evaluate    "${xy}[x]"
    ${y} =    Evaluate    "${xy}[y]"
    Click    \#clickWithOptions    position_x=0    position_y=0
    # Give five pixels of leeway since the elements visual boundingbox might differ from the box used by click
    Get Text    \#coordinatesX    validate    abs(${x} - float(value)) < 5
    Get Text    \#coordinatesY    validate    abs(${y} - float(value)) < 5
