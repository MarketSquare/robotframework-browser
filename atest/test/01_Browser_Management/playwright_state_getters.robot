*** Settings ***
Resource            imports.resource

Test Teardown       Close Browser    ALL

*** Test Cases ***
Get Multiple Browsers
    [Tags]    slow
    New Browser
    New Page    ${FORM_URL}
    New Context
    New Page    ${LOGIN_URL}
    New Browser
    New Context
    ${oldtimeout} =    Set Browser Timeout    15s
    New Page    http://example.com
    ${browsers} =    Get Browser Catalog    then
    ...    [(b['type'], b['activeBrowser'], [[p['url'] for p in c['pages']] for c in b['contexts']]) for b in value]
    ${expected} =    Evaluate
    ...    [('chromium', False, [['http://${SERVER}/prefilled_email_form.html'], ['${LOGIN_URL}']]), ('chromium', True, [['http://example.com/']])]
    Should Be Equal    ${browsers}    ${expected}

Get Closed Browsers
    New Browser
    Close Browser
    ${browsers} =    Get Browser Catalog
    Should Be Empty    ${browsers}

Get Browser Catalog Default Error
    [Tags]    slow
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
    ${size} =    Evaluate    {"height": 600, "width": 800}
    Get Viewport Size    ALL    ==    {"height": 600, "width": 800}
    Get Viewport Size    ALL    ==    ${size}
    Get Viewport Size    width    ==    800
    Get Viewport Size    height    ==    600

Multipage Order
    [Tags]    slow
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Page Encapsulating Keyword
    Get Title    ==    prefilled_email_form.html
    [Teardown]    Close Page

Multicontext Order
    New Context
    New Page    ${WELCOME_URL}
    Get Title    ==    Welcome Page
    Context Encapsulating Keyword
    Get Title    ==    Welcome Page
    [Teardown]    Close Context

Multibrowser Order
    [Tags]    slow
    New Browser    browser=chromium
    New Page    ${ERROR_URL}
    Get Title    ==    Error Page
    Browser Encapsulating Keyword
    Get Title    ==    Error Page
    [Teardown]    Close Browser

Get Browser Catalog After First Popup Close
    New Browser
    New Page    ${CREATE_POPUPS_URL}
    Get Title    ==    Call Popups Page
    ${pages} =    Get Browser Catalog    then    value[1]['contexts'][0]['pages']
    ${pages amount} =    Get Length    ${pages}
    Should Be Equal As Integers    ${pages amount}    1
    Click    id=first_popup
    Get Browser Catalog    validate    len(value[1]['contexts'][0]['pages']) == 2
    Switch Page    NEW
    Click    id=close_popup
    Get Browser Catalog    validate    len(value[1]['contexts'][0]['pages']) == 1
    [Teardown]    Close Browser

Get Browser Catalog After Second Popup Close
    New Browser
    New Page    ${CREATE_POPUPS_URL}
    Get Title    ==    Call Popups Page
    Get Browser Catalog    validate    len(value[1]['contexts'][0]['pages']) == 1
    Click    id=first_popup
    Get Browser Catalog    validate    len(value[1]['contexts'][0]['pages']) == 2
    Switch Page    NEW
    Click    id=second_popup
    Get Browser Catalog    validate    len(value[1]['contexts'][0]['pages']) == 2
    [Teardown]    Close Browser

*** Keywords ***
Page Encapsulating Keyword
    New Page    ${WELCOME_URL}
    Get Title    ==    Welcome Page
    Page Encapsulating Keyword 2
    Get Title    ==    Welcome Page
    [Teardown]    Close Page

Page Encapsulating Keyword 2
    New Page    ${ERROR_URL}
    Get Title    ==    Error Page
    [Teardown]    Close Page

Context Encapsulating Keyword
    New Context
    New Page    ${ERROR_URL}
    Get Title    ==    Error Page
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    [Teardown]    Close Context

Browser Encapsulating Keyword
    New Browser    browser=${BROWSER}
    New Page    ${WELCOME_URL}
    Get Title    ==    Welcome Page
    [Teardown]    Close Browser
