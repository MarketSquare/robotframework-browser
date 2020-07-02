*** Settings ***
Library           Browser
Test Setup        Open Browser
Test Teardown     Close Browser

*** Test Cases ***
test server title
    Go To    http://localhost:7272/
    Get Title    ==    Login Page

about:blank title
    Get Title    ==    ${EMPTY}
