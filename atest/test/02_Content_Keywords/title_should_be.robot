*** Settings ***
Resource          imports.resource

*** Test Cases ***
test server title
    New Page    ${LOGIN_URL}/
    Get Title    ==    Login Page

about:blank title
    New Page    about:blank
    Get Title    ==    ${EMPTY}
