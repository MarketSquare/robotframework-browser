*** Settings ***
Resource        imports.resource

Suite Setup     Open Browser To No Page
Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Function No Element And Fail On Timeout
    ${timeout} =    Set Browser Timeout    200ms
    TRY
        Wait For Function    () => {return false;}
    EXCEPT    TimeoutError: page.waitForFunction: Timeout 200ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Set Browser Timeout    ${timeout}

Wait For Function Element And Fail On Timeout
    ${timeout} =    Set Browser Timeout    500ms
    TRY
        Wait For Function    () => {return false;}    body
    EXCEPT    TimeoutError: page.waitForFunction: Timeout 500ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END
    [Teardown]    Set Browser Timeout    ${timeout}

Succesful Wait For Function
    Wait For Function    true    timeout=500ms

Failed Wait For Function
    TRY
        Wait For Function    false    timeout=100ms
    EXCEPT    TimeoutError: page.waitForFunction: Timeout 100ms exceeded*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failed Complicated Wait For Function
    [Tags]    no-iframe
    TRY
        Wait For Function
        ...    (selector) => document.activeElement === selector    selector=\#username_field    timeout=100ms
    EXCEPT    TimeoutError*    type=GLOB    AS    ${error}
        Log    ${error}
    END

Failed Wait For Function Promise
    [Tags]    no-iframe
    ${promise} =    Promise To    Wait For Function
    ...    (selector) => {console.log(selector); return document.activeElement === selector}
    ...    selector=\#username_field    timeout=100ms
    TRY
        Wait For    ${promise}
    EXCEPT    TimeoutError: page.waitForFunction: Timeout 100ms exceeded*    type=GLOB    AS    ${error}
        Log    {error}
    END

Succesful Wait For Function Promise
    [Tags]    no-iframe
    ${promise} =    Promise To    Wait For Function    (selector) => document.activeElement === selector
    ...    selector=\#username_field    timeout=750ms
    Click    \#username_field
    Wait For    ${promise}
