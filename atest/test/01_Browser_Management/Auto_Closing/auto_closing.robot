*** Settings ***
Library         Browser    timeout=3s
Resource        ../imports.resource

Suite Setup     New Page    ${ERROR_URL}

*** Test Cases ***
Resource leaker
    New Context
    New Page    ${WELCOME_URL}

New context is closed after test
    Get Title    ==    Error Page

Page leaker
    Go To    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New page in same context is closed after test
    Get Title    ==    Welcome Page

Unhandled alert does not block execution
    New Page    ${ERROR_URL}
    Click    text="Do not click!"
