*** Settings ***
Library           Browser  auto_closing_level=SUITE
Resource          ../imports.resource
Suite Setup       New Page    ${ERROR_URL}

*** Test Cases ***
Resource leaker
    New context
    New Page    ${WELCOME_URL}

New context is not closed after test
    Get title    ==    Welcome Page

Page leaker
    Go to    ${WELCOME_URL}
    New Page    ${FORM_URL}
    Get title    ==    prefilled_email_form.html

New page is not closed after test
    Get title    ==    prefilled_email_form.html
