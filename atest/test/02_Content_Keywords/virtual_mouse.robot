*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Variables ***
${Center_Func} =    {'x': (value["x"] + (value["width"] / 2)), 'y': (value["y"] + (value["height"] / 2))}

*** Test Cases ***
Click With coordinates
    ${x} =    Get Boundingbox    \#login_button    x
    ${y} =    Get Boundingbox    \#login_button    y
    Mouse Button    click    ${x+5}    ${y+5}
    Get Text    text=Login failed. Invalid user name and/or password.

Move In Circle
    Mouse Move    400    400
    Mouse Move    0    400
    Mouse Move    400    0
    Mouse Move    0    0

Draggable Test
    ${x} =    Get Boundingbox    \#draggable    x
    ${y} =    Get Boundingbox    \#draggable    y
    # evaluate end coordinates
    ${xnew} =    Evaluate    ${x}+400
    ${ynew} =    Evaluate    ${y}+400
    Mouse Button    down    ${x}    ${y}
    Mouse Button    up    ${xnew}    ${ynew}
    # just do a random move to make sure the element is not stuck to mouse any more
    Mouse Move    0    0
    Get Text    \#dragX    ==    400
    Get Text    \#dragY    ==    400

Drag and Drop
    Drag And Drop    id=draggable    id=clickWithOptions
    ${obj_center} =    Get Boundingbox    id=draggable    ALL    evaluate    ${Center_Func}
    ${dest_center} =    Get Boundingbox    id=clickWithOptions    ALL    evaluate    ${Center_Func}
    Should Be True    ${obj_center}[x] - ${dest_center}[x] < 1 or ${obj_center}[x] - ${dest_center}[x] > -1
    Should Be True    ${obj_center}[y] - ${dest_center}[y] < 1 or ${obj_center}[y] - ${dest_center}[y] > -1

Drag And Drop With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Drag And Drop    //input    id=clickWithOptions
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Drag And Drop    id=draggable    //input
    Drag And Drop    id=draggable    //input    strict=False
    Drag And Drop    //input    id=clickWithOptions    strict=False

Drag and Drop with coordinates
    ${obj_center} =    Get Boundingbox    id=draggable    ALL    evaluate    ${Center_Func}
    ${dest_center} =    Get Boundingbox    id=clickWithOptions    ALL    evaluate    ${Center_Func}
    Drag And Drop By Coordinates
    ...    from_x=${obj_center}[x]    from_y=${obj_center}[y]
    ...    to_x=${dest_center}[x]    to_y=${dest_center}[y]    steps=200
    ${obj_center} =    Get Boundingbox    id=draggable    ALL    evaluate    ${Center_Func}
    ${x_diff} =    Evaluate    ${obj_center}[x] - ${dest_center}[x]
    ${y_diff} =    Evaluate    ${obj_center}[y] - ${dest_center}[y]
    Log    X-Diff: ${x_diff}, Y-Diff: ${y_diff}
    Should Be True    ${x_diff} < 1 or ${x_diff} > -1
    Should Be True    ${y_diff} < 1 or ${y_diff} > -1

Hover and Drop to Hover
    Hover    id=draggable    10    10
    Mouse Button    down
    Hover    id=draggable    30    40
    Mouse Button    up
    Get Text    \#dragX    ==    20
    Get Text    \#dragY    ==    30

Hover With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Hover    //input
    Hover    //input    strict=False

Drag and Drop with Move Relative
    Relative DnD    32    64    32    64
    Relative DnD    0    -64    32    0
    Relative DnD    -20    0    12    0
    Relative DnD    -22    -20    -10    -20

Click Count
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    clickCount=10
    Get Text    \#click_count    ==    10

Delay click
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    delay=1000
    Get Text    \#mouse_delay_time    validate    int(value) > 950

Left Right and Middle Click
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    button=right
    Get Text    \#mouse_button    ==    right
    Mouse Button    click    ${x}    ${y}    button=middle
    Get Text    \#mouse_button    ==    middle
    Mouse Button    click    ${x}    ${y}    button=left
    Get Text    \#mouse_button    ==    left

Get Boundingbox With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Get Boundingbox    //input
    ${x} =    Get Boundingbox    //input    x    strict=False
    Should Be True    ${x}

*** Keywords ***
Relative DnD
    [Arguments]    ${x}    ${y}    ${txt_x}    ${txt_y}
    Hover    id=draggable
    Mouse Button    down
    Mouse Move Relative To    id=draggable    ${x}    ${y}    steps=2
    Mouse Button    up
    Get Text    \#dragX    ==    ${txt_x}
    Get Text    \#dragY    ==    ${txt_y}
