*** Settings ***
Resource          imports.resource
Test Setup        Create Page    ${LOGIN URL}

*** Test Cases ***
Click Button
    Click    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Click Nonmatching Selector
    [Setup]    Set Timeout    50ms
    Run Keyword And Expect Error    Could not find element with selector `css=notamatch` within timeout.    Click    css=notamatch
    [Teardown]    Set Timeout    ${PLAYWRIGHT TIMEOUT}
