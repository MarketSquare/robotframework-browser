*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${FORM_URL}

*** Test Cases ***
Press Keys Generate Characters
    Clear Text    input[name="name"]
    Press Keys    input[name="name"]    True    H    e    l    l    o    Space    W    o    r    l    d    !
    Get Text    input[name="name"]    ==    Hello World!

Press Keys With Strict
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 12 elements.*
    ...    Press Keys    //input    True    Foo
    Press Keys    //input    False    T    i    d    i    i

Press Key Combinations of Keystrokes in TextField
    Press Keys    input[name="email"]    True    Home    Shift+End    Delete
    Press Keys    input[name="email"]    True    Shift+KeyA    KeyA
    Get Text    input[name="email"]    ==    Aa

Press Keys Combination of Keystrokes in Select List
    Click    select[name="possible_channels"] > option[value="email"]
    Browser.Press Keys    select[name="possible_channels"]    True    Shift+ArrowDown
    Browser.Press Keys    select[name="possible_channels"]    True    Shift+ArrowDown
    Get Selected Options    select[name="possible_channels"]    value    ==    email    phone    directmail

Press Keys With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "css=notamatch"*    Press Keys
    ...    css=notamatch    True    F
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}
