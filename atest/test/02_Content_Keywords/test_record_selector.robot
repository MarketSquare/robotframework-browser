*** Settings ***
Resource            imports.resource

Suite Setup         New Browser    headless=False
Suite Teardown      Close Browser

*** Test Cases ***
Finds A Selector
    [Tags]    no-mac-support    slow    no-docker-pr
    [Timeout]    2 minutes
    New Page    ${LOGIN_URL}
    ${recording} =    Promise To    record selector
    Hover    \#browser-library-selector-recorder >> h5
    Mouse Button    down
    Mouse Move Relative To    \#browser-library-selector-recorder >> h5    300    300
    Mouse Button    up
    Hover    h1
    Click    id=browser-library-select-selector
    Click    id=browser-library-selection-ok-button
    ${selector} =    Wait For    ${recording}
    Get Text    ${selector}    ==    Login Page
