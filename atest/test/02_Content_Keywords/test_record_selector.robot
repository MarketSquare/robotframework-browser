*** Settings ***
Library             Browser
Resource            imports.resource

Suite Setup         New Browser    headless=False
Suite Teardown      Close Browser

*** Test Cases ***
Finds a selector
    New Page    ${LOGIN_URL}
    ${recording} =    promise to    record selector
    Hover    h1
    Click    id=browser-library-select-selector
    ${selector} =    wait for    ${recording}
    get text    ${selector}    ==    Login Page

Finds multiple selectors
    New Page    ${LOGIN_URL}
    ${recording} =    promise to    record selector
    # Move selector screen away by dragging it
    Hover    \#browser-library-selector-recorder >> h5
    mouse button    down
    mouse move relative to    \#browser-library-selector-recorder >> h5    300    300
    mouse button    up
    Hover    \#username_field
    Click    id=browser-library-select-selector
    ${username} =    wait for    ${recording}
    Should be equal    ${username}    \#username_field
    type text    ${username}    user
    ${recording} =    promise to    record selector
    Hover    \#browser-library-selector-recorder >> h5
    mouse button    down
    mouse move relative to    \#browser-library-selector-recorder >> h5    300    300
    mouse button    up
    Hover    \#password_field
    Click    id=browser-library-select-selector
    ${password} =    wait for    ${recording}
    type text    ${password}    pw
    ${recording} =    promise to    record selector
    Hover    \#browser-library-selector-recorder >> h5
    mouse button    down
    mouse move relative to    \#browser-library-selector-recorder >> h5    300    300
    mouse button    up
    Hover    \#login_button
    Click    id=browser-library-select-selector
    ${login_button} =    wait for    ${recording}
    click    ${login_button}
    get title    ==    Error Page
