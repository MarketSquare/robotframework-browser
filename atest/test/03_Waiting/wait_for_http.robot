*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Wait For Request synchronous
    Fail

Wait For Request async
    Fail

Wait For Response synchronous
    Fail

Wait For Response async
    Fail
