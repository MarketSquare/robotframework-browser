*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation
Test Teardown     Close All Browsers

*** Test Cases ***
Get Multiple Browsers
    [Tags]    Not-Implemented
    New Browser
    New Page    ${FORM_URL}
    New Context
    New Page    ${LOGIN_URL}
    New Browser
    New Page    http://example.com
    ${browsers}    Get Browser Catalog
    Fail

Get Closed Browsers
    New Browser
    Close Browser
    ${browsers}    Get Browser Catalog
    ${closed_browser}    Evaluate    {'type': 'browser', 'id': 0, 'state': 'CLOSED'}
    Should Contain    ${browsers}    ${closed_browser}

Get Viewport Size
    New Context    viewport={"height": 600, "width": 800}
    New Page
    ${size}    Get Viewport Size
    ${second}    Evaluate    {"height": 600, "width": 800}
    Should Be Equal    ${size}    ${second}
