*** Settings ***
Resource          imports.resource

*** Test Cases ***
Enable Tracing To File
    New Context    tracing=trace_1.zip
    New Page    ${LOGIN_URL}
    Click    button
    Close Context
    ${tmp_traces} =    Set Variable    ${OUTPUT_DIR}/browser/traces
    ${count} =    Glob Files Count    ${tmp_traces}
    Should Be True    ${count} == ${0}
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_1.zip

When Not Enabled No Trace File
    New Context
    New Page    ${LOGIN_URL}
    Close Context
    ${tmp_traces} =    Set Variable    ${OUTPUT_DIR}/browser/traces
    ${count} =    Glob Files Count    ${tmp_traces}
    Should Be True    ${count} == ${0}
    Wait File Count In Directory    ${OUTPUT_DIR}    1    trace*.zip

