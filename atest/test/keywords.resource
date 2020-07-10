*** Settings ***
Library           Browser
Library           OperatingSystem
Resource          variables.resource

*** Keywords ***
Open Browser To Login Page
    New Browser  ${BROWSER}  headless=${HEADLESS}
    New Page  ${LOGIN URL}    
    # Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Get Title    matches    (?i)login

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Login User
    Input Username    demo
    Input Pwd    mode
    Submit Credentials

Input Username
    [Arguments]    ${username}
    Fill Text    input#username_field    ${username}

Input Pwd
    [Arguments]    ${password}
    Fill Secret    input#password_field    ${password}

Submit Credentials
    Click    css=input#login_button

Welcome Page Should Be Open
    Get Url    ==    ${WELCOME URL}
    Get Title    ==    Welcome Page
