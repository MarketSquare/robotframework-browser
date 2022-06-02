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

Click With All Modifier
    Click
    ...    \#clickWithOptions
    ...    left
    ...    1
    ...    None
    ...    None
    ...    None
    ...    False
    ...    False
    ...    Alt
    ...    Control
    ...    Meta
    ...    Shift
    Get Text    \#mouse_button    ==    left
    Get Text    \#alt_key    ==    true
    Get Text    \#ctrl_key    ==    true
    Get Text    \#meta_key    ==    true
    Get Text    \#shift_key    ==    true

Click With Control Modifier
    Click    \#clickWithOptions    right    1    None    None    None    False    False    Control
    Get Text    \#mouse_button    ==    right
    Get Text    \#alt_key    ==    false
    Get Text    \#ctrl_key    ==    true
    Get Text    \#meta_key    ==    false
    Get Text    \#shift_key    ==    false

Click With Shift Modifier
    Click    \#clickWithOptions    middle    1    None    None    None    False    False    Shift
    Get Text    \#mouse_button    ==    middle
    Get Text    \#alt_key    ==    false
    Get Text    \#ctrl_key    ==    false
    Get Text    \#meta_key    ==    false
    Get Text    \#shift_key    ==    true

Click With Meta Modifier
    Click    \#clickWithOptions    left    1    None    None    None    False    False    Meta
    Get Text    \#mouse_button    ==    left
    Get Text    \#alt_key    ==    false
    Get Text    \#ctrl_key    ==    false
    Get Text    \#meta_key    ==    true
    Get Text    \#shift_key    ==    false

Click With Alt Modifier
    Click    \#clickWithOptions    left    1    None    None    None    False    False    Alt
    Get Text    \#mouse_button    ==    left
    Get Text    \#alt_key    ==    true
    Get Text    \#ctrl_key    ==    false
    Get Text    \#meta_key    ==    false
    Get Text    \#shift_key    ==    false

Click With No Modifier
    Click    \#clickWithOptions    left    1    None    None    None    False    False
    Get Text    \#mouse_button    ==    left
    Get Text    \#alt_key    ==    false
    Get Text    \#ctrl_key    ==    false
    Get Text    \#meta_key    ==    false
    Get Text    \#shift_key    ==    false

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
