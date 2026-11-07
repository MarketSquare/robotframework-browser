*** Settings ***
Resource          ../variables.resource
Library           Browser    auto_delete_passed_tracing=True
Library           OperatingSystem
Library           ../../library/trace_files.py

Suite Setup       Open Suite Context
Suite Teardown    Close Browser    ALL

*** Variables ***
${TRACES} =    ${OUTPUT_DIR}${/}browser${/}traces

*** Test Cases ***
Trace Ending With A Passed Test Is Not Saved
    Start Tracing    scope=Test
    Mark    MARK_passed_test_scope

Trace Of The Passed Test Was Not Saved
    Run Keyword And Expect Error    *No trace is running*    Stop Tracing
    ${traces} =    Find Traces With Mark    ${TRACES}    MARK_passed_test_scope
    Should Be Empty    ${traces}

Trace Stopped By The Test Is Kept
    Start Tracing    scope=Test
    Mark    MARK_stopped_by_test
    ${trace} =    Stop Tracing    path=ad_hoc_kept.zip
    Set Suite Variable    ${KEPT_TRACE}    ${trace}

Trace Stopped By The Passed Test Still Exists
    File Should Not Be Empty    ${KEPT_TRACE}

*** Keywords ***
Open Suite Context
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Context
    New Page    ${LOGIN_URL}
