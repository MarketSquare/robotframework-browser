*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Scroll By With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Scroll By    //input
    Set Strict Mode    False
    Scroll By    //input
    [Teardown]    Set Strict Mode    True

Scroll To With Strict
    [Tags]    slow
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Scroll To    //input
    Set Strict Mode    False
    Scroll To    //input
    [Teardown]    Set Strict Mode    True

Scroll To Elements
    [Setup]    New Page    ${TABLES_URL}
    Scroll To Element    id=table2 >> "Model"
    Check Visibility    id=table2 >> "Model"
    Scroll To Element    id=table1 >> "Model"
    Check Visibility    id=table1 >> "Model"
    Scroll To Element    id=table2
    Check Visibility    id=table2
    Scroll To Element    h2
    Check Visibility    h2
    Click    id=divscroll
    Scroll To Element    id=table2 >> "Model"
    Check Visibility    id=table2 >> "Model"
    Scroll To Element    id=table1 >> "Model"
    Check Visibility    id=table1 >> "Model"
    Scroll To Element    id=table2
    Check Visibility    id=table2
    Scroll To Element    h2
    Check Visibility    h2

Scroll To/By All
    [Setup]    New Page    ${TABLES_URL}
    Scroll To Scroll By    body
    Click    id=divscroll
    Scroll To Scroll By    id=scrollable

*** Keywords ***
Check Visibility
    [Arguments]    ${selector}
    ${s} =    Get Client Size
    Get BoundingBox    ${selector}    ALL    validate
    ...    value.x >= 0 and value.y >= 0 and value.width+value.x <= $s.width and value.height+value.y <= $s.height

Scroll To Scroll By
    [Arguments]    ${Selector}=${None}
    ${s} =    Get Scroll Size    ${Selector}
    Scroll To    ${Selector}    top    right
    Get Scroll Position    ${Selector}    ALL    validate    value.top == 0 and value.right == $s.width
    Scroll To    ${Selector}    bottom    right
    Get Scroll Position    ${Selector}    ALL    validate    value.bottom == $s.height and value.right == $s.width
    Scroll To    ${Selector}    bottom    left
    Get Scroll Position    ${Selector}    ALL    validate    value.bottom == $s.height and value.left == 0
    Scroll To    ${Selector}    top    left
    Get Scroll Position    ${Selector}    ALL    validate    value.top == 0 and value.left == 0
    Scroll To    ${Selector}    200    200
    Get Scroll Position    ${Selector}    ALL    validate    value.top == 200 and value.left == 200
    Scroll To    ${Selector}    50%    50%
    Get Scroll Position    ${Selector}    ALL    validate
    ...    value.left > 400 and value.top > 400 and value.bottom < $s.height-400 and value.right < $s.width-400
    Scroll To    ${Selector}    top    left
    Scroll By    ${Selector}    200    200
    Get Scroll Position    ${Selector}    ALL    validate    value.top == 200 and value.left == 200
    Scroll By    ${Selector}    200    200
    Get Scroll Position    ${Selector}    ALL    validate    value.top == 400 and value.left == 400
    Scroll To    ${Selector}    top    left
    Scroll By    ${Selector}    height    width
    Scroll To    ${Selector}    top    left
    Scroll By    ${Selector}    50%    50%
    Get Scroll Position    ${Selector}    ALL    validate
    ...    value.left > 400 and value.top > 400 and value.bottom < $s.height-400 and value.right < $s.width-400
