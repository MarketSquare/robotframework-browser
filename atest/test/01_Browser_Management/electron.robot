*** Settings ***
Resource            imports.resource

Suite Setup         Setup Electron Test Suite
Suite Teardown      Close Electron Application

*** Variables ***
# Paths resolved relative to this file so they work from any working directory.
${ELECTRON_APP_DIR} =       ${CURDIR}${/}..${/}..${/}..${/}node${/}electron-test-app
${ELECTRON_APP_MAIN} =      ${ELECTRON_APP_DIR}${/}main.js

# ${ELECTRON_BIN} is set dynamically in Suite Setup based on the current platform.
${ELECTRON_BIN} =           ${EMPTY}

*** Test Cases ***
New Electron Application Returns Browser Context And Page Ids
    [Documentation]    New Electron Application returns a non-empty
    ...    (browser_id, context_id, page_id) triple.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    ${browser_id}    ${context_id}    ${page_details} =    New Electron Application
    ...    executable_path=${ELECTRON_BIN}    args=@{args}
    Should Not Be Empty    ${browser_id}
    Should Not Be Empty    ${context_id}
    Should Not Be Empty    ${page_details.page_id}
    [Teardown]    Close Electron Application

Title Is Correct After Launch
    [Documentation]    The window title matches the value set in index.html.
    Launch Test App
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Heading Text Is Readable
    [Documentation]    Get Text works against Electron renderer content.
    Launch Test App
    Get Text    css=h1#title    ==    Electron Test App
    [Teardown]    Close Electron Application

Click Increments Counter
    [Documentation]    Click triggers JavaScript in the renderer and the
    ...    result is visible via Get Text.
    Launch Test App
    Get Text    css=#click-counter    ==    0
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    1
    Click    css=#btn-click
    Get Text    css=#click-counter    ==    2
    [Teardown]    Close Electron Application

Fill Text Updates Input Value
    [Documentation]    Fill Text and Get Property work in Electron windows.
    Launch Test App
    Fill Text    css=#text-input    Hello Electron
    Get Property    css=#text-input    value    ==    Hello Electron
    [Teardown]    Close Electron Application

Fill Text Triggers Input Event
    [Documentation]    Typing into the input element updates the description
    ...    paragraph through the JavaScript input event listener.
    Launch Test App
    Fill Text    css=#text-input    live update
    Get Text    css=#description    ==    live update
    [Teardown]    Close Electron Application

Select Option Works
    [Documentation]    Select Options By works against a select element.
    Launch Test App
    Select Options By    css=#select-box    value    two
    Get Selected Options    css=#select-box    value    ==    two
    [Teardown]    Close Electron Application

Check Checkbox Works
    [Documentation]    Check Checkbox and Get Checkbox State work in
    ...    Electron renderer pages.
    Launch Test App
    Get Checkbox State    css=#checkbox    ==    False
    Check Checkbox    css=#checkbox
    Get Checkbox State    css=#checkbox    ==    True
    [Teardown]    Close Electron Application

Wait For Elements State Works
    [Documentation]    Wait For Elements State correctly tracks a DOM element
    ...    that is toggled from hidden to visible via a button click.
    ...    This exercises Playwright's promise-based selector API
    ...    through the gRPC bridge.
    Launch Test App
    Wait For Elements State    css=#toggle-target    hidden
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    visible
    Get Text    css=#toggle-target    ==    Now you see me
    Click    css=#btn-toggle
    Wait For Elements State    css=#toggle-target    hidden
    [Teardown]    Close Electron Application

Async Content Appears After Delay
    [Documentation]    An element that becomes visible after an 800 ms
    ...    JavaScript timeout is correctly awaited by
    ...    Wait For Elements State (tests promise handling).
    Launch Test App
    Wait For Elements State    css=#async-output    hidden
    Click    css=#btn-async
    Wait For Elements State    css=#async-output    visible    timeout=5s
    Get Text    css=#async-output    ==    Loaded
    [Teardown]    Close Electron Application

Keyboard Input Works
    [Documentation]    Press a keyboard shortcut and verify the effect.
    ...    Uses Ctrl+A to select all text then Delete to clear.
    Launch Test App
    Fill Text    css=#text-input    to be deleted
    Click    css=#text-input
    Keyboard Key    press    Control+a
    Keyboard Key    press    Delete
    Get Property    css=#text-input    value    ==    ${EMPTY}
    [Teardown]    Close Electron Application

File Input Accepts A File
    [Documentation]    Upload a file through the native file input element
    ...    and verify the filename is reflected in the page.
    Launch Test App
    Upload File By Selector    css=#file-input    ${ELECTRON_APP_DIR}${/}package.json
    Get Text    css=#file-name    ==    package.json
    [Teardown]    Close Electron Application

Evaluate JavaScript Returns Promise Result
    [Documentation]    Evaluate JavaScript can run async JS and return a
    ...    resolved promise value (tests the async eval path).
    Launch Test App
    ${result} =    Evaluate JavaScript    css=#title
    ...    async (el) => { await new Promise(r => setTimeout(r, 50)); return el.textContent.trim(); }
    Should Be Equal    ${result}    Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With Explicit Timeout
    [Documentation]    Passing an explicit timeout does not prevent a
    ...    successful launch.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    timeout=30 seconds
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Close Electron Application Removes Active Browser
    [Documentation]    After Close Electron Application there is no active
    ...    browser and page keywords raise an error.
    Launch Test App
    Close Electron Application
    Run Keyword And Expect Error    *    Get Title

Close Electron Application When No App Open Is Safe
    [Documentation]    Calling Close Electron Application when nothing is
    ...    running must not raise an error.
    Close Electron Application

New Electron Application With Invalid Path Raises Error
    [Documentation]    A descriptive error is raised when the executable
    ...    path does not exist.
    Run Keyword And Expect Error    *
    ...    New Electron Application    executable_path=/nonexistent/electron
    [Teardown]    Close Electron Application

New Electron Application With Extra Args
    [Documentation]    Additional command-line arguments are forwarded to
    ...    the Electron process without error.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}    --no-sandbox
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With slowMo
    [Documentation]    slowMo slows down operations without causing a launch failure.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    slowMo=100ms
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With colorScheme Dark
    [Documentation]    colorScheme=dark is accepted without error.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    colorScheme=dark
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With acceptDownloads False
    [Documentation]    acceptDownloads=False is forwarded to Playwright without error.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    acceptDownloads=False
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

New Electron Application With bypassCSP
    [Documentation]    bypassCSP=True is accepted and the page still loads.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application
    ...    executable_path=${ELECTRON_BIN}
    ...    args=@{args}
    ...    bypassCSP=True
    Get Title    ==    Browser Library Electron Test App
    [Teardown]    Close Electron Application

Open Electron Dev Tools Does Not Raise
    [Documentation]    Open Electron Dev Tools executes without error.
    ...    The visual effect is not asserted because headless
    ...    CI environments do not render the DevTools panel.
    Launch Test App
    Open Electron Dev Tools
    [Teardown]    Close Electron Application

*** Keywords ***
Setup Electron Test Suite
    [Documentation]    Install the test-app npm dependencies (via npm ci for
    ...    reproducible installs) and resolve the platform-specific
    ...    Electron binary path.    Both steps are required before any
    ...    Electron test can run.    The install step is skipped when
    ...    node_modules already exists to avoid redundant network
    ...    round-trips on repeated local runs.
    ...
    ...    The entire suite is skipped when the test app source tree is absent
    ...    (e.g. BrowserBatteries / install-test runs that remove node/).
    ${app_dir_exists} =    Run Keyword And Return Status    Directory Should Exist    ${ELECTRON_APP_DIR}
    IF    not ${app_dir_exists}
        Skip    Electron test app not present (node/electron-test-app/ missing) — skipping suite.
    END
    ${platform} =    Evaluate    __import__('sys').platform
    ${npm} =    Set Variable If    '${platform}' == 'win32'    npm.cmd    npm
    ${node_modules} =    Set Variable    ${ELECTRON_APP_DIR}${/}node_modules
    ${installed} =    Run Keyword And Return Status    Directory Should Exist    ${node_modules}
    IF    not ${installed}
        ${result} =    Run Process    ${npm}    ci
        ...    cwd=${ELECTRON_APP_DIR}    stdout=PIPE    stderr=PIPE
        Should Be Equal As Integers    ${result.rc}    0
        ...    msg=npm ci failed in node/electron-test-app:\n${result.stderr}
    END
    IF    '${platform}' == 'win32'
        Set Suite Variable    ${ELECTRON_BIN}
        ...    ${ELECTRON_APP_DIR}${/}node_modules${/}electron${/}dist${/}electron.exe
    ELSE IF    '${platform}' == 'darwin'
        Set Suite Variable    ${ELECTRON_BIN}
        ...    ${ELECTRON_APP_DIR}${/}node_modules${/}electron${/}dist${/}Electron.app${/}Contents${/}MacOS${/}Electron
    ELSE
        Set Suite Variable    ${ELECTRON_BIN}
        ...    ${ELECTRON_APP_DIR}${/}node_modules${/}electron${/}dist${/}electron
    END

Launch Test App
    [Documentation]    Launch the test app and wait for the DOM to be ready.
    @{args} =    Create List    ${ELECTRON_APP_MAIN}
    New Electron Application    executable_path=${ELECTRON_BIN}    args=@{args}
