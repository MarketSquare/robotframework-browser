*** Settings ***
Resource          imports.resource
Suite Setup       Open Browser To No Page
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Mutate Element On Page With ElementHandle
    ${ref}=    Get Element    h1
    Get Property    ${ref}    innerText    ==    Login Page
    Execute JavaScript    (elem) => elem.innerText = "abc"    ${ref}
    Get Property    ${ref}    innerText    ==    abc

Wait For Progress Bar
    ${promise}    Promise To    Wait For Function    element => element.style.width=="100%"    selector=\#progress_bar    timeout=4s
    Click    \#progress_bar
    Wait For    ${promise}
