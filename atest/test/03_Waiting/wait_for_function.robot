*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Succesful Wait For Function
    Wait For Function    true    timeout=500ms

Failed Wait For Function
    Run Keyword and Expect Error    Timeout 100ms exceeded during page.waitForFunction*    Wait For Function    false    timeout=100ms

Failed complicated Wait For Function
    Run Keyword And Expect Error    Timeout 100ms exceeded during page.waitForFunction*    Wait For Function    (selector) => document.activeElement === selector    selector=\#username_field    timeout=100ms

Failed Wait For Function Promise
    ${promise}    Promise To    Wait For Function    (selector) => {console.log(selector); return document.activeElement === selector}    selector=\#username_field    timeout=100ms
    Run Keyword and Expect Error    Timeout 100ms exceeded during page.waitForFunction*    Wait For    ${promise}

Succesful Wait For Function Promise
    ${promise}    Promise To    Wait For Function    (selector) => document.activeElement === selector    selector=\#username_field    timeout=500ms
    Click    \#username_field
    Wait For    ${promise}
