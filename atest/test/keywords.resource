*** Settings ***
Resource    variables.resource
Library     Collections
Library     DateTime
Library     OperatingSystem
Library     Browser    timeout=${PLAYWRIGHT_TIMEOUT}    enable_playwright_debug=${True}
Library     ../library/common.py
Library     ../library/os_wrapper.py
Library     ../library/show_trace_tool.py

*** Keywords ***
Open Browser To No Page
    New Browser    ${BROWSER}    headless=${HEADLESS}

Open Browser To Frame Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${FRAMES_URL}

Open Browser To Deep Frame Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${DEEP_FRAMES_URL}

Open Browser To Form Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${FORM_URL}

Open Browser To Login Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${LOGIN_URL}
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

Verify Browser Type
    [Arguments]    ${expectedType}
    Get Browser Catalog    validate    value[0]['type'] == $expectedType

Suite Cleanup
    IF    "${SUITE STATUS}" == "PASS" and "${SYS_VAR_CLEAN}" == "${True}"
        Delete Files On Teardown
    ELSE
        Log    Suite ${SUITE NAME} status is ${SUITE STATUS}, not running stuie cleaning
    END

Delete Files On Teardown
    Remove Directory    ${OUTPUT_DIR}/browser    recursive=True
    Remove File    ${OUTPUT_DIR}/*.png
    Remove File    ${OUTPUT_DIR}/*.zip
    Remove File    ${OUTPUT_DIR}/*.webm
