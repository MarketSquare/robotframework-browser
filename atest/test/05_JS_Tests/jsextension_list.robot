*** Settings ***
Library         Browser    jsextension=${js_plugins}
Resource        imports.resource

Force Tags      no-iframe

*** Variables ***
@{js_plugins} =     ${CURDIR}/funky.js    ${CURDIR}/another.js

*** Test Cases ***
Promise To Call Custom Js Keyword
    New Page
    ${promise} =    Promise To    My Funky keyword    h1
    Go To    ${LOGIN_URL}
    Wait For    ${promise}
    Get Text    h1    ==    Funk yeah!

Calling Custom Js Keyword
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    MyFunkyKeyword    h1
    Get Text    h1    ==    Funk yeah!

Calling New Style Custom Js Keyword
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    MyNewStyleFunkyKeyword    h1
    Get Text    h1    ==    Funk yeah again!

Calling Custom Js Keyword With Default Value
    New Page    ${LOGIN_URL}
    ${val} =    WithDefaultValue
    Should Be Equal    ${val}    DEFAULT
    ${val2} =    WithDefaultValue    odd
    Should Be Equal    ${val2}    ODD
    ${val3} =    WithDefaultValue    a=even
    Should Be Equal    ${val3}    EVEN

Connecting And Creating A Remote Browser
    [Tags]    slow    no-docker-pr
    ${wsEndpoint} =    Create Remote Browser
    ${browser} =    Connect To Browser    ${wsEndpoint}
    Should Not Be Equal    ${browser}    ${NULL}
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page
    [Teardown]    Close Remote Clean

Defaults In The Keyword From Python To JS And Back
    [Tags]    no-docker-pr
    ${result} =    MoreDefaults
    Should Be Equal    ${result}[bTrue]    ${TRUE}
    Should Be Equal    ${result}[bFalse]    ${FALSE}
    Should Be Equal    ${result}[integer]    ${123}
    Should Be Equal    ${result}[floater]    ${1.3}
    Should Be Equal    ${result}[text]    hello
    Should Be Equal    ${result}[nothing]    ${NONE}
    Should Be Equal    ${result}[undefineder]    ${NONE}
    ${result2} =    MoreDefaults    bFalse=${TRUE}
    Should Be Equal    ${result2}[bFalse]    ${TRUE}
    ${result3} =    MoreDefaults    bTrue=${FALSE}
    Should Be Equal    ${result3}[bTrue]    ${FALSE}
    ${result4} =    MoreDefaults    integer=${456}
    Should Be Equal    ${result4}[integer]    ${456}
    ${result5} =    MoreDefaults    floater=${2.3}
    Should Be Equal    ${result5}[floater]    ${2.3}
    ${result6} =    MoreDefaults    text=bye
    Should Be Equal    ${result6}[text]    bye
    ${result7} =    MoreDefaults    nothing=${NONE}
    Should Be Equal    ${result7}[nothing]    ${NONE}
    ${result8} =    MoreDefaults    undefineder=${NONE}
    Should Be Equal    ${result8}[undefineder]    ${NONE}

Crashing Keyword
    [Tags]    no-docker-pr
    Run Keyword And Expect Error    Error: Crash    CrashKeyword

Failing Import
    Run Keyword And Expect Error    Initializing library 'Browser' with arguments*    Import Library    Browser
    ...    jsextension=${CURDIR}/wrong.js

List Imports
    [Tags]    no-docker-pr
    ${r} =    My Other Keyword    test
    Should Be Equal    ${r}    test

Using Context And Browser In Custom Js Keyword
    New Browser    chromium
    New Context    viewport={'width': 1920, 'height': 1080}
    New Page    ${LOGIN_URL}
    ${result} =    Context And Browser Demo    Testing context and browser access
    Should Be Equal    ${result}[message]    Testing context and browser access
    Should Be Equal    ${result}[browserType]    chromium
    Should Be Equal As Numbers    ${result}[pageCount]    ${1}
    # Create another page to verify pageCount changes
    New Page    ${LOGIN_URL}
    ${result2} =    Context And Browser Demo    Checking with two pages
    Should Be Equal As Numbers    ${result2}[pageCount]    ${2}

*** Keywords ***
Close Remote Clean
    Close Browser
    CloseRemoteBrowser
