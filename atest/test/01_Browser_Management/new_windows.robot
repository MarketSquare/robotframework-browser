*** Settings ***
Resource          imports.resource
Test Setup        Open Browser    ${LOGIN URL}

*** Test Cases ***
Focus Next Page on popup
    Focus Next Page
    Click    button#pops_up
    Get Text  h1  ==  Popped Up!

Switch Active Page after popup
    Click    button#pops_up
    Switch Active Page    0
    Get Text  h1  ==  Popped Up!
    Switch Active Page  1
    Get Text  button#pops_up
