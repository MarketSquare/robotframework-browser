*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Variables ***
${UserNameLabel} =      label[for="username_field"]
${InputUsername} =      id=username_field

*** Test Cases ***
Get Text
    ${h1} =    Get Text    h1
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
    Get Property    h1    innerText    !=    ${None}

Get Property With Strict Mode
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Get Property    //input    id
    ${property} =    Get Property    //input    id    strict=False
    Should Not Be Empty    ${property}

Get Property Default Error
    Run Keyword And Expect Error
    ...    Property innerText 'Login Page' (str) should not be 'Login Page' (str)
    ...    Get Property    h1    innerText    !=    Login Page

Get Property Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Property    h1    innerText    !=    Login Page    Tidii

Get Property innerText
    ${inner_text} =    Get Property    ${UserNameLabel}    innerText
    Should Be Equal    ${inner_text}    User Name:

Get Property size
    Get Property    ${InputUsername}    type    ==    text

Get Property For Element Property Which Does Not Exist
    Run Keyword And Expect Error
    ...    *Property 'not_here' not found!
    ...    Get Property    ${UserNameLabel}    not_here
    ${attribute} =    Get Property    ${UserNameLabel}    not_here    ==    ${None}

Get Property and Then .. (Closure)
    ${text} =    Get Property    h1    innerText    then    value.replace('g', 'k')
    Should be equal    ${text}    Lokin Pake

Get Property With Nonmatching Selector
    [Setup]    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Get Property
    ...    notamatch    attributeName
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Get Attribute
    ${type} =    Get Attribute    id=login_button    type
    Should Be Equal    ${type}    submit

Get Attribute Default Error
    Run Keyword And Expect Error
    ...    Attribute 'disabled' not found!
    ...    Get Attribute    id=login_button    disabled

Get Attribute Custom Error
    Run Keyword And Expect Error    None, nonetype, True, bool    Get Attribute    id=login_button    disabled    ==
    ...    ${True}    message={value}, {value_type}, {expected}, {expected_type}

Get Attribute and Verify absense
    Get Attribute    id=login_button    disabled    ==    ${None}

Get Attribute and return presents state
    ${present} =    Get Attribute    id=login_button    value    evaluate    value is not None
    Should Be True    ${present}
    ${present} =    Get Attribute    id=login_button    disabled    evaluate    value is None
    Should Be True    ${present}

Get Attribute Names
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    ${attrs} =    Get Attribute Names    [name="readonly_input"]
    FOR    ${attr}    IN    @{attrs}
        ${value} =    Get Attribute    [name="readonly_input"]    ${attr}
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
    Run Keyword And Expect Error    Custom error ?'1', '3'? list    Get Attribute Names    [name="readonly_input"]
    ...    ==    ${expected}    message=Custom error {expected} {expected_type}
    Run Keyword And Expect Error    Custom error ?'1', '3'? list    Get Attribute Names    [name="readonly_input"]
    ...    ==    1    3    message=Custom error {expected} {expected_type}
    [Teardown]    Close Page

Get Attribute Names and Assert single and multiple
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    Get Attribute Names    [name="readonly_input"]    ==    type    name    value    readonly
    Get Attribute Names    [name="disabled_input"]    contains    disabled
    Get Attribute Names    [name="disabled_input"]    validate    value[-1] == "disabled"
    [Teardown]    Close Page

Get Classes
    ${classes} =    Get Classes    id=draggable
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
    ${count} =    Get Element Count    h1
    Should Be Equal    ${count}    ${1}
    ${count} =    Get Element Count    label
    Should Be Equal    ${count}    ${2}
    ${count} =    Get Element Count    not-existing
    Should Be Equal    ${count}    ${0}

Get Element Count and Assert
    Get Element Count    h1    ==    1
    Get Element Count    h1    ==    ${1}
    Get Element Count    label    validate    value == 2
    Get Element Count    label    >    1
    Get Element Count    not-existing    ==
    ${promise} =    Promise to    Get Element Count    label
    ${count} =    Wait for    ${promise}
    should be equal    ${count}    ${2}

Get Element Count Default Error
    Run Keyword And Expect Error
    ...    Element count for selector `h1` is '1' (int) should be less than '1.0' (float)
    ...    Get Element Count    h1    <    1

Get Element Count Custom Error
    Run Keyword And Expect Error
    ...    My Errör
    ...    Get Element Count    h1    <    1    My Errör
