*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation
Test Teardown     Close All Browsers

*** Test Cases ***
Get Multiple Browsers
    [Tags]    Not-Implemented
    Create Browser
    Create Page    ${FORM_URL}
    Create Context
    Create Page    ${LOGIN_URL}
    Create Browser
    Create Page    http://example.com
    ${browsers}    Get Browser Catalog
    Fail

Get Closed Browsers
    Create Browser
    Close Browser
    ${browsers}    Get Browser Catalog
    ${closed_browser}    Evaluate    {'type': 'browser', 'id': 0, 'state': 'CLOSED'}
    Should Contain    ${browsers}    ${closed_browser}
