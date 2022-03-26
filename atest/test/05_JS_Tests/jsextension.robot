*** Settings ***
Library     Browser    jsextension=${CURDIR}/funky.js
Resource    imports.resource

*** Test Cases ***
Calling custom js keyword
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    MyFunkyKeyword    h1
    Get Text    h1    ==    Funk yeah!

Calling new style custom js keyword
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    MyNewStyleFunkyKeyword    h1
    Get Text    h1    ==    Funk yeah again!

Calling custom js keyword with default value
    New Page    ${LOGIN_URL}
    ${val} =    WithDefaultValue
    Should Be Equal    ${val}    DEFAULT
    ${val2} =    WithDefaultValue    odd
    Should Be Equal    ${val2}    ODD
    ${val3} =    WithDefaultValue    a=even
    Should Be Equal    ${val3}    EVEN

Connecting and creating a remote browser
    [Tags]    slow
    ${wsEndpoint} =    Create Remote Browser
    ${browser} =    Connect To Browser    ${wsEndpoint}
    Should Not Be Equal    ${browser}    ${NULL}
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    [Teardown]    Close Remote Clean

Defaults in the keyword from Python to JS and back
    ${result} =    moreDefaults
    Should Be Equal    ${result}[bTrue]    ${TRUE}
    Should Be Equal    ${result}[bFalse]    ${FALSE}
    Should Be Equal    ${result}[integer]    ${123}
    Should Be Equal    ${result}[floater]    ${1.3}
    Should Be Equal    ${result}[text]    hello
    Should Be Equal    ${result}[nothing]    ${NONE}
    ${result} =    moreDefaults    bFalse=${TRUE}
    Should Be Equal    ${result}[bFalse]    ${TRUE}
    ${result} =    moreDefaults    bTrue=${FALSE}
    Should Be Equal    ${result}[bTrue]    ${FALSE}
    ${result} =    moreDefaults    integer=${456}
    Should Be Equal    ${result}[integer]    ${456}
    ${result} =    moreDefaults    floater=${2.3}
    Should Be Equal    ${result}[floater]    ${2.3}
    ${result} =    moreDefaults    text=bye
    Should Be Equal    ${result}[text]    bye
    ${result} =    moreDefaults    nothing=${NONE}
    Should Be Equal    ${result}[nothing]    ${NONE}

Crashing keyword
    Run Keyword And Expect Error    Error: Crash    crashKeyword

Failing import
    Run Keyword And Expect Error    Initializing library 'Browser' with arguments*    Import Library    Browser
    ...    jsextension=${CURDIR}/wrong.js

*** Keywords ***
Close Remote Clean
    Close Browser
    CloseRemoteBrowser
