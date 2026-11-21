*** Settings ***
Resource          imports.resource

Suite Setup       New Context
Suite Teardown    Close Context

*** Test Cases ***
Reload
    New Page    ${WELCOME_URL}
    Reload
    Reload    timeout=10s    waitUntil=load

Reload Uses Custom Timeout And Wait Until
    New Page    ${STALLED_PAGE}    wait_until=commit
    Reload    waitUntil=commit
    Run Keyword And Expect Error    *Timeout 100ms exceeded*    Reload    timeout=100ms
