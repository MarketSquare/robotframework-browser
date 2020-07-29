*** Settings ***
Resource          imports.resource
Test Setup        Open Browser To Form Page

*** Test Cases ***
Cookies From Closed Context
    Close All Browsers
    Run Keyword And Expect Error
    ...    Tried to get cookeis but not context open.
    ...    Get Cookies

Get Cookies
    ${cookies} =    Get Cookies
    Log    ${cookies}
