*** Settings ***
Library      Browser    jsextension=${CURDIR}/adopt.js
Resource     ../variables.resource

Test Tags    no-iframe

*** Test Cases ***
Browser Keywords Work On A Context Adopted By A JavaScript Extension
    ${adopted} =    Open Adopted Persistent Context    ${OUTPUT_DIR}/adopted-profile    ${LOGIN_URL}    ${HEADLESS}
    Get Browser Ids    ACTIVE    contains    ${adopted}[browserId]
    Get Browser Catalog    validate    [b["type"] for b in value if b["id"] == "${adopted}[browserId]"] == ["adopted"]
    Get Text    h1    ==    Login Page
    Close Browser
    ${closed} =    Adopted Context Is Closed
    Should Be True    ${closed}
    ${on_close_called} =    Adopted Context On Close Was Called
    Should Be True    ${on_close_called}
