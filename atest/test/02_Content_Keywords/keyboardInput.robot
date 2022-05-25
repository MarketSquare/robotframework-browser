*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Keyboard Inputtype Type
    Focus    \#username_field
    Keyboard Input    type    0123456789
    Get Text    \#username_field    ==    0123456789
    Get Text    \#countKeyPress    ==    10

Keyboard Inputtype InsertText
    Focus    \#username_field
    Keyboard Input    insertText    0123456789
    Get Text    \#username_field    ==    0123456789
    Get Text    \#countKeyPress    ==    1
