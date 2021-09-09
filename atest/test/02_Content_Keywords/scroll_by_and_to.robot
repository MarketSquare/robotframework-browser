*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Scroll By With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Scroll By    //input
    Scroll By    //input    strict=False

Scroll To With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 4 elements.*
    ...    Scroll To    //input
    Scroll To    //input    strict=False
