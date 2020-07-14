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

*** Test Cases ***
Open Firefox
    Open Browser and assert Login Page    firefox

Open Chrome
    Open Browser and assert Login Page    chromium

Create Browser does not open a page
    Create Browser
    Run Keyword And Expect Error    *"Tried to do playwright action 'goto', but no open page."*    Go To    ${LOGIN URL}

Create Browser does not create a context
    Create Browser
    # Use Switch context to test that no context exists here
    Run Keyword And Expect Error    *No context for index 0.*    Switch Context    0

Create Context does not open a page
    Create Context
    Run Keyword And Expect Error    *"Tried to do playwright action 'goto', but no open page."*    Go To    ${LOGIN URL}

Switch Browser
    Create Browser    chromium
    Create Browser    firefox
    Switch Browser    1
    # TODO:

Switch Context
    Create Context
    Create Context
    Switch Context    1
    # TODO: asser that context has been switched by looking at something specific to context

Create Page can create context and browser
    Create Page    ${LOGIN URL}
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
