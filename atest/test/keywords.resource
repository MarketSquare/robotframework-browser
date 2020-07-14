*** Settings ***
Library           Browser    timeout=${PLAYWRIGHT TIMEOUT}    enable_playwright_debug=${True}
Library           OperatingSystem
Resource          variables.resource

*** Variables ***
${PLAYWRIGHT TIMEOUT}      1 second

*** Keywords ***
Open Browser To No Page
    Create Browser  ${BROWSER}  headless=${HEADLESS}

Open Browser To Frame Page
    Create Browser  ${BROWSER}  headless=${HEADLESS}
    Create Page  ${FRAMES URL}

Open Browser To Form Page
    Create Browser  ${BROWSER}  headless=${HEADLESS}
    Create Page  ${FORM_URL}

Open Browser To Login Page
    Create Browser  ${BROWSER}  headless=${HEADLESS}
    Create Page  ${LOGIN URL}    
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
