*** Settings ***
Resource          ../imports.resource

Suite Setup       Open Context Shared By Both Suites
Suite Teardown    Close Context

*** Keywords ***
Open Context Shared By Both Suites
    New Context
    New Page    ${LOGIN_URL}
