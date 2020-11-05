*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Type Text with Clearing
    Type Text    input#username_field    Wrong Text
    Type Text    input#username_field    user
    Type Text    input#username_field    name    clear=No
    Get TextField Value    css=input#username_field    ==    username

Type Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Type Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Clear Text
    Fill Text    input#username_field    Wrong Text
    Get TextField Value    css=input#username_field    ==    Wrong Text
    Clear Text    input#username_field
    Get TextField Value    css=input#username_field    ==    ${EMPTY}
    Type Text    input#username_field    username    clear=No
    Get TextField Value    css=input#username_field    ==    username

Clear Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Clear Text    notamatch
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill with css selector
    Fill Text    css=input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Fill Text With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Fill Text    notamatch    text
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Fill Secret
    Fill Secret    css=input#password_field    password11
    Get TextField Value    css=input#password_field    ==    password11

Type Secret
    Type Secret    css=input#password_field    password22
    Get TextField Value    css=input#password_field    ==    password22

Fill Secret With Nonmatching Selector
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Fill Secret    notamatch    secret
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Type Text with Delay
    Type Text    input#username_field    username    delay=10 ms
    Get TextField Value    css=input#username_field    ==    username

Fill Text with Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get TextField Value    css=input#username_field    ==    username
