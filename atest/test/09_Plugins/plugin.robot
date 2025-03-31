*** Settings ***
Resource            ../variables.resource
Library             Browser
...                     timeout=${PLAYWRIGHT_TIMEOUT}
...                     enable_playwright_debug=${True}
...                     enable_presenter_mode=False
...                     selector_prefix=${SELECTOR_PREFIX}
...                     plugins=${CURDIR}/ExamplePlugin.py

Suite Setup         New Browser    ${BROWSER}    headless=${HEADLESS}
Test Teardown       Close Context    ALL

*** Test Cases ***
Set Message On Suite Level
    Set Last Log Message    Suite Level Message    scope=Suite

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
    [Setup]    New Page    ${FORM_URL}
    ${location} =    Get Location Object
    ${url} =    Get Url
    Should Be Equal    ${location.hostname}    localhost
    Should Be Equal    ${location.pathname}    /prefilled_email_form.html
    Should Be Equal    ${location.protocol}    http:
    Should Be Equal    ${location.href}    ${FORM_URL}

Check Plugin Suite Scope Setting 1
    [Documentation]
    ...    LOG 1:3    INFO    Suite Level Message
    ...    LOG 2:3    INFO    Suite Level Message
    Log    Test
    Log    Hello

Set And Check Plugin Scope Setting
    [Documentation]
    ...    LOG 1:2    INFO    Hello World
    ...    LOG 2:2    INFO    Test
    ...    LOG 2:3    INFO    Hello World
    ...    LOG 3:2    INFO    Hello
    ...    LOG 3:3    INFO    Hello World
    Set Last Log Message    Hello World    scope=Test
    Log    Test
    Log    Hello

Check Plugin Suite Scope Setting 2
    [Documentation]
    ...    LOG 1:3    INFO    Suite Level Message
    ...    LOG 1:3    INFO    Suite Level Message
    Log    Test
    Log    Hello
