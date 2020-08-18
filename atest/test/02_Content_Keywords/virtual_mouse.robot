*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click With coordinates
    ${xy}=    Get BoundingBox    \#login_button    x    y
    Mouse Button    click    &{xy}
    Get Text    text=Login failed. Invalid user name and/or password.

Move In Circle
    Mouse Move    400    400
    Mouse Move    0    400
    Mouse Move    400    0
    Mouse Move    0    0

Click Count
    [Documentation]
    # The coordinates shall point to the button Click with options
    Mouse Button    click    700    250    clickCount=10
    Get Text        \#click_count    ==    10

Delay click
    [Documentation]
    # The coordinates shall point to the button Click with options
    Mouse Button    click    700    250    delay=1000
    Get Text        \#mouse_delay_time    validate     int(value) > 1000

Left Right and Middle Click
    [Documentation]
    # The coordinates shall point to the button Click with options
    Mouse Button    click    700    250     right
    Get Text        \#mouse_button    ==    right
    Mouse Button    click    700    250     middle
    Get Text        \#mouse_button    ==    middle
    Mouse Button    click    700    250     left
    Get Text        \#mouse_button    ==    left