*** Settings ***
Resource          imports.resource
Test Setup        New Page  ${LOGIN URL}

*** Test Cases ***
Test clicking submit
    Click    css=input#login_button
    Get Text    text=Login failed. Invalid user name and/or password.
