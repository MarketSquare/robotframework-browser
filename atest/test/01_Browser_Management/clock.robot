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

Clock Install, Pause Advance (Fast_forward) Resume
    ${time_set} =    Get Current Date    increment=6 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_set}
    Delta Time Is Less Than    ${time_set}    id=current-time    180
    ${pause_time} =    Get Current Date    increment=7 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Pause At    ${pause_time}
    Sleep    2s    # Wait for the clock to pause
    ${time1} =    Get Text    id=current-time
    Sleep    2s    # Make sure that clock is still paused
    ${time2} =    Get Text    id=current-time
    Should Be Equal As Strings    ${time1}    ${time2}
    Should Not Be Empty    ${time1}
    Should Not Be Empty    ${time2}
    Dates Are Equal    ${pause_time}    ${time1}
    Clock Advance    30 minutes
    Sleep    2s    # Wait for the clock to advance
    ${time3} =    Get Text    id=current-time
    ${advance_time} =    Add Time To Date    ${pause_time}    30 minutes    result_format=%Y-%m-%d %H:%M:%S
    Dates Are Equal    ${advance_time}    ${time3}
    Clock Resume
    ${time1} =    Get Text    id=current-time
    Sleep    2s    # Wait for the clock to update
    ${time2} =    Get Text    id=current-time
    Time1 Is Less Than Time2    ${time1}    ${time2}

Clock Advance Run_for Argument
    ${time_set} =    Get Current Date    increment=1 minute    result_format=%Y-%m-%d %H:%M:%S
    Clock Set Time    ${time_set}
    Delta Time Is Less Than    ${time_set}    id=current-time    180
    ${pause_time} =    Get Current Date    increment=1 hours    result_format=%Y-%m-%d %H:%M:%S
    Clock Pause At    ${pause_time}
    Sleep    2s    # Wait for the clock to pause
    ${time1} =    Get Text    id=current-time
    Sleep    2s    # Make sure that clock is still paused
    ${time2} =    Get Text    id=current-time
    Should Be Equal As Strings    ${time1}    ${time2}
    Dates Are Equal    ${pause_time}    ${time2}
    Clock Advance    10 seconds    run_for
    Sleep    2s    # Wait for the clock to advance
    ${time3} =    Get Text    id=current-time
    ${advance_time} =    Add Time To Date    ${pause_time}    10 seconds    result_format=%Y-%m-%d %H:%M:%S
    Dates Are Equal    ${advance_time}    ${time3}

*** Keywords ***
Suite Setup For Clock
    New Context    locale=fi-FI

Test Setup For Clock
    New Page    ${CLOCK_URL}
    ${ASSERTION_TIMEOUT} =    Set Retry Assertions For    5s
    Set Suite Variable    ${ASSERTION_TIMEOUT}
    Get Text    id=current-time    !=    ${EMPTY}    # To make sure that clock is loaded

Suite Teardown For Clock
    Close Context
    Set Retry Assertions For    ${ASSERTION_TIMEOUT}
