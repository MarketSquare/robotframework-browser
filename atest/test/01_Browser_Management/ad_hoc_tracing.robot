*** Settings ***
Resource          imports.resource
Library           ../../library/trace_files.py

Suite Setup       Open Suite Context
Suite Teardown    Close Context    ALL    ALL

*** Variables ***
${TRACES} =    ${OUTPUT_DIR}${/}browser${/}traces

*** Test Cases ***
Trace Holds Only What Happened Between Start And Stop
    Mark    MARK_before_start
    Start Tracing
    Mark    MARK_while_tracing
    ${trace} =    Stop Tracing    path=ad_hoc_between.zip
    Mark    MARK_after_stop
    Trace Should Be    ${trace}    ${OUTPUT_DIR}    ad_hoc_between.zip
    ${marks} =    Get Trace Marks    ${trace}
    Should Be Equal    ${marks}    ${{['MARK_while_tracing']}}

One Context Records Several Traces One After Another
    Start Tracing    title=First
    Mark    MARK_first_trace
    ${first} =    Stop Tracing
    Start Tracing    title=Second
    Mark    MARK_second_trace
    ${second} =    Stop Tracing
    Should Not Be Equal    ${first}    ${second}
    Trace Should Be In Directory    ${first}    ${TRACES}
    ${first_marks} =    Get Trace Marks    ${first}
    ${second_marks} =    Get Trace Marks    ${second}
    Should Be Equal    ${first_marks}    ${{['MARK_first_trace']}}
    Should Be Equal    ${second_marks}    ${{['MARK_second_trace']}}

Stop Tracing Saves Into A Directory Under The Traces Folder
    Start Tracing
    Mark    MARK_into_directory
    ${trace} =    Stop Tracing    path=ad_hoc_dir
    Trace Should Be In Directory    ${trace}    ${TRACES}    ad_hoc_dir
    File Should Not Be Empty    ${trace}

Starting A Second Trace Fails
    Start Tracing
    Run Keyword And Expect Error    *Tracing is already running*    Start Tracing
    Stop Tracing

Stopping Without A Running Trace Fails
    Run Keyword And Expect Error    *No trace is running*    Stop Tracing

Test Scope Trace Ends With Its Test
    Start Tracing    scope=Test
    Mark    MARK_test_scope

Test Scope Trace Was Saved When Its Test Ended
    Run Keyword And Expect Error    *No trace is running*    Stop Tracing
    ${traces} =    Find Traces With Mark    ${TRACES}    MARK_test_scope
    Length Should Be    ${traces}    1

Suite Scope Trace Outlives Its Test
    Start Tracing
    Mark    MARK_suite_scope

Suite Scope Trace Is Still Running In The Next Test
    Run Keyword And Expect Error    *Tracing is already running*    Start Tracing
    ${trace} =    Stop Tracing
    ${marks} =    Get Trace Marks    ${trace}
    Should Be Equal    ${marks}    ${{['MARK_suite_scope']}}

Trace Is Saved When Its Context Closes First
    New Context
    New Page    ${LOGIN_URL}
    Start Tracing
    Mark    MARK_context_closed_first

Trace Of A Context Closed At Test End Was Saved
    ${traces} =    Find Traces With Mark    ${TRACES}    MARK_context_closed_first
    Length Should Be    ${traces}    1

Stop Tracing Stops A Context Trace
    New Context    tracing=ad_hoc_context_trace.zip
    New Page    ${LOGIN_URL}
    Mark    MARK_context_trace
    ${trace} =    Stop Tracing
    Trace Should Be    ${trace}    ${OUTPUT_DIR}    ad_hoc_context_trace.zip
    Start Tracing
    Stop Tracing    path=ad_hoc_after_context_trace.zip
    Close Context
    ${marks} =    Get Trace Marks    ${trace}
    Should Be Equal    ${marks}    ${{['MARK_context_trace']}}

Starting On A Context Trace Fails
    New Context    tracing=True
    Run Keyword And Expect Error    *Tracing is already running*    Start Tracing
    Close Context

*** Keywords ***
Open Suite Context
    New Context
    New Page    ${LOGIN_URL}
