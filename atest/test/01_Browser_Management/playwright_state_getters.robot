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
    ${size}    Evaluate    {"height": 600, "width": 800}
    Get Viewport Size    ==    {"height": 600, "width": 800}
    Get Viewport Size    ==    ${size}

Multipage order
    New Page    ${FORM_URL}
    Get title    ==    prefilled_email_form.html
    Page encapsulating keyword
    Get title    ==    prefilled_email_form.html
    [Teardown]    Close Page

Multicontext order
    New Context
    New Page    ${WELCOME_URL}
    Get title    ==    Welcome Page
    Context encapsulating keyword
    Get title    ==    Welcome Page
    [Teardown]    Close Context

*** Keywords ***
Page encapsulating keyword
    New Page    ${WELCOME_URL}
    Get title    ==    Welcome Page
    Page encapsulating keyword 2
    Get title    ==    Welcome Page
    [Teardown]    Close Page

Page encapsulating keyword 2
    New Page    ${ERROR_URL}
    Get title    ==    Error Page
    [Teardown]    Close Page

Context encapsulating keyword
    New Context
    New Page    ${ERROR_URL}
    Get title    ==    Error Page
    New Page    ${FORM_URL}
    Get title    ==    prefilled_email_form.html
    [Teardown]   Close Context
