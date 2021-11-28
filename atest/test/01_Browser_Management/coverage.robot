*** Settings ***
Resource    imports.resource

*** Test Cases ***
Coverage
    New Page    ${LOGIN_URL}
    Start Coverage
    Type Text    input#username_field    Wrong Text
    Click    input#username_field
    Stop Coverage
