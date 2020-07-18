*** Settings ***
Resource          variables.resource
Library           Browser    timeout=${PLAYWRIGHT_TIMEOUT}    enable_playwright_debug=${True}
Library           OperatingSystem

*** Keywords ***
Open Browser To No Page
    New Browser  ${BROWSER}  headless=${HEADLESS}

Open Browser To Frame Page
    New Browser  ${BROWSER}  headless=${HEADLESS}
    New Page  ${FRAMES_URL}

Open Browser To Form Page
    New Browser  ${BROWSER}  headless=${HEADLESS}
    New Page  ${FORM_URL}

Open Browser To Login Page
    New Browser  ${BROWSER}  headless=${HEADLESS}
    New Page  ${LOGIN_URL}
    # Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Get Title    matches    (?i)login

Go To Login Page
    Go To    ${LOGIN_URL}
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
    Get Url    ==    ${WELCOME_URL}
    Get Title    ==    Welcome Page
