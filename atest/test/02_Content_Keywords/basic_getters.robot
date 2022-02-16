*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Retry Assertions For    ${assert_timeout}

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
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Get Property    //input    id
    Set Strict Mode    False
    ${property} =    Get Property    //input    id
    Should Not Be Empty    ${property}
    [Teardown]    Set Strict Mode    True

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

Get Attribute
    ${type} =    Get Attribute    id=login_button    type
    Should Be Equal    ${type}    submit

Get Attribute Default Error
    Run Keyword And Expect Error
    ...    *Attribute 'disabled' not found!
    ...    Get Attribute    id=login_button    disabled

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

Get Attribute Names With Strict
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 12 elements*
    ...    Get Attribute Names    //input
    Set Strict Mode    False
    ${attrs} =    Get Attribute Names    //input
    Should Not Be Empty    ${attrs}
    [Teardown]    Set Strict Mode    True

Get Attribute Names and Assert single and multiple
    [Setup]    New Page    ${ELEMENT_STATE_URL}
    Get Attribute Names    [name="readonly_input"]    ==    type    name    value    readonly
    Get Attribute Names    [name="disabled_input"]    contains    disabled
    Get Attribute Names    [name="disabled_input"]    validate    value[-1] == "disabled"
    [Teardown]    Close Page

Get Classes
    ${classes} =    Get Classes    id=draggable
    Should Be Equal    ${classes}    ${{["box", "react-draggable"]}}

Get Classes With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//button*resolved to 11 elements*
    ...    Get Classes    //button
    Set Strict Mode    False
    ${classes} =    Get Classes    //button
    Should Be Equal    ${classes}    ${None}
    [Teardown]    Set Strict Mode    True

Get Classes and Assert
    Get Classes    id=draggable    contains    react-draggable
    Get Classes    id=draggable    ==    react-draggable    box
    Get Classes    id=draggable    validate    "react-draggable-dragged" not in value

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

*** Keywords ***
Setup
    Close Page    ALL
    New Page    ${LOGIN_URL}
    ${assert_timeout} =    Set Retry Assertions For    2 sec
    Set Suite Variable    $assert_timeout
