*** Settings ***
Library    ArchiveLibrary
Library    Collections
Library    ../../library/tracing_groups.py

*** Keywords ***
Trace Two Contexts At The Same Time
    [Arguments]    ${dir}
    ${a} =    New Context    tracing=${dir}/a.zip
    New Page    about:blank
    ${b} =    New Context
    New Page    about:blank
    Start Tracing    scope=Test
    Switch Context    ${a}
    Get Title
    Switch Context    ${b}
    ${b_trace} =    Stop Tracing    path=${dir}/b.zip
    Close Context    ${a}
    Extract Zip File    zip_file=${dir}/a.zip    dest=${dir}/a/
    Extract Zip File    zip_file=${b_trace}    dest=${dir}/b/

Trace A Should Show Only The Keywords That Ran On A
    [Arguments]    ${dir}
    ${groups} =    Get Trace Group Titles    ${dir}/a/trace.trace
    Should Contain Match    ${groups}    Browser.Get Title*
    Match Count Should Be    ${groups}    Browser.New Context*    1
    Match Count Should Be    ${groups}    Browser.New Page*    1
    Match Count Should Be    ${groups}    Browser.Switch Context*    1
    Should Contain Match    ${groups}    Browser.Close Context*
    Should Not Contain Match    ${groups}    Browser.Start Tracing*
    Should Not Contain Match    ${groups}    Browser.Stop Tracing*

Trace B Should Show Only The Keywords That Ran On B
    [Arguments]    ${dir}
    ${groups} =    Get Trace Group Titles    ${dir}/b/trace.trace
    Should Contain Match    ${groups}    Browser.Start Tracing*
    Should Contain Match    ${groups}    Browser.Stop Tracing*
    Match Count Should Be    ${groups}    Browser.Switch Context*    1
    Should Not Contain Match    ${groups}    Browser.Get Title*
    Should Not Contain Match    ${groups}    Browser.Close Context*

Match Count Should Be
    [Arguments]    ${groups}    ${pattern}    ${expected}
    ${count} =    Get Match Count    ${groups}    ${pattern}
    Should Be Equal As Integers    ${count}    ${expected}    ${pattern} in ${groups}
