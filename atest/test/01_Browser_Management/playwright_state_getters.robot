*** Settings ***
Resource          imports.resource
Test Teardown     Close Browser    ALL

*** Test Cases ***
Get Multiple Browsers
    New Browser
    New Page    ${FORM_URL}
    New Context
    New Page    ${LOGIN_URL}
    New Browser
    New Context
    ${oldtimeout}=    Set Browser Timeout    15s
    New Page    http://example.com
    ${browsers}    Get Browser Catalog    then    [(b['type'], b['activeBrowser'], [[p['url'] for p in c['pages']] for c in b['contexts']]) for b in value]
    ${expected}    evaluate    [('chromium', False, [['http://${SERVER}/prefilled_email_form.html'], ['${LOGIN_URL}']]), ('chromium', True, [['http://example.com/']])]
    should be equal    ${browsers}    ${expected}

Get Closed Browsers
    New Browser
    Close Browser
    ${browsers}    Get Browser Catalog
    should be empty    ${browsers}

Get Browser Catalog Default Error
    New Browser
    ${expected} =    Create List    1    2
    Run Keyword And Expect Error
    ...    Browser Catalog '*' (list) should be '[[]'1', '2'[]]' (list)
    ...    Get Browser Catalog    ==    ${expected}

Get Browser Catalog Custom Error
    New Browser
    ${expected} =    Create List    1    2
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Browser Catalog    ==    ${expected}    Tidii

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
