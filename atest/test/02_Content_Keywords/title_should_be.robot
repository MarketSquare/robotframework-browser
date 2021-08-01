*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${FORM_URL}

*** Test Cases ***
test server title
    New Page    ${LOGIN_URL}/
    Get Title    ==    Login Page

about:blank title
    New Page    about:blank
    Get Title    ==    ${EMPTY}

Get Title Default Error
    Run Keyword And Expect Error
    ...    Title 'prefilled_email_form.html' (str) should be 'Not Here' (str)
    ...    Get Title    ==    Not Here

Get Title Custom Error
    Run Keyword And Expect Error
    ...    Tidii
    ...    Get Title    ==    Not Here    Tidii
