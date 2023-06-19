*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Teardown

*** Test Cases ***
New Page Will Not Timeout
    [Tags]    slow
    New Page    ${SLOW_PAGE}
    Get Title    ==    Slow page

*** Keywords ***
Setup
    Set Browser Timeout    15s    scope=Suite
    ${original} =    Register Keyword To Run On Failure    ${None}
    Set Suite Variable    $original
    New Browser    headless=${HEADLESS}

Teardown
    Register Keyword To Run On Failure    ${original}
    Close Browser
