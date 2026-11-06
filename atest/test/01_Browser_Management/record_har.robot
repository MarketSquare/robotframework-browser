*** Settings ***
Resource       imports.resource

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

Har With Content Mode And UrlFilter Defined
    VAR    &{har} =    path=${OUTPUT_DIR}/filtered.har    content=omit    mode=minimal    urlFilter=**/*.js
    New Context    recordHar=${har}
    New Page    ${LOGIN_URL}
    Close Context
    ${log} =    Evaluate    json.load(open(r"${OUTPUT_DIR}/filtered.har"))["log"]    modules=json
    Should Not Be Empty    ${log}[entries]
    FOR    ${entry}    IN    @{log}[entries]
        Should End With    ${entry}[request][url]    .js
        Dictionary Should Not Contain Key    ${entry}[response][content]    text
    END
    Dictionary Should Not Contain Key    ${log}    pages
