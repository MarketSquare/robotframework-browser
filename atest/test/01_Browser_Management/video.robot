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
    New Context    acceptDownloads=${True}    recordVideo=${record_video}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    1
    Should Be Equal    ${record_video.dir}    ${OUTPUT_DIR}/video

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
    Should Start With    ${details}[video_path]    ${OUTPUT_DIR}${/}browser${/}video${/}my_video
    Should End With    ${details}[video_path]    .webm
    Should Be Equal    ${record_video.dir}    my_video
    New Context    viewport={'width': 2048, 'height': 1200}
    New Page    file://${details}[video_path]
    Get BoundingBox    video    ALL    validate    value['width'] == 1280 and value['height'] == 720

Create Video With VideoSize
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="300" height="200"*.webm"*
    ${size} =    Create Dictionary    width    300    height    ${200}
    ${record_video} =    Create Dictionary    size    ${size}
    New Context    recordVideo=${record_video}
    ${details} =    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Close Context    CURRENT
    Wait Until File Exists    ${details}[video_path]
    New Context    viewport={'width': 2048, 'height': 1200}
    New Page    file://${details}[video_path]
    Get BoundingBox    video    ALL    validate    value['width'] == 300 and value['height'] == 200

Create Video With Viewport
    [Documentation]
    ...    LOG 4:3    INFO    GLOB:    *width="400" height="250"*.webm"*
    ${size} =    Create Dictionary    width    400    height    250
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    recordVideo=${record_video}    viewport=${size}
    ${details} =    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${2}
    New Context    viewport={'width': 2048, 'height': 1200}
    New Page    file://${details}[video_path]
    Get BoundingBox    video    ALL    validate    value['width'] == 400 and value['height'] == 250

No Video
    [Documentation]
    ...    LOG 2:3    DEBUG    Video is not enabled.
    New Context
    New Page    ${LOGIN_URL}
    Verify Video Files    ${2}

Video Must Be Created When Close Browser Is Called
    [Setup]    OperatingSystem.Remove Directory    ${OUTPUT_DIR}/video    recursive=True
    ${record_video} =    Create Dictionary    dir    ${OUTPUT_DIR}/video
    New Context    acceptDownloads=${True}    recordVideo=${record_video}
    ${details} =    New Page    ${LOGIN_URL}
    Close Browser    ALL
    Wait Until File Exists    ${details}[video_path]
    New Context    viewport={'width': 2048, 'height': 1200}
    New Page    file://${details}[video_path]
    Get BoundingBox    video    ALL    validate    value['width'] == 1280 and value['height'] == 720

*** Keywords ***
Video Setup
    New Browser    headless=${HEADLESS}
    OperatingSystem.Remove Directory    ${OUTPUT_DIR}/video    recursive=True

Verify Video Files
    [Arguments]    ${count}
    Close Page
    Wait File Count In Directory    ${OUTPUT_DIR}/video    ${count}
