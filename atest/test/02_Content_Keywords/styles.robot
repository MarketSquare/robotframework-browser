*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Add Style
    Browser.Add Style Tag    \#goes_hidden{color:aqua}

Verify Style
    Browser.Add Style Tag    \#goes_hidden{color:aqua}
    Browser.Get Style    \#goes_hidden    color    ==     rgb(0, 255, 255)