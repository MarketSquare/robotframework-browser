*** Settings ***
Library           ../../library/electron_setup.py
Resource          ../keywords.resource

Suite Setup       Setup Electron Test Suite
Suite Teardown    Close Electron Application
Test Teardown     Close Browser    ALL

Test Tags         requires-electron-app    no-iframe

*** Variables ***
${ELECTRON_APP_DIR} =     ${CURDIR}${/}..${/}..${/}..${/}node${/}electron-test-app
${ELECTRON_APP_MAIN} =    ${ELECTRON_APP_DIR}${/}main.js
${ELECTRON_BIN} =         ${EMPTY}

*** Test Cases ***
New Electron Application Returns Browser Context And Page Ids
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    ${browser_id}    ${context_id}    ${page_details} =    New Electron Application
    ...    executable_path=${ELECTRON_BIN}    args=@{args}
    Should Not Be Empty    ${browser_id}
    Should Not Be Empty    ${context_id}
    Should Not Be Empty    ${page_details}[page_id]

Title Is Correct After Launch
    Launch Test App
    Get Title    ==    Browser Library Electron Test App

Heading Text Is Readable
    Launch Test App
    Get Text    css=h1#title    ==    Electron Test App

Click Increments Counter
    Launch Test App
    Get Text    css=#click-counter    ==    0
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    1
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    2

Fill Text Updates Input Value
    Launch Test App
    Fill Text    css=#text-input    Hello Electron
    Get Property    css=#text-input    value    ==    Hello Electron

Fill Text Triggers Input Event
    Launch Test App
    Fill Text    css=#text-input    live update
    Get Text    css=#description    ==    live update

Select Option Works
    Launch Test App
    Select Options By    css=#select-box    value    two
    Get Selected Options    css=#select-box    value    ==    two

Check Checkbox Works
    Launch Test App
    Get Checkbox State    css=#checkbox    ==    False
    Check Checkbox    css=#checkbox
    Get Checkbox State    css=#checkbox    ==    True

Wait For Elements State Works
    Launch Test App
    Wait For Elements State    css=#toggle-target    hidden
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    visible
    Get Text    css=#toggle-target    ==    Now you see me
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    hidden

Async Content Appears After Delay
    Launch Test App
    Wait For Elements State    css=#async-output    hidden
    Click    css=#btn-async
    Wait For Elements State    css=#async-output    visible    timeout=5s
    Get Text    css=#async-output    ==    Loaded

Keyboard Input Works
    Launch Test App
    Fill Text    css=#text-input    to be deleted
    Click    css=#text-input
    Keyboard Key    press    ControlOrMeta+a
    Keyboard Key    press    Delete
    Get Property    css=#text-input    value    ==    ${EMPTY}

File Input Accepts A File
    Launch Test App
    Upload File By Selector    css=#file-input    ${ELECTRON_APP_MAIN}
    Get Text    css=#file-name    ==    main.js

Evaluate JavaScript Returns Promise Result
    Launch Test App
    ${result} =    Evaluate JavaScript    css=#title
    ...    async (el) => { await new Promise(r => setTimeout(r, 50)); return el.textContent.trim(); }
    Should Be Equal    ${result}    Electron Test App

New Electron Application With Explicit Timeout
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    timeout=30 seconds
    Get Title    ==    Browser Library Electron Test App

Close Electron Application Removes Active Browser
    Launch Test App
    Close Electron Application
    ${browsers} =    Get Browser Ids
    Should Be Empty    ${browsers}

Close Electron Application When No App Open Is Safe
    Close Electron Application

New Electron Application With Invalid Path Raises Error
    Run Keyword And Expect Error    *
    ...    New Electron Application    executable_path=/nonexistent/electron

New Electron Application With Extra Args
    @{args} =    Create List    ${ELECTRON_APP_MAIN}    --no-sandbox
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
    Get Title    ==    Browser Library Electron Test App

New Electron Application With slowMo
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    slowMo=100ms
    Get Title    ==    Browser Library Electron Test App

New Electron Application With colorScheme Dark
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    colorScheme=dark
    Get Title    ==    Browser Library Electron Test App

New Electron Application With acceptDownloads False
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    acceptDownloads=False
    Get Title    ==    Browser Library Electron Test App

New Electron Application With bypassCSP
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    bypassCSP=True
    Get Title    ==    Browser Library Electron Test App

Open Electron Dev Tools Does Not Raise
    Launch Test App
    Open Electron Dev Tools

Zero Timeout Launches An Electron Application
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application    ${ELECTRON_BIN}    args=${args}    timeout=0
    Get Title    ==    Browser Library Electron Test App

Launching Again Replaces The Electron Browser
    Launch Test App
    Launch Test App
    ${browsers} =    Get Browser Ids
    Length Should Be    ${browsers}    1
    Get Title    ==    Browser Library Electron Test App

Close Browser Closes Electron And Allows Relaunch
    Launch Test App
    Close Browser
    Launch Test App
    Get Title    ==    Browser Library Electron Test App

Closing Electron Preserves Another Active Browser
    Launch Test App
    ${browser} =    New Browser    chromium
    New Page    data:text/html,<title>Other browser</title>
    Close Electron Application
    Get Title    ==    Other browser
    ${browsers} =    Get Browser Ids
    Should Be Equal    ${browsers}    ${{[$browser]}}

Electron Remains Separate From A Persistent Context
    ${browser}    ${context}    ${page} =    New Persistent Context
    ...    ${OUTPUT_DIR}/electron-profile
    ...    url=data:text/html,<title>Persistent browser</title>
    Launch Test App
    Close Electron Application
    Get Title    ==    Persistent browser
    ${browsers} =    Get Browser Ids
    Should Be Equal    ${browsers}    ${{[$browser]}}

Electron Video Is Saved When The Application Closes
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    ${browser}    ${context}    ${page} =    New Electron Application
    ...    ${ELECTRON_BIN}
    ...    args=${args}
    ...    recordVideo={'dir': '${OUTPUT_DIR}/electron-video', 'size': {'width': 640, 'height': 480}}
    Should Not Be Empty    ${page}[video_path]
    Click    css=#btn-click
    Close Electron Application
    File Should Exist    ${page}[video_path]
    ${size} =    Get File Size    ${page}[video_path]
    Should Be True    ${size} > 0

*** Keywords ***
Setup Electron Test Suite
    ${ELECTRON_BIN} =    Get Electron Binary Path    ${ELECTRON_APP_DIR}
    Set Suite Variable    ${ELECTRON_BIN}

Launch Test App
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
