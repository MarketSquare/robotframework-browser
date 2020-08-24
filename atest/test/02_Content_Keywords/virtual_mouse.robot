*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click With coordinates
    ${x}=    Get Boundingbox    \#login_button    x
    ${y}=    Get Boundingbox    \#login_button    y
    Mouse Button    click    ${x+5}    ${y+5}
    Get Text    text=Login failed. Invalid user name and/or password.

Move In Circle
    Mouse Move    400    400
    Mouse Move    0    400
    Mouse Move    400    0
    Mouse Move    0    0

Draggable Test
    ${x}=    Get Boundingbox    \#draggable    x
    ${y}=    Get Boundingbox    \#draggable    y
    # evaluate end coordinates
    ${xnew}    Evaluate    ${x}+400
    ${ynew}    Evaluate    ${y}+400
    Mouse Button    down    ${x}    ${y}
    Mouse Button    up    ${xnew}    ${ynew}
    # just do a random move to make sure the element is not stuck to mouse any more
    Mouse Move    0    0
    Get Text    \#dragX    ==    400
    Get Text    \#dragY    ==    400

Click Count
    ${x}=    Get Boundingbox    \#clickWithOptions    x
    ${y}=    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    clickCount=10
    Get Text    \#click_count    ==    10

Delay click
    ${x}=    Get Boundingbox    \#clickWithOptions    x
    ${y}=    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    delay=1000
    Get Text    \#mouse_delay_time    validate    int(value) > 1000

Left Right and Middle Click
    ${x}=    Get Boundingbox    \#clickWithOptions    x
    ${y}=    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    button=right
    Get Text    \#mouse_button    ==    right
    Mouse Button    click    ${x}    ${y}    button=middle
    Get Text    \#mouse_button    ==    middle
    Mouse Button    click    ${x}    ${y}    button=left
    Get Text    \#mouse_button    ==    left
