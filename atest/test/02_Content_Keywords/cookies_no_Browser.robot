*** Settings ***
Resource        imports.resource

Suite Setup     Close Browser    ALL

*** Test Cases ***
Cookies From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Get Cookies

Add Cookie Should Fail If Context Is Not Open
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Add Cookie    Foo    Bar    url=${ELEMENT_STATE_URL}

Delete All Cookies From Closed Context
    Run Keyword And Expect Error
    ...    Error: no open context.
    ...    Delete All Cookies
