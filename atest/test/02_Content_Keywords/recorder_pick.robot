*** Settings ***
Resource          recorder.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
A Picked Selector Becomes A Comment And Recording Goes On
    ${promise} =    Promise To    Record Keyword    Pick And Fill    ${RESOURCE}
    Toolbar State Should Be    recording
    Send Command    {cmd: 'pick'}
    Picker Should Be Picking
    Click    id=input_name
    Wait For Function
    ...    () => { const p = window.__rfbToolbarState.picker; return p && p.phase === 'picked' && p.count && p.count.count === 1; }
    ${selector} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.picker.selector
    Get Element Count    ${selector}    ==    1
    # Trying the page out before Use records nothing.
    Fill Text    id=input_name    while picked
    Sleep    0.8s
    Send Command    {cmd: 'pick-use'}
    Wait For Function    () => window.__rfbToolbarState.picker === null
    Wait Until Calls    1
    Wait For Function    () => !document.body.hasAttribute('data-pw-cursor')    timeout=2s
    Fill Text    id=input_name    after the pick
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    \n${SPACE*4}\# Picked Selector${SPACE*4}${selector}\n
    Should Contain    ${file}    after the pick
    Should Not Contain    ${file}    while picked
    Recorded Keyword Replays    ${RESOURCE}    Pick And Fill

Playwright's Pick Locator Opens The Toolbar's Picker And Records Nothing Meanwhile
    ${promise} =    Promise To    Record Keyword    Fill After Picking    ${RESOURCE}
    Toolbar State Should Be    recording
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording-inspecting')
    Picker Should Be Picking
    Fill Text    id=input_name    while picking
    Send Command    {cmd: 'pick-cancel'}
    Wait For Function    () => window.__rfbToolbarState.picker === null
    Wait For Function    () => !document.body.hasAttribute('data-pw-cursor')    timeout=2s
    Fill Text    id=input_name    after picking
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    after picking
    Should Not Contain    ${file}    while picking

A Minimized Toolbar Offers Only The Pick's Buttons While Picking
    Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript    ${None}    () => sessionStorage.setItem('rfb.toolbar.collapsed', 'true')
    ${promise} =    Promise To    Record Keywords    ${None}
    Toolbar State Should Be    idle
    Send Command    {cmd: 'new', name: 'Pick Minimized'}
    Toolbar State Should Be    recording
    Send Command    {cmd: 'pick'}
    Picker Should Be Picking
    Toolbar Element Should Be Hidden    headSave
    Toolbar Element Should Be Shown    headCancel
    Click    id=input_name
    Wait For Function    () => (window.__rfbToolbarState.picker || {}).phase === 'picked'
    Toolbar Element Should Be Hidden    headSave
    Toolbar Element Should Be Shown    headUse
    Toolbar Element Should Be Shown    headReselect
    Send Command    {cmd: 'finish'}
    Wait For Function    () => window.__rfbToolbarState.error === 'Use or cancel the picked selector first.'
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('headCancel')
    Wait For Function    () => window.__rfbToolbarState.picker === null
    Toolbar Element Should Be Shown    headSave
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Pick Starts On The Page Its Button Was Pressed On
    ${promise} =    Promise To    Record Keyword    Pick In Second Window    ${None}
    Toolbar State Should Be    recording
    ${second} =    Open Second Window
    Wait For Function    () => !!window.second.__rfbCommand && !!window.second.__rfbToolbarState
    # Browser's active page stays the first one; the Pick button is pressed in the second.
    Evaluate JavaScript    ${None}    () => window.second.__rfbCommand({cmd: 'pick'})
    Wait For Function    () => window.second.document.body.getAttribute('data-pw-cursor') === 'pointer'
    Switch Page    ${second}
    Click    id=input_name
    Wait For Function    () => (window.__rfbToolbarState.picker || {}).phase === 'picked'
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Playwright's Pick Locator Picks On The Page Pressed Last
    ${promise} =    Promise To    Record Keyword    Pick Where Pressed    ${None}
    Toolbar State Should Be    recording
    ${second} =    Open Second Window
    Wait For Function    () => !!window.second.__rfbToolbarState
    ${first} =    Switch Page    ${second}
    Mouse Button    click    700    500
    Switch Page    ${first}
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording-inspecting')
    Wait For Function    () => (window.__rfbToolbarState.picker || {}).phase === 'picking'
    # Playwright takes the pick up with a later poll; until then a click is an Action.
    Wait Until Keyword Succeeds    10s    0.5s    Click Picks On    ${second}    ${first}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Undo Removes A Picked Selector
    ${promise} =    Promise To    Record Keyword    Pick Undone    ${None}
    Toolbar State Should Be    recording
    Send Command    {cmd: 'pick'}
    Picker Should Be Picking
    Click    id=input_name
    Wait For Function    () => (window.__rfbToolbarState.picker || {}).phase === 'picked'
    Send Command    {cmd: 'pick-use'}
    Wait Until Calls    1
    Send Command    {cmd: 'undo'}
    Wait Until Calls    0
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Picking While Idle Asks For A Keyword First
    ${promise} =    Promise To    Record Keywords    ${None}
    Toolbar State Should Be    idle
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording-inspecting')
    Wait For Function    () => (window.__rfbToolbarState.notice || '').includes('Start recording a keyword')
    Wait For Function    () => window.__rfbToolbarState.picker === null
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

An Assertion Tool Leaves The Page Its Own Pointer
    ${promise} =    Promise To    Record Keyword    Assert And Back    ${None}
    Toolbar State Should Be    recording
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('assertingVisibility')
    Wait For Function    () => document.body.getAttribute('data-pw-cursor') === 'pointer'
    # A person stays in the tool longer than one poll of the recorder (200 ms).
    Sleep    0.5s
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording')
    Wait For Function    () => !document.body.hasAttribute('data-pw-cursor')    timeout=2s
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Assert Snapshot Becomes Get Aria Snapshot
    ${promise} =    Promise To    Record Keyword    Check Heading Snapshot    ${RESOURCE}
    Toolbar State Should Be    recording
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('assertingSnapshot')
    # The assert tool needs an element with text under the pointer.
    Hover    css=label[for="input_name"]
    Click    css=label[for="input_name"]
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Match Regexp    ${file}    Get Aria Snapshot\\s+\\S+\\s+yaml\\s+==\\s+- text
    Recorded Keyword Replays    ${RESOURCE}    Check Heading Snapshot
