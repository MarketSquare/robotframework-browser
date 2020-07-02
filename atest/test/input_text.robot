*** Settings ***
Library           Browser
Test Setup        Open Browser    http://localhost:7272
Test Teardown     Close Browser

*** Test Cases ***
Test inputting with css selector
    Input Text    css=input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Test Typing
    Input Text    css=input#username_field    username    type=True
    Get TextField Value    css=input#username_field    ==    username

Test inputting password
    Input Password    css=input#password_field    password
    Get TextField Value    css=input#password_field    ==    password

Type Text with Delay
    Type Text    input#username_field    username    delay=10 ms
    Get TextField Value    css=input#username_field    ==    username

Fill Text
    Fill Text    input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Fill Text with Clearing
    Fill Text    input#username_field    Wrong Text
    Fill Text    input#username_field    username
    Get TextField Value    css=input#username_field    ==    username

Type Text with Clearing
    Type Text    input#username_field    Wrong Text
    Type Text    input#username_field    user
    Type Text    input#username_field    name    clear=No
    Get TextField Value    css=input#username_field    ==    username

Clear Text
    Type Text    input#username_field    Wrong Text
    Clear Text    input#username_field
    Type Text    input#username_field    username    clear=No
    Get TextField Value    css=input#username_field    ==    username