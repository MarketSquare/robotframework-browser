*** Settings ***
Resource            imports.resource

Suite Setup         Ensure Open Browser
Test Setup          New Page    ${FORM_URL}
Test Teardown       Close Context    ALL

*** Test Cases ***
Pluging Keyword Example
    ${url} =    Get Url
    Add Cookie
    ...    Foo22
    ...    Bar22
    ...    url=${url}
    ...    expires=3 155 760 000,195223
    ${cookies} =    New Plugin Cookie Keyword
    Should Not Be Empty    ${cookies}
    Should Be Equal    ${cookies}[name]    Foo22
    Should Be Equal    ${cookies}[value]    Bar22
    Add Cookie
    ...    Foo11
    ...    Bar11
    ...    url=${url}
    ...    expires=3 155 760 000,195223
    Run Keyword And Expect Error
    ...    Too many cookies.
    ...    New Plugin Cookie Keyword
