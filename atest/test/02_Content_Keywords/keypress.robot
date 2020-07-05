*** Settings ***
Resource          imports.resource
Suite Setup       Go To    ${FORM_URL}

*** Test Cases ***
Press Keys - Generate Characters
    Clear Text    input[name="name"]
    Press Keys    input[name="name"]    H    e    l    l    o    Space    W    o    r    l    d    !
    Get TextField Value    input[name="name"]    ==    Hello World!

Press Keys - Cominations of Keystrokes in TextField
    Press Keys    input[name="email"]    Home    Shift+End    Delete
    Press Keys    input[name="email"]    Shift+KeyA    KeyA
    Get TextField Value    input[name="email"]    ==    Aa

Press Keys - Combination of Keystrokes in Select List
    Click    select[name="possible_channels"] > option[value="email"]
    Browser.Press Keys    select[name="possible_channels"]    Shift+ArrowDown
    Browser.Press Keys    select[name="possible_channels"]    Shift+ArrowDown
    Get Selected Options    select[name="possible_channels"]    value    ==    email    phone    directmail
