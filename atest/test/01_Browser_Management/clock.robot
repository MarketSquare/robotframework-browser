*** Settings ***
Resource            imports.resource

Suite Setup         Suite Setup For Clock
Suite Teardown      Suite Teardown For Clock
Test Setup          Test Setup For Clock

*** Test Cases ***
Set Time To Fixed
    ${time_past} =    Get Current Date    increment=-5 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}    Fixed
    Delta Time Is Less Than    ${time_past}    id=current-time    180

    ${time_past} =    Get Current Date    increment=-2 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}
    Delta Time Is Less Than    ${time_past}    id=current-time    180

Set Time To System
    ${time_past} =    Get Current Date    increment=+5 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}    system
    Delta Time Is Less Than    ${time_past}    id=current-time    180

Set Time Install
    ${time_past} =    Get Current Date    increment=-15 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_past}    install
    Delta Time Is Less Than    ${time_past}    id=current-time    180

*** Keywords ***
Suite Setup For Clock
    New Context    locale=fi-FI

Test Setup For Clock
    New Page    ${CLOCK_URL}

Suite Teardown For Clock
    Close Browser
