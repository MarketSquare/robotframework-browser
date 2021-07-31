*** Settings ***
Library     Browser
Resource    imports.resource

*** Test Cases ***
Finds a selector
    New Page    ${LOGIN_URL}
    ${recording}=    promise to    record selector
    Hover    h1
    Keyboard Key    press    s
    ${selector}=    wait for    ${recording}
    get text    ${selector}    ==    Login Page

Finds multiple selectors
    New page    ${LOGIN_URL}
    ${recording}=    promise to    record selector
    # Move selector screen away by mousing on it
    Hover    \#browser-library-selector-recorder
    Hover    \#username_field
    Keyboard Key    press    s
    ${username}=    wait for    ${recording}
    Should be equal    ${username}    \#username_field
    type text    ${username}    user
    ${recording}=    promise to    record selector
    Hover    \#password_field
    Keyboard Key    press    s
    ${password}=    wait for    ${recording}
    type text    ${password}    pw
    ${recording}=    promise to    record selector
    Hover    \#login_button
    Keyboard Key    press    s
    ${login_button}=    wait for    ${recording}
    click    ${login_button}
    get title    ==    Error Page
