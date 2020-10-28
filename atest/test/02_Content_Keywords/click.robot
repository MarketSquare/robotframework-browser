*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Click Button
    Click    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Click Nonmatching Selector
    ${originaltimeout}=    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "css=notamatch"*    Click    css=notamatch
    [Teardown]    Set Browser Timeout    ${originaltimeout}

Click With Invalid Selector
    Run Keyword And Expect Error    STARTS: Invalid selector    Click    input[type="submit"]X
