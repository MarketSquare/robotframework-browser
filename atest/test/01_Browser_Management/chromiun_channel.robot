*** Settings ***
Resource            imports.resource

Suite Teardown      Close Browser    ALL

Test Tags           no-docker-pr

*** Test Cases ***
Wrong Browser With Channel
    Run Keyword And Expect Error
    ...    ValueError: Must use chromium browser with channel definition
    ...    New Browser    firefox    channel=chrome

Use Chrome Stable With Channel Argument
    [Tags]    not-implemented    # This fails very often in CI, disable it.
    [Timeout]    60s    # Is slow in Windows OS.
    New Browser    chromium    headless=False    channel=chrome
    New Context
    ${TIMEOUT} =    Set Browser Timeout    30 s
    Set Suite Variable    ${TIMEOUT}
    New Page    ${LOGIN_URL}
    [Teardown]    Set Browser Timeout    ${TIMEOUT}
