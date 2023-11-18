*** Settings ***
Resource            imports.resource

Suite Setup         Close Browser    ALL
Test Teardown       Close Browser    ALL

*** Variables ***
${ARGS} =       ["--user-agent FAKE_AGENT"]

*** Test Cases ***
New Browser With Reuse_existing Does Not Open New Browser If Matching One Exists
    ${browser_id} =    New Browser    reuse_existing=True
    ${catalog} =    Get Browser Catalog
    ${new_browser_id} =    New Browser    reuse_existing=True
    ${new_catalog} =    Get Browser Catalog
    Should Be Equal    ${browser_id}    ${new_browser_id}
    Should Be Equal    ${catalog}    ${new_catalog}

New Browser With Reuse_existing Opens New Browser If No Matching One Is Found
    [Tags]    firefox
    ${browser_id} =    New Browser    browser=firefox    reuse_existing=True
    ${catalog} =    Get Browser Catalog
    Should Be True    len($catalog) == 1
    ${new_browser_id} =    New Browser    reuse_existing=True
    ${new_catalog} =    Get Browser Catalog
    Should Not Be Equal    ${browser_id}    ${new_browser_id}
    Should Not Be Equal    ${catalog}    ${new_catalog}
    Should Be True    len($new_catalog) == 2

New Browser Behaviour With List Arguments
    ${browser_id} =    New Browser
    ...    browser=chromium
    ...    headless=True
    ...    args=${ARGS}
    ...    channel=${NONE}
    ...    devtools=True
    ...    downloadsPath=${OUTPUTDIR}
    ...    env=${NONE}
    ...    executablePath=${NONE}
    ...    proxy=${NONE}
    ...    reuse_existing=False
    ...    slowMo=200 ms
    ${catalog} =    Get Browser Catalog
    ${new_browser_id} =    New Browser
    ...    reuse_existing=True
    ...    args=${ARGS}
    ...    downloadsPath=${OUTPUTDIR}
    ...    slowMo=200 ms
    ...    devtools=True
    ...    timeout=30 seconds
    ${new_catalog} =    Get Browser Catalog
    Should Be Equal    ${browser_id}    ${new_browser_id}
    Should Be Equal    ${catalog}    ${new_catalog}
    Should Be Equal    ${browser_id}    ${new_browser_id}
    New Browser    reuse_existing=True    args=["--user-agent DIFFERENT"]
    ${third_catalog} =    Get Browser Catalog
    Should Not Be Equal    ${catalog}    ${third_catalog}
    Close Browser    ${new_browser_id}
    ${last_browser_id} =    New Browser
    ...    reuse_existing=False
    ...    args=${ARGS}
    ...    downloadsPath=${OUTPUTDIR}
    ...    slowMo=200 ms
    ...    devtools=True
    ...    timeout=30 seconds
    Should Not Be Equal    ${last_browser_id}    ${new_browser_id}
    Should Be True    len($third_catalog) == 2

New Browser Reuse Switching
    ${browser_id} =    New Browser
    ...    browser=chromium
    ...    headless=True
    ...    args=${ARGS}
    ...    channel=${NONE}
    ...    devtools=True
    ...    downloadsPath=${OUTPUTDIR}
    ...    env=${NONE}
    ...    executablePath=${NONE}
    ...    proxy=${NONE}
    ...    reuse_existing=False
    ...    slowMo=200 ms
    New Page    ${LOGIN_URL}
    ${title} =    Get Title
    New Browser    reuse_existing=True    args=["--user-agent DIFFERENT"]
    New Page    ${FORM_URL}
    ${new_title} =    Get Title    !=    ${title}
    ${new_browser_id} =    New Browser
    ...    reuse_existing=True
    ...    args=${ARGS}
    ...    downloadsPath=${OUTPUTDIR}
    ...    slowMo=200 ms
    ...    devtools=True
    ...    timeout=30 seconds
    Get Title    ==    ${title}
