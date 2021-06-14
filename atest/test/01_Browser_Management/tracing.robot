*** Settings ***
Resource          imports.resource

*** Test Cases ***
Enable Tracing To File
    New Context    tracing=trace_1.zip
    New Page    ${LOGIN_URL}
    Click    button
    Close Context
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} == ${0}
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_1.zip

When Not Enabled No Trace File
    New Context
    New Page    ${LOGIN_URL}
    Close Context
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} == ${0}
    Wait File Count In Directory    ${OUTPUT_DIR}    1    trace*.zip

Enable Tracing To File With Two Brwosers
    ${browser1} =    New Browser
    New Context    tracing=trace_1.zip
    New Page    ${LOGIN_URL}
    ${browser2} =    New Browser
    New Context    tracing=trace_2.zip
    New Page    ${FORM_URL}
    Click    //input[@name="submit"]
    Close Context
    Switch Browser    ${browser1}
    New Page    ${LOGIN_URL}
    Click    button
    Close Context
    Close Browser    ALL
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} > ${1}    # There are leftover files
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_1.zip
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_2.zip
