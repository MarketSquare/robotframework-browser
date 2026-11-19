*** Settings ***
Resource       imports.resource
Library        ../../library/har_files.py

Suite Setup    New Browser    headless=${HEADLESS}

*** Test Cases ***
Har Path Only Defined
    VAR    &{har} =    path=${OUTPUT_DIR}/har-1.file
    New Context    recordHar=${har}
    New Page    ${LOGIN_URL}
    Close Context
    File Should Not Be Empty    ${OUTPUT_DIR}/har-1.file

Har Path And OmitContent Defined
    VAR    &{har} =    path=${OUTPUT_DIR}/har-2.file    omitContent=True
    New Context    recordHar=${har}
    New Page    ${LOGIN_URL}
    Close Context
    File Should Not Be Empty    ${OUTPUT_DIR}/har-2.file

Har Path And OmitContent Defined As String
    New Context    recordHar={"path": r"${OUTPUT_DIR}/har-3.file", "omitContent": "True"}
    New Page    ${LOGIN_URL}
    Close Context
    File Should Not Be Empty    ${OUTPUT_DIR}/har-3.file

No Har Created
    Remove File    path
    New Context
    New Page    ${LOGIN_URL}
    Close Context
    ${files} =    List Files In Directory    ${OUTPUT_DIR}    har*
    Length Should Be    ${files}    3

Relative Har Path Is Relative To The Output Directory
    New Context    recordHar={"path": "relative-path.har"}
    New Page    ${LOGIN_URL}
    Close Context
    File Should Not Be Empty    ${OUTPUT_DIR}/relative-path.har

Minimal Har Records No Pages
    New Context    recordHar={"path": "minimal.har", "mode": "minimal"}
    New Page    ${LOGIN_URL}
    Close Context
    Har Should Not Have Pages    ${OUTPUT_DIR}/minimal.har

Har Records Only The Requests That Match A Glob
    New Context    recordHar={"path": "api-glob.har", "urlFilter": "**/api/get/**"}
    New Page    ${ROOT_URL}delayed-load.html
    Get Text    id=server_delayed_response    ==    after some time I respond
    Close Context
    ${paths} =    Get Har Request Paths    ${OUTPUT_DIR}/api-glob.har
    Should Be Equal    ${paths}    ${{["/api/get/delay"]}}

Har Records Only The Requests That Match A Regex
    New Context    recordHar={"path": "api-regex.har", "urlFilter": "/\\.JS$/i"}
    New Page    ${ROOT_URL}delayed-load.html
    Get Text    id=server_delayed_response    ==    after some time I respond
    Close Context
    ${paths} =    Get Har Request Paths    ${OUTPUT_DIR}/api-regex.har
    Should Be Equal    ${paths}    ${{["/test-app-logger.js"]}}

Unknown Har Mode Fails
    Run Keyword And Expect Error
    ...    *cannot be converted to RecordHar*
    ...    New Context    recordHar={"path": "unknown-mode.har", "mode": "tiny"}
