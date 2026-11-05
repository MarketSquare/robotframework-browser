*** Settings ***
Resource       imports.resource

Suite Setup    Close Browser    ALL

*** Test Cases ***
Cookies From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Get Cookies

Cookies For Url From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Get Cookies    urls=https://a.example

Add Cookie Should Fail If Context Is Not Open
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Add Cookie    Foo    Bar    url=${ELEMENT_STATE_URL}

Delete All Cookies From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Delete All Cookies

Delete Filtered Cookies From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Delete All Cookies    name=session
