*** Settings ***
Resource        imports.resource

Test Setup      Test Setup For Clock
Suite Teardown    Suite Teardown For Clock

*** Test Cases ***
Set Time To Fixed
    ${time_past} =    Get Current Date    increment=-5 hours    result_format=%Y-%m-%d %H:%M:%S
    ${time_past_hour} =    Get Current Date    increment=-5 hours    result_format=%d.%m.%Y klo %H
    Clock Set Time    ${time_past}
    Get Text    id=current-time    starts    ${time_past_hour}

Set Time To System
    ${time_past} =    Get Current Date    increment=-5 hours    result_format=%Y-%m-%d %H:%M:%S
    ${time_past_hour} =    Get Current Date    increment=-5 hours    result_format=%d.%m.%Y klo %H
    Clock Set Time    ${time_past}    system
    Get Text    id=current-time    starts    ${time_past_hour}


*** Keywords ***
Test Setup For Clock
    New Context    locale=fi-FI
    New Page    ${CLOCK_URL}

Suite Teardown For Clock
    Close Browser