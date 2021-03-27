*** Settings ***
Resource          imports.resource

*** Test Cases ***
Wrong Browser With Channel
    Run Keyword And Expect Error
    ...    ValueError: Must use chromium browser with channel definition
    ...    New Browser    firefox    channel=chrome

Use Chrome Stable With Channel Argument
    New Browser    chromium    headless=False    channel=chrome
    New Context
    New Page    ${LOGIN_URL}
