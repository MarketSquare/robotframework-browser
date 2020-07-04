*** Settings ***
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Get and Assert Text Simple
    Get Text    h1    ==    Login Page

Get Text
    ${h1}=    Get Text    h1
    Should Be Equal    ${h1}    Login Page

Get and Assert Attribute
    Get Attribute    h1    innerText    ==    Login Page

Get Attribute
    ${text}=    Get Attribute    h1    innerText
    Should Be Equal    ${text}    Login Page

Assert Validate
    Get Text   h1  validate  value.startswith('Login')

Closure
   ${text}=    Get Attribute    h1    innerText  then  value.replace('g', 'k')
   Should be equal     ${text}    Lokin Pake