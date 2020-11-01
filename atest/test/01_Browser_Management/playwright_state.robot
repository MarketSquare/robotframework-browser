*** Settings ***
Resource          imports.resource
Test Teardown     Close Browser    ALL

*** Keywords ***
Open Browser and assert Login Page
    [Arguments]    ${local_browser}
    Open Browser To Login Page
    Get Text    h1    ==    Login Page

New Page Form
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New Page Login
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login

*** Test Cases ***
Open Firefox
    Open Browser and assert Login Page    firefox

Open Chrome
    Open Browser and assert Login Page    chromium

New Browser does not open a page
    New Browser
    Run Keyword And Expect Error    Tried to do playwright action 'goto', but no open page.    Go To    ${LOGIN_URL}

New Browser does not create a context
    New Browser
    # Use Switch context to test that no context exists here
    ${no_context_id}    Switch Context    CURRENT
    Should Be Equal    ${no_context_id}    NO CONTEXT OPEN

New Context does not open a page
    New Context
    ${no_page_id}    Switch Page    CURRENT
    Should Be Equal    ${no_page_id}    NO PAGE OPEN

Open Browser opens everything
    Open Browser    url=${FORM_URL}
    Get Title    ==    prefilled_email_form.html

Open Browser with invalid browser fails on RF side
    Run Keyword and Expect Error    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    Open Browser    url=${FORM_URL}    browser=netscape
    [Teardown]    no operation

New Browser with invalid browser fails on RF side
    Run Keyword and Expect Error    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    New Browser    netscape
    [Teardown]    no operation

Create Chain Works
    New Browser
    New Context
    ${first}=    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    Switch Page    ${first}
    Get Title    matches    (?i)login

Close Browser switches active page
    New Browser
    New Page Login
    New Browser
    New Page Form
    Close Browser
    Get Title    matches    (?i)login

Close Context switches active page
    New Context
    New Page Login
    New Context
    New Page Form
    Close Context
    Get Title    matches    (?i)login

Close Page switches active page
    New Page Login
    New Page Form
    Close Page
    Get Title    matches    (?i)login

Switch Browser
    ${first_browser}    New Browser    chromium
    New Page Login
    ${first_url}    Get Url
    ${second_browser}    New Browser    firefox
    New Context
    ${timeout}=    Set Browser Timeout    10s
    New Page Form
    ${second_url}    Get Url
    ${before_switch}    Switch Browser    ${first_browser}
    Should Be Equal As Strings    ${second_browser}    ${before_switch}
    ${third_url}    Get Url
    Get Title    matches    (?i)login

Browser, Context and Page UUIDs
    ${browser}=    New Browser
    ${context}=    New Context
    ${page}=    New Page
    Should Start With    ${browser}    browser=
    Should Start With    ${context}    context=
    Should Start With    ${page}    page=
    [Teardown]    Close Browser

Switch Context
    ${first_context}    New Context
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${second_context}    New Context
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Switch Context    ${first_context}
    Get Title    matches    (?i)login

New Page can New Context and browser
    New Page    ${LOGIN_URL}
    Get Text    h1    ==    Login Page

Switch Page after popup
    Open Browser and assert Login Page    chromium
    Click    button#pops_up
    ${previous}=    Switch Page    NEW
    Wait For Elements State    "Popped Up!"
    Switch Page    ${previous}
    Wait For Elements State    button#pops_up

Switch New Page fails when no new pages
    New Page    ${LOGIN_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${timeout}=    Set Browser Timeout    0.1s
    Run Keyword And Expect Error    Tried to activate a new page but no new pages were detected in context.    Switch Page    NEW
    Get Title    ==    prefilled_email_form.html
    [Teardown]    Set Browser Timeout    ${timeout}

Set Viewport Size
    New Page
    ${size}    Get Viewport Size
    ${desired_first}    Evaluate    {"height": 720, "width": 1280}
    Should Be Equal    ${size}    ${desired_first}
    Set Viewport Size    height=600    width=800
    ${desired_second}    Evaluate    {"height": 600, "width": 800}
    ${second_size}    Get Viewport Size
    Should Be Equal    ${desired_second}    ${second_size}

Page Index is stable when other pages closed
    ${first}=    New Page
    ${second}=    New Page
    ${third}=    New Page
    Close Page
    Close Page
    ${last}=    Switch Page    ${first}
    Should Be Equal    ${first}    ${last}

Context Index is stable when other contexts closed
    ${first}=    New Context
    ${second}=    New Context
    ${third}=    New Context
    Close Context
    Close Context
    ${last}=    Switch Context    ${first}
    Should Be Equal    ${first}    ${last}

Page indices are unique
    ${first}=    New Page
    Close Page
    ${second}=    New Page
    Should Not Be Equal    ${first}    ${second}

Context indices are unique
    ${first}=    New Context
    Close Context
    ${second}=    New Context
    Should Not Be Equal    ${first}    ${second}

Browser indices are unique
    ${first}=    New Browser
    Close Browser
    ${second}=    New Browser
    Should Not Be Equal    ${first}    ${second}

Close All Contexts
    New Context
    New Context
    New Context
    Close Context    ALL
    ${current}=    Switch Context    CURRENT
    Should Be Equal    ${current}    NO CONTEXT OPEN

Close All Pages
    New Page
    New Page
    New Page
    Close Page    ALL
    ${current}=    Switch Page    CURRENT
    Should Be Equal    ${current}    NO PAGE OPEN

Closing Page/Contex/Browser Multiple Times Should Not Cause Errors
    New Context
    New Page
    Close Page
    Close Page
    Close Context
    Close Context
    Close Browser
    Close Browser

Closing Page/Contex/Browser Multiple Times With All Should Not Cause Errors
    New Context
    New Page
    Close Page    ALL
    Close Page    ALL
    Close Context    ALL    ALL
    Close Context    ALL    ALL
    Close Browser    ALL
    Close Browser    ALL

New Context with defaultBrowserType ff
    New Context    defaultBrowserType=firefox
    Verify Browser Type    firefox

New Context with defaultBrowserType chromium
    New Context    defaultBrowserType=chromium
    Verify Browser Type    chromium
