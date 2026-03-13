*** Settings ***
Library             ../../library/electron_setup.py
Resource            imports.resource

Suite Setup         Setup Electron Test Suite
Suite Teardown      Close Electron Application

*** Variables ***
${ELECTRON_APP_DIR} =       ${CURDIR}${/}..${/}..${/}..${/}node${/}electron-test-app
${ELECTRON_APP_MAIN} =      ${ELECTRON_APP_DIR}${/}main.js
${ELECTRON_BIN} =           ${EMPTY}

*** Test Cases ***
New Electron Application Returns Browser Context And Page Ids
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    ${browser_id}    ${context_id}    ${page_details} =    New Electron Application
    ...    executable_path=${ELECTRON_BIN}    args=@{args}
    Should Not Be Empty    ${browser_id}
    Should Not Be Empty    ${context_id}
    Should Not Be Empty    ${page_details.page_id}
    [Teardown]    Close Electron Application

Title Is Correct After Launch
    Launch Test App
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Heading Text Is Readable
    Launch Test App
    Get Text    css=h1#title    ==    Electron Test App
    [Teardown]    Close Electron Application

Click Increments Counter
    Launch Test App
    Get Text    css=#click-counter    ==    0
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    1
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    2
    [Teardown]    Close Electron Application

Fill Text Updates Input Value
    Launch Test App
    Fill Text    css=#text-input    Hello Electron
    Get Property    css=#text-input    value    ==    Hello Electron
    [Teardown]    Close Electron Application

Fill Text Triggers Input Event
    Launch Test App
    Fill Text    css=#text-input    live update
    Get Text    css=#description    ==    live update
    [Teardown]    Close Electron Application

Select Option Works
    Launch Test App
    Select Options By    css=#select-box    value    two
    Get Selected Options    css=#select-box    value    ==    two
    [Teardown]    Close Electron Application

Check Checkbox Works
    Launch Test App
    Get Checkbox State    css=#checkbox    ==    False
    Check Checkbox    css=#checkbox
    Get Checkbox State    css=#checkbox    ==    True
    [Teardown]    Close Electron Application

Wait For Elements State Works
    Launch Test App
    Wait For Elements State    css=#toggle-target    hidden
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    visible
    Get Text    css=#toggle-target    ==    Now you see me
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    hidden
    [Teardown]    Close Electron Application

Async Content Appears After Delay
    Launch Test App
    Wait For Elements State    css=#async-output    hidden
    Click    css=#btn-async
    Wait For Elements State    css=#async-output    visible    timeout=5s
    Get Text    css=#async-output    ==    Loaded
    [Teardown]    Close Electron Application

Keyboard Input Works
    Launch Test App
    Fill Text    css=#text-input    to be deleted
    Click    css=#text-input
    Keyboard Key    press    Control+a
    Keyboard Key    press    Delete
    Get Property    css=#text-input    value    ==    ${EMPTY}
    [Teardown]    Close Electron Application

File Input Accepts A File
    Launch Test App
    Upload File By Selector    css=#file-input    ${ELECTRON_APP_DIR}${/}package.json
    Get Text    css=#file-name    ==    package.json
    [Teardown]    Close Electron Application

Evaluate JavaScript Returns Promise Result
    Launch Test App
    ${result} =    Evaluate JavaScript    css=#title
    ...    async (el) => { await new Promise(r => setTimeout(r, 50)); return el.textContent.trim(); }
    Should Be Equal    ${result}    Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With Explicit Timeout
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    timeout=30 seconds
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Close Electron Application Removes Active Browser
    Launch Test App
    Close Electron Application
    Run Keyword And Expect Error    *    Get Title

Close Electron Application When No App Open Is Safe
    Close Electron Application

New Electron Application With Invalid Path Raises Error
    Run Keyword And Expect Error    *
    ...    New Electron Application    executable_path=/nonexistent/electron
    [Teardown]    Close Electron Application

New Electron Application With Extra Args
    @{args} =    Create List    ${ELECTRON_APP_MAIN}    --no-sandbox
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With slowMo
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    slowMo=100ms
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With colorScheme Dark
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    colorScheme=dark
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With acceptDownloads False
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    acceptDownloads=False
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With bypassCSP
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    bypassCSP=True
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Open Electron Dev Tools Does Not Raise
    Launch Test App
    Open Electron Dev Tools
    [Teardown]    Close Electron Application

*** Keywords ***
Setup Electron Test Suite
    ${ELECTRON_BIN} =    Get Electron Binary Path    ${ELECTRON_APP_DIR}
    Set Suite Variable    ${ELECTRON_BIN}

Launch Test App
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
