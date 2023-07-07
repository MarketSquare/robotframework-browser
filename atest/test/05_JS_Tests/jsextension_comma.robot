*** Settings ***
Library         Browser    jsextension=${CURDIR}/funky.js,${CURDIR}/another.js
Resource        imports.resource

Force Tags      no-iframe

*** Test Cases ***
Calling Custom Js Keyword
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    MyFunkyKeyword    h1
    Get Text    h1    ==    Funk yeah!

List Imports
    ${r} =    My Other Keyword    test
    Should Be Equal    ${r}    test
