*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Variables ***
${Center_Func} =    {'x': (value["x"] + (value["width"] / 2)), 'y': (value["y"] + (value["height"] / 2))}
${Dim_Func} =       {'width': value["width"], 'height': value["height"]}
${tol} =            1

*** Test Cases ***
Click With Coordinates
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
    [Setup]    New Page    ${DRAGGAME_URL}
    ${x} =    Get Boundingbox    id=blue-box    x
    ${y} =    Get Boundingbox    id=blue-box    y
    # evaluate end coordinates
    ${xnew} =    Evaluate    ${x}-200
    ${ynew} =    Evaluate    ${y}-200
    Mouse Button    down    ${x}    ${y}
    Mouse Button    up    ${xnew}    ${ynew}
    # just do a random move to make sure the element is not stuck to mouse any more
    Mouse Move    0    0
    Get Text    id=blue-box-x-value    ==    360
    Get Text    id=blue-box-y-value    ==    80

Drag And Drop
    [Setup]    New Page    ${DRAGGAME_URL}
    Drag And Drop    id=blue-box    id=invisible-element
    Take Screenshot
    ${dest_center} =    Get Boundingbox
    ...    id=invisible-element
    ...    ALL
    ...    evaluate
    ...    ${Center_Func}
    ...    allow_hidden=True
    Take Screenshot
    Assert Position    ${dest_center}[x]    ${dest_center}[y]    ${tol}

Drag And Drop With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Drag And Drop    //input    id=clickWithOptions
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Drag And Drop    id=clickWithOptions    //input
    Set Strict Mode    False
    Drag And Drop    id=clickWithOptions    //input
    Drag And Drop    //input    id=clickWithOptions
    [Teardown]    Set Strict Mode    True

Drag And Drop With Coordinates
    [Tags]    slow
    [Timeout]    60s
    [Setup]    New Page    ${DRAGGAME_URL}
    ${obj_center} =    Get Boundingbox    id=blue-box    ALL    evaluate    ${Center_Func}
    ${obj_dim} =    Get Boundingbox    id=blue-box    ALL    evaluate    ${Dim_Func}
    ${dest_center} =    Get Boundingbox    id=goal-post    ALL    evaluate    ${Center_Func}
    # Tests with implicit argument drop=True
    Drag And Drop By Coordinates
    ...    from_x=${obj_center}[x]    from_y=${obj_center}[y]
    ...    to_x=${dest_center}[x]    to_y=${dest_center}[y]    steps=200
    Assert Position    ${dest_center}[x]    ${dest_center}[y]    ${tol}
    Take Screenshot
    Drag And Drop By Coordinates
    ...    from_x=${dest_center}[x]    from_y=${dest_center}[y]
    ...    to_x=${obj_center}[x]    to_y=${obj_center}[y]    steps=200
    Take Screenshot
    Assert Position    ${obj_center}[x]    ${obj_center}[y]    ${tol}
    # Tests with explicit values True or False for argument drop
    # "Start coordinates" of blue-box object:
    ${x1} =    Set Variable    ${obj_center}[x]
    ${y1} =    Set Variable    ${obj_center}[y]
    ${width} =    Set Variable    ${obj_dim}[width]
    ${height} =    Set Variable    ${obj_dim}[height]
    Log    blue-box object: ${obj_center}
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
    ${time} =    Set Variable    1

Hover And Drop To Hover
    [Setup]    New Page    ${DRAGGAME_URL}
    ${x} =    Get Text    id=blue-box-x-value
    ${y} =    Get Text    id=blue-box-y-value
    Hover    id=blue-box    10    10
    Mouse Button    down
    Hover    id=blue-box    30    40
    Mouse Button    up
    ${x} =    Evaluate    ${x}+30
    ${y} =    Evaluate    ${y}+40
    ${x} =    Convert To String    ${x}
    ${y} =    Convert To String    ${y}
    Get Text    id=blue-box-x-value    ==    ${x}
    Get Text    id=blue-box-y-value    ==    ${y}

Hover With Strict
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Hover    //input
    Set Strict Mode    False
    Hover    //input
    [Teardown]    Set Strict Mode    True

Drag And Drop With Move Relative
    [Setup]    New Page    ${DRAGGAME_URL}
    Relative DnD    32    64    672    424
    Relative DnD    0    -64    752    440
    Relative DnD    -20    0    812    520
    Relative DnD    -22    -20    870    580

Drag And Drop Relative To
    [Setup]    New Page    ${DRAGGAME_URL}
    DnD Relative To    32    64    672    424
    DnD Relative To    0    -64    752    440
    DnD Relative To    -20    0    812    520
    DnD Relative To    -22    -20    870    580

Click Count
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    clickCount=10
    Get Text    \#click_count    ==    10

Delay Click
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    delay=100ms
    Get Text    \#mouse_delay_time    validate    int(value) > 90

Left Right And Middle Click
    ${x} =    Get Boundingbox    \#clickWithOptions    x
    ${y} =    Get Boundingbox    \#clickWithOptions    y
    Mouse Button    click    ${x}    ${y}    button=right
    Get Text    \#mouse_button    ==    right
    Mouse Button    click    ${x}    ${y}    button=middle
    Get Text    \#mouse_button    ==    middle
    Mouse Button    click    ${x}    ${y}    button=left
    Get Text    \#mouse_button    ==    left

Get Boundingbox With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Boundingbox    //input
    Set Strict Mode    False
    ${x} =    Get Boundingbox    //input    x
    Should Be True    ${x}
    [Teardown]    Set Strict Mode    True

Mouse Move Relative To With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Mouse Move Relative To    //input    4    2
    Set Strict Mode    False
    Mouse Move Relative To    //input    4    2
    [Teardown]    Set Strict Mode    True

Scroll By Mouse Wheel
    [Setup]    New Page    ${TABLES_URL}
    Get Scroll Position    body    left    ==    0
    Get Scroll Position    body    top    ==    0
    Hover    id=table1
    Mouse Wheel    30    400
    Get Scroll Position    body    left    ==    30
    Get Scroll Position    body    top    ==    400
    Mouse Wheel    -40    100
    Get Scroll Position    body    left    ==    0
    Get Scroll Position    body    top    ==    500

*** Keywords ***
Relative DnD
    [Arguments]    ${x}    ${y}    ${txt_x}    ${txt_y}
    Hover    id=blue-box
    Mouse Button    down
    Mouse Move Relative To    id=blue-box    ${x}    ${y}    steps=2
    Mouse Button    up
    Get Text    id=blue-box-x-value    ==    ${txt_x}
    Get Text    id=blue-box-y-value    ==    ${txt_y}

DnD Relative To
    [Arguments]    ${x}    ${y}    ${txt_x}    ${txt_y}
    Drag And Drop Relative To    id=blue-box    ${x}    ${y}    steps=2
    Get Text    id=blue-box-x-value    ==    ${txt_x}
    Get Text    id=blue-box-y-value    ==    ${txt_y}
