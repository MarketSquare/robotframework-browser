*** Settings ***
Library  Browser

*** Test Cases ***
Open and Close a Chrome Browser
   Open Browser		browser=Chrome
   Close Browser

Open and Close a Firefox Browser
    Open Browser	browser=firefox
    Close Browser

Open and Close a WebKit Browser
    Open Browser	browser=webkit
    Close Browser

Open Browser to URL
   Open Browser		http://localhost:7272
   ${url}=    Get URL
   Should Be Equal    ${url}    http://localhost:7272/
   Close Browser
