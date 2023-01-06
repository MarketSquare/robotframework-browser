*** Settings ***
Library             Browser    plugins=${CURDIR}/ExamplePlugin.py
Test Setup          New Page    https://www.google.com/

*** Test Cases ***
Example
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
