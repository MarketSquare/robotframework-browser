*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Scroll By With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Scroll By    //input
    Set Strict Mode    False
    Scroll By    //input
    [Teardown]    Set Strict Mode    True

Scroll To With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 4 elements*
    ...    Scroll To    //input
    Set Strict Mode    False
    Scroll To    //input
    [Teardown]    Set Strict Mode    True

# Scroll to corners
#    [Setup]    New Page    ${TABLES_URL}
#    Execute JavaScript    e => e.style = "width: 90vw;height: 90vh;overflow: auto;"    id=scrollable
#    Execute JavaScript    e => e.style = ""    id=scrollable
#    Scroll To    horizontal=right
#    Scroll To    horizontal=left
#    Scroll To    horizontal=left    vertical=bottom
#    Scroll To    horizontal=right    vertical=bottom
#    Get Scroll Position
#    Get Scroll Size
#    Get Scroll Position
#    Get Scroll Size
#    Scroll By    horizontal=left    vertical=bottom
#    Get Scroll Size
#    Get Scroll Position

# Scroll To Element that is visible
#    [Setup]    New Page    ${TABLES_URL}
#    [Timeout]    6000s
#    DEBUG
