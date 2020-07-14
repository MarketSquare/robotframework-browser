*** Settings ***
Resource          imports.resource

*** Test Cases ***
test server title
    Create Page    ${LOGIN URL}/
    Get Title    ==    Login Page

about:blank title
    Create Page    about:blank
    Get Title    ==    ${EMPTY}
