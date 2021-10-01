*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Normal Selector
    Tidii    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Normal With Strict Mode
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: "//button" resolved to 11 elements:*
    ...    Tidii    //button
    Set Strict Mode    False
    Tidii    //button
    [Teardown]    Set Strict Mode    True

Frame With Strict Mode
    Go To    ${FRAMES_URL}
    Tidii    iframe[name="left"] >>> "foo"
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: "//iframe" resolved to 2 elements:*
    ...    Tidii    //iframe >>> "foo"
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: "//input" resolved to 2 elements:*
    ...    Tidii    iframe[name="left"] >>> //input
    Set Strict Mode    False
    Tidii    //iframe >>> "foo"
    Tidii    iframe[name="left"] >>> //input
    [Teardown]    Set Strict Mode    True

Get Element And Get Elements
    ${element} =    Tidii Get Element    input#login_button
    Should Start With    ${element}    element
    ${elements} =    Tidii Get Elements    input
    Length Should Be    ${elements}    4
    FOR    ${element}    IN    @{elements}
        Should Start With    ${element}    element

    END

Click With Element ID
    ${element} =    Tidii Get Element    //tbody/tr[2]
    Run Keyword And Expect Error
    ...    TimeoutError: locator.click: Timeout 3000ms exceeded.*
    ...    Tidii    ${element} >> css=input#login_button
    Get Text    text=Login Page
    ${element} =    Tidii Get Element    //tbody/tr[3]
    Tidii    ${element} >> css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Frames With Element ID
    Go To    ${FRAMES_URL}
    ${element} =    Tidii Get Element    iframe[name="left"]
    Run Keyword And Expect Error
    ...    TimeoutError: locator.click: Timeout 3000ms exceeded.*
    ...    Tidii    ${element} >>> "foo"
