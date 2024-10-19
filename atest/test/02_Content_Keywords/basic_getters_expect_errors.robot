*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    ${assert_timeout}

*** Test Cases ***
Get Style Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Computed style is * (dotdict) should contain 'tidii' (str)
    ...    Get Style    h1    ALL    *=    tidii
    Run Keyword And Expect Error
    ...    Style value for align-content is 'normal' (str) should not be 'normal' (str)
    ...    Get Style    h1    align-content    !=    normal

Get Style Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    foobar
    ...    Get Style    h1    ALL    *=    tidii    foobar
    Run Keyword And Expect Error
    ...    foobar
    ...    Get Style    h1    align-content    !=    normal    foobar

Get BoundingBox Normal Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    BoundingBox x is '0' (int) should be '99.0' (float)
    ...    Get BoundingBox    \#progress_bar    x    ==    99

Get BoundingBox Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Custom Error 0 int 99.0 float
    ...    Get BoundingBox
    ...    \#progress_bar    x    ==    99
    ...    Custom Error {value} {value_type} {expected} {expected_type}

Get Page Source Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    HTML: '<!DOCTYPE html* (str) should contain 'tidii' (str)
    ...    Get Page Source    contains    tidii

Get Page Source Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    KalaKala
    ...    Get Page Source    contains    tidii    KalaKala

Get Client Size With Strict
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Client Size    //input
    Set Strict Mode    False
    ${size} =    Get Client Size    //input
    Should Be True    ${size}[width] > 0
    [Teardown]    Set Strict Mode    True

Get Client Size Element Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Client height is '*' (int) should be less than '0.0' (float)
    ...    Get Client Size    h1    height    <    0
    ${expected} =    Create Dictionary    wrong=value
    Run Keyword And Expect Error
    ...    KeyError: 'width'
    ...    Get Client Size    h1    all    <    ${expected}

Get Client Size Element Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Custom Error With ÄÄÄÄ 0.0
    ...    Get Client Size    h1    height    <    0    Custom Error With ÄÄÄÄ {expected}
    ${expected} =    Create Dictionary    wrong=value
    Run Keyword And Expect Error
    ...    Custom Error With ÄÄÄÄ {'wrong': 'value'}
    ...    Get Client Size    h1    all    ==    ${expected}    Custom Error With ÄÄÄÄ {expected}

Get Scroll Position With Strict
    [Tags]    expect_error
    Get Scroll Position
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Scroll Position    //input
    Set Strict Mode    False
    Get Scroll Position    //input
    [Teardown]    Set Strict Mode    True

Get Scroll Position Element Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Scroll position top is '0' (int) should be less than '0.0' (float)
    ...    Get Scroll Position    h1    top    <    0
    ${expected} =    Create Dictionary    top=-1    left=-1    bottom=-1    right=-1
    Run Keyword And Expect Error
    ...    Scroll position is * (dotdict) should be '{'top': '-1', 'left': '-1', 'bottom': '-1', 'right': '-1'}' (dotdict)
    ...    Get Scroll Position
    ...    h1
    ...    all
    ...    ==
    ...    ${expected}

Get Scroll Position Element Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Kala ÄÄ 0.0
    ...    Get Scroll Position    h1    top    <    0    Kala ÄÄ {expected}
    ${expected} =    Create Dictionary    top=-1    left=-1    bottom=-1    right=-1
    Run Keyword And Expect Error
    ...    Kala ÄÄ {'top': '-1', 'left': '-1', 'bottom': '-1', 'right': '-1'}
    ...    Get Scroll Position    h1    all    ==    ${expected}    Kala ÄÄ {expected}

Get Scroll Size With Strict
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Scroll Size    //input
    Set Strict Mode    False
    ${size} =    Get Scroll Size    //input
    Should Be True    ${size}[width] >= 0
    [Teardown]    Set Strict Mode    True

Get Scroll Size Element Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Scroll width is * (int) should be less than '0.0' (float)
    ...    Get Scroll Size    h1    width    <    0
    ${expected} =    Create Dictionary    top=-1    left=-1
    Run Keyword And Expect Error
    ...    Scroll size is * (dotdict) should be '{'top': '-1', 'left': '-1'}' (dotdict)
    ...    Get Scroll Size    h1    all    ==    ${expected}

Get Scroll Size Element Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Scroll Size    h1    width    <    0    Tidii
    ${expected} =    Create Dictionary    top=-1    left=-1
    Run Keyword And Expect Error
    ...    Tidii {'top': '-1', 'left': '-1'}"
    ...    Get Scroll Size    h1    all    ==    ${expected}    Tidii {expected}"

Get Viewport Size Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    SizeFields.height is '720' (int) should be less than '0.0' (float)
    ...    Get Viewport Size    height    <    0
    ${expected} =    Create Dictionary    width=-1    height=-1
    Run Keyword And Expect Error
    ...    Viewport size is * (dotdict) should be '{'width': '-1', 'height': '-1'}' (dotdict)
    ...    Get Viewport Size    all    ==    ${expected}

Get Viewport Size Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    My error
    ...    Get Viewport Size    height    <    0    My error
    ${expected} =    Create Dictionary    width=-1    height=-1
    Run Keyword And Expect Error
    ...    My error dotdict
    ...    Get Viewport Size    all    ==    ${expected}    My error {expected_type}

Get Url Default Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    URL 'http://localhost:*' (str) should contain 'Valid' (str)
    ...    Get Url    contains    Valid

Get Url Custom Error
    [Tags]    expect_error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Url    contains    Valid    Tidii

Get Property Default Error
    Run Keyword And Expect Error
    ...    Property innerText 'Login Page' (str) should not be 'Login Page' (str)
    ...    Get Property    h1    innerText    !=    Login Page

Get Property Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Property    h1    innerText    !=    Login Page    Tidii

Get Property With Nonmatching Selector
    [Tags]    no-iframe
    [Setup]    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.elementHandle: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Get Property    notamatch    attributeName
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Attribute With Strict
    TRY
        Get Attribute    //input    id
    EXCEPT    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*    type=glob    AS    ${error}
        Log    ${error}
    END
    TRY
        Get Attribute    //input    id    equal    nothere
    EXCEPT    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*    type=glob    AS    ${error}
        Log    ${error}
    END
    Set Strict Mode    False
    ${id} =    Get Attribute    //input    id
    Should Be Equal    ${id}    username_field
    Get Attribute    //input    id    equal    username_field
    [Teardown]    Set Strict Mode    True

Get Attribute Custom Error
    Run Keyword And Expect Error    None, nonetype, True, bool    Get Attribute    id=login_button    disabled    ==
    ...    ${True}    message={value}, {value_type}, {expected}, {expected_type}

Get Attribute Names Default Error
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${expected} =    Create List    1    3
    Run Keyword And Expect Error
    ...    Attribute names '*' (list) should be '?'1', '3'?' (list)
    ...    Get Attribute Names    [name="readonly_input"]    ==    @{expected}
    [Teardown]    Close Page

Get Attribute Names Custom Error
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${expected} =    Create List    1    3
    Run Keyword And Expect Error    Custom error ?'1', '3'? list    Get Attribute Names    [name="readonly_input"]
    ...    ==    @{expected}    message=Custom error {expected} {expected_type}
    Run Keyword And Expect Error    Custom error ?'1', '3'? list    Get Attribute Names    [name="readonly_input"]
    ...    ==    1    3    message=Custom error {expected} {expected_type}
    [Teardown]    Close Page

Get Classes Default Error
    Run Keyword And Expect Error
    ...    EQUALS: Classes of ${SELECTOR_PREFIX_SPACED}id=draggable '['box', 'react-draggable']' (list) should contain '['not-here']' (list)
    ...    Get Classes
    ...    id=draggable
    ...    contains
    ...    not-here

Get Classes Custom Error
    Run Keyword And Expect Error
    ...    My Custom Error
    ...    Get Classes    id=draggable    contains    not-here    message=My Custom Error

Get Element Count Default Error
    Run Keyword And Expect Error
    ...    Element count for selector `${SELECTOR_PREFIX_SPACED}h1` is '1' (int) should be less than '1.0' (float)
    ...    Get Element Count    h1    <    1

Get Element Count Custom Error
    Run Keyword And Expect Error
    ...    My Errör
    ...    Get Element Count    h1    <    1    My Errör

Get Element States And Check Error Message Equal
    Wait For Elements State    h1
    Run Keyword And Expect Error
    ...    EQUALS:Elements states '['attached', 'defocused', 'editable', 'enabled', 'visible']' (list) should be '['attached', 'enabled', 'readonly', 'visible']' (list)
    ...    Get Element States
    ...    h1
    ...    ==
    ...    visible
    ...    attached
    ...    enabled
    ...    readonly

Get Element States And Check Error Message Contains
    Wait For Elements State    h1
    Run Keyword And Expect Error
    ...    EQUALS:Elements states '['attached', 'defocused', 'editable', 'enabled', 'visible']' (list) should contain '['detached', 'enabled', 'readonly', 'visible']' (list)
    ...    Get Element States
    ...    h1
    ...    *=
    ...    visible
    ...    detached
    ...    enabled
    ...    readonly

Get Element States And Check Error Message Validate
    Wait For Elements State    h1
    Run Keyword And Expect Error
    ...    Elements states '*' (elementstate) should validate to true with 'value & detached == detached' (str)
    ...    Get Element States    h1    validate    value & detached == detached

Get Element States And Check Custom Error
    Wait For Elements State    h1
    Run Keyword And Expect Error
    ...    EQUALS:Oh NOO!
    ...    Get Element States    h1    *=    selected    message=Oh NOO!

Get Element States And Check Custom Error With Values
    Wait For Elements State    h1
    Run Keyword And Expect Error
    ...    EQUALS:Oh NOO! <h1> should contain ['selected'] but the states where ['attached', 'defocused', 'editable', 'enabled', 'visible']
    ...    Get Element States
    ...    h1
    ...    *=
    ...    selected
    ...    message=Oh NOO! <h1> should contain {expected} but the states where {value}

*** Keywords ***
Setup
    Close Page    ALL
    New Page    ${LOGIN_URL}
    ${assert_timeout} =    Set Retry Assertions For    0 sec
    Set Suite Variable    $assert_timeout
