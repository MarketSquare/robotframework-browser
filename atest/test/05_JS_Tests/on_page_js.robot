*** Settings ***
Resource          imports.resource
Suite Setup       New Browser
Test Setup        New Page    ${LOGIN_URL}
Suite Teardown    Close Browser

*** Test Cases ***
Results from page
    ${result}=    Execute JavaScript    "hello from page "+location.href
    should be equal    ${result}    hello from page http://localhost:7272/dist/
    ${result2}=    Execute JavaScript    1+2+3
    should be equal    ${result2}    ${6}
    ${result3}=    Execute JavaScript    1.3314*3.13432
    should be equal    ${result3}    ${4.173033648}

Mutate Element On Page
    Get Attribute    h1    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    h1
    Get Attribute    h1    innerText    ==    abc

Mutate Element On Page With ElementHandle
    ${ref}=    Get Element    h1
    Get Attribute    ${ref}    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    ${ref}
    Get Attribute    ${ref}    innerText    ==    abc

Highlight Element on page
    Highlight Elements    css=input#login_button    duration=100ms
    Get Element Count    .robotframework-browser-highlight    ==    1
    Sleep    100ms
    Get Element Count    .robotframework-browser-highlight    ==    0
    Highlight Elements    .pure-button    duration=200ms
    Get Element Count    .robotframework-browser-highlight    ==    5
    Sleep    400ms
    Get Element Count    .robotframework-browser-highlight    ==    0

Page state
    Get page state    validate    value['a'] == 'HELLO FROM PAGE!' and value['b'] == 123
