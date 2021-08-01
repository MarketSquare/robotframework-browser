*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Add Style
    Add Style Tag    \#username_field:focus {background-color: aqua;}
    Focus    \#username_field
    Get Style    \#username_field    background-color    ==    rgb(0, 255, 255)
