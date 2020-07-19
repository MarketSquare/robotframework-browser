*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Elements State to hide
    Get Attribute    button#goes_hidden    style
    Click    button#goes_hidden
    Wait For Elements State    button#goes_hidden    hidden    1s

Wait For Elements State fails on too short timeout
    Get Attribute    button#goes_hidden    style
    Click    button#goes_hidden
    Run Keyword and Expect Error    Could not find element with selector `button#goes_hidden` within timeout.    Wait For Elements State    button#goes_hidden    hidden    400ms

Wait For Elements State to hide with Promise
    ${promise}=  Promise to  Wait For Elements State    button#goes_hidden    hidden    1s
    Click    button#goes_hidden
    Get Attribute    button#goes_hidden    style
    Wait for  ${promise}
    Run Keyword and Expect Error    *    Get Attribute    button#goes_hidden    style