*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Add Style
    [Tags]    no-iframe
    Add Style Tag    \#username_field:focus {background-color: aqua;}
    Focus    \#username_field
    Get Style    \#username_field    background-color    ==    rgb(0, 255, 255)

Focus With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to ${INPUT_ELEMENT_COUNT_IN_LOGIN} elements*
    ...    Focus    //input
    Set Strict Mode    False
    Focus    //input
    [Teardown]    Set Strict Mode    True
