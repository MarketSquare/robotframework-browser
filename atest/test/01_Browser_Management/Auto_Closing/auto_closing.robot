*** Settings ***
Library         Browser    timeout=3s
Resource        ../imports.resource

Suite Setup     New Page    ${ERROR_URL}

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
    New Page    ${ERROR_URL}
    Click    text="Do not click!"
