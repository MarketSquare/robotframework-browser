*** Settings ***
Resource        imports.resource

Suite Setup     Open Browser To No Page
Test Setup      New Page    ${LOGIN_URL}

*** Variables ***
${timeout_message} =    TimeoutError: page.waitForFunction: Timeout 100ms exceeded.

*** Test Cases ***
Wait For Function No Element And Fail On Timeout
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error
    ...    TimeoutError*
    ...    Wait For Function    () => {return false;}
    Set Browser Timeout    ${timeout}

Wait For Function Element And Fail On Timeout
    ${timeout} =    Set Browser Timeout    200ms
    Run Keyword And Expect Error
    ...    TimeoutError*
    ...    Wait For Function    () => {return false;}    body
    Set Browser Timeout    ${timeout}

Succesful Wait For Function
    Wait For Function    true    timeout=500ms

Failed Wait For Function
    Run Keyword And Expect Error
    ...    STARTS: ${timeout_message}
    ...    Wait For Function    false    timeout=100ms

Failed Complicated Wait For Function
    Run Keyword And Expect Error    STARTS: ${timeout_message}    Wait For Function
    ...    (selector) => document.activeElement === selector    selector=\#username_field    timeout=100ms

Failed Wait For Function Promise
    ${promise} =    Promise To    Wait For Function
    ...    (selector) => {console.log(selector); return document.activeElement === selector}
    ...    selector=\#username_field    timeout=100ms
    Run Keyword And Expect Error
    ...    STARTS: ${timeout_message}
    ...    Wait For    ${promise}

Succesful Wait For Function Promise
    ${promise} =    Promise To    Wait For Function    (selector) => document.activeElement === selector
    ...    selector=\#username_field    timeout=750ms
    Click    \#username_field
    Wait For    ${promise}
