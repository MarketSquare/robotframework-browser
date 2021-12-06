*** Settings ***
Library             Browser
Resource            imports.resource

Suite Setup         New Browser    headless=False
Suite Teardown      Close Browser

*** Test Cases ***
Finds a selector
    [Timeout]    2 minutes
    New Page    ${LOGIN_URL}
    ${recording} =    promise to    record selector
    Hover    \#browser-library-selector-recorder >> h5
    mouse button    down
    mouse move relative to    \#browser-library-selector-recorder >> h5    300    300
    mouse button    up
    Hover    h1
    Click    id=browser-library-select-selector
    Click    id=browser-library-selection-ok-button
    ${selector} =    wait for    ${recording}
    get text    ${selector}    ==    Login Page
