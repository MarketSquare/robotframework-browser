*** Settings ***
Resource        imports.resource

Test Setup      Ensure Location    ${LOGIN_URL}

*** Test Cases ***
Wait For Page Load States Load
    Go To    ${ROOT_URL}delayed-load.html
    Wait For Load State    state=load

Wait For Page Load States Networkidle
    Go To    ${ROOT_URL}delayed-load.html
    Wait For Load State    state=networkidle
    Go To    ${ROOT_URL}delayed-load.html
    Get Text    \#server_delayed_response    ==    Server response after 400ms
    TRY
        Wait For Load State    state=networkidle    timeout=0.02s
    EXCEPT    AS    ${error}
        Should Start With    ${error}    TimeoutError: page.waitForLoadState:
    END

Wait For Page Load States Domcontentloaded
    Go To    ${ROOT_URL}delayed-load.html
    Get Text    \#server_delayed_response    ==    Server response after 400ms
    Wait For Load State    state=domcontentloaded    timeout=1s
