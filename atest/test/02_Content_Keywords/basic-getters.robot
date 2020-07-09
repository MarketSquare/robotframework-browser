*** Settings ***
Resource          imports.resource
Suite Setup       Go To    ${LOGIN URL}

*** Variables ***
${UserNameLabel}=    label[for="username_field"]
${InputUsername}=    ${UserNameLabel} >> //.. >> input

*** Test Cases ***
Get Text
    ${h1}=    Get Text    h1
    Should Be Equal    ${h1}    Login Page

Get Text and Assert ==
    Get Text    ${UserNameLabel}    ==    User Name:

Get Text and Assert !=
    Get Text    ${UserNameLabel}    !=

Get Text Assert Validate
    Get Text    h1    validate    value.startswith('Login')

Get Attribute and Assert
    Get Attribute    h1    innerText    ==    Login Page

Get Attribute innerText
    ${innerText}=    Get Attribute    ${UserNameLabel}    innerText
    Should Be Equal    ${innerText}    User Name:

Get Attribute size
    ${size}=    Get Attribute    ${InputUsername}    type
    Should Be Equal    ${size}    text

Get Attribute and Then .. (Closure)
    ${text}=    Get Attribute    h1    innerText    then    value.replace('g', 'k')
    Should be equal    ${text}    Lokin Pake

Get Element Count
    ${count}=    Get Element Count    h1
    Should Be Equal    ${count}    1
    ${count}=    Get Element Count    label
    Should Be Equal    ${count}    2
    ${count}=    Get Element Count    not-existing
    Should Be Equal    ${count}    0

Get Element Count and Assert
    Get Element Count    h1    ==     1
    Get Element Count    label    >   1
