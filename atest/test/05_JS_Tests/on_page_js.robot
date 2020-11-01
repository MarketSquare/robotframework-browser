*** Settings ***
Resource          imports.resource
Suite Setup       New Browser
Test Setup        New Page    ${LOGIN_URL}
Suite Teardown    Close Browser

*** Test Cases ***
Results from page
    ${result}=    Execute JavaScript    "hello from page "+location.href
    should be equal    ${result}    hello from page ${LOGIN_URL}
    ${result2}=    Execute JavaScript    1+2+3
    should be equal    ${result2}    ${6}
    ${result3}=    Execute JavaScript    1.3314*3.13432
    should be equal    ${result3}    ${4.173033648}

Mutate Element On Page
    Get Property    h1    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    h1
    Get Property    h1    innerText    ==    abc

Mutate Element On Page With ElementHandle
    ${ref}=    Get Element    h1
    Get Property    ${ref}    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    ${ref}
    Get Property    ${ref}    innerText    ==    abc

Highlight Element on page
    Highlight Elements    css=input#login_button    duration=100ms
    Get Element Count    .robotframework-browser-highlight    ==    1
    Sleep    100ms
    Get Element Count    .robotframework-browser-highlight    ==    0
    Highlight Elements    .pure-button    duration=200ms
    Get Element Count    .robotframework-browser-highlight    ==    5
    Sleep    400ms
    Get Element Count    .robotframework-browser-highlight    ==    0

Highlight Element with style
    Highlight Elements    input#login_button    duration=200ms
    Get Style    .robotframework-browser-highlight    border-bottom-width    ==    2px
    Get Style    .robotframework-browser-highlight    border-bottom-style    ==    dotted
    Get Style    .robotframework-browser-highlight    border-bottom-color    ==    rgb(0, 0, 255)
    Sleep    200ms
    Highlight Elements    input#login_button    duration=100ms    width=4px    style=solid    color=\#FF00FF
    ${style}=    Get Style    .robotframework-browser-highlight
    Should Be True    "${style}[border-bottom-width]" == "4px"
    Should Be True    "${style}[border-bottom-style]" == "solid"
    Should Be True    "${style}[border-bottom-color]" == "rgb(255, 0, 255)"
    Sleep    100ms

Page state
    [Tags]    Not-Implemented
    #Get page state    validate    value['a'] == 'HELLO FROM PAGE!' and value['b'] == 123
