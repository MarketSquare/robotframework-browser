*** Settings ***
Resource          imports.resource

*** Keywords ***
Open Browser and assert Login Page
    [Arguments]    ${local_browser}
    Open Browser    url=${LOGIN URL}    browser=${local_browser}    headless=${HEADLESS}
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
