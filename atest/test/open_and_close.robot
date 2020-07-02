*** Settings ***
Library           Browser

*** Test Cases ***
Open and Close a Chromium Browser
    Open Browser    browser=Chromium
    Close Browser

Open and Close a Firefox Browser
    Open Browser    browser=firefox
    Close Browser

Open Browser to URL
    Open Browser    http://localhost:7272
    Get URL    ==    http://localhost:7272/
    Close Browser
