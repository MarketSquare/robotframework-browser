*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    ${assert_timeout}

*** Test Cases ***
Get Style and Assert
    Get Style    h1    ALL    *=    align-content
    Get Style    h1    align-content    ==    normal

Get Style with element
    ${elem} =    Get Element    h1
    Get Style    ${elem}    align-content    ==    normal

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

Get Page Source
    Get Page Source    contains    <title>Login Page</title>

Get Client Size
    ${size} =    Get Client Size
    Should Be True    ${size}[width] > 0
    Should Be True    ${size}[height] > 0

Get Client Size Element
    ${size} =    Get Client Size    \#progress_bar    width    >    0
    Should Be True    ${size}

Get Scroll Position
    ${position} =    Get Scroll Position
    Should Be True    ${position}[top] >= 0
    Should Be True    ${position}[left] >= 0
    Should Be True    ${position}[bottom] > 0
    Should Be True    ${position}[right] > 0
    Length Should Be    ${position}    4

Get Scroll Position Element
    Get Scroll Position    h1    top    >=    0

Get Scroll Size
    ${size} =    Get Scroll Size
    Should Be True    ${size}[width] >= 0
    Should Be True    ${size}[height] >= 0
    Length Should Be    ${size}    2

Get Scroll Size With Strict No Element
    ${size} =    Get Scroll Size
    Should Be True    ${size}[width] >= 0

Get Scroll Size Element
    ${size} =    Get Scroll Size    h1    width    >=    0

Get Viewport Size
    ${size} =    Get Viewport Size
    Should Be True    ${size}[width] >= 0
    Should Be True    ${size}[height] >= 0
    Length Should Be    ${size}    2

Get Element State
    [Tags]    deprecated
    ${state} =    Get Element State    h1    assertion_operator=equal    assertion_expected=True
    Should Be True    ${state}
    ${state} =    Get Element State    h1
    Should Be True    ${state}

Get Element State With Assertion
    [Tags]    deprecated
    Get Element State    h1    readonly    ==    False

Get Element States
    Wait For Elements State    h1
    ${state} =    Get Element States    h1
    Sort List    ${state}
    ${expected} =    Create List    attached    defocused    editable    enabled    stable    visible
    FOR    ${state}    ${exp}    IN ZIP    ${state}    ${expected}
        Should Be Equal    ${state}    ${exp}
    END

Get Element States Check hidden and retry
    ${org} =    Set Retry Assertions For    2 sec
    Click    id=goes_hidden
    Get Element States    id=goes_hidden    *=    hidden
    [Teardown]    Set Retry Assertions For    ${org}

Get Element States Checkboxes and RadioButton checked
    Go To    ${FORM_URL}
    Wait For Elements State    [name='can_send_sms']
    Get Element States    [name='can_send_sms']    *=    unchecked
    Get Element States    [name='can_send_email']    *=    checked
    Get Element States    [name='can_send_email']    not contains    unchecked
    Get Element States    [name='can_send_sms']    not contains    checked
    Get Element States    [name="sex"][value="female"]    contains    checked
    Get Element States    [name="sex"][value="male"]    not contains    checked

Get Element States Focused
    Wait For Elements State    textarea[name="comment"]
    Focus    textarea[name="comment"]
    Get Element States    textarea[name="comment"]    contains    focused
    Get Element States    textarea[name="comment"]    not contains    defocused
    Get Element States    [name='can_send_sms']    contains    defocused
    Get Element States    [name='can_send_sms']    not contains    focused
    Focus    [name='can_send_sms']
    Get Element States    textarea[name="comment"]    contains    defocused
    Get Element States    textarea[name="comment"]    not contains    focused
    Get Element States    [name='can_send_sms']    contains    focused
    Get Element States    [name='can_send_sms']    not contains    defocused

Get Element States readonly disabled
    GoTo    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    Get Element States    [name="enabled_input"]
    Get Element States    [name="enabled_input"]    contains    enabled    editable
    Get Element States    [name="readonly_input"]    contains    enabled    readonly
    Get Element States    [name="disabled_input"]    contains    disabled    readonly
    Get Element States    [name="enabled_input_button"]    contains    enabled    editable
    Get Element States    [name="disabled_input_button"]    contains    disabled    readonly
    Get Element States    [name="select"]    contains    enabled    editable
    Get Element States    id=enabled_option    contains    selected
    Get Element States    id=disabled_option    contains    deselected
    Get Element States    [name='disabled_button']    contains    disabled    readonly
    Get Element States    [name='disabled_only']    contains    disabled    readonly

Get Element States Then Flag Operations
    Wait For Elements State    [name="enabled_input"]
    ${filtered} =    Get Element States    [name="enabled_input"]    evaluate    value & (visible | attached)
    ${exp} =    Create List    attached    visible
    Lists Should Be Equal    ${filtered}    ${exp}

Get Element States Validate Flag Operations
    Wait For Elements State    [name="enabled_input"]
    Get Element States    [name="enabled_input"]    validate    value | (visible | attached)

Get Element States Return single element
    Wait For Elements State    [name="enabled_input"]
    ${visibility} =    Get Element States    [name="enabled_input"]    then    value & visible
    Should Be Equal    visible    @{visibility}
    ${hiddibility} =    Get Element States    [name="enabled_input"]    then    value & hidden
    Should Be Equal    ${{[]}}    ${hiddibility}

Get Element States Return Flags
    Wait For Elements State    [name="enabled_input"]
    ${flags} =    Get Element States    [name="enabled_input"]    return_names=False
    Evaluate    $flags & (type($flags).attached | type($flags).visible) == 5
    Wait For Elements State    [name="enabled_input"]    stable
    ${input_state} =    Get Element States    [name="enabled_input"]    return_names=False
    Wait For Elements State    [name="enabled_password"]    stable
    ${pwd_state} =    Get Element States    [name="enabled_password"]    return_names=False
    Should Be Equal    ${input_state}    ${pwd_state}

*** Keywords ***
Setup
    Close Page    ALL
    New Page    ${LOGIN_URL}
    ${assert_timeout} =    Set Retry Assertions For    2 sec
    Set Suite Variable    $assert_timeout
