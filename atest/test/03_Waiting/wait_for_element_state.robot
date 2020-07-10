*** Settings ***
Resource          imports.resource
Test Setup        New Page  ${LOGIN URL}

*** Test Cases ***
Wait For Elements State to hide
    Get Attribute    button#goes_hidden    style
    Click    button#goes_hidden
    Wait For Elements State    button#goes_hidden    hidden    1s

Wait For Elements State fails on too short timeout
    Get Attribute    button#goes_hidden    style
    Click    button#goes_hidden
    Run Keyword and Expect Error    *Timeout 400ms exceeded during page.waitForSelector.*button\#goes_hidden*    Wait For Elements State    button#goes_hidden    hidden    400ms
