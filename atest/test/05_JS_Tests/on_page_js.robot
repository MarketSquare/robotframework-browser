*** Settings ***
Resource            imports.resource

Suite Setup         New Browser    headless=${HEADLESS}
Suite Teardown      Close Browser
Test Setup          New Page    ${LOGIN_URL}

*** Test Cases ***
JS Execute Without And With Element
    ${result} =    Evaluate JavaScript    ${None}    () => {return false;}
    Should Be Equal    ${result}    ${False}
    ${result} =    Evaluate JavaScript    body    () => {return false;}
    Should Be Equal    ${result}    ${False}

Evaluate Multiline JavaScript With Array
    ${texts} =    Evaluate JavaScript    button
    ...    (elements, arg) => {
    ...    let text = []
    ...    for (e of elements) {
    ...    console.log(e.innerText)
    ...    text.push(e.innerText)
    ...    }
    ...    text.push(arg)
    ...    return text
    ...    }
    ...    all_elements=True
    ...    arg=${{[1,2,3]}}
    Length Should Be    ${texts}    16
    Should Be Equal    ${texts}[-1]    ${{[1,2,3]}}

Evaluate Multiline JavaScript With Singel Element
    ${texts} =    Evaluate JavaScript    button >> nth=0
    ...    (e, arg) => {
    ...    let text = []
    ...    console.log(e.innerText)
    ...    text.push(e.innerText)
    ...    text.push(arg)
    ...    return text
    ...    }
    ...    arg=Hello World
    Length Should Be    ${texts}    2
    Should Be Equal    ${texts}[-1]    Hello World

Evaluate Multiline JavaScript With Strict Mode Disabled And All Elements
    ${org} =    Set Strict Mode    False
    ${length} =    Evaluate JavaScript    button
    ...    (elements) => {
    ...    return elements.length
    ...    }
    ...    all_elements=True
    Should Be Equal    ${length}    ${15}
    [Teardown]    Set Strict Mode    ${org}

Evaluate Multiline JavaScript With Strict Mode Enabled And All Elements
    ${org} =    Set Strict Mode    True
    ${length} =    Evaluate JavaScript    button
    ...    (elements) => {
    ...    return elements.length
    ...    }
    ...    all_elements=True
    Should Be Equal    ${length}    ${15}
    [Teardown]    Set Strict Mode    ${org}

Evaluate Multiline JavaScript With Strict Mode Disabled And Single Element
    ${org} =    Set Strict Mode    False
    ${text} =    Evaluate JavaScript    button
    ...    (e) => {
    ...    return e.innerText
    ...    }
    Should Be Equal    ${text}    Visible
    [Teardown]    Set Strict Mode    ${org}

Evaluate Multiline JavaScript Strict Mode Error
    Run Keyword And Expect Error
    ...    *strict mode violation*input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Evaluate JavaScript    input
    ...    (e, arg) => {
    ...    let text = []
    ...    console.log(e.innerText)
    ...    text.push(e.innerText)
    ...    text.push(arg)
    ...    return text
    ...    }
    ...    arg=Hello World

Evaluate Multiline JavaScript On Page
    [Tags]    no-iframe
    ${arg} =    Create Dictionary    selector=input#login_button    text=-APPENDIX
    ${texts} =    Evaluate JavaScript    ${NONE}
    ...    (arg) => {
    ...    e = document.querySelector(arg.selector);
    ...    return e.nodeName + arg.text
    ...    }
    ...    arg=${arg}
    Should Be Equal    ${texts}    INPUT-APPENDIX

JS Execute Without Element On Strict Mode
    ${result} =    Evaluate JavaScript    ${None}    () => {return false;}
    Should Be Equal    ${result}    ${False}
    Set Strict Mode    False
    ${result} =    Evaluate JavaScript    ${None}    () => {return false;}
    Should Be Equal    ${result}    ${False}
    [Teardown]    Set Strict Mode    True

JS Execute With Element On Strict Mode
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Evaluate JavaScript    //input    () => {return false;}
    Set Strict Mode    False
    ${result} =    Evaluate JavaScript    //input    () => {return false;}
    Should Be Equal    ${result}    ${False}
    [Teardown]    Set Strict Mode    True

Results From Page
    ${result} =    Evaluate JavaScript    ${None}    "hello from page "+location.href
    Should Be Equal    ${result}    hello from page ${LOGIN_URL}
    ${result2} =    Evaluate JavaScript    ${None}    1+2+3
    Should Be Equal    ${result2}    ${6}
    ${result3} =    Evaluate JavaScript    ${None}    1.3314*3.13432
    Should Be Equal    ${result3}    ${4.173033648}

Mutate Element On Page
    Get Property    h1    innerText    ==    Login Page
    Evaluate JavaScript    h1    (elem) => elem.innerText = "abc"
    Get Property    h1    innerText    ==    abc

Mutate Element On Page With ElementHandle
    ${ref} =    Get Element    h1
    Get Property    ${ref}    innerText    ==    Login Page
    Evaluate JavaScript    ${ref}    (elem) => elem.innerText = "abc"
    Get Property    ${ref}    innerText    ==    abc

Highlight Element On Page
    [Tags]    slow
    Highlight Elements    css=input#login_button    duration=200ms
    Get Element Count    .robotframework-browser-highlight    ==    1
    Sleep    200ms
    Get Element Count    .robotframework-browser-highlight    ==    0
    Set Strict Mode    False
    ${count} =    Highlight Elements    .pure-button    duration=1000ms
    Set Strict Mode    True
    Get Element Count    .robotframework-browser-highlight    ==    5
    Should Be Equal    ${count}    ${5}
    Sleep    1500ms
    Get Element Count    .robotframework-browser-highlight    ==    0

Highlight Element With Invalid Selector
    Highlight Elements    %inva$id[Unparse//elem    duration=200ms
    Sleep    100ms
    Get Element Count    .robotframework-browser-highlight    ==    0

Highlight Element With Strict
    Set Strict Mode    True
    Highlight Elements    //input    duration=200ms
    [Teardown]    Set Strict Mode    True

Highlight Element With Style
    [Tags]    slow
    Set Retry Assertions For    200ms    scope=Test
    ${bbox} =    Get Bounding Box    input#login_button
    Highlight Elements    input#login_button    duration=500ms
    ${bbox_highlight} =    Run Keyword And Continue On Failure
    ...    Get Bounding Box
    ...    .robotframework-browser-highlight
    ...    ALL
    ...    validate
    ...    value.x + 2 == $bbox.x and value.y + 2 == $bbox.y and value.width - 4 == $bbox.width and value.height - 4 == $bbox.height
    Get Style    .robotframework-browser-highlight    border-bottom-width    ==    2px
    Get Style    .robotframework-browser-highlight    border-bottom-style    ==    dotted
    Get Style    .robotframework-browser-highlight    border-bottom-color    ==    rgb(0, 0, 255)
    Sleep    600ms
    Highlight Elements    input#login_button    duration=500ms    width=4px    style=solid    color=\#FF00FF
    Add Style Tag    * {box-sizing: border-box;}
    ${style} =    Get Style    .robotframework-browser-highlight
    ${bbox_highlight} =    Run Keyword And Continue On Failure
    ...    Get Bounding Box
    ...    .robotframework-browser-highlight
    ...    ALL
    ...    validate
    ...    value.x + 4 == $bbox.x and value.y + 4 == $bbox.y and value.width - 8 == $bbox.width and value.height - 8 == $bbox.height
    Should Be True    "${style}[border-bottom-width]" == "4px"
    Should Be True    "${style}[border-bottom-style]" == "solid"
    Should Be True    "${style}[border-bottom-color]" == "rgb(255, 0, 255)"
    Sleep    600ms

Highlight Element With Element Selector
    New Page    ${LOGIN_URL}
    ${elem} =    Get Element    input#login_button
    Highlight Elements    ${elem}
    Get Element Count    .robotframework-browser-highlight    ==    1

Page State
    [Tags]    not-implemented
    Log    Is that art???
    # Get page state    validate    value['a'] == 'HELLO FROM PAGE!' and value['b'] == 123
