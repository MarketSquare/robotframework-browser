*** Settings ***
Documentation     Tests for Get Element and `element=<ref>` selector syntax
Resource          imports.resource
Library           Collections
Test Setup        New Page    ${FORM_URL}

*** Test Cases ***
Get Element
    ${ref}=    Get Element    select[name="preferred_channel"]
    ${option_value}=    Get Attribute    ${ref} >> option    value
    Should Be Equal    ${option_value}    email

Get Element With Nonmatching child selector
    ${ref}=    Get Element    select[name="preferred_channel"]
    Run Keyword And Expect Error    Could not find element with selector `.notamatch` within timeout.
    ...    Get Attribute    ${ref}>> .notamatch    value

Using Invalid Element Reference Fails
    Run Keyword And Expect Error    Invalid element selector `element=1234-4321`.
    ...    Click    element=1234-4321
    Run Keyword And Expect Error    No element handle found with id `1234-4321`.
    ...    Click    element=1234-4321 >> .css

Get Element From Frame
    [Setup]    New Page    ${FRAMES_URL}
    ${ref}=    Get Element    body >> [src="left.html"] >>> body
    Get Attribute    ${ref} >> //input[@name="searchbutton"]    value    ==    Search

Get Elements when only 1 match
    ${refs}=    Get Elements    select[name="preferred_channel"]
    ${ref}=    Get From List    ${refs}    0
    ${option_value}=    Get Attribute    ${ref} >> option    value
    Should Be Equal    ${option_value}    email

Get And Match list of elements
    ${refs}=    Get Elements    input
    Should Be Equal As Integers    12    ${{len(${refs})}}
