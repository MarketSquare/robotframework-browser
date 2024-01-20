*** Settings ***
Resource            imports.resource

Suite Setup         Setup Keyword
Suite Teardown      Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}
Test Setup          Ensure Open Page    ${LOGIN_URL}

*** Test Cases ***
Normal Selector
    Click    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Normal With Strict Mode
    Run Keyword And Expect Error
    ...    *strict mode violation*//button*resolved to 11 elements:*
    ...    Click    //button
    Set Strict Mode    False
    Click    //button
    [Teardown]    Set Strict Mode    True

Frame With Strict Mode
    [Setup]    Go To    ${FRAMES_URL}
    Click    iframe[name="left"] >>> "foo"
    Run Keyword And Expect Error
    ...    *strict mode violation*//iframe*resolved to 2 elements:*
    ...    Click    //iframe >>> "foo"
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 2 elements:*
    ...    Click    iframe[name="left"] >>> //input
    Set Strict Mode    False
    Click    //iframe >>> "foo"
    Click    iframe[name="left"] >>> //input
    [Teardown]    Set Strict Mode    True

Nested Frame With Strict Mode
    [Setup]    Go To    ${DEEP_FRAMES_URL}
    Click    id=b >>> id=c >>> id=cc
    ${element} =    Get Element    id=b >>> id=c >>> id=cc
    Should Start With    ${element}    id
    ${elements} =    Get Elements    id=b >>> id=c >>> id=cc
    Length Should Be    ${elements}    1

Get Element And Get Elements
    ${element} =    Get Element    input#login_button
    Should Start With    ${element}    input
    ${elements} =    Get Elements    input
    Length Should Be    ${elements}    4
    FOR    ${element}    IN    @{elements}
        Should Start With    ${element}    input
    END

Click With Element ID
    ${element} =    Get Element    //tbody/tr[2] >> nth=0
    ${Timeout} =    Set Browser Timeout    200ms
    TRY
        Click    ${element} >> css=input#login_button
    EXCEPT    TimeoutError: locator.click: Timeout 200ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    Set Browser Timeout    ${Timeout}
    Get Text    text=Login Page
    ${element} =    Get Element    //tbody/tr[3] >> nth=0
    Click    ${element} >> css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Frames With Element ID
    [Setup]    Go To    ${FRAMES_URL}
    ${element} =    Get Element    iframe[name="left"]
    Click    ${element} >>> "foo"
    Get Text    iframe[name="right"] >>> body    ==    You're looking at foo.

Get Element Count In IFrame
    [Setup]    Go To    ${FRAMES_URL}
    Get Element Count    iframe[name="left"] >>> //input    ==    2

Get Element Should Wait For Attached State
    [Setup]    Go To    ${WAIT_URL}
    Select Options By    \#dropdown    value    True    attached
    Click With Options    \#submit    noWaitAfter=True
    ${locator} =    Get Element    id=victim
    Should Not Be Empty    ${locator}

*** Keywords ***
Setup Keyword
    Set Browser Timeout    3 seconds
    Ensure Open Page
