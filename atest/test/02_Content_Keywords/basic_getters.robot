*** Settings ***
Resource            imports.resource
Library             ../../library/presenter_mode.py

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    ${assert_timeout}
Test Setup          Ensure Location    ${LOGIN_URL}

*** Variables ***
${UserNameLabel} =      label[for="username_field"]
${InputUsername} =      id=username_field

*** Test Cases ***
Get Text
    ${h1} =    Get Text    h1
    Should Be Equal    ${h1}    Login Page

Get Text Disabled
    [Setup]    Go To    ${ELEMENT_STATE_URL}
    Set Presenter Mode    {"color": "red", "duration": "1s", "style": "solid"}
    ${text} =    Get Text    //input[@name="readonly_with_equals_only"]
    [Teardown]    Set Presenter Mode    False

Get Text And Assert ==
    Get Text    ${UserNameLabel}    ==    User Name:

Get Text And Assert !=
    Get Text    ${UserNameLabel}    !=

Get Text Assert Validate
    Get Text    h1    validate    value.startswith('Login')

Get Text With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.elementHandle: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Get Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Property And Assert
    Get Property    h1    innerText    ==    Login Page
    Get Property    h1    innerText    !=    ${None}
    Get Property    id=progress    innerHTML    contains    <div id="progress_bar" style="width: 10%; heig
    Get Property    id=progress    outerHTML    contains    <div id="progress" style="position:

Get Property With Strict Mode
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Property    //input    id
    Set Strict Mode    False
    ${property} =    Get Property    //input    id
    Should Not Be Empty    ${property}
    [Teardown]    Set Strict Mode    True

Get Property InnerText
    ${inner_text} =    Get Property    ${UserNameLabel}    innerText
    Should Be Equal    ${inner_text}    User Name:

Get Property Size
    Get Property    ${InputUsername}    type    ==    text

Get Property For Element Property Which Does Not Exist
    Run Keyword And Expect Error
    ...    *Property 'not_here' not found!
    ...    Get Property    ${UserNameLabel}    not_here
    ${attribute} =    Get Property    ${UserNameLabel}    not_here    ==    ${None}

Get Property And Then .. (Closure)
    ${text} =    Get Property    h1    innerText    then    value.replace('g', 'k')
    Should Be Equal    ${text}    Lokin Pake

Get Attribute
    ${type} =    Get Attribute    id=login_button    type
    Should Be Equal    ${type}    submit

Get Attribute Default Error
    Run Keyword And Expect Error
    ...    *Attribute 'disabled' not found!
    ...    Get Attribute    id=login_button    disabled

Get Attribute And Verify Absense
    Get Attribute    id=login_button    disabled    ==    ${None}

Get Attribute And Return Presents State
    ${present} =    Get Attribute    id=login_button    value    evaluate    value is not None
    Should Be True    ${present}
    ${present} =    Get Attribute    id=login_button    disabled    evaluate    value is None
    Should Be True    ${present}

Get Attribute Names
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    ${attrs} =    Get Attribute Names    [name="readonly_input"]
    FOR    ${attr}    IN    @{attrs}
        ${value} =    Get Attribute    [name="readonly_input"]    ${attr}
        Log    ${attr}=${value}
    END

Get Attribute Names With Strict
    [Tags]    slow
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 12 elements*
    ...    Get Attribute Names    //input
    Set Strict Mode    False
    ${attrs} =    Get Attribute Names    //input
    Should Not Be Empty    ${attrs}
    [Teardown]    Set Strict Mode    True

Get Attribute Names And Assert Single And Multiple
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Get Attribute Names    [name="readonly_input"]    ==    type    name    value    readonly
    Get Attribute Names    [name="disabled_input"]    contains    disabled
    Get Attribute Names    [name="disabled_input"]    validate    value[-1] == "disabled"
    ${names} =    Get Attribute Names    //title
    Length Should Be    ${names}    0
    ${names} =    Get Attribute Names    [name="select"]
    Length Should Be    ${names}    1

Get Classes
    [Setup]    Ensure Location    ${LOGIN_URL}
    ${classes} =    Get Classes    id=draggable
    Should Be Equal    ${classes}    ${{["box", "react-draggable"]}}

Get Classes With Strict
    [Tags]    slow
    [Setup]    Ensure Location    ${LOGIN_URL}
    Run Keyword And Expect Error
    ...    *strict mode violation*//button*resolved to ${BUTTON_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Get Classes    //button
    Set Strict Mode    False
    ${classes} =    Get Classes    //button
    Should Be Equal    ${classes}    ${{[]}}
    [Teardown]    Set Strict Mode    True

Get Classes And Assert
    [Setup]    Ensure Location    ${LOGIN_URL}
    Get Classes    id=draggable    contains    react-draggable
    Get Classes    id=draggable    ==    react-draggable    box
    Get Classes    id=draggable    validate    "react-draggable-dragged" not in value
    Drag And Drop Relative To    id=draggable    10    10    steps=2
    Get Classes    id=draggable    *=    react-draggable    box
    Get Classes    id=draggable    ==    react-draggable    box    react-draggable-dragged
    Get Classes    id=draggable    validate    "react-draggable-dragged" in value

Get Element Count
    [Setup]    Ensure Location    ${LOGIN_URL}
    ${count} =    Get Element Count    h1
    Should Be Equal    ${count}    ${1}
    ${count} =    Get Element Count    label
    Should Be Equal    ${count}    ${13}
    ${count} =    Get Element Count    not-existing
    Should Be Equal    ${count}    ${0}

Get Element Count And Assert
    [Setup]    Ensure Location    ${LOGIN_URL}
    Get Element Count    h1    ==    1
    Get Element Count    h1    ==    ${1}
    Get Element Count    label    validate    value == 13
    Get Element Count    label    >    1
    Get Element Count    not-existing    ==
    ${promise} =    Promise To    Get Element Count    label
    ${count} =    Wait For    ${promise}
    Should Be Equal    ${count}    ${13}

Get Style And Assert
    Get Style    h1    ALL    *=    align-content
    Get Style    h1    align-content    ==    normal

Get Style With Element
    ${elem} =    Get Element    h1
    Get Style    ${elem}    align-content    ==    normal

Get Element Size And Assert
    ${expected} =    Evaluate    {'x': 0, 'y': 660, 'width': 40, 'height': 30}
    ${bounding_box} =    Get BoundingBox    \#progress_bar    ALL    ==    ${expected}
    Should Be Equal    ${bounding_box}    ${expected}
    Get BoundingBox    \#progress_bar    ALL    ==    ${{{'x': 0, 'y': 660, 'width': 40, 'height': 30}}}

Get Bounding Box Of Hidden Elements
    VAR    @{hidden_with_bbox}    id=no-size    id=hidden-visibility-btn
    VAR    @{hidden_without_bbox}    id=hidden-btn    id=hidden-display-btn
    FOR    ${element}    IN    @{hidden_with_bbox}
        ${bbox} =    Get BoundingBox    ${element}
        Should Be True    ${bbox}
    END
    FOR    ${element}    IN    @{hidden_without_bbox}
        Get BoundingBox    ${element}    x    ==    ${None}    allow_hidden=True
        ${bbox} =    Get BoundingBox    ${element}    ALL    ==    ${None}    allow_hidden=True
        Should Be Equal    ${bbox}    ${None}
        TRY
            Get BoundingBox    ${element}
        EXCEPT    ValueError: Element is not visible and has no bounding box: ${element}    AS    ${e}
            Log    failed as expected
        END
    END

Get Element And Assert X
    ${x} =    Get BoundingBox    \#progress_bar    x    ==    0
    Should Be Equal    ${x}    ${0}

Get Element And Assert Y
    Get BoundingBox    \#progress_bar    y    validate    value - 660 == 0

Get Element Width And Height
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

Get Element States
    Wait For Elements State    h1
    ${state} =    Get Element States    h1
    Sort List    ${state}
    ${expected} =    Create List    attached    defocused    editable    enabled    visible
    FOR    ${state}    ${exp}    IN ZIP    ${state}    ${expected}
        Should Be Equal    ${state}    ${exp}
    END

Get Element States Check Hidden And Retry
    [Tags]    slow
    ${org} =    Set Retry Assertions For    2 sec
    Click    id=goes_hidden
    Get Element States    id=goes_hidden    *=    hidden
    [Teardown]    Set Retry Assertions For    ${org}

Get Element States Checkboxes And RadioButton Checked
    [Setup]    Ensure Location    ${FORM_URL}
    Wait For Elements State    [name='can_send_sms']
    Get Element States    [name='can_send_sms']    *=    unchecked
    Get Element States    [name='can_send_email']    *=    checked
    Get Element States    [name='can_send_email']    not contains    unchecked
    Get Element States    [name='can_send_sms']    not contains    checked
    Get Element States    [name="sex"][value="female"]    contains    checked
    Get Element States    [name="sex"][value="male"]    not contains    checked

Get Element States Focused
    [Setup]    Ensure Location    ${FORM_URL}
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

Get Element States Readonly Disabled
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
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
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${filtered} =    Get Element States    [name="enabled_input"]    evaluate    value & (visible | attached)
    ${exp} =    Create List    attached    visible
    Lists Should Be Equal    ${filtered}    ${exp}

Get Element States Validate Flag Operations
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    Get Element States    [name="enabled_input"]    validate    value | (visible | attached)

Get Element States Return Single Element
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${visibility} =    Get Element States    [name="enabled_input"]    then    value & visible
    Should Be Equal    visible    @{visibility}
    ${hiddibility} =    Get Element States    [name="enabled_input"]    then    value & hidden
    Should Be Equal    ${{[]}}    ${hiddibility}

Get Element States Return Flags
    [Setup]    Ensure Location    ${ELEMENT_STATE_URL}
    Wait For Elements State    [name="enabled_input"]
    ${flags} =    Get Element States    [name="enabled_input"]    return_names=False
    Evaluate    $flags & (type($flags).attached | type($flags).visible) == 5
    Wait For Elements State    [name="enabled_input"]    stable
    ${input_state} =    Get Element States    [name="enabled_input"]    return_names=False
    Wait For Elements State    [name="enabled_password"]    stable
    ${pwd_state} =    Get Element States    [name="enabled_password"]    return_names=False
    Should Be Equal    ${input_state}    ${pwd_state}

Get Console Log Test
    [Setup]    Setup
    ${first} =    Get Console Log    then    len(value)
    Click With Options    "Click with Options"    left    ALT    SHIFT
    ${logs} =    Get Console Log    validate    len(value) == 5
    Should Be Equal    ${logs}[2][type]    log
    Should Start With    ${logs}[2][text]    Mouse button: left
    Should Be True    $logs[2]['location']['url'].startswith('${LOGIN_URL[:-2]}')
    Should Be Equal    ${logs}[3][type]    error
    Should Be Equal    ${logs}[3][text]    1
    Should Be Equal    ${logs}[4][type]    warning
    Should Be True    ${logs}[4][text] > 0
    ${errors} =    Get Page Errors    validate    len(value) == 2
    Should Be Equal    ${errors}[0][name]    EvalError
    Should Be Equal    ${errors}[0][message]    You are not allowed to use this site
    ${last_time} =    Set Variable    ${errors}[-1][time]
    Should Be True
    ...    datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.strptime($last_time, '%Y-%m-%dT%H:%M:%S.%f%z') < datetime.timedelta(seconds=1)
    Get Console Log    validate    len(value) == 0
    Get Page Errors    validate    len(value) == 0
    Sleep    500ms
    Click With Options    "Click with Options"    left    ALT    SHIFT
    ${last} =    Get Console Log    validate    len(value) == 3
    Get Console Log    validate    len(value) == $first + len($logs) + len($last)    full=True
    Get Page Errors    validate    len(value) == 2
    ${now} =    Evaluate    datetime.datetime.now(datetime.timezone.utc)
    ${first_log} =    Get Console Log    then    value[0]    full=True    last=500ms
    Should Be True
    ...    $now - datetime.datetime.strptime($first_log['time'], '%Y-%m-%dT%H:%M:%S.%f%z') < datetime.timedelta(seconds=0.5)

*** Keywords ***
Setup
    Close Page    ALL
    Ensure Open Page    ${LOGIN_URL}
    ${assert_timeout} =    Set Retry Assertions For    2 sec
    Set Suite Variable    $assert_timeout
