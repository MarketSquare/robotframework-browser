*** Settings ***
Library             Browser    timeout=15s    run_on_failure=None
Resource            imports.resource

Suite Setup         New Browser
Suite Teardown      Close Browser

*** Test Cases ***
New Page Will Not Timeout
    [Tags]    slow
    New Page    ${SLOW_PAGE}
    Get Title    ==    Slow page
