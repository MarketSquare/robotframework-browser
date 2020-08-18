*** Settings ***
Resource          imports.resource
Test Teardown     Close All Browsers

*** Test Cases ***
Get Multiple Browsers
    New Browser
    New Page    ${FORM_URL}
    New Context
    New Page    ${LOGIN_URL}
    New Browser
    New Page    http://example.com
    ${browsers}    Get Browser Catalog
    ${expected}    evaluate    [{"type": "chromium", "id": 0, "contexts": [{"type": "context", "id": 0, "pages": [{"type": "page", "title": "prefilled_email_form.html", "url": "http://${SERVER}/prefilled_email_form.html", "id": 0}]}, {"type": "context", "id": 1, "pages": [{"type": "page", "title": "Login Page", "url": "http://${SERVER}/dist/", "id": 0}]}], "activePage": 0, "activeContext": 1, "activeBrowser": False}, {"type": "chromium", "id": 1, "contexts": [{"type": "context", "id": 0, "pages": [{"type": "page", "title": "Example Domain", "url": "http://example.com/", "id": 0}]}], "activePage": 0, "activeContext": 0, "activeBrowser": True}]
    should be equal    ${browsers}    ${expected}

Get Closed Browsers
    New Browser
    Close Browser
    ${browsers}    Get Browser Catalog
    should be empty    ${browsers}

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

Multibrowser order
    New Browser    browser=chromium
    New Page    ${ERROR_URL}
    Get title    ==    Error Page
    Browser encapsulating keyword
    Get title    ==    Error Page
    [Teardown]    Close Browser

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
    [Teardown]    Close Context

Browser encapsulating keyword
    New Browser    browser=${BROWSER}
    New Page    ${WELCOME_URL}
    Get title    ==    Welcome Page
    [Teardown]    Close Browser
