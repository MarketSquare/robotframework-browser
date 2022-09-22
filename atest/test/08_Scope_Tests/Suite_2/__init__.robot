*** Settings ***
Resource        ../scope_keywords.resource

Suite Setup     Set Suite Scope

*** Keywords ***
Set Suite Scope
    Ensure Open Page    ${WAIT_URL}
    Set Browser Timeout    1 sec
    Set Retry Assertions For    1 sec
    Set Strict Mode    False