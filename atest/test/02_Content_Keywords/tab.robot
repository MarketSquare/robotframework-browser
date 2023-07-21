*** Settings ***
Resource    imports.resource

*** Test Cases ***
Tab Button Without hasTouch
    [Setup]    Open Page With Touch Not Enabled
    TRY
        Tap    css=input#login_button
    EXCEPT    *locator.tap*hasTouch context option to enable touch support*    type=GLOB    AS    ${error}
        Log    Corrent error: ${error}
    END

Tab Button
    [Setup]    Open Page With Touch Enabled
    Tap    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.

Tab Button With Trial
    [Setup]    Open Page With Touch Enabled
    Tap    css=input#login_button    trial=True
    Get Text    text=Please input your user name and password and click the login button.

Tab Button With Options
    [Setup]    Open Page With Touch Enabled
    Tap    css=input#login_button    force=True    noWaitAfter=True    position_x=3    position_y=4
    Get Text    text=Login failed. Invalid user name and/or password.

Tab Button With Modifiers
    [Setup]    Open Page With Touch Enabled
    Tap    \#clickWithOptions    Shift    Alt
    Get Text    text=Please input your user name and password and click the login button.

*** Keywords ***
Open Page With Touch Enabled
    New Context    hasTouch=${True}
    New Page    ${LOGIN_URL}

Open Page With Touch Not Enabled
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Context    hasTouch=${False}
    New Page    ${LOGIN_URL}
