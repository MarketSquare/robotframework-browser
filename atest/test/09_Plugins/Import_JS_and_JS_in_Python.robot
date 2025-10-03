*** Settings ***
Resource            ../variables.resource
Library             Browser
...                     timeout=${PLAYWRIGHT_TIMEOUT}
...                     enable_playwright_debug=${True}
...                     enable_presenter_mode=False
...                     selector_prefix=${SELECTOR_PREFIX}
...                     jsextension=${CURDIR}/../05_JS_Tests/funky.js
...                     plugins=${CURDIR}/ExamplePlugin.py

Suite Setup         New Browser    ${BROWSER}    headless=${HEADLESS}
Test Teardown       Close Context    ALL

Test Tags           no-iframe

*** Test Cases ***
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

Pluging Keyword Example
    [Setup]    New Page    ${FORM_URL}
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

Test Js Plugin Called From Python Plugin
    [Setup]    New Page    ${TABLES_URL}
    Mouse Wheel    0    100
    Get Scroll Position    ${None}    top    ==    100
    Mouse Wheel    50    100
    Get Scroll Position    ${None}    top    ==    200
    Get Scroll Position    ${None}    left    ==    50
    Mouse Wheel    -20    -150
    Get Scroll Position    ${None}    top    ==    50
    Get Scroll Position    ${None}    left    ==    30

Pluging Keyword Example Location
    [Tags]    no-docker-pr
    [Setup]    New Page    ${FORM_URL}
    ${location} =    Get Location Object
    ${url} =    Get Url
    Should Be Equal    ${location.hostname}    localhost
    Should Be Equal    ${location.pathname}    /prefilled_email_form.html
    Should Be Equal    ${location.protocol}    http:
    Should Be Equal    ${location.href}    ${FORM_URL}

*** Keywords ***
Close Remote Clean
    Close Browser
    CloseRemoteBrowser
