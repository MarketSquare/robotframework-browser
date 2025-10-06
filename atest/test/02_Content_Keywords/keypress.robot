*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${FORM_URL}

*** Test Cases ***
Press Keys Generate Characters
    Clear Text    input[name="name"]
    Press Keys    input[name="name"]    H    e    l    l    o    Space    W    o    r    l    d    !
    Get Text    input[name="name"]    ==    Hello World!

Press Keys With Strict
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 12 elements*
    ...    Press Keys    //input    Foo
    Set Strict Mode    False
    Press Keys    //input    T    i    d    i    i
    [Teardown]    Set Strict Mode    True

Press Key Combinations Of Keystrokes In TextField
    Press Keys    input[name="email"]    Home    Shift+End    Delete
    Press Keys    input[name="email"]    Shift+KeyA    KeyA
    Get Text    input[name="email"]    ==    Aa

Press Keys Combination Of Keystrokes In Select List
    Click    select[name="possible_channels"] > option[value="email"]
    Browser.Press Keys    select[name="possible_channels"]    Shift+ArrowDown
    Browser.Press Keys    select[name="possible_channels"]    Shift+ArrowDown
    Get Selected Options    select[name="possible_channels"]    value    ==    email    phone    directmail

Press Keys With Nonmatching Selector
    [Tags]    no-iframe
    Set Browser Timeout    50ms
    Run Keyword And Expect Error
    ...    *Error: locator.press: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Press Keys    css=notamatch    F
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Check Press Keys Events
    [Setup]    New Page    ${EVENTS_URL}
    Click    id=event_log_clear
    Press Keys    id=event_test_input    a    b    press_duration=200 ms    key_delay=100ms
    ${log} =    Get Text    id=event_log_text
    Assert Key Timings    ${log}    a    b    expected_press_duration_ms=200ms    expected_key_delay_ms=100ms
    Click    id=event_log_clear
    Press Keys    id=event_test_input    c    d    e    press_duration=10ms    key_delay=0
    ${log} =    Get Text    id=event_log_text
    Assert Key Timings    ${log}    c    d    e    expected_press_duration_ms=10ms    expected_key_delay_ms=0
    Click    id=event_log_clear
    Press Keys    id=event_test_input    f    g    h
    ${log} =    Get Text    id=event_log_text
    Assert Key Timings    ${log}    f    g    h    expected_press_duration_ms=0    expected_key_delay_ms=0
