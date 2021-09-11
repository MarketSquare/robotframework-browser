*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
Get Style and Assert
    Get Style    h1    ALL    *=    align-content
    Get Style    h1    align-content    ==    normal

Get Style with element
    ${elem} =    Get Element    h1
    Get Style    ${elem}    align-content    ==    normal

Get Style Default Error
    Run Keyword And Expect Error
    ...    Computed style is * (dict) should contain 'tidii' (str)
    ...    Get Style    h1    ALL    *=    tidii
    Run Keyword And Expect Error
    ...    Style value for align-content is 'normal' (str) should not be 'normal' (str)
    ...    Get Style    h1    align-content    !=    normal

Get Style Custom Error
    Run Keyword And Expect Error
    ...    foobar
    ...    Get Style    h1    ALL    *=    tidii    foobar
    Run Keyword And Expect Error
    ...    foobar
    ...    Get Style    h1    align-content    !=    normal    foobar

Get Element Size and Assert
    ${expected} =    Evaluate    {'x': 0, 'y': 500, 'width': 40, 'height': 30}
    ${bounding_box} =    Get BoundingBox    \#progress_bar    ALL    ==    ${expected}
    Should Be Equal    ${bounding_box}    ${expected}
    Get BoundingBox    \#progress_bar    ALL    ==    ${{{'x': 0, 'y': 500, 'width': 40, 'height': 30}}}

Get Element and Assert x
    ${x} =    Get BoundingBox    \#progress_bar    x    ==    0
    Should Be Equal    ${x}    ${0}

Get Element and Assert y
    Get BoundingBox    \#progress_bar    y    validate    value - 500 == 0

Get Element width and height
    ${expected} =    Evaluate    {'w': 40, 'h': 30}
    ${wh} =    Get BoundingBox    \#progress_bar    ALL    validate    value['width'] == 40
    ${wh} =    Get BoundingBox    \#progress_bar    ALL    evaluate    {'w': value['width'], 'h': value['height']}
    Should Be Equal    ${wh}    ${expected}

Get BoundingBox Normal Error
    Run Keyword And Expect Error
    ...    BoundingBox x is '0' (int) should be '99.0' (float)
    ...    Get BoundingBox    \#progress_bar    x    ==    99

Get BoundingBox Custom Error
    Run Keyword And Expect Error
    ...    Custom Error 0 int 99.0 float
    ...    Get BoundingBox
    ...    \#progress_bar    x    ==    99
    ...    Custom Error {value} {value_type} {expected} {expected_type}

Get Page Source
    Get Page Source    contains    <title>Login Page</title>

Get Page Source Default Error
    Run Keyword And Expect Error
    ...    HTML: '<!DOCTYPE html* (str) should contain 'tidii' (str)
    ...    Get Page Source    contains    tidii

Get Page Source Custom Error
    Run Keyword And Expect Error
    ...    KalaKala
    ...    Get Page Source    contains    tidii    KalaKala

Get Client Size
    ${size} =    Get Client Size
    Should Be True    ${size}[width] > 0
    Should Be True    ${size}[height] > 0

Get Client Size Element
    ${size} =    Get Client Size    \#progress_bar    width    >    0
    Should Be True    ${size}

Get Client Size With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Get Client Size    //input
    Set Strict Mode    False
    ${size} =    Get Client Size    //input
    Should Be True    ${size}[width] > 0
    [Teardown]    Set Strict Mode    True

Get Client Size Element Default Error
    Run Keyword And Expect Error
    ...    Client height is '*' (int) should be less than '0.0' (float)
    ...    Get Client Size    h1    height    <    0
    ${expected} =    Create Dictionary    wrong=value
    Run Keyword And Expect Error
    ...    KeyError: 'width'
    ...    Get Client Size    h1    all    <    ${expected}

Get Client Size Element Custom Error
    Run Keyword And Expect Error
    ...    Custom Error With ÄÄÄÄ 0.0
    ...    Get Client Size    h1    height    <    0    Custom Error With ÄÄÄÄ {expected}
    ${expected} =    Create Dictionary    wrong=value
    Run Keyword And Expect Error
    ...    Custom Error With ÄÄÄÄ {'wrong': 'value'}
    ...    Get Client Size    h1    all    ==    ${expected}    Custom Error With ÄÄÄÄ {expected}

Get Scroll Position
    ${position} =    Get Scroll Position
    Should Be True    ${position}[top] >= 0
    Should Be True    ${position}[left] >= 0
    Should Be True    ${position}[bottom] > 0
    Should Be True    ${position}[right] > 0
    Length Should Be    ${position}    4

Get Scroll Position Element
    Get Scroll Position    h1    top    >=    0

Get Scroll Position With Strict
    Get Scroll Position
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Get Scroll Position    //input
    Set Strict Mode    False
    Get Scroll Position    //input
    [Teardown]    Set Strict Mode    True

Get Scroll Position Element Default Error
    Run Keyword And Expect Error
    ...    Scroll position top is '0' (int) should be less than '0.0' (float)
    ...    Get Scroll Position    h1    top    <    0
    ${expected} =    Create Dictionary    top=-1    left=-1    bottom=-1    right=-1
    Run Keyword And Expect Error
    ...    Scroll position is * (dict) should be '{'top': '-1', 'left': '-1', 'bottom': '-1', 'right': '-1'}' (dotdict)
    ...    Get Scroll Position    h1    all    ==    ${expected}

Get Scroll Position Element Custom Error
    Run Keyword And Expect Error
    ...    Kala ÄÄ 0.0
    ...    Get Scroll Position    h1    top    <    0    Kala ÄÄ {expected}
    ${expected} =    Create Dictionary    top=-1    left=-1    bottom=-1    right=-1
    Run Keyword And Expect Error
    ...    Kala ÄÄ {'top': '-1', 'left': '-1', 'bottom': '-1', 'right': '-1'}
    ...    Get Scroll Position    h1    all    ==    ${expected}    Kala ÄÄ {expected}

Get Scroll Size
    ${size} =    Get Scroll Size
    Should Be True    ${size}[width] >= 0
    Should Be True    ${size}[height] >= 0
    Length Should Be    ${size}    2

Get Scroll Size With Strict No Element
    ${size} =    Get Scroll Size
    Should Be True    ${size}[width] >= 0

Get Scroll Size With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Get Scroll Size    //input
    Set Strict Mode    False
    ${size} =    Get Scroll Size    //input
    Should Be True    ${size}[width] >= 0
    [Teardown]    Set Strict Mode    True

Get Scroll Size Element
    ${size} =    Get Scroll Size    h1    width    >=    0

Get Scroll Size Element Default Error
    Run Keyword And Expect Error
    ...    Scroll width is * (int) should be less than '0.0' (float)
    ...    Get Scroll Size    h1    width    <    0
    ${expected} =    Create Dictionary    top=-1    left=-1
    Run Keyword And Expect Error
    ...    Scroll size is * (dict) should be '{'top': '-1', 'left': '-1'}' (dotdict)
    ...    Get Scroll Size    h1    all    ==    ${expected}

Get Scroll Size Element Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Scroll Size    h1    width    <    0    Tidii
    ${expected} =    Create Dictionary    top=-1    left=-1
    Run Keyword And Expect Error
    ...    Tidii {'top': '-1', 'left': '-1'}"
    ...    Get Scroll Size    h1    all    ==    ${expected}    Tidii {expected}"

Get Viewport Size
    ${size} =    Get Viewport Size
    Should Be True    ${size}[width] >= 0
    Should Be True    ${size}[height] >= 0
    Length Should Be    ${size}    2

Get Viewport Size Default Error
    Run Keyword And Expect Error
    ...    SizeFields.height is '720' (int) should be less than '0.0' (float)
    ...    Get Viewport Size    height    <    0
    ${expected} =    Create Dictionary    width=-1    height=-1
    Run Keyword And Expect Error
    ...    Viewport size is * (dict) should be '{'width': '-1', 'height': '-1'}' (dotdict)
    ...    Get Viewport Size    all    ==    ${expected}

Get Viewport Size Custom Error
    Run Keyword And Expect Error
    ...    My error
    ...    Get Viewport Size    height    <    0    My error
    ${expected} =    Create Dictionary    width=-1    height=-1
    Run Keyword And Expect Error
    ...    My error dotdict
    ...    Get Viewport Size    all    ==    ${expected}    My error {expected_type}

Get Element State
    ${state} =    Get Element State    h1    assertion_operator=equal    assertion_expected=True
    Should Be True    ${state}
    ${state} =    Get Element State    h1
    Should Be True    ${state}

Get Element State With Strict On ElementSelectorWithOptions
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 18 elements.*
    ...    Get Element State    //div
    Set Strict Mode    False
    ${state} =    Get Element State    //div
    Should Be True    ${state}
    [Teardown]    Set Strict Mode    True

Get Element State With Strict On WaitForFunctionOptions
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 18 elements.*
    ...    Get Element State    //div    state=disabled
    Set Strict Mode    False
    ${state} =    Get Element State    //div    state=disabled
    Should Not Be True    ${state}
    [Teardown]    Set Strict Mode    True

Get Element State With Assertion
    Get Element State    h1    readonly    ==    False

Get Element State Default Error
    Run Keyword And Expect Error
    ...    State 'readonly' of 'h1' is 'False' (bool) should be 'True' (bool)
    ...    Get Element State    h1    readonly    ==    True

Get Element State Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Element State    h1    readonly    ==    True    Tidii

Get Url Default Error
    Run Keyword And Expect Error
    ...    URL 'http://localhost:*' (str) should contain 'Valid' (str)
    ...    Get Url    contains    Valid

Get Url Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Url    contains    Valid    Tidii
