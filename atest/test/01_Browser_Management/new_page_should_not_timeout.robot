*** Settings ***
Library             Browser    timeout=15s    run_on_failure=None
Resource            imports.resource

Suite Setup         New Browser
Suite Teardown      Close Browser

*** Test Cases ***
New Page will not timeout
    [Tags]    slow
    New Page    ${SLOW_PAGE}
    Get Title    ==    Slow page
