*** Settings ***
Resource          imports.resource
Suite Setup       New Browser

*** Test Cases ***
Create Video
    New Context    videosPath=${OUTPUT_DIR}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}

Create Video With videoSize
    ${size} =    Create Dictionary    width    300    height    200
    New Context    videosPath=${OUTPUT_DIR}    videoSize=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}

Create Video With viewport
    ${size} =    Create Dictionary    width    400    height    250
    New Context    videosPath=${OUTPUT_DIR}    viewport=${size}
    New Page    ${LOGIN_URL}
    Go To    ${FRAMES_URL}

No Video
    New Context
    New Page    ${LOGIN_URL}
