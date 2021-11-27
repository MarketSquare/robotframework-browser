*** Settings ***
Resource        imports.resource

Suite Setup     Video Setup

*** Test Cases ***
Create Video With Full Path
    [Documentation]
    ...    LOG 5:3    INFO    GLOB:    *video width="1280" height="720" controls*src="video*.webm"*
    ${files} =    Glob Files Count    ${OUTPUT_DIR}/video
    Should Be Equal    ${0}    ${files}
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    ${True}    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    1

Create Video With Relative Path
    [Documentation]
    ...    LOG 5:3    INFO    GLOB:    *video width="1280" height="720" controls*src="browser/video/my_video*.webm"*
    ${files} =    Glob Files Count    ${OUTPUT_DIR}/browser/video/my_video
    Should Be Equal    ${0}    ${files}
    ${record_video} =    Create Dictionary    dir    my_video
    New Context    recordVideo=${record_video}
    ${details} =    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Close Context
    Wait File Count In Directory    ${OUTPUT_DIR}/browser/video/my_video    ${1}
    Should Start With    ${details}[video_path]    ${OUTPUT_DIR}/browser/video/my_video
    Should End With    ${details}[video_path]    .webm

Create Video With videoSize
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="300" height="200"*.webm"*
    ${size} =    Create Dictionary    width    300    height    200
    ${record_video} =    Create Dictionary    size    ${size}    dir    ${OUTPUT_DIR}/video
    New Context    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${2}

Create Video With viewport
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="400" height="250"*.webm"*
    ${size} =    Create Dictionary    width    400    height    250
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    recordVideo=${record_video}    viewport=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${3}

No Video
    [Documentation]
    ...    LOG 2:3    DEBUG    Video is not enabled.
    New Context
    New Page    ${LOGIN_URL}
    Verify Video Files    ${3}

Create Video With Deprecated Options
    [Documentation]
    ...    LOG 3:3    INFO    GLOB:    *width="300" height="200"*.webm"*
    ...    LOG 2:2    WARN    Browser library New Context keyword has deprecated videosPath, use recordVideo
    ...    LOG 2:3    WARN    Browser library New Context keyword has deprecated videoSize, use recordVideo
    ${size} =    Create Dictionary    width    300    height    200
    New Context    videosPath=${OUTPUT_DIR}/video    videoSize=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    4

*** Keywords ***
Video Setup
    New Browser
    OperatingSystem.Remove Directory    ${OUTPUT_DIR}/video    recursive=True

Verify Video Files
    [Arguments]    ${count}
    Close Page
    Wait File Count In Directory    ${OUTPUT_DIR}/video    ${count}
