*** Settings ***
Resource          imports.resource
Test Setup        Open Browser To Form Page

*** Test Cases ***
Get Cookies
    ${cookies} =    Get Cookies
    Log    ${cookies}
