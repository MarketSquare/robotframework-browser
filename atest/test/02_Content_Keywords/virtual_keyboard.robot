*** Settings ***
Resource      imports.resource

Test Setup    New Page    ${FORM_URL}

*** Test Cases ***
Keyboard Key Inputs Characters
    Clear Text    input[name="name"]
    Click    input[name="name"]
    Keyboard Key    press    H
    Keyboard Key    press    e
    Keyboard Key    press    l
    Keyboard Key    press    l
    Keyboard Key    press    o
    Get Text    input[name="name"]    ==    Hello

Select List Options
    Click    select[name="possible_channels"] > option[value="email"]
    Keyboard Key    down    Shift
    Keyboard Key    press    ArrowDown
    Keyboard Key    press    ArrowDown
    Get Selected Options    select[name="possible_channels"]    value    ==    email    phone    directmail

Keyboard Key Press Holds The Key For The Given Delay
    [Setup]    New Page    ${EVENTS_URL}
    Click    id=event_log_clear
    Click    id=event_test_input
    Keyboard Key    press    a    delay=200 ms
    ${log} =    Get Text    id=event_log_text
    Assert Key Timings    ${log}    a    expected_press_duration_ms=200ms

Keyboard Key Press Without Delay Does Not Hold The Key
    [Setup]    New Page    ${EVENTS_URL}
    Click    id=event_log_clear
    Click    id=event_test_input
    Keyboard Key    press    b
    ${log} =    Get Text    id=event_log_text
    Assert Key Timings    ${log}    b    expected_press_duration_ms=0

Keyboard Key Delay Is Only Valid For Press
    Run Keyword And Expect Error
    ...    ValueError: delay is only valid if action is 'press'
    ...    Keyboard Key    down    Shift    delay=100 ms
    Run Keyword And Expect Error
    ...    ValueError: delay is only valid if action is 'press'
    ...    Keyboard Key    up    Shift    delay=100 ms
