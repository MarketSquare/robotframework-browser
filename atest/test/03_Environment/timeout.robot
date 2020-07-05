*** Settings ***
Library           Browser    timeout=1ms
Suite Setup       Open Browser    url=${None}    browser=${BROWSER}    headless=${HEADLESS}
Suite Teardown    Close Browser

*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chromium
${HEADLESS}       True
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html
${FORM_URL}       http://${SERVER}/prefilled_email_form.html

*** Test Cases ***
Test GoTo With Short Default Timeout
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN_URL}

Test Overriding With Long
    Set Timeout    10 s
    Go To    ${FORM_URL}

Test Overriding With Short
    Set Timeout    10 s
    Go To    ${ERROR URL}
    Set Timeout    1 ms
    Run Keyword And Expect Error    *Timeout 1ms exceeded during page.goto*    Go To    ${LOGIN URL}
