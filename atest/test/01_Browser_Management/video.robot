*** Settings ***
Resource        imports.resource

Suite Setup     Video Setup

*** Test Cases ***
Create Video With Full Path
    [Documentation]
    ...    LOG 3:3    INFO    GLOB:    *video width="1280" height="720" controls*src="video*.webm"*
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    ${True}    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${0}    ${1}

Create Video With Relative Path
    [Documentation]
    ...    LOG 3:3    INFO    GLOB:    *video width="1280" height="720" controls*src="browser/video/my_video*.webm"*
    ${record_video} =    Create Dictionary    dir    my_video
    New Context    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    ${files} =    List Files In Directory    ${OUTPUT_DIR}/browser/video/my_video
    Should Be Equal    ${{len(${files})}}    ${0}
    Close Page
    Wait File Count In Directory    ${OUTPUT_DIR}/browser/video/my_video    1

Create Video With videoSize
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="300" height="200"*.webm"*
    ${size} =    Create Dictionary    width    300    height    200
    ${record_video} =    Create Dictionary    size    ${size}    dir    ${OUTPUT_DIR}/video
    New Context    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${1}    ${2}

Create Video With viewport
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="400" height="250"*.webm"*
    ${size} =    Create Dictionary    width    400    height    250
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    recordVideo=${record_video}    viewport=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${2}    ${3}

No Video
    [Documentation]
    ...    LOG 2:3    DEBUG    Video is not enabled.
    New Context
    New Page    ${LOGIN_URL}
    Verify Video Files    ${3}    ${3}

*** Keywords ***
Video Setup
    New Browser
    OperatingSystem.Remove Directory    ${OUTPUT_DIR}/video    recursive=True

Verify Video Files
    [Arguments]    ${start count}    ${end count}
    ${files} =    Wait File Count In Directory    ${OUTPUT_DIR}/video    ${start count}
    Close Page
    ${files} =    Wait File Count In Directory    ${OUTPUT_DIR}/video    ${end count}
