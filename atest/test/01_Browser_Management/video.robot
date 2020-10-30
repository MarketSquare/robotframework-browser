*** Settings ***
Resource          imports.resource

*** Test Cases ***
Create Video
    New Browser
    New Context    videosPath=${OUTPUT_DIR}
    New Page    ${LOGIN_URL}
    ${c} =    Get Browser Catalog
    Log    ${c}
