*** Settings ***
Library      Browser    jsextension=${CURDIR}/adopt.js
Library      OperatingSystem
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

An Adopted Context Is Traced And Accepts Downloads
    Open Adopted Persistent Context With Tracing And Downloads
    ...    ${OUTPUT_DIR}/adopted-profile-traced    ${LOGIN_URL}    ${HEADLESS}    ${OUTPUT_DIR}/adopted-trace.zip
    ${download_url} =    Get Property    id=file_download    href
    ${download} =    Download    ${download_url}
    File Should Exist    ${download}[saveAs]
    Close Browser
    File Should Exist    ${OUTPUT_DIR}/adopted-trace.zip
