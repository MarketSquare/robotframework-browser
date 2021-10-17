*** Settings ***
Resource            imports.resource

Suite Setup         New Browser
Suite Teardown      Close Browser
Test Setup          New Page    ${LOGIN_URL}

*** Test Cases ***
JS execute without and with element
    ${result} =    Execute JavaScript    () => {return false;}
    Should Be Equal    ${result}    ${False}
    ${result} =    Execute JavaScript    () => {return false;}    body
    Should Be Equal    ${result}    ${False}

JS Execute Without Element On Strict Mode
    ${result} =    Execute JavaScript    () => {return false;}
    Should Be Equal    ${result}    ${False}
    Set Strict Mode    False
    ${result} =    Execute JavaScript    () => {return false;}
    Should Be Equal    ${result}    ${False}
    [Teardown]    Set Strict Mode    True

JS Execute With Element On Strict Mode
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: "//input" resolved to 4 elements*
    ...    Execute JavaScript    () => {return false;}    //input
    Set Strict Mode    False
    ${result} =    Execute JavaScript    () => {return false;}    //input
    Should Be Equal    ${result}    ${False}
    [Teardown]    Set Strict Mode    True

Results from page
    ${result} =    Execute JavaScript    "hello from page "+location.href
    should be equal    ${result}    hello from page ${LOGIN_URL}
    ${result2} =    Execute JavaScript    1+2+3
    should be equal    ${result2}    ${6}
    ${result3} =    Execute JavaScript    1.3314*3.13432
    should be equal    ${result3}    ${4.173033648}

Mutate Element On Page
    Get Property    h1    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    h1
    Get Property    h1    innerText    ==    abc

Mutate Element On Page With ElementHandle
    ${ref} =    Get Element    h1
    Get Property    ${ref}    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    ${ref}
    Get Property    ${ref}    innerText    ==    abc

Highlight Element on page
    Highlight Elements    css=input#login_button    duration=200ms
    Get Element Count    .robotframework-browser-highlight    ==    1
    Sleep    200ms
    Get Element Count    .robotframework-browser-highlight    ==    0
    Set Strict Mode    False
    Highlight Elements    .pure-button    duration=200ms
    Set Strict Mode    True
    Get Element Count    .robotframework-browser-highlight    ==    5
    Sleep    400ms
    Get Element Count    .robotframework-browser-highlight    ==    0

Highlight Element With Strict
    Set Strict Mode    True
    Highlight Elements    //input    duration=200ms
    [Teardown]    Set Strict Mode    True

Highlight Element with style
    Highlight Elements    input#login_button    duration=400ms
    Get Style    .robotframework-browser-highlight    border-bottom-width    ==    2px
    Get Style    .robotframework-browser-highlight    border-bottom-style    ==    dotted
    Get Style    .robotframework-browser-highlight    border-bottom-color    ==    rgb(0, 0, 255)
    Sleep    400ms
    Highlight Elements    input#login_button    duration=400ms    width=4px    style=solid    color=\#FF00FF
    ${style} =    Get Style    .robotframework-browser-highlight
    Should Be True    "${style}[border-bottom-width]" == "4px"
    Should Be True    "${style}[border-bottom-style]" == "solid"
    Should Be True    "${style}[border-bottom-color]" == "rgb(255, 0, 255)"
    Sleep    400ms

Highlight Element with element selector
    New Page    ${LOGIN_URL}
    ${elem} =    Get Element    input#login_button
    Highlight Elements    ${elem}
    Get Element Count    .robotframework-browser-highlight    ==    1

Page state
    [Tags]    not-implemented
    #Get page state    validate    value['a'] == 'HELLO FROM PAGE!' and value['b'] == 123
