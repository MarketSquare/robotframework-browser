*** Settings ***
Library           Browser    jsextension=${CURDIR}/funky.js
Resource          imports.resource

*** Test Cases ***
Calling custom js keyword
    New Page    ${LOGIN_URL}
    get text    h1    ==    Login Page
    myFunkyKeyword    h1
    get text    h1    ==    Funk yeah!
