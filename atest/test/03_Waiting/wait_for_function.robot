*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Succesful Wait For Function
    Wait For Function    true    timeout=500ms

Failed Wait For Function
    Run Keyword and Expect Error    Timeout 100ms exceeded during page.waitForFunction*    Wait For Function    false    timeout=100ms

Failed Wait For Function Promise
    ${promise}    Promise To    Wait For Function    document.activeElement === document.querySelector('#username_field')    timeout=100ms
    Run Keyword and Expect Error    Timeout 100ms exceeded during page.waitForFunction*    Wait For    ${promise}
