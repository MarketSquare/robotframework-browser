*** Settings ***
Documentation       Tests for Get Element and `element=<ref>` selector syntax

Resource            imports.resource

Test Setup          New Page    ${FORM_URL}

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
    Should Start With    ${element}    element=
    [Teardown]    Set Strict Mode    True

Get Element With Nonmatching child selector
    ${ref} =    Get Element    select[name="preferred_channel"]
    Run Keyword And Expect Error    *TimeoutError: locator.elementHandle: Timeout 3000ms exceeded.*
    ...    Get Property    ${ref}>> .notamatch    value

Using Invalid Element Reference Fails
    Run Keyword And Expect Error
    ...    Error: No locator handle found with "1234-4321".
    ...    Click    element=1234-4321
    Run Keyword And Expect Error
    ...    Error: No locator handle found with "1234-4321".
    ...    Click    element=1234-4321 >> .css

Get Element From Frame
    [Setup]    New Page    ${FRAMES_URL}
    ${ref} =    Get Element    body >> [src="left.html"] >>> body
    Get Property    ${ref} >> //input[@name="searchbutton"]    value    ==    Search

Using Element Handle directly as selector
    New Page    ${LOGIN_URL}
    ${login_btn} =    Get Element    input#login_button
    Click    ${login_btn}
    Get Text    text=Login failed. Invalid user name and/or password.

Get Elements when only 1 match
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
    ${refs} =    Get Elements    xpath=//not_here
    Should Be Empty    ${refs}

Get Elements Should Fail With Invalid Selector
    Run Keyword And Expect Error
    ...    * Unknown engine "invalid" *
    ...    Get Elements    invalid=//foobar

Get Element and Click
    New Page    ${LOGIN_URL}
    ${refs} =    Get Elements    .pure-button
    Should Be Equal As Numbers    ${{ len(${refs}) }}    5
    FOR    ${elem}    IN    @{refs}
        Click    ${elem}
    END
