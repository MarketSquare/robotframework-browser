*** Settings ***
Library         Browser    auto_closing_level=SUITE    run_on_failure=None
Resource        ../imports.resource

Suite Setup     New Page    ${ERROR_URL}

Force Tags      no-iframe

*** Test Cases ***
Resource Leaker
    New Context
    New Page    ${WELCOME_URL}

New Context Is Not Closed After Test
    Get Title    ==    Welcome Page

Page Leaker
    Go To    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get Title    ==    prefilled_email_form.html

New Page Is Not Closed After Test
    Get Title    ==    prefilled_email_form.html
