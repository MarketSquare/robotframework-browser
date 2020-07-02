*** Settings ***
Resource          keywords.resource
Test Setup        Open Browser
Test Teardown     Close Browser

*** Test Cases ***
test server title
    Go To    ${LOGIN URL}/
    Get Title    ==    Login Page

about:blank title
    Get Title    ==    ${EMPTY}
