*** Settings ***
Documentation     Tests for Get Element and `element=<ref>` selector syntax
Resource          imports.resource
Test Setup        New Page    ${FORM_URL}

*** Test Cases ***
Get Element
    ${ref}=    Get Element    select[name="preferred_channel"]
    ${option_value}=    Get Attribute    element=${ref} >> option    value
    Should Be Equal    ${option_value}    email

Get Element With Nonmatching child selector
    ${ref}=    Get Element    select[name="preferred_channel"]
    Run Keyword And Expect Error    Could not find element with selector `.notamatch` within timeout.
    ...    Get Attribute    element=${ref}>> .notamatch    value

Using Invalid Element Reference Fails
    Run Keyword And Expect Error    Invalid element selector `element=1234-4321`.
    ...    Click    element=1234-4321
    Run Keyword And Expect Error    No element handle found with id `1234-4321`.
    ...    Click    element=1234-4321 >> .css
