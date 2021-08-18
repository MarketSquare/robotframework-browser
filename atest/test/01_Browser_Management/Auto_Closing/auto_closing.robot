*** Settings ***
Library         Browser    timeout=3s
Resource        ../imports.resource

Suite Setup     New Page    ${ERROR_URL}

*** Test Cases ***
Resource leaker
    New context
    New Page    ${WELCOME_URL}

New context is closed after test
    Get title    ==    Error Page

Page leaker
    Go to    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get title    ==    prefilled_email_form.html

New page in same context is closed after test
    Get title    ==    Welcome Page

Unhandled alert does not block execution
    New Page    ${ERROR_URL}
    Click    text="Do not click!"
