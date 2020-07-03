*** Comments ***
Sourced with small modifications from https://robotframework.org/#examples

*** Settings ***
Library           Browser

*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chrome
${DELAY}          0
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${BROWSER}
    Go To    ${LOGIN URL}
    # Maximize Browser Window
    # Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Login Page

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
    Click Button    css=input#login_button

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Welcome Page
