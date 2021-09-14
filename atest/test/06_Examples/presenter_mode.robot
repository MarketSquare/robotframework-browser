*** Settings ***
Resource    ../variables.resource
Library     Browser    enable_presenter_mode=True

*** Test Cases ***
Filling the text
    open browser    ${LOGIN_URL}
    type text    input#username_field    user
