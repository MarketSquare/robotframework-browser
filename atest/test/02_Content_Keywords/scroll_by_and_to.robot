*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Scroll By With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Scroll By    //input
    Set Strict Mode    False
    Scroll By    //input
    [Teardown]    Set Strict Mode    True

Scroll To With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Scroll To    //input
    Set Strict Mode    False
    Scroll To    //input
    [Teardown]    Set Strict Mode    True
