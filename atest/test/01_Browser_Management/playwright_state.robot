*** Settings ***
Resource          imports.resource
Suite Setup       No Operation
Test Setup        No Operation
Test Teardown     Close Browser

*** Keywords ***
Open Browser and assert Login Page
    [Arguments]    ${local_browser}
    Open Browser To Login Page
    Get Text    h1    ==    Login Page

Create Page Form
    Create Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

Create Page Login
    Create Page    ${LOGIN_URL}
    Get Title    matches    (?i)login

*** Test Cases ***
Open Firefox
    Open Browser and assert Login Page    firefox

Open Chrome
    Open Browser and assert Login Page    chromium

Create Browser does not open a page
    Create Browser
    Run Keyword And Expect Error    Tried to do playwright action 'goto', but no open page.    Go To    ${LOGIN_URL}

Create Browser does not create a context
    Create Browser
    # Use Switch context to test that no context exists here
    Run Keyword And Expect Error    *No context for index 0.*    Switch Context    0

Create Context does not open a page
    Create Context
    Run Keyword And Expect Error    *No page for index 0.*    Switch Page    0

Open Browser opens everything
    Open Browser    url=${FORM_URL}
    Get Title    ==    prefilled_email_form.html

Open Browser with invalid browser fails on RF side
    Run Keyword and Expect Error    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    Open Browser    url=${FORM_URL}    browser=netscape
    [Teardown]    no operation

Create Browser with invalid browser fails on RF side
    Run Keyword and Expect Error    *Argument 'browser' got value 'netscape' that cannot be converted to SupportedBrowsers*    Create Browser    netscape
    [Teardown]    no operation

Switch Browser
    Create Browser    chromium
    Pass Execution    Switch Browser doesn't work yet
    Create Page Login
    Create Browser    firefox
    Create Page Form
    Switch Browser    0
    Get Title    matches    (?i)login

Switch Context
    Create Context
    Create Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    Create Context
    Create Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    Switch Context    0
    Get Title    matches    (?i)login

Create Page can create context and browser
    Create Page    ${LOGIN_URL}
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
