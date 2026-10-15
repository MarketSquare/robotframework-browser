*** Settings ***
Library      ../../library/AdoptingLibrary.py    jsextension=${CURDIR}/adopt.js
Library      ArchiveLibrary
Library      Collections
Library      OperatingSystem
Library      ../01_Browser_Management/tracing_groups.py
Resource     ../variables.resource

Test Tags    no-iframe

*** Test Cases ***
A Library Built On Browser Traces And Records An Adopted Context
    ${video} =    Open Adopted Context With Recording
    ...    ${OUTPUT_DIR}/adopted-profile-recorded    ${LOGIN_URL}    ${HEADLESS}
    ...    ${OUTPUT_DIR}/adopted-recording.zip    {}
    Get Text    h1    ==    Login Page
    Close Browser
    Should Contain    ${video}    browser${/}video
    File Should Not Be Empty    ${video}
    Extract Zip File    ${OUTPUT_DIR}/adopted-recording.zip    ${OUTPUT_DIR}/adopted-recording
    ${groups} =    Get Trace Group Titles    ${OUTPUT_DIR}/adopted-recording/trace.trace
    Should Contain Match    ${groups}    AdoptingLibrary.Open Adopted Context With Recording*
    Should Contain Match    ${groups}    AdoptingLibrary.Get Text*
