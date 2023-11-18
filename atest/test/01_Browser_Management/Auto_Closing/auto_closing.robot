*** Settings ***
Resource        ../imports.resource

Suite Setup     Setup Suite

*** Test Cases ***
Resource Leaker
    New Context
    New Page    ${WELCOME_URL}

New Context Is Closed After Test
    Get Title    ==    Error Page

Page Leaker
    Go To    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New Page In Same Context Is Closed After Test
    Get Title    ==    Welcome Page

Unhandled Alert Does Not Block Execution
    [Tags]    debug
    New Page    ${ERROR_URL}
    Click    text="Do not click!"

*** Keywords ***
Setup Suite
    New Page    ${ERROR_URL}
    Set Browser Timeout    3s    Suite
