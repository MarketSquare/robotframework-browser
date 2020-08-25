*** Settings ***
Resource          imports.resource
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
    # ${expected}    evaluate    [{"type": "chromium", "id": 0, "contexts": [{"type": "context", "id": 0, "pages": [{"type": "page", "title": "prefilled_email_form.html", "url": "http://${SERVER}/prefilled_email_form.html", "id": 0}]}, {"type": "context", "id": 1, "pages": [{"type": "page", "title": "Login Page", "url": "http://${SERVER}/dist/", "id": 0}]}], "activePage": 0, "activeContext": 1, "activeBrowser": False}, {"type": "chromium", "id": 1, "contexts": [{"type": "context", "id": 0, "pages": [{"type": "page", "title": "Example Domain", "url": "http://example.com/", "id": 0}]}], "activePage": 0, "activeContext": 0, "activeBrowser": True}]
    ${expected}=    evaluate    [{'activeBrowser': False, 'activeContext': 'f5225111-5402-4477-8e28-f2545b32b986', 'activePage': '5b60d5a7-22e6-406c-a9bb-2903ff3a635d', 'id': '1a41a7cc-bfd1-4e02-9925-6a681d1fd56e', 'type': 'chromium', 'contexts': [{'type': 'context', 'id': '2be4fcd3-a3fe-45a8-85a9-168a059b3298', 'pages': [{'type': 'page', 'title': 'prefilled_email_form.html', 'url': 'http://localhost:56993/prefilled_email_form.html', 'id': 'd40a0e2f-bf41-44bf-b90c-45e8884117d9'}]}, {'type': 'context', 'id': 'f5225111-5402-4477-8e28-f2545b32b986', 'pages': [{'type': 'page', 'title': 'Login Page', 'url': 'http://localhost:56993/dist/', 'id': '5b60d5a7-22e6-406c-a9bb-2903ff3a635d'}]}]}, {'activeBrowser': True, 'activeContext': 'c6aa5392-e524-4a17-a9ba-c90a29575ffb', 'activePage': '135a68d9-e3ec-4683-80bf-8320c2a7d1e8', 'id': '5558575c-1454-4553-9ea5-f43e203bc566', 'type': 'chromium', 'contexts': [{'type': 'context', 'id': 'c6aa5392-e524-4a17-a9ba-c90a29575ffb', 'pages': [{'type': 'page', 'title': 'Example Domain', 'url': 'http://example.com/', 'id': '135a68d9-e3ec-4683-80bf-8320c2a7d1e8'}]}]}]
    should be equal    ${browsers}    ${expected}
    Should Contain    ${expected}[0]

Get Closed Browsers
    New Browser
    Close Browser
    ${browsers}    Get Browser Catalog
    should be empty    ${browsers}

Get Viewport Size
    New Context    viewport={"height": 600, "width": 800}
    New Page
    ${size}    Evaluate    {"height": 600, "width": 800}
    Get Viewport Size    ALL    ==    {"height": 600, "width": 800}
    Get Viewport Size    ALL    ==    ${size}
    Get Viewport Size    width    ==    800
    Get Viewport Size    height    ==    600

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
