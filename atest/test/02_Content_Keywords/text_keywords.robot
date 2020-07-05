*** Settings ***
Resource          imports.resource
Suite Setup       Go To    ${LOGIN URL}

*** Test Cases ***
Type Text with Clearing
    Type Text    input#username_field    Wrong Text
    Type Text    input#username_field    user
    Type Text    input#username_field    name    clear=No
    Get TextField Value    css=input#username_field    ==    username

Clear Text
    Fill Text    input#username_field    Wrong Text
    Get TextField Value    css=input#username_field    ==    Wrong Text
    Clear Text    input#username_field
    Get TextField Value    css=input#username_field    ==    ${EMPTY}
    Type Text    input#username_field    username    clear=No
    Get TextField Value    css=input#username_field    ==    username

Test fill with css selector
    Fill Text    css=input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Test Typing
    Type Text    css=input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Test inputting password
    Fill Secret    css=input#password_field    password
    Get TextField Value    css=input#password_field    ==    password

Type Text with Delay
    Type Text    input#username_field    username    delay=10 ms
    Get TextField Value    css=input#username_field    ==    username

Fill Text with Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get TextField Value    css=input#username_field    ==    username
