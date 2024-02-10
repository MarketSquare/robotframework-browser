*** Settings ***
Resource        imports.resource

Test Setup      Ensure Location    ${LOGIN_URL}

*** Test Cases ***
Wait For Page Load States
    Wait For Load State    state=load
    Wait For Load State    state=networkidle
    Wait For Load State    state=domcontentloaded    timeout=1s
