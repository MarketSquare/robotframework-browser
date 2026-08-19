*** Settings ***
Resource            imports.resource

Suite Setup         Tracing Timeout
Suite Teardown      Set Browser Timeout    ${OLD_BROWSER_TIMEOUT}

*** Test Cases ***
Enable Tracing To File
    [Tags]    slow
    New Context    tracing=trace_0.zip
    New Page    ${LOGIN_URL}
    Click    id=goes_hidden
    Close Context
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} == ${0}
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_0.zip

When Not Enabled No Trace File
    [Tags]    slow    # Depends on previous test
    New Context
    New Page    ${LOGIN_URL}
    Close Context
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} == ${0}
    Wait File Count In Directory    ${OUTPUT_DIR}    1    trace*.zip

Enable Tracing To File With Two Browsers
    [Tags]    slow
    [Timeout]    90s
    ${browser1} =    New Browser    headless=${HEADLESS}
    New Context    tracing=trace_1.zip
    New Page    ${LOGIN_URL}
    ${browser2} =    New Browser    headless=${HEADLESS}    reuse_existing=False
    New Context    tracing=trace_2.zip
    New Page    ${FORM_URL}
    Click    //input[@name="submit"]
    Close Context
    Switch Browser    ${browser1}
    New Page    ${LOGIN_URL}
    Click    id=goes_hidden
    Close Context
    Close Browser    ALL
    ${count} =    Glob Files Count    ${OUTPUT_DIR}/browser/traces
    Should Be True    ${count} > ${1}    # There are leftover files
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_1.zip
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_2.zip

Check Show-Trace Command Help
    [Timeout]    60s
    ${help} =    Run Rfbrowser Show Trace Help
    Should Contain    ${help}    Start the Playwright trace viewer.
    Should Contain    ${help}    --stdin
    Should Contain    ${help}    show-trace [OPTIONS] [FILE]

Check Show-Trace Command
    [Tags]    slow    no-windows-support    # slow: needs trace_1.zip from the test above
    [Timeout]    90s
    ${process}    ${procss_stdout_file} =    Start Show Trace    ${OUTPUT_DIR}/trace_1.zip
    Check Trace Process    ${process}    ${procss_stdout_file}
    [Teardown]    Stop Show Trace

Tracing And Closing All Browsers
    [Tags]    slow
    [Timeout]    90s
    New Browser    headless=${HEADLESS}
    New Context    tracing=trace_10.zip
    New Page    ${LOGIN_URL}
    Click    id=login_button
    New Page    ${LOGIN_URL}
    Click    id=login_button
    Close Browser    ALL
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_10.zip

Tracing And Closing Current Browsers
    [Tags]    slow
    [Timeout]    90s
    New Browser    headless=${HEADLESS}
    New Context    tracing=trace_20.zip
    New Context    tracing=trace_21.zip
    New Page    ${LOGIN_URL}
    Click    id=login_button
    New Page    ${LOGIN_URL}
    Click    id=login_button
    Close Browser    CURRENT
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_20.zip
    File Should Not Be Empty    ${OUTPUT_DIR}/trace_21.zip

*** Keywords ***
Tracing Timeout
    ${OLD_BROWSER_TIMEOUT} =    Set Browser Timeout    15s
    VAR    ${OLD_BROWSER_TIMEOUT} =    ${OLD_BROWSER_TIMEOUT}    scope=SUITE
    Remove Directory    ${OUTPUT_DIR}/browser/traces/    recursive=True
    Create Directory    ${OUTPUT_DIR}/browser/traces/
