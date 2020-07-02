*** Comments ***
Sourced with small modifications from https://robotframework.org/#examples

*** Settings ***
Library           Browser

*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chromium
${DELAY}          0
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    # Maximize Browser Window
    # Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Get Title    matches    (?i)login

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    css=input#username_field    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    css=input#password_field    ${password}

Submit Credentials
    Click    css=input#login_button

Welcome Page Should Be Open
    Get Url    ==    ${WELCOME URL}
    Get Title    ==    Welcome Page
