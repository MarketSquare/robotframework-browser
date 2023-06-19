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
    ...    *TimeoutError: locator.press: Timeout 50ms exceeded.*waiting for locator('notamatch')*
    ...    Press Keys    css=notamatch    F
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}
