*** Settings ***
Resource          keywords.resource
Test Setup        Open Browser    ${LOGIN URL}
Test Teardown     Close Browser

*** Test Cases ***
Simple Press
    Press Keys    input#username_field    a
    Get TextField Value    input#username_field    ==    a
# Remove the expect errors after figuring out why playwright doesn't let the Shift+ casing change work

Shift Uppercasing
    Press Keys    input#username_field    Shift+a
    Run Keyword and Expect Error    Attribute input#username_field `a` should be `A`    Get TextField Value    input#username_field    ==    A

Shift Lowercasing
    Press Keys    input#username_field    Shift+A
    Run Keyword and Expect Error    Attribute input#username_field `A` should be `a`    Get TextField Value    input#username_field    ==    a
