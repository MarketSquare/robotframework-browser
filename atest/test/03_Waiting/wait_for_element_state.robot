*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Elements State to hide
    Get Property    button#goes_hidden    style
    Click    button#goes_hidden
    Wait For Elements State    button#goes_hidden    hidden    1s

Wait For Elements State fails on too short timeout
    Get Property    button#goes_hidden    style
    Click    button#goes_hidden
    Run Keyword and Expect Error    Could not find element with selector `button#goes_hidden` within timeout.    Wait For Elements State    button#goes_hidden    hidden    400ms

Wait For Elements State to hide with Promise
    ${promise}=    Promise to    Wait For Elements State    button#goes_hidden    hidden    3s
    Wait For Elements State    button#goes_hidden    visible    300ms
    Click    button#goes_hidden
    Wait for    ${promise}
    Run Keyword and Expect Error    Could not find element with selector `button#goes_hidden` within timeout.    Wait For Elements State    button#goes_hidden    visible    40ms

Wait For Elements State to hide fails with Promise
    ${promise}=    Promise to    Wait For Elements State    button#goes_hidden    hidden    300ms
    Run Keyword and Expect Error    Could not find element with selector `button#goes_hidden` within timeout.    Wait for    ${promise}

Wait For Elements State to hide with Promise and wait for all promises
    Promise to    Wait For Elements State    button#goes_hidden    hidden    3s
    Wait For Elements State    button#goes_hidden    visible    300ms
    Click    button#goes_hidden
    Wait for all promises
    Run Keyword and Expect Error    Could not find element with selector `button#goes_hidden` within timeout.    Wait For Elements State    button#goes_hidden    visible    40ms
