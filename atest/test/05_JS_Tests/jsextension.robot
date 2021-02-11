*** Settings ***
Library           Browser    jsextension=${CURDIR}/funky.js
Resource          imports.resource

*** Test Cases ***
Calling custom js keyword
    New Page    ${LOGIN_URL}
    get text    h1    ==    Login Page
    myFunkyKeyword    h1
    get text    h1    ==    Funk yeah!

Connecting and creating a remote browser
    ${wsEndpoint}=    Create remote browser
    ${browser}=    Connect To Browser    ${wsEndpoint}
    Should Not Be Equal    ${browser}    ${NULL}
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    [Teardown]    Close Remote Clean

Crashing keyword
    Run Keyword And Expect Error    Error: Crash    crashKeyword

*** Keywords ***
Close Remote Clean
    close browser
    closeRemoteBrowser
