*** Settings ***
Documentation       Tests for Get Element and `element=<ref>` selector syntax

Resource            imports.resource

Suite Setup         Ensure Open Page
Test Setup          Element Selector Setup

*** Test Cases ***
Get Element
    ${ref} =    Get Element    select[name="preferred_channel"]
    Set Strict Mode    False
    ${option_value} =    Get Property    ${ref} >> option    value
    Should Be Equal    ${option_value}    email
    [Teardown]    Set Strict Mode    True

Get Element With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation:*//input*resolved to 12 elements*
    ...    Get Element    //input
    Set Strict Mode    False
    ${element} =    Get Element    //input
    Should Start With    ${element}    //input
    [Teardown]    Set Strict Mode    True

Get Element With Nonmatching Child Selector
    ${ref} =    Get Element    select[name="preferred_channel"]
    ${timeout} =    Set Browser Timeout    100ms
    Run Keyword And Expect Error
    ...    *Error: locator.elementHandle: Timeout 100ms exceeded.*    Get Property
    ...    ${ref}>> .notamatch    value
    [Teardown]    Set Browser Timeout    ${timeout}

Using Invalid Element Reference Fails
    Run Keyword And Expect Error
    ...    Error: locator.click: Unknown engine "element"*
    ...    Click    element=1234-4321
    Run Keyword And Expect Error
    ...    Error: locator.click: Unknown engine "element"*
    ...    Click    element=1234-4321 >> .css

Get Element From Frame
    [Setup]    New Page    ${FRAMES_URL}
    ${ref} =    Get Element    body >> [src="left.html"] >>> body
    Get Property    ${ref} >> //input[@name="searchbutton"]    value    ==    Search

Using Element Handle Directly As Selector
    New Page    ${LOGIN_URL}
    ${login_btn} =    Get Element    input#login_button
    Click    ${login_btn}
    Get Text    text=Login failed. Invalid user name and/or password.

Get Elements When Only 1 Match
    ${refs} =    Get Elements    select[name="preferred_channel"]
    ${elem} =    Get From List    ${refs}    0
    Set Strict Mode    False
    ${option_value} =    Get Property    ${elem} >> option    value
    Should Be Equal    ${option_value}    email
    [Teardown]    Set Strict Mode    True

Get Elements Include Hidden
    ${refs} =    Get Elements    input
    Should Be Equal As Integers    12    ${{ len(${refs}) }}

Get Elements Should Not Fail If Element Is Not Found
    ${timeout} =    Set Browser Timeout    100ms
    ${refs} =    Get Elements    xpath=//not_here
    Should Be Empty    ${refs}
    [Teardown]    Set Browser Timeout    ${timeout}

Get Elements Should Fail With Invalid Selector
    Run Keyword And Expect Error
    ...    * Unknown engine "invalid" *
    ...    Get Elements    invalid=//foobar

Get Element And Click
    New Page    ${LOGIN_URL}
    ${refs} =    Get Elements    .pure-button
    Should Be Equal As Numbers    ${{ len(${refs}) }}    5
    FOR    ${elem}    IN    @{refs}
        Click    ${elem}
    END

Get Element By Role
    [Documentation]    This test does not only test the Get Element By Role keyword.
    ...
    ...    It also tests the ``all_elements`` argument and ``strict_mode``.
    ...    Due to the JS implementation these two things do not need to be tested
    ...    with the other Get Element By keyword.
    ${e} =    Get Element By Role    textbox    name=Name:
    Get Element States    ${e}    *=    visible
    ${e} =    Get Element By Role    textbox    name=/.*label.email$/i
    Get Element States    ${e}    *=    visible
    ${e} =    Get Element By Role    textbox    name=Website:
    Get Text    ${e}    ==    https://example.com
    Evaluate JavaScript    ${e}    e => e.disabled = true
    ${e} =    Get Element By Role    textbox    disabled=True
    Get Text    ${e}    ==    https://example.com
    ${e} =    Get Element By Role    radio    all_elements=True
    FOR    ${e}    IN    @{e}
        Get Element States    ${e}    *=    visible
    END
    ${e} =    Get Element By Role    radio    checked=True
    Get Element States    ${e}    *=    visible
    ${exp_list} =    Create List    Telephone    Email    Telephone    Option 1    0    DEFAULT OPTION
    ${element_list} =    Get Element By Role    option    selected=True    all_elements=True
    FOR    ${el}    ${exp_text}    IN ZIP    ${element_list}    ${exp_list}
        Get Text    ${el}    ==    ${exp_text}
    END
    Set Browser Timeout    timeout=100ms    scope=Test
    ${e} =    Get Element By Role    role=heading    all_elements=True
    Should Be Empty    ${e}
    Run Keyword And Expect Error    *Error: strict mode violation: getByRole('textbox') resolved to 4 elements*
    ...    Get Element By Role    role=textbox
    Set Strict Mode    False
    ${e} =    Get Element By Role    role=textbox
    Get Text    ${e}    ==    Prefilled Name

Get Element By Role In Frame
    Go To    ${FRAMES_URL}
    TRY
        Get Element By Role    textbox    name=right >>> name=searchbutton
    EXCEPT    TimeoutError:*    type=GLOB
        Log    Correct error.
    END

Get Element By - AltText
    ${e} =    Get Element By    AltText    Logo
    Get BoundingBox    ${e}    ALL    ==    {'x': 8, 'y': 8, 'width': 50, 'height': 50}
    ${e} =    Get Element By    AltText    logo    exact=True
    Get BoundingBox    ${e}    ALL    ==    {'x': 8, 'y': 8, 'width': 50, 'height': 50}
    ${e} =    Get Element By    AltText    /.ogo/
    Get BoundingBox    ${e}    ALL    ==    {'x': 8, 'y': 8, 'width': 50, 'height': 50}

Get Element By - Label
    ${e} =    Get Element By    Label    Name:    exact=True
    Get Text    ${e}    ==    Prefilled Name

Get Element By - Placeholder
    ${e} =    Get Element By    Placeholder    /FiLl.*hErE/i    all_elements=true
    FOR    ${el}    ${placeholder}    IN ZIP    ${e}    ${{['fill name here', 'fill email here']}}
        Get Attribute    ${el}    placeholder    ==    ${placeholder}
    END

Get Element By - TestID
    Get Element By    TestID    testid-mail
    Get Element By    TestID    testid-sms
    ${e} =    Get Element By    TestID    /testid/    all_elements=True
    Length Should Be    ${e}    2
    Set Browser Timeout    100ms    Test
    Run Keyword And Expect Error    *    Get Element By    TestID    testid-not-existing

Get Element By - Text
    Get Element By    Text    name    exact=False
    Get Element By    Text    Name:    exact=True
    Set Browser Timeout    100ms    Test
    Run Keyword And Expect Error    *    Get Element By    Text    name    exact=True

Get Element By - Title
    ${e} =    Get Element By    Title    /^name$/i
    Get Text    ${e}    ==    Prefilled Name

Get Element By In Iframe
    [Setup]    Go To    ${FRAMES_URL}
    Set Selector Prefix    id=left >>>
    ${e} =    Get Element By    Text    Search
    Get Attribute    ${e}    name    ==    searchbutton

Get Element By Role In Iframe
    [Setup]    Go To    ${FRAMES_URL}
    Set Selector Prefix    id=left >>>
    ${e} =    Get Element By Role    button    name=Search
    Get Attribute    ${e}    name    ==    searchbutton

*** Keywords ***
Element Selector Setup
    Go To    ${FORM_URL}
    Set Browser Timeout    500ms
