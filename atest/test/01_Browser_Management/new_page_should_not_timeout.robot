*** Settings ***
Resource          imports.resource

Suite Setup       Setup
Suite Teardown    Teardown

*** Test Cases ***
New Page Will Not Timeout
    [Tags]    slow
    New Page    ${SLOW_PAGE}
    Get Title    ==    Slow page

New Page Will Timeout And Page Will Be Removed From Catalog
    [Tags]    slow
    Set Browser Timeout    1s    scope=Test
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

Failure Handling Sees The Page That Stalled While Loading
    [Tags]    slow
    Set Browser Timeout    1s    scope=Test
    New Context
    New Page    about:blank
    ${catalog} =    Get Browser Catalog
    Register Keyword To Run On Failure    Remember Active Page    scope=Test
    TRY
        New Page    ${STALLED_PAGE}
    EXCEPT    *Timeout*    type=glob
        Should Be Equal    ${URL_ON_FAILURE}    ${STALLED_PAGE}
        Should Be Equal    ${TITLE_ON_FAILURE}    Stalled page
        ${catalog_after_failure} =    Get Browser Catalog
        Should Be Equal    ${catalog}    ${catalog_after_failure}
    ELSE
        Fail    Expected timeout
    END

*** Keywords ***
Remember Active Page
    ${url} =    Get Url
    ${title} =    Get Title
    VAR    ${URL_ON_FAILURE} =    ${url}    scope=TEST
    VAR    ${TITLE_ON_FAILURE} =    ${title}    scope=TEST

Setup
    Set Browser Timeout    15s    scope=Suite
    ${original} =    Register Keyword To Run On Failure    ${None}
    VAR    ${original} =    ${original}    scope=SUITE
    New Browser    headless=${HEADLESS}

Teardown
    Register Keyword To Run On Failure    ${original}
    Close Browser
