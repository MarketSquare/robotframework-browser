*** Settings ***
Resource    ../imports.resource
Library     ../../../library/trace_files.py

*** Test Cases ***
Suite Scope Trace Is Left Running When The Suite Ends
    Start Tracing    scope=Suite
    Mark    MARK_suite_end
