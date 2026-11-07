*** Settings ***
Resource    ../imports.resource
Library     ../../../library/trace_files.py

*** Variables ***
${TRACES} =    ${OUTPUT_DIR}${/}browser${/}traces

*** Test Cases ***
Suite Scope Trace Was Saved When Its Suite Ended
    Run Keyword And Expect Error    *No trace is running*    Stop Tracing
    ${traces} =    Find Traces With Mark    ${TRACES}    MARK_suite_end
    Length Should Be    ${traces}    1
