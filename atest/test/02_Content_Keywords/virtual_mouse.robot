*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Variables ***
${Center_Func} =    {'x': (value["x"] + (value["width"] / 2)), 'y': (value["y"] + (value["height"] / 2))}
${Dim_Func} =       {'width': value["width"], 'height': value["height"]}
${tol} =            1

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
    Assert Position    ${dest_center}[x]    ${dest_center}[y]    ${tol}

Drag And Drop With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Drag And Drop    //input    id=clickWithOptions
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Drag And Drop    id=draggable    //input
    Set Strict Mode    False
    Drag And Drop    id=draggable    //input
    Drag And Drop    //input    id=clickWithOptions
    [Teardown]    Set Strict Mode    True

Drag and Drop with coordinates
    ${obj_center} =    Get Boundingbox    id=draggable    ALL    evaluate    ${Center_Func}
    ${obj_dim} =    Get Boundingbox    id=draggable    ALL    evaluate    ${Dim_Func}
    ${dest_center} =    Get Boundingbox    id=clickWithOptions    ALL    evaluate    ${Center_Func}
    # Tests with implicit argument drop=True
    Drag And Drop By Coordinates
    ...    from_x=${obj_center}[x]    from_y=${obj_center}[y]
    ...    to_x=${dest_center}[x]    to_y=${dest_center}[y]    steps=200
    Assert Position    ${dest_center}[x]    ${dest_center}[y]    ${tol}
    Drag And Drop By Coordinates
    ...    from_x=${dest_center}[x]    from_y=${dest_center}[y]
    ...    to_x=${obj_center}[x]    to_y=${obj_center}[y]    steps=200
    Assert Position    ${obj_center}[x]    ${obj_center}[y]    ${tol}
    # Tests with explicit values True or False for argument drop
    # "Start coordinates" of draggable object:
    ${x1} =    Set Variable    ${obj_center}[x]
    ${y1} =    Set Variable    ${obj_center}[y]
    ${width} =    Set Variable    ${obj_dim}[width]
    ${height} =    Set Variable    ${obj_dim}[height]
    Log    Draggable object: ${obj_center}
    # coordinates where to drag in relative values:
    ${x2} =    Evaluate    ${x1} + 0.1 * ${width}
    ${y2} =    Evaluate    ${y1} - 1.0 * ${height}
    ${x3} =    Evaluate    ${x2} + 0.06 * ${width}
    ${y3} =    Evaluate    ${y2} + 1.2 * ${height}
    ${x4} =    Evaluate    ${x3} + 0.08 * ${width}
    ${y4} =    Set Variable    ${y3}
    ${x5} =    Set Variable    ${x4}
    ${y5} =    Set Variable    ${height}
    ${steps} =    Set Variable    200
    Drag And Drop By Coordinates    ${x1}    ${y1}    ${x2}    ${y2}    ${steps}    False
    Assert Position    ${x2}    ${y2}    ${tol}
    Drag And Drop By Coordinates    ${x2}    ${y2}    ${x3}    ${y3}    ${steps}    True
    Assert Position    ${x3}    ${y3}    ${tol}
    Drag And Drop By Coordinates    ${x3}    ${y3}    ${x4}    ${y4}    ${steps}    False
    Assert Position    ${x4}    ${y4}    ${tol}
    Drag And Drop By Coordinates    ${x4}    ${y4}    ${x5}    ${y5}    ${steps}    False
    Assert Position    ${x5}    ${y5}    ${tol}
    Drag And Drop By Coordinates    ${x5}    ${y5}    ${x1}    ${y1}    ${steps}    True

Hover and Drop to Hover
    Hover    id=draggable    10    10
    Mouse Button    down
    Hover    id=draggable    30    40
    Mouse Button    up
    Get Text    \#dragX    ==    20
    Get Text    \#dragY    ==    30

Hover With Strict
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Hover    //input
    Set Strict Mode    False
    Hover    //input
    [Teardown]    Set Strict Mode    True

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
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Get Boundingbox    //input
    Set Strict Mode    False
    ${x} =    Get Boundingbox    //input    x
    Should Be True    ${x}
    [Teardown]    Set Strict Mode    True

Mouse Move Relative To With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Mouse Move Relative To    //input    4    2
    Set Strict Mode    False
    Mouse Move Relative To    //input    4    2
    [Teardown]    Set Strict Mode    True

*** Keywords ***
Relative DnD
    [Arguments]    ${x}    ${y}    ${txt_x}    ${txt_y}
    Hover    id=draggable
    Mouse Button    down
    Mouse Move Relative To    id=draggable    ${x}    ${y}    steps=2
    Mouse Button    up
    Get Text    \#dragX    ==    ${txt_x}
    Get Text    \#dragY    ==    ${txt_y}
