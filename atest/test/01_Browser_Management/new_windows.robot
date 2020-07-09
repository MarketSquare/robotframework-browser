*** Settings ***
Resource          imports.resource
Test Setup        Open Browser    ${LOGIN URL}

*** Test Cases ***
Focus Next Page on popup
    Focus Next Page
    Click    button#pops_up
    Page Should Contain    Popped Up!

Switch Active Page after popup
    Click    button#pops_up
    Switch Active Page    0
    Page Should Contain    Popped Up!
    Switch Active Page  1
    Page Should Contain  button#pops_up
