*** Settings ***
Resource            imports.resource

Suite Setup         New Context
Suite Teardown      Close Context

*** Test Cases ***
Reload
    New Page    ${WELCOME_URL}
    Reload
    Reload    timeout=10s    waitUntil=load
