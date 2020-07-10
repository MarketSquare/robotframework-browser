*** Settings ***
Resource          imports.resource

*** Keywords ***
Open Browser and assert Login Page
    [Arguments]    ${local_browser}
    New Browser    browser=${local_browser}    headless=${HEADLESS}
    New Page    url=${LOGIN URL}
    Get Text    h1    ==    Login Page
    [Teardown]    Close Browser

*** Test Cases ***
Open Firefox
    Run Keyword if    str($BROWSER).lower() != "Firefox"
    ...    Open Browser and assert Login Page    firefox
    ...    ELSE
    ...    Pass Execution    Firefox was already opened

Open Chrome
    Run Keyword if    str($BROWSER).lower() != "chromium"
    ...    Open Browser and assert Login Page    chromium
    ...    ELSE
    ...    Pass Execution    Chrome was already opened

Create New Context
    New Context

New Page implicitly opens browser
    New Page    ${LOGIN URL}

Focus Next Page on popup
    Auto Activate Pages
    Click    button#pops_up
    # FIXME: Workaround, this need is caused by eventhandlers laziness
    Sleep    1s
    Wait For Elements State    "Popped Up!"

Switch Active Page after popup
    Click    button#pops_up
    Switch Active Page    1
    Wait For Elements State    "Popped Up!"
    Switch Active Page    0
    Wait For Elements State    button#pops_up
