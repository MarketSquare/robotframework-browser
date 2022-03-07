*** Settings ***
Library     Browser    jsextension=${CURDIR}/funky.js
Resource    imports.resource

*** Test Cases ***
Calling custom js keyword
    New Page    ${LOGIN_URL}
    get text    h1    ==    Login Page
    myFunkyKeyword    h1
    get text    h1    ==    Funk yeah!

Calling new style custom js keyword
    New Page    ${LOGIN_URL}
    get text    h1    ==    Login Page
    myNewStyleFunkyKeyword    h1
    get text    h1    ==    Funk yeah again!

Calling custom js keyword with default value
    New Page    ${LOGIN_URL}
    ${val} =    withDefaultValue
    Should Be Equal    ${val}    DEFAULT
    ${val2} =    withDefaultValue    odd
    Should Be Equal    ${val2}    ODD
    ${val3} =    withDefaultValue    a=even
    Should Be Equal    ${val3}    EVEN

Connecting and creating a remote browser
    ${wsEndpoint} =    Create remote browser
    ${browser} =    Connect To Browser    ${wsEndpoint}
    Should Not Be Equal    ${browser}    ${NULL}
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    [Teardown]    Close Remote Clean

Crashing keyword
    Run Keyword And Expect Error    Error: Crash    crashKeyword

Failing import
    Run Keyword And Expect Error    Initializing library 'Browser' with arguments*    Import Library    Browser
    ...    jsextension=${CURDIR}/wrong.js

*** Keywords ***
Close Remote Clean
    close browser
    closeRemoteBrowser
