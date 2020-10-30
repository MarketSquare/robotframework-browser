*** Settings ***
Resource          imports.resource
Suite Setup       Video Setup

*** Test Cases ***
Create Video
    [Documentation]
    ...   LOG 2:3    INFO    GLOB:    *iframe width="1280" height="720" src="video*.webm"*
    New Context    videosPath=${OUTPUT_DIR}/video
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${0}    ${1}

Create Video With videoSize
    [Documentation]
    ...   LOG 3:3    INFO    GLOB:    *width="300" height="200"*.webm"*
    ${size} =    Create Dictionary    width    300    height    200
    New Context    videosPath=${OUTPUT_DIR}/video    videoSize=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${1}    ${2}

Create Video With viewport
    [Documentation]
    ...   LOG 3:3    INFO    GLOB:    *width="400" height="250"*.webm"*
    ${size} =    Create Dictionary    width    400    height    250
    New Context    videosPath=${OUTPUT_DIR}/video    viewport=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}
    Verify Video Files    ${2}    ${3}

No Video
    [Documentation]
    ...   LOG 2:3    DEBUG    Video is not enabled.
    New Context
    New Page    ${LOGIN_URL}
    Verify Video Files    ${3}    ${3}

*** Keywords ***
Video Setup
    New Browser
    OperatingSystem.Remove Directory    ${OUTPUT_DIR}/video    recursive=True

Verify Video Files
    [Arguments]    ${start count}    ${end count}
    ${files} =    List Files In Directory    ${OUTPUT_DIR}/video
    Should Be Equal    ${{len(${files})}}    ${start count}
    Close Page
    ${files} =    List Files In Directory    ${OUTPUT_DIR}/video
    Should Be Equal    ${{len(${files})}}    ${end count}
