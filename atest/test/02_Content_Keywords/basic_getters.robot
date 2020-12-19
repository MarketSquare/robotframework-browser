*** Settings ***
Resource          imports.resource
Suite Setup       New Page    ${LOGIN_URL}

*** Variables ***
${UserNameLabel}=    label[for="username_field"]
${InputUsername}=    ${UserNameLabel} >> //.. >> input

*** Test Cases ***
Get Text
    ${h1}=    Get Text    h1
    Should Be Equal    ${h1}    Login Page

Get Text and Assert ==
    Get Text    ${UserNameLabel}    ==    User Name:

Get Text and Assert !=
    Get Text    ${UserNameLabel}    !=

Get Text Assert Validate
    Get Text    h1    validate    value.startswith('Login')

Get Text With Nonmatching Selector
    [Setup]    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Get Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Property and Assert
    Get Property    h1    innerText    ==    Login Page

Get Property innerText
    ${inner_text}=    Get Property    ${UserNameLabel}    innerText
    Should Be Equal    ${inner_text}    User Name:

Get Property size
    [Tags]    Not-Implemented
    Should Be Equal    ${size}    text
    Get Property    ${InputUsername}    type    ==    text

Get Property and Then .. (Closure)
    ${text}=    Get Property    h1    innerText    then    value.replace('g', 'k')
    Should be equal    ${text}    Lokin Pake

Get Property With Nonmatching Selector
    [Setup]    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Get Property    notamatch    attributeName
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Attribute
    ${type}=    Get Attribute    id=login_button    type
    Should Be Equal    ${type}    submit

Get Attribute Default Error
    Run Keyword And Expect Error
    ...    Attribute 'disabled' not found!
    ...    Get Attribute    id=login_button    disabled

Get Attribute Custom Error
    Run Keyword And Expect Error
    ...    None, nonetype, True, bool
    ...    Get Attribute    id=login_button    disabled    ==    ${True}    message={value}, {value_type}, {expected}, {expected_type}

Get Attribute and Verify absense
    Get Attribute    id=login_button    disabled    ==    ${None}

Get Attribute and return presents state
    ${present}=    Get Attribute    id=login_button    value    evaluate    value is not None
    Should Be True    ${present}
    ${present}=    Get Attribute    id=login_button    disabled    evaluate    value is None
    Should Be True    ${present}

Get Attribute Names
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${attrs}=    Get Attribute Names    [name="readonly_input"]
    FOR    ${attr}    IN    @{attrs}
        ${value}=    Get Attribute    [name="readonly_input"]    ${attr}
        Log    ${attr}=${value}
    END
    [Teardown]    Close Page

Get Attribute Names Default Error
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${expected} =    Create List    1    3
    Run Keyword And Expect Error
    ...    Attribute names '*' (list) should be '?'1', '3'?' (list)
    ...    Get Attribute Names    [name="readonly_input"]    ==    ${expected}
    [Teardown]    Close Page

Get Attribute Names Custom Error
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${expected} =    Create List    1    3
    Run Keyword And Expect Error
    ...    Custom error ?'1', '3'? list
    ...    Get Attribute Names    [name="readonly_input"]    ==    ${expected}    message=Custom error {expected} {expected_type}
    Run Keyword And Expect Error
    ...    Custom error ?'1', '3'? list
    ...    Get Attribute Names    [name="readonly_input"]    ==    1    3    message=Custom error {expected} {expected_type}
    [Teardown]    Close Page

Get Attribute Names and Assert single and multiple
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    Get Attribute Names    [name="readonly_input"]    ==    type    name    value    readonly
    Get Attribute Names    [name="disabled_input"]    contains    disabled
    Get Attribute Names    [name="disabled_input"]    validate    value[-1] == "disabled"
    [Teardown]    Close Page

Get Classes
    ${classes}=    Get Classes    id=draggable
    Should Be Equal    ${classes}    ${{["box", "react-draggable"]}}

Get Classes and Assert
    Get Classes    id=draggable    contains    react-draggable
    Get Classes    id=draggable    ==    react-draggable    box
    Get Classes    id=draggable    validate    "react-draggable-dragged" not in value

Get Classes Default Error
    Run Keyword And Expect Error
    ...    Classes of id=draggable '[[]'box', 'react-draggable'[]]' (list) should contain 'not-here' (str)
    ...    Get Classes    id=draggable    contains    not-here

Get Classes Custom Error
    Run Keyword And Expect Error
    ...    My Custom Error
    ...    Get Classes    id=draggable    contains    not-here    message=My Custom Error

Get Element Count
    ${count}=    Get Element Count    h1
    Should Be Equal    ${count}    ${1}
    ${count}=    Get Element Count    label
    Should Be Equal    ${count}    ${2}
    ${count}=    Get Element Count    not-existing
    Should Be Equal    ${count}    ${0}

Get Element Count and Assert
    Get Element Count    h1    ==    1
    Get Element Count    h1    ==    ${1}
    Get Element Count    label    validate    value == 2
    Get Element Count    label    >    1
    Get Element Count    not-existing    ==
    ${promise}=    Promise to    Get Element Count    label
    ${count}=    Wait for    ${promise}
    should be equal    ${count}    ${2}

Get Element Count Default Error
    Run Keyword And Expect Error
    ...    Element count for selector `h1` is '1' (int) should be less than '1.0' (float)
    ...    Get Element Count    h1    <    1

Get Element Count Custom Error
    Run Keyword And Expect Error
    ...    My Errör
    ...    Get Element Count    h1    <    1    My Errör

Get Style and Assert
    Get Style    h1    ALL    *=    align-content
    Get Style    h1    align-content    ==    normal

Get Style with element
    ${elem}=    Get Element    h1
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
    ${expected}=    Evaluate    {'x': 0, 'y': 400, 'width': 40, 'height': 30}
    ${bounding_box}=    Get BoundingBox    \#progress_bar    ALL    ==    ${expected}
    Should Be Equal    ${bounding_box}    ${expected}
    Get BoundingBox    \#progress_bar    ALL    ==    ${{{'x': 0, 'y': 400, 'width': 40, 'height': 30}}}

Get Element and Assert x
    ${x}=    Get BoundingBox    \#progress_bar    x    ==    0
    Should Be Equal    ${x}    ${0}

Get Element and Assert y
    Get BoundingBox    \#progress_bar    y    validate    value - 400 == 0

Get Element width and height
    ${expected}=    Evaluate    {'w': 40, 'h': 30}
    ${wh}=    Get BoundingBox    \#progress_bar    ALL    validate    value['width'] == 40
    ${wh}=    Get BoundingBox    \#progress_bar    ALL    evaluate    {'w': value['width'], 'h': value['height']}
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

Get Client Size
    ${size} =    Get Client Size
    Should Be True    ${size}[width] > 0
    Should Be True    ${size}[height] > 0

Get Client Size Element
    ${size} =    Get Client Size    \#progress_bar    width    >    0

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
    ${state} =    Get Element State    h1
    Should Be True    ${state}

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
