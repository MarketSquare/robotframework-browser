*** Settings ***
Library         Browser    auto_closing_level=SUITE    run_on_failure=None
Resource        ../imports.resource

Suite Setup     New Page    ${ERROR_URL}

*** Test Cases ***
Resource leaker
    New Context
    New Page    ${WELCOME_URL}

New context is not closed after test
    Get Title    ==    Welcome Page

Page leaker
    Go To    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New page is not closed after test
    Get Title    ==    prefilled_email_form.html
