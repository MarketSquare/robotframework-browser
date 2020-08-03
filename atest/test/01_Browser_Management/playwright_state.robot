*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation
Test Teardown     Close All Browsers

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
    Run Keyword And Expect Error    *No context for index 0.*    Switch Context    0

New Context does not open a page
    New Context
    Run Keyword And Expect Error    *No page for index 0.*    Switch Page    0

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
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    Switch Page    0
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
    New Page Form
    ${second_url}    Get Url
    ${before_switch}    Switch Browser    ${first_browser}
    Should Be Equal As Numbers    ${second_browser}    ${before_switch}
    ${third_url}    Get Url
    Get Title    matches    (?i)login

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

Focus Next Page on popup
    Open Browser and assert Login Page    chromium
    Auto Activate Pages
    Click    button#pops_up
    # FIXME: Workaround, this need is caused by eventhandlers laziness
    Sleep    1s
    Wait For Elements State    "Popped Up!"

Switch Page after popup
    Open Browser and assert Login Page    chromium
    Click    button#pops_up
    Switch Page    1
    Wait For Elements State    "Popped Up!"
    Switch Page    0
    Wait For Elements State    button#pops_up

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
