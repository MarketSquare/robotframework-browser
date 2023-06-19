*** Settings ***
Resource        imports.resource

Suite Setup     New Browser    headless=${HEADLESS}

*** Test Cases ***
Har Path Only Defined
    ${har} =    Create Dictionary    path=${OUTPUT_DIR}/har-1.file
    New Context    recordHar=${har}
    New Page    ${LOGIN_URL}
    Close Context
    File Should Not Be Empty    ${OUTPUT_DIR}/har-1.file

Har Path And OmitContent Defined
    ${har} =    Create Dictionary    path=${OUTPUT_DIR}/har-2.file    omitContent=True
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
