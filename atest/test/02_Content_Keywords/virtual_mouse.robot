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
    ${xy}=  Get Boundingbox    \#clickWithOptions    x  y 
    Mouse Button    click    @{xy}  clickCount=10
    Get Text        \#click_count    ==    10

Delay click
    ${xy}=  Get Boundingbox    \#clickWithOptions    x  y 
    Mouse Button    click    &{xy}    delay=1000
    Get Text        \#mouse_delay_time    validate     int(value) > 1000

Left Right and Middle Click
    ${xy}=  Get Boundingbox    \#clickWithOptions    x  y 
    Mouse Button    click    &{xy}  button=right
    Get Text        \#mouse_button    ==    right
    Mouse Button    click    &{xy}     button=middle
    Get Text        \#mouse_button    ==    middle
    Mouse Button    click    &{xy}     button=left
    Get Text        \#mouse_button    ==    left
