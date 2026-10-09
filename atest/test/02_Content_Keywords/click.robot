*** Settings ***
Resource       imports.resource

Suite Setup    New Browser    ${BROWSER}    headless=${HEADLESS}
Test Setup     Ensure Open Page    ${LOGIN_URL}

*** Test Cases ***
Click Button
    Click    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Click Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms    scope=Test
    Run Keyword And Expect Error
    ...    *Error: locator.click: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Click    css=notamatch

Click With Invalid Selector
    Run Keyword And Expect Error
    ...    *input?type="submit"?X' is not a valid selector.*
    ...    Click
    ...    input[type="submit"]X
