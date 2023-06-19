*** Settings ***
Resource        imports.resource

Suite Setup     New Browser    ${BROWSER}    headless=${HEADLESS}
Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Mutate Element On Page With ElementHandle
    ${ref} =    Get Element    h1
    Get Property    ${ref}    innerText    ==    Login Page
    Evaluate JavaScript    ${ref}    (elem) => elem.innerText = "abc"
    Get Property    ${ref}    innerText    ==    abc

Wait For Progress Bar
    [Tags]    slow
    ${promise} =    Promise To    Wait For Function    element => element.style.width=="100%"
    ...    selector=\#progress_bar    timeout=4s
    Click    \#progress_bar
    Wait For    ${promise}
