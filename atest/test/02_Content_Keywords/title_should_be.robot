*** Settings ***
Resource          imports.resource

*** Test Cases ***
test server title
    Create Page    ${LOGIN_URL}/
    Get Title    ==    Login Page

about:blank title
    Create Page    about:blank
    Get Title    ==    ${EMPTY}
