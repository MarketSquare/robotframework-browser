*** Settings ***
Documentation       Tests for Electron application support using New Electron Application keyword.
...                 These tests require an Electron executable to be available.
...                 Set the ELECTRON_APP environment variable to the path of the Electron executable.
...                 On Windows: set ELECTRON_APP=C:\path\to\your\app.exe
...                 On macOS/Linux: set ELECTRON_APP=/path/to/your/app

Resource            imports.resource
Library             OperatingSystem

*** Variables ***
${ELECTRON_APP}     ${EMPTY}

*** Test Cases ***
New Electron Application Missing Executable Throws
    [Documentation]    Launching Electron with a non-existent path should raise an error.
    Run Keyword And Expect Error    *    New Electron Application    /nonexistent/path/to/app.exe

New Electron Application And Close
    [Documentation]    Launch an Electron app, verify a page is active, then close it.
    ...                Requires ELECTRON_APP environment variable to be set to a valid Electron executable.
    Skip If    '${ELECTRON_APP}' == ''
    ...    Set ELECTRON_APP environment variable to run this test
    ${browser_id}    ${context_id}    ${page_details} =    New Electron Application
    ...    ${ELECTRON_APP}
    Should Not Be Empty    ${browser_id}
    Should Not Be Empty    ${context_id}
    Should Not Be Empty    ${page_details.page_id}
    Close Electron Application

New Electron Application Exposes Active Page
    [Documentation]    After launching Electron, standard Browser keywords should work
    ...                against the Electron first window.
    ...                Requires ELECTRON_APP environment variable to be set.
    Skip If    '${ELECTRON_APP}' == ''
    ...    Set ELECTRON_APP environment variable to run this test
    New Electron Application    ${ELECTRON_APP}
    ${title} =    Get Title
    Log    Electron window title: ${title}
    ${url} =    Get Url
    Log    Electron window URL: ${url}
    [Teardown]    Close Electron Application

New Electron Application With Args
    [Documentation]    Launch Electron app with additional arguments.
    ...                Requires ELECTRON_APP environment variable to be set.
    Skip If    '${ELECTRON_APP}' == ''
    ...    Set ELECTRON_APP environment variable to run this test
    ${args} =    Create List    --no-sandbox    --disable-dev-shm-usage
    New Electron Application    ${ELECTRON_APP}    args=${args}
    ${title} =    Get Title
    Log    Electron window title: ${title}
    [Teardown]    Close Electron Application

Close Electron Application No App Open Is Safe
    [Documentation]    Calling Close Electron Application when no Electron app is open
    ...                should not raise an error.
    Close Electron Application
