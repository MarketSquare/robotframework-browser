*** Settings ***
Resource    ../variables.resource
Resource    trace_groups_of_two_contexts.resource
Library     Browser    tracing_group_mode=Browser

*** Test Cases ***
Each Of Two Traced Contexts Shows Only Its Own Keywords
    Trace Two Contexts At The Same Time    ${OUTPUT_DIR}/two-contexts-browser
    Trace A Should Show Only The Keywords That Ran On A    ${OUTPUT_DIR}/two-contexts-browser
    Trace B Should Show Only The Keywords That Ran On B    ${OUTPUT_DIR}/two-contexts-browser
    [Teardown]    Close Context    ALL
