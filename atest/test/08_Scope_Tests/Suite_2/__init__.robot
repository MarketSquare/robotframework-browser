*** Settings ***
Resource        ../scope_keywords.resource

Suite Setup     Set Suite Scope

*** Keywords ***
Set Suite Scope
    Log All Scopes    1500    1500    True    ${IFRAME_PREFIX}
    Ensure Open Page    ${WAIT_URL_DIRECT}
    Set Browser Timeout    1 sec
    Set Retry Assertions For    1 sec
    Set Strict Mode    False
    Set Selector Prefix    ${EMPTY}
    Log All Scopes    1000    1000    False    ${EMPTY}
