*** Settings ***
Library  Browser

*** Test Cases ***
Open and Close a Chrome Browser
   Open Browser		Chrome
   Close Browser

Open Browser to URL
   Open Browser		Chrome    http://localhost:7272
   ${url}=    Get URL
   Should Be Equal    ${url}    http://localhost:7272/
   Close Browser
