*** Settings ***
Resource          Keywords.resource

*** Test Cases ***
Open and Close a Chromium Browser
    Open Browser    browser=Chromium
    Close Browser

Open and Close a Firefox Browser
    Open Browser    browser=firefox
    Close Browser

Open Browser to URL
    Open Browser    ${LOGIN URL}
    Get URL    ==    ${LOGIN URL}
    Close Browser
