*** Settings ***
Resource           keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Test clicking submit
    Click    css=input#login_button
    Page Should Contain    Login failed. Invalid user name and/or password.
