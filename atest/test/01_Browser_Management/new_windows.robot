*** Settings ***
Resource          imports.resource
Test Setup        Open Browser    ${LOGIN URL}

*** Test Cases ***
Focus Next Page on popup
    Auto Activate Pages
    Click    button#pops_up
    # Workaround, this need is caused by eventhandlers laziness
    Sleep    1s
    Wait For Elements State    "Popped Up!"

Switch Active Page after popup
    Click    button#pops_up
    Switch Active Page    1
    Wait For Elements State    "Popped Up!"
    Switch Active Page    0
    Wait For Elements State    button#pops_up
