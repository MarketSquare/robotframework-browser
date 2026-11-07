*** Settings ***
Resource          recorder.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
The Toolbar Works On A Strict Page
    Go To    ${RECORDER_CSP_URL}
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Styled    ${None}
    Toolbar State Should Be    recording
    Get Element Count    css=rfb-recorder-toolbar    ==    1
    ${style} =    Evaluate JavaScript    ${None}
    ...    () => {
    ...    const style = (id) => getComputedStyle(window.toolbarRoot.getElementById(id));
    ...    return [style('panel').backgroundColor, style('panel').direction, style('title').letterSpacing,
    ...    style('title').wordSpacing, style('title').textTransform, style('calls').cursor];
    ...    }
    Should Be Equal    ${style}    ${{['rgb(28, 34, 39)', 'ltr', 'normal', '0px', 'none', 'auto']}}
    ${host} =    Evaluate JavaScript    rfb-recorder-toolbar
    ...    (host) => { const style = getComputedStyle(host); return [style.position, style.opacity, style.filter]; }
    Should Be Equal    ${host}    ${{['fixed', '1', 'none']}}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${promise} =    Promise To    Record Keyword    Styled Again    ${None}
    Toolbar State Should Be    recording
    Get Element Count    css=rfb-recorder-toolbar    ==    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

A Resize Released On The Page Records No Click
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    No Resize Click    ${None}
    Toolbar State Should Be    recording
    ${grip} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('panel').getBoundingClientRect(); return [r.right - 4, r.bottom - 4]; }
    Mouse Move    ${grip}[0]    ${grip}[1]
    Mouse Button    down
    Mouse Move    ${grip}[0]    ${{$grip[1] + 200}}    steps=5
    Mouse Button    up
    Fill Text    id=input_name    after the resize
    Wait Until Calls    1
    Sleep    1s
    Toolbar Calls Should Be    Fill Text
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Keys After A Click On The Toolbar Text Are Not Recorded
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    No Toolbar Keys    ${None}
    Toolbar State Should Be    recording
    ${title} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('title').getBoundingClientRect(); return [r.x + 5, r.y + r.height / 2]; }
    Mouse Button    click    ${title}[0]    ${title}[1]
    Keyboard Key    press    ArrowUp
    Keyboard Key    press    Control+c
    Fill Text    id=input_name    after the keys
    Wait Until Calls    1
    Sleep    1s
    Toolbar Calls Should Be    Fill Text
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Page Clicks Without A Pointer Still Work After A Toolbar Click
    Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript
    ...    ${None}
    ...    () => { const b = document.createElement('button'); b.id = 'counter'; b.textContent = 'Count'; window.clicks = 0; b.addEventListener('click', () => window.clicks++); document.body.prepend(b); }
    ${promise} =    Promise To    Record Keyword    Keyboard Click    ${None}
    Toolbar State Should Be    recording
    ${title} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('title').getBoundingClientRect(); return [r.x + 5, r.y + r.height / 2]; }
    Mouse Button    click    ${title}[0]    ${title}[1]
    Focus    id=counter
    Keyboard Key    press    Enter
    ${clicks} =    Evaluate JavaScript    ${None}    () => window.clicks
    Should Be Equal As Integers    ${clicks}    1
    ${save} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('finish').getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }
    Mouse Button    click    ${save}[0]    ${save}[1]
    Wait For    ${promise}
    Focus    id=counter
    Keyboard Key    press    Enter
    ${clicks} =    Evaluate JavaScript    ${None}    () => window.clicks
    Should Be Equal As Integers    ${clicks}    2

A Minimized Record Keyword Toolbar Offers Save
    Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript    ${None}    () => sessionStorage.setItem('rfb.toolbar.collapsed', 'true')
    ${promise} =    Promise To    Record Keyword    Saved Minimized    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    minimized
    Wait Until Calls    1
    Toolbar Element Should Be Hidden    headNew
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('headSave')
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    minimized

Toolbar Collapse And Position Survive A Reload
    Open The Toolbar Shadow Root For Inspection
    ${promise} =    Promise To    Record Keyword    Toolbar Layout    ${RESOURCE}
    Toolbar State Should Be    recording
    ${expanded} =    Get BoundingBox    rfb-recorder-toolbar    height
    Click Toolbar Collapse Button
    Get Element States    rfb-recorder-toolbar >> #body    *=    hidden
    ${collapsed} =    Get BoundingBox    rfb-recorder-toolbar    height
    Should Be True    ${collapsed} < ${expanded}
    Evaluate JavaScript
    ...    ${None}
    ...    () => window.sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 40, y: 70}))
    Reload
    Toolbar Is Ready
    ${after} =    Get BoundingBox    rfb-recorder-toolbar    height
    Should Be Equal As Numbers    ${after}    ${collapsed}
    ${transform} =    Evaluate JavaScript    rfb-recorder-toolbar    (element) => element.style.transform
    Should Be Equal    ${transform}    translate(40px, 70px)
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

The Toolbar Is Removed From All Pages After The Session
    ${first} =    Get Page Ids    ACTIVE
    New Page    ${FORM_URL}
    ${second} =    Get Page Ids    ACTIVE
    ${promise} =    Promise To    Record Keyword    Two Pages    ${RESOURCE}
    Toolbar State Should Be    recording
    Get Element Count    css=rfb-recorder-toolbar    ==    1
    Switch Page    ${first}[0]
    Get Element Count    css=rfb-recorder-toolbar    ==    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    Get Element Count    css=rfb-recorder-toolbar    ==    0
    Switch Page    ${second}[0]
    Get Element Count    css=rfb-recorder-toolbar    ==    0

Typing In The Toolbar Does Not Reach The Page
    Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript
    ...    ${None}
    ...    () => { window.pageKeys = []; document.addEventListener('keydown', (event) => window.pageKeys.push(event.key), true); }
    ${promise} =    Promise To    Record Keyword    Typed Argument    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Evaluate JavaScript    ${None}    () => { window.pageKeys.length = 0; }
    Click Inside Toolbar    () => [...window.toolbarRoot.querySelectorAll('.cell.pick')].pop()
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('argName')
    Keyboard Input    type    who
    Keyboard Key    press    Enter
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    ${page_keys} =    Evaluate JavaScript    ${None}    () => window.pageKeys
    Should Be Empty    ${page_keys}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${who}=Alice

Minimized Toolbar Starts And Saves A Keyword
    Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript    ${None}    () => window.sessionStorage.setItem('rfb.toolbar.collapsed', 'true')
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar State Should Be    idle
    Toolbar Element Should Be Hidden    body
    Toolbar Element Should Be Hidden    headSave
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('headNew')
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('nameInput')
    Keyboard Input    type    Minimized
    Keyboard Key    press    Enter
    Toolbar State Should Be    recording
    Toolbar Element Should Be Hidden    headNew
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('headSave')
    Toolbar State Should Be    idle
    Toolbar Element Should Be Shown    headNew
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Minimized\n

Toolbar Sits Flush With The Bottom Right Corner
    Open The Toolbar Shadow Root For Inspection
    Evaluate JavaScript    ${None}
    ...    () => window.sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 99999, y: 99999}))
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar State Should Be    idle
    Toolbar Should Touch The Bottom Right Corner
    Click Toolbar Collapse Button
    Toolbar Should Touch The Bottom Right Corner
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Dragging Past The Edge Does Not Shift The Next Drag
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar State Should Be    idle
    ${start} =    Toolbar Header Point
    Mouse Move    ${start}[0]    ${start}[1]
    Mouse Button    down
    Mouse Move    ${{ $start[0] + 3000 }}    ${start}[1]    steps=5
    Mouse Button    up
    Toolbar Should Touch The Right Edge
    ${edge} =    Toolbar Left
    ${grab} =    Toolbar Header Point
    Mouse Move    ${grab}[0]    ${grab}[1]
    Mouse Button    down
    Mouse Move    ${{ $grab[0] - 50 }}    ${grab}[1]    steps=5
    Mouse Button    up
    ${moved} =    Toolbar Left
    Should Be True    abs(${edge} - ${moved} - 50) < 1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Toolbar Clicks Are Neither Recorded Nor Swallow A Navigation
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Go To After Toolbar    ${RESOURCE}
    Toolbar State Should Be    recording
    # The hint, not the header: Playwright's overlay may cover the header at the top centre.
    ${point} =    Toolbar Element Point    hint
    Mouse Button    click    ${point}[0]    ${point}[1]
    Mouse Button    click    ${point}[0]    ${point}[1]    button=right
    # Playwright credits a navigation within 5 s to the last Action it saw.
    Go To    ${FORM_URL}?after_toolbar
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Go To${SPACE*4}${FORM_URL}?after_toolbar
    Should Not Contain    ${file}    Click

The Toolbar Works Over A Modal Of The Page
    Keep The Closed Toolbar Root Reachable
    # Like Radix and similar: body without pointer events, a focus trap, closing on a press outside.
    Evaluate JavaScript
    ...    ${None}
    ...    () => {
    ...    const modal = document.createElement('div'); modal.id = 'page-modal';
    ...    const input = document.createElement('input'); modal.appendChild(input); document.body.appendChild(modal);
    ...    document.body.style.pointerEvents = 'none'; modal.style.pointerEvents = 'auto'; input.focus();
    ...    document.addEventListener('focusin', (e) => { if (!modal.contains(e.target)) input.focus(); });
    ...    document.addEventListener('focusout', (e) => { if (e.relatedTarget && !modal.contains(e.relatedTarget)) input.focus(); });
    ...    document.addEventListener('pointerdown', (e) => { if (!modal.contains(e.target)) modal.remove(); });
    ...    }
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('new')
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('nameInput')
    Keyboard Input    type    Over The Modal
    Keyboard Key    press    Enter
    Toolbar State Should Be    recording
    Get Element Count    id=page-modal    ==    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

The Toolbar Comes Back When The Page Swaps Its Body
    ${promise} =    Promise To    Record Keyword    Fill After A Swap    ${RESOURCE}
    Toolbar State Should Be    recording
    # As Turbo, htmx or a framework re-bootstrap would, without a navigation.
    Evaluate JavaScript    ${None}    () => { document.body.innerHTML = '<input id="swapped">'; }
    Get Element Count    css=rfb-recorder-toolbar    ==    1
    Fill Text    id=swapped    after the swap
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    after the swap
