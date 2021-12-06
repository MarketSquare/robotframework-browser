*** Settings ***
Resource            imports.resource

Test Teardown       Close Browser    ALL

*** Test Cases ***
Switch Browser
    [Timeout]    2 minutes
    ${first_browser} =    New Browser    chromium
    New Page    ${LOGIN_URL}
    Get Title    matches    (?i)login
    ${first_url} =    Get Url
    ${second_browser} =    New Browser    firefox    timeout=1 minute
    New Context
    ${timeout} =    Set Browser Timeout    10s
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html
    ${second_url} =    Get Url
    ${before_switch} =    Switch Browser    ${first_browser}
    Should Be Equal As Strings    ${second_browser}    ${before_switch}
    ${third_url} =    Get Url
    Get Title    matches    (?i)login
