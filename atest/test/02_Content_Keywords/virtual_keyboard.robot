*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${FORM_URL}

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
