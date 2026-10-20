*** Settings ***
Library      ../../library/AdoptingLibrary.py    jsextension=${CURDIR}/adopt.js
Library      ArchiveLibrary
Library      Collections
Library      OperatingSystem
Library      ../../library/tracing_groups.py
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

An Adopted Context Records Its Video In The Size Of Its Viewport
    Open Adopted Context With Recording
    ...    ${OUTPUT_DIR}/adopted-profile-viewport    ${LOGIN_URL}    ${HEADLESS}
    ...    tracing=${None}    record_video={}    viewport={"width": 800, "height": 600}
    ${size} =    Video Size Of The Active Context
    Should Be Equal    ${size}    ${{ {"width": 800, "height": 600} }}
    [Teardown]    Close Browser

An Adopted Context Records Its Video In The Size It Was Given
    Open Adopted Context With Recording
    ...    ${OUTPUT_DIR}/adopted-profile-video-size    ${LOGIN_URL}    ${HEADLESS}
    ...    tracing=${None}    record_video={"size": {"width": 640, "height": 480}}
    ...    viewport={"width": 800, "height": 600}
    ${size} =    Video Size Of The Active Context
    Should Be Equal    ${size}    ${{ {"width": 640, "height": 480} }}
    [Teardown]    Close Browser
