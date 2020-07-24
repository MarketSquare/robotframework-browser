*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Fails if no success
    Run Keyword And Expect Error    Timeout 100ms exceeded during page.waitForRequest.*    Wait For Request    /api/get/json    timeout=100ms

Wait For Request synchronous
    Click    \#delayed_request
    Wait For Request    timeout=1s

Wait For Request async
    ${promise}    Promise To    Wait For Request    matcher=    timeout=3s
    # Go To    http://localhost:7272/api/get/json
    Click    \#delayed_request
    Wait For    ${promise}

Wait For Response synchronous
    Click    \#delayed_request
    Wait For Request    timeout=1s

Wait For Response async
    Click    \#delayed_request
    Wait For Request    timeout=3s
