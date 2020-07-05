*** Settings ***
Resource          imports.resource
Test Setup        Go To    ${LOGIN URL}

*** Test Cases ***
Test clicking submit
    Click    css=input#login_button
    Page Should Contain    Login failed. Invalid user name and/or password.
