*** Settings ***
Resource          imports.resource

*** Test Cases ***
test server title
    Go To    ${LOGIN URL}/
    Get Title    ==    Login Page

about:blank title
    Go To    about:blank
    Get Title    ==    ${EMPTY}
