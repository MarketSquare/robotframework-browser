*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

Test Tags       no-iframe

*** Test Cases ***
Add Style
    Add Style Tag    \#goes_hidden{color:aqua}

Verify Style
    Add Style Tag    \#goes_hidden{color:aqua}
    Get Style    \#goes_hidden    color    ==    rgb(0, 255, 255)
