*** Settings ***
Resource    imports.resource

*** Test Cases ***
Toggling Offline Disables Connection
    [Tags]    slow
    New Page    ${LOGIN_URL}
    Set Offline
    # The element checking for network pings every 500ms
    Sleep    600ms
    Get Text    \#network_pinger    ==    no connection

Creating Offline Context Works
    New Context    offline=True
    Run Keyword And Expect Error
    ...    STARTS:Error: page.goto: net::ERR_INTERNET_DISCONNECTED
    ...    New Page    ${LOGIN_URL}
