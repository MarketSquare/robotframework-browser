*** Settings ***
Resource            imports.resource

Test Teardown       Close Browser    ALL

*** Test Cases ***
Switch Browser
    [Tags]    no-mac-support    slow
    [Timeout]    2 minutes
    ${first_browser} =    New Browser    chromium
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${first_url} =    Get Url
    ${second_browser} =    New Browser    firefox    timeout=1 minute
    New Context
    ${timeout} =    Set Browser Timeout    30s
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${second_url} =    Get Url
    ${before_switch} =    Switch Browser    ${first_browser}
    Should Be Equal As Strings    ${second_browser}    ${before_switch}
    ${third_url} =    Get Url
    Get Title    matches    (?i)login

Switch Context
    ${br} =    New Browser    headless=True
    ${ctx} =    New Context
    ${pg} =    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${br2} =    New Browser    headless=True    reuse_existing=False
    ${ctx2} =    New Context
    ${pg2} =    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${ctx3} =    New Context
    ${pg3} =    New Page    ${ERROR_URL}
    Get Title    ==    Error Page

    Switch Context    ${ctx}    ${br}
    Get Title    ==    prefilled_email_form.html
    Switch Context    ${ctx2}    ALL
    Get Title    matches    (?i)login
    Switch Context    ${ctx3}    ${br2}
    Get Title    ==    Error Page
    Switch Context    ${ctx2}    CURRENT
    Get Title    matches    (?i)login
    Run Keyword And Expect Error    *    Switch Context    ${ctx}    CURRENT
    Run Keyword And Expect Error
    ...    ValueError: Context ${ctx} is not in browser ${br2}
    ...    Switch Context
    ...    ${ctx}
    ...    ${br2}

Switch Page
    ${br1} =    New Browser    headless=True
    ${ctx1_1} =    New Context
    ${pg1_1_1} =    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${br2} =    New Browser    headless=True    reuse_existing=False
    ${ctx2_1} =    New Context
    ${pg2_1_1} =    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${pg2_1_2} =    New Page    ${ERROR_URL}
    Get Title    ==    Error Page

    Switch Page    ${pg1_1_1}    ${ctx1_1}    ${br1}
    Get Title    ==    prefilled_email_form.html
    Switch Page    ${pg2_1_1}    ${ctx2_1}    ALL
    Get Title    matches    (?i)login
    Switch Page    ${pg1_1_1}    ALL    ALL
    Get Title    ==    prefilled_email_form.html
    Switch Page    ${pg2_1_2}    CURRENT    ${br2}
    Get Title    ==    Error Page
    Switch Page    ${pg2_1_1}    CURRENT    CURRENT
    Get Title    matches    (?i)login
    Switch Page    ${pg1_1_1}    CURRENT    ALL
    Get Title    ==    prefilled_email_form.html
    Switch Page    # This passses because the browser and context are ignored
    ...    ${pg2_1_2}
    ...    ${ctx1_1}
    ...    ${br1}
    Get Title    ==    Error Page
    Switch Page
    ...    ${pg2_1_1}
    ...    ${ctx1_1}
    ...    ANY
    Get Title    matches    (?i)login
