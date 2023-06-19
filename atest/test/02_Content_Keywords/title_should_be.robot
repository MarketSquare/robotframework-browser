*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${FORM_URL}

*** Test Cases ***
Test Server Title
    New Page    ${LOGIN_URL}/
    Get Title    ==    Login Page

About:blank Title
    New Page    about:blank
    Get Title    ==    ${EMPTY}

Get Title Default Error
    Set Retry Assertions For    100ms
    Run Keyword And Expect Error
    ...    Title 'prefilled_email_form.html' (str) should be 'Not Here' (str)
    ...    Get Title    ==    Not Here
    [Teardown]    Set Retry Assertions For    1s

Get Title Custom Error
    Set Retry Assertions For    100ms
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Title    ==    Not Here    Tidii
    [Teardown]    Set Retry Assertions For    1s
