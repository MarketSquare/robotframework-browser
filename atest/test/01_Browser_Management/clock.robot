*** Settings ***
Resource            imports.resource

Suite Setup         Suite Setup For Clock
Suite Teardown      Suite Teardown For Clock
Test Setup          Test Setup For Clock

*** Test Cases ***
Set Time To Fixed
    ${time_past} =    Get Current Date    increment=-5 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}
    ${set_time} =    Get Text    id=current-time    matches    \\d{4}
    Take Screenshot
    Delta Time Is Less Than    ${set_time}    ${time_past}    180

Set Time To System
    ${time_past} =    Get Current Date    increment=-5 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}    system
    ${set_time} =    Get Text    id=current-time    matches    \\d{4}
    Delta Time Is Less Than    ${set_time}    ${time_past}    180

*** Keywords ***
Suite Setup For Clock
    New Context    locale=fi-FI

Test Setup For Clock
    New Page    ${CLOCK_URL}

Suite Teardown For Clock
    Close Browser
