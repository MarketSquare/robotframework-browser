*** Settings ***
Resource          imports.resource
Library           OperatingSystem
Test Setup        Go To    ${LOGIN_URL}

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

Fill Secret env
    Set Environment Variable    FILL_SECRET    password11
    Fill Secret    css=input#password_field    %FILL_SECRET
    Get TextField Value    css=input#password_field    ==    password11

Fill Secret local
    ${var}=    Set Variable    password123
    Fill Secret    css=input#password_field    $var
    Get TextField Value    css=input#password_field    ==    password123

Fill Secret fails when env variable is not set
    Run Keyword And Expect Error    Environment variable 'NONE_EXISTING_ENV_VARIABLE' has no value.    Fill Secret    css=input#password_field    %NONE_EXISTING_ENV_VARIABLE

Fill Secret fails when direct value given
    Run Keyword And Expect Error    ValueError: variable_name 'hushhush' must start with \% or \$ sign    Fill Secret    css=input#password_field    hushhush

Type Secret env
    Set Environment Variable    TYPE_SECRET    password22
    Type Secret    css=input#password_field    %TYPE_SECRET
    Get TextField Value    css=input#password_field    ==    password22

Type Secret fails when direct value given
    Run Keyword And Expect Error    ValueError: variable_name 'hushhush' must start with \% or \$ sign    Type Secret    css=input#password_field    hushhush

Type Secret local
    ${var}=    Set Variable    password321
    Type Secret    css=input#password_field    $var
    Get TextField Value    css=input#password_field    ==    password321

Type Secret fails when env variable is not set
    Run Keyword And Expect Error    Environment variable 'NONE_EXISTING_ENV_VARIABLE' has no value.    Type Secret    css=input#password_field    %NONE_EXISTING_ENV_VARIABLE

Fill Secret With Nonmatching Selector
    Set Environment Variable    MY_RFBROWSER_SECRET    secret
    Set Browser Timeout    50ms
    Run Keyword And Expect Error    *Timeout 50ms exceeded.*waiting for selector "notamatch"*    Fill Secret    notamatch    %MY_RFBROWSER_SECRET
    [Teardown]    Set Browser Timeout    ${PLAYWRIGHT_TIMEOUT}

Type Text with Delay
    Type Text    input#username_field    username    delay=10 ms
    Get TextField Value    css=input#username_field    ==    username

Fill Text with Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get TextField Value    css=input#username_field    ==    username
