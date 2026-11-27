*** Settings ***
Documentation     A JS extension changes what Record Keyword and Record Selector record
...               through its ``__rewriteAction`` hook, which runs in the page when the
...               Action happens. The extension stays loaded in this library instance, so
...               these tests have a suite of their own.

Resource          recorder.resource

Suite Setup       Load The Hook Extension
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
A Hook Changes The Selector Of A Recorded Action
    ${promise} =    Promise To    Record Keyword    Choose A Make    ${RESOURCE}
    Toolbar State Should Be    recording
    Select Options By    id=ManyOptions    value    13: 6792
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    >> nth=0${SPACE*4}value${SPACE*4}13: 6792\n
    Select Options By    id=ManyOptions    value    0: null
    Recorded Keyword Replays    ${RESOURCE}    Choose A Make
    Get Selected Options    id=ManyOptions    value    ==    13: 6792

A Hook Sees The Clicked Element Before The Click Changes It
    Open Rewrite Page
    ${promise} =    Promise To    Record Keyword    Ship The Order    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=ship
    Get Text    id=ship    ==    Shipped
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    text="Ship"
    Should Not Contain    ${file}    Shipped
    Recorded Keyword Replays    ${RESOURCE}    Ship The Order    ${RECORDER_REWRITE_URL}
    Get Text    id=ship    ==    Shipped

A Hook Runs On A Page Navigated To During The Recording
    Move The Toolbar Away
    ${promise} =    Promise To    Record Keyword    Open And Ship    ${RESOURCE}
    Toolbar State Should Be    recording
    Go To    ${RECORDER_REWRITE_URL}
    Toolbar Is Ready
    Click    id=ship
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    text="Ship"

A Hook Runs On A Page Opened During The Recording
    Move The Toolbar Away
    ${promise} =    Promise To    Record Keyword    Ship In A New Page    ${RESOURCE}
    Toolbar State Should Be    recording
    New Page    ${RECORDER_REWRITE_URL}
    Move The Toolbar Away
    Reload
    Toolbar Is Ready
    Click    id=ship
    Get Text    id=ship    ==    Shipped
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    text="Ship"

A Selector A Hook Gives In A Frame Keeps The Frame Playwright Recorded
    Open Rewrite Page
    ${promise} =    Promise To    Record Keyword    Click Inside    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=frame >>> id=inside
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    iframe[title="Frame"] >>> text="Inside"
    Recorded Keyword Replays    ${RESOURCE}    Click Inside    ${RECORDER_REWRITE_URL}
    Get Text    id=frame >>> id=inside    ==    Clicked inside

A Selector That Finds Another Element Is Not Recorded
    Open Rewrite Page
    ${promise} =    Promise To    Record Keyword    Click First    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=first
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Not Contain    ${file}    \#second
    Recorded Keyword Replays    ${RESOURCE}    Click First    ${RECORDER_REWRITE_URL}
    Get Text    id=first    ==    First clicked
    Get Text    id=second    ==    Second

A Hook Changes Another Part Of A Recorded Action
    Open Rewrite Page
    ${promise} =    Promise To    Record Keyword    Greet    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=greeting    Hi
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    ${SPACE*4}Hello\n
    Should Not Contain    ${file}    ${SPACE*4}Hi\n
    Recorded Keyword Replays    ${RESOURCE}    Greet    ${RECORDER_REWRITE_URL}
    Get Property    id=greeting    value    ==    Hello

A Hook Runs On A Page With A Strict Content Security Policy
    New Page    ${RECORDER_CSP_URL}
    Move The Toolbar Away
    ${promise} =    Promise To    Record Keyword    Enter A Name    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=name    Ada
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    >> nth=0${SPACE*4}Ada\n

A Hook Changes The Selector Of A Pick
    New Page    ${RECORDER_SELECTORS_URL}
    Move The Toolbar Away
    ${promise} =    Promise To    Record Selector
    Wait For Function
    ...    () => window.__rfbToolbarState && window.__rfbToolbarState.mode === 'selector' && window.__rfbToolbarState.phase === 'picking'
    Playwright Should Be Picking
    Click    text=Pressed
    Wait For Function    () => window.__rfbToolbarState.phase === 'picked'
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should End With    ${selector}    >> nth=0
    Get Text    ${selector}    ==    Pressed

*** Keywords ***
Load The Hook Extension
    Allow Recording Headless    ${True}
    ${lib} =    Get Library Instance    Browser
    VAR    ${path} =    ${CURDIR}${/}recorder_hooks.js
    Evaluate    $lib.init_js_extension($path)

Open Rewrite Page
    New Page    ${RECORDER_REWRITE_URL}
    Move The Toolbar Away

Move The Toolbar Away
    Evaluate JavaScript
    ...    ${None}
    ...    () => sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000}))
