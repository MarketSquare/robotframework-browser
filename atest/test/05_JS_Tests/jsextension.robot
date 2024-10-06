*** Settings ***
Library         Browser    jsextension=${CURDIR}/funky.js
Resource        imports.resource

Force Tags      no-iframe

*** Test Cases ***
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
