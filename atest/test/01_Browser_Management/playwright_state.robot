*** Settings ***
Resource          imports.resource
Test Teardown     Close Browser

*** Keywords ***
Open Browser and assert Login Page
    [Arguments]    ${local_browser}
    New Browser    browser=${local_browser}    headless=${HEADLESS}
    New Page    url=${LOGIN URL}
    Get Text    h1    ==    Login Page

*** Test Cases ***
Open Firefox
    Open Browser and assert Login Page    firefox

Open Chrome
    Open Browser and assert Login Page    chromium

New Browser does not open a page
    New Browser
    Run Keyword And Expect Error    *"Tried to do playwright action 'goto', but no open page."*    Go To    ${LOGIN URL}

New Browser does not create a context
    # Use Switch context to test that no context exists here
    Pass Execution    Not Implemented yet
    [Teardown]
    Switch Context

New Context does not open a page
    New Context
    Run Keyword And Expect Error    *"Tried to do playwright action 'goto', but no open page."*    Go To    ${LOGIN URL}

Switch Browser
    Pass Execution    Not Implemented yet
    [Teardown]
    New Browser    chromium
    New Browser    firefox
    Switch Browser

Switch Context
    Pass Execution    Not Implemented yet
    [Teardown]
    New Context
    New Context
    Switch Context

New Page can create context and browser
    New Page    ${LOGIN URL}
    Get Text    h1    ==    Login Page

Focus Next Page on popup
    Open Browser and assert Login Page    chromium
    Auto Activate Pages
    Click    button#pops_up
    # FIXME: Workaround, this need is caused by eventhandlers laziness
    Sleep    1s
    Wait For Elements State    "Popped Up!"

Switch Active Page after popup
    Open Browser and assert Login Page    chromium
    Click    button#pops_up
    Switch Active Page    1
    Wait For Elements State    "Popped Up!"
    Switch Active Page    0
    Wait For Elements State    button#pops_up
