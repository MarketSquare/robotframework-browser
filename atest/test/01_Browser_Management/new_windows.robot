*** Settings ***
Resource          imports.resource
Test Setup        Open Browser    ${LOGIN URL}

*** Test Cases ***
Switch Active Page On Popup 
    Click    button#pops_up
    Switch Active Page    1
    Page Should Contain    Popped Up!
