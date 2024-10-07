*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Teardown

*** Test Cases ***
New Page Will Not Timeout
    [Tags]    slow
    New Page    ${SLOW_PAGE}
    Get Title    ==    Slow page

New Page Will Timeout And Page Will Be Removed From Catalog
    [Tags]    slow
    Set Browser Timeout    1s
    New Context
    ${Catalog} =    Get Browser Catalog
    TRY
        New Page    ${SLOW_PAGE}
    EXCEPT    *Timeout*    type=glob
        ${new_catalog} =    Get Browser Catalog
        Should Be Equal    ${Catalog}    ${new_catalog}
    ELSE
        Fail    Expected timeout
    END

*** Keywords ***
Setup
    Set Browser Timeout    15s    scope=Suite
    ${original} =    Register Keyword To Run On Failure    ${None}
    Set Suite Variable    $original
    New Browser    headless=${HEADLESS}

Teardown
    Register Keyword To Run On Failure    ${original}
    Close Browser
