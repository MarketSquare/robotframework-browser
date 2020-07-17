*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation
Test Teardown     Close All Browsers

*** Test Cases ***
Get Pages
    Create Browser
    Create Page    ${FORM_URL}
    Create Context
    Create Page    ${LOGIN_URL}
    Create Browser
    Create Page    http://example.com
    ${pages}    Get Browsers
