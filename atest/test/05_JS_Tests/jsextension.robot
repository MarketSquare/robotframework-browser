*** Settings ***
Library      Browser    jsextension=${CURDIR}/funky.js
Library      ../../library/http_test_page.py
Resource     imports.resource

Test Tags    no-iframe

*** Test Cases ***
Plugin Routes Survive Remove All Route Rules
    [Setup]    New Context
    ${path} =    Unique HTTP Path    /api/echo/mock-plugin
    ${url} =    HTTP Page Url    ${HTTP_URL}    send=False    url=${path}
    New Page    ${url}
    Add Plugin Route    **${path}
    Mock Responses    **${path}    body=library
    Remove All Route Rules
    Click    id=send
    Get Text    id=state    ==    done
    Get Text    id=response-body    ==    plugin
    [Teardown]    Close Context

Test Lazy Playwright Loading
    [Documentation]    Tests that Playwright is loaded if jsextension is used
    ${browser_lib} =    Get Library Instance    Browser
    Should Be True    isinstance($browser_lib._playwright, Browser.playwright.Playwright)

Promise To Call Custom Js Keyword
    New Page
    ${promise} =    Promise To    My Funky keyword    h1
    Go To    ${LOGIN_URL}
    Wait For    ${promise}
    Get Text    h1    ==    Funk yeah!
