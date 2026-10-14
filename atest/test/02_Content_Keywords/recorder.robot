*** Settings ***
Documentation     Scripted recording sessions. The toolbar's closed shadow root cannot be
...               clicked from a test, so commands go through `window.__rfbCommand`, the
...               same channel the toolbar uses, and the page is driven by Browser keywords.

Resource          imports.resource
Library           OperatingSystem

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
Session Records Two Keywords And Skips Idle Actions
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Fill Text    id=input_name    ignored while idle
    Send Command    {cmd: 'new', name: 'Check Sms'}
    Toolbar State Should Be    recording
    Check Checkbox    [data-testid="testid-sms"]
    Finish Keyword
    # Playwright would credit a navigation within 5 s of a fill or click to that Action.
    Go To    ${FORM_URL}?visited_while_idle
    Toolbar Is Ready
    Send Command    {cmd: 'new', name: 'Fill Name'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Finish Keyword
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Fill Name
    Should Contain    ${text}    Check Sms
    ${file} =    Get File    ${RESOURCE}
    Should Not Contain    ${file}    ignored while idle
    Should Not Contain    ${file}    visited_while_idle
    Should Contain    ${file}    [Tags]${SPACE*4}recorded
    Recorded Keyword Replays    ${RESOURCE}    Fill Name
    Get Property    id=input_name    value    ==    Alice

Record Keyword Returns Its Text
    ${promise} =    Promise To    Record Keyword    Fill Alice    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Start With    ${text}    *** Keywords ***\nFill Alice\n

Undo And Discard
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Send Command    {cmd: 'new', name: 'Undone'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    first
    Check Checkbox    [data-testid="testid-sms"]
    Wait Until Calls    2
    Send Command    {cmd: 'undo'}
    Wait Until Calls    1
    Finish Keyword
    Send Command    {cmd: 'new', name: 'Thrown Away'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    second
    Wait Until Calls    1
    Send Command    {cmd: 'discard'}
    Toolbar State Should Be    idle
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Undone
    Should Not Contain    ${file}    Check Checkbox
    Should Not Contain    ${file}    Thrown Away

Click Right Before Finish Lands In The Keyword
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Send Command    {cmd: 'new', name: 'Click Then Finish'}
    Toolbar State Should Be    recording
    Click    id=input_name
    Finish Keyword
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Match Regexp    ${file}    Click Then Finish\\n\\s+\\[Tags\\]\\s+recorded\\n\\s+Click\\s+\\S+

Log Only Mode Writes No File
    # Positional ${None}: the whole argument stays the None object through Promise To.
    ${promise} =    Promise To    Record Keyword    Logged Only    ${None}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Bob
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Logged Only
    File Should Not Exist    ${RESOURCE}

Keyword Arguments With Partial Value And Default
    ${promise} =    Promise To    Record Keyword    Fill Parametrised    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    id-42
    Wait Until Calls    1
    Send Command    {cmd: 'argument', call: 0, value: 1, start: 3, end: 5, name: 'number', raw: 'id-42'}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${number}=42
    Should Contain    ${file}    id-\${number}
    Import Resource    ${RESOURCE}
    Fill Parametrised    number=7
    Get Property    id=input_name    value    ==    id-7

Part Of A Multi-Line Value Becomes An Argument
    Open The Toolbar Shadow Root For Inspection
    ${promise} =    Promise To    Record Keyword    Comment On Lines    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    textarea[name="comment"]    first line\nsecond line
    Wait Until Calls    1
    # Untrusted clicks and values, so the recorder does not record the toolbar itself.
    Evaluate JavaScript    rfb-recorder-toolbar >> .cell.pick >> nth=-1    (element) => element.click()
    Evaluate JavaScript
    ...    rfb-recorder-toolbar >> #argValue
    ...    (element) => { const at = element.value.indexOf('second'); element.setSelectionRange(at, at + 6); }
    Evaluate JavaScript    rfb-recorder-toolbar >> #argName    (element) => { element.value = 'which'; }
    Evaluate JavaScript    rfb-recorder-toolbar >> #argOk    (element) => element.click()
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${which}=second
    Should Contain    ${file}    first line\\n\${which} line
    Should Not Contain    ${file}    Make argument

An Argument Made Without A Default Is Required
    Open The Toolbar Shadow Root For Inspection
    ${promise} =    Promise To    Record Keyword    Fill Required Name    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Evaluate JavaScript    rfb-recorder-toolbar >> .cell.pick >> nth=-1    (element) => element.click()
    Evaluate JavaScript    rfb-recorder-toolbar >> #argName    (element) => { element.value = 'who'; }
    Evaluate JavaScript    rfb-recorder-toolbar >> #argDefault    (element) => element.click()
    Evaluate JavaScript    rfb-recorder-toolbar >> #argOk    (element) => element.click()
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    Get Text    rfb-recorder-toolbar >> #args    ==    \${who}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${who}\n

A Long Value Becomes An Argument
    ${long} =    Evaluate    "x" * 10000 + "end"
    ${promise} =    Promise To    Record Keyword    Comment At Length    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    textarea[name="comment"]    ${long}
    Wait Until Calls    1
    Evaluate JavaScript    ${None}
    ...    () => {
    ...    const raw = window.__rfbToolbarState.calls[0].values[1].raw;
    ...    window.__rfbCommand({cmd: 'argument', call: 0, value: 1, start: 0, end: raw.length, name: 'text', raw});
    ...    }
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${text}=${long}
    Should Contain    ${file}    ${SPACE*4}\${text}\n

Popup Becomes Switch Page New
    Go To    ${CREATE_POPUPS_URL}
    ${promise} =    Promise To    Record Keyword    Open Popup    ${RESOURCE}
    Toolbar State Should Be    recording
    # Playwright's own recorder overlay covers the top centre of the page.
    Click With Options    id=first_popup    position_x=20    position_y=9
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Switch Page${SPACE*4}NEW
    Should Not Contain    ${file}    New Page

Dialog Gets Handled Before The Click
    Go To    ${DIALOGS_URL}
    Handle Future Dialogs    action=accept
    ${promise} =    Promise To    Record Keyword    Confirm Something    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=confirm_btn
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Match Regexp    ${file}    Handle Future Dialogs\\s+action=accept\\n\\s+Click

Download Is Wrapped In A Download Promise
    Go To    ${LOGIN_URL}
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Download File    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=file_download
    Wait Until Calls    3
    ${shown} =    Evaluate JavaScript    ${None}
    ...    () => window.toolbarRoot.querySelector('#calls li').textContent
    Should Start With    ${shown}    \${download}=Promise To Wait For Download
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Match Regexp
    ...    ${file}
    ...    \\$\\{download\\}=\\s{4}Promise To Wait For Download\\n\\s+Click\\s+\\S.*\\n\\s+Wait For\\s{4}\\$\\{download\\}
    Recorded Keyword Replays    ${RESOURCE}    Download File    ${LOGIN_URL}

Idle Timeout Ends The Session
    ${text} =    Record Keywords    ${RESOURCE}    idle_timeout=1s
    Should Be Empty    ${text}

Closing All Pages Ends The Session
    ${promise} =    Promise To    Record Keyword    Until Closed    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Carol
    Wait Until Calls    1
    Close Page    ALL
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Until Closed
    New Page    ${FORM_URL}

Shadowing Name Is Rejected
    Run Keyword And Expect Error    *would be shadowed*    Record Keyword    click    ${RESOURCE}

Second Session In Same Context Records Nothing Twice
    FOR    ${name}    IN    First Run    Second Run
        ${promise} =    Promise To    Record Keyword    ${name}    ${RESOURCE}
        Toolbar State Should Be    recording
        Fill Text    id=input_name    ${name}
        Wait Until Calls    1
        Send Command    {cmd: 'stop'}
        Wait For    ${promise}
    END
    ${file} =    Get File    ${RESOURCE}
    Should Contain X Times    ${file}    Fill Text    2
    # Playwright 1.64 hides its own overlay only in mode none.
    ${mode} =    Evaluate JavaScript    ${None}    async () => (await window.__pw_recorderState()).mode
    Should Be Equal    ${mode}    none

Name Dialog Closes When A Name Is Accepted After A Rejected One
    Open The Toolbar Shadow Root For Inspection
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Click    rfb-recorder-toolbar >> #new
    Fill Text    rfb-recorder-toolbar >> #nameInput    click
    Keyboard Key    press    Enter
    Get Text    rfb-recorder-toolbar >> #modalErr    *=    shadowed
    Fill Text    rfb-recorder-toolbar >> #nameInput    Named After Rejection
    Keyboard Key    press    Enter
    Toolbar State Should Be    recording
    Wait For Elements State    rfb-recorder-toolbar >> #modal    hidden    timeout=2s
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Pick Locator Mode Shows A Notice And Records Nothing
    ${promise} =    Promise To    Record Keyword    Fill After Picking    ${RESOURCE}
    Toolbar State Should Be    recording
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording-inspecting')
    Wait For Function    () => window.__rfbToolbarState.picking === true
    Fill Text    id=input_name    while picking
    Evaluate JavaScript    ${None}    () => window.__pw_recorderSetMode('recording')
    Wait For Function    () => window.__rfbToolbarState.picking === false
    Fill Text    id=input_name    after picking
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    after picking
    Should Not Contain    ${file}    while picking

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

Argument Dialog Validates In Place And Accepts Variable Syntax
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Validated Argument    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Click Inside Toolbar    () => [...window.toolbarRoot.querySelectorAll('.cell.pick')].pop()
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('argName')
    Keyboard Input    type    \${who
    Toolbar Element Should Be Shown    argErr
    Keyboard Key    press    Enter
    Toolbar Element Should Be Shown    argModal
    Keyboard Input    type    }
    Toolbar Element Should Be Hidden    argErr
    Keyboard Key    press    Enter
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    Toolbar Element Should Be Hidden    argModal
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]${SPACE*4}\${who}=Alice

Argument Dialog Keeps A Rejected Name And Closes On The Glass Pane
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Glass Pane    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Click Inside Toolbar    () => [...window.toolbarRoot.querySelectorAll('.cell.pick')].pop()
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('argName')
    Keyboard Input    type    SPACE
    Keyboard Key    press    Enter
    Wait For Function    () => window.toolbarRoot.getElementById('argErr').textContent.includes('built-in')
    Toolbar Element Should Be Shown    argModal
    Mouse Button    click    3    300
    Toolbar Element Should Be Hidden    argModal
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Not Contain    ${file}    [Arguments]

Name Dialog Shows That Recording Starts And Idle Shows No Call List
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar State Should Be    idle
    Toolbar Element Should Be Hidden    calls
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('new')
    Keyboard Input    type    Shows Starting
    Keyboard Key    press    Enter
    Toolbar Element Should Be Shown    starting
    Toolbar State Should Be    recording
    Toolbar Element Should Be Hidden    modal
    Toolbar Element Should Be Shown    calls
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

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

Recording Fails In A Headless Browser
    Allow Recording Headless    ${False}
    New Browser    ${BROWSER}    headless=True
    New Page    ${FORM_URL}
    TRY
        Run Keyword And Expect Error    *Recording needs a visible browser*
        ...    Record Keywords    ${RESOURCE}
    FINALLY
        Allow Recording Headless    ${True}
        Close Browser    CURRENT
    END
    File Should Not Exist    ${RESOURCE}

*** Keywords ***
Allow Recording Headless
    [Arguments]    ${allow}
    ${lib} =    Get Library Instance    Browser
    Evaluate    setattr($lib, "recorder_allows_headless", $allow)

Open Form And Name Resource
    New Page    ${FORM_URL}
    # The toolbar starts at the top left; keep it off the elements the tests use.
    Evaluate JavaScript    ${None}
    ...    () => window.sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 12}))
    ${slug} =    Evaluate    "${TEST_NAME}".lower().replace(" ", "_")
    Set Test Variable    ${RESOURCE}    ${OUTPUT_DIR}${/}recorded_${slug}.resource
    Remove File    ${RESOURCE}

End Any Recording Session
    Run Keyword And Ignore Error    Send Command    {cmd: 'stop'}

Toolbar Is Ready
    Wait For Function    () => typeof window.__rfbCommand === 'function' && !!window.__rfbToolbarState

Send Command
    [Arguments]    ${command}
    Evaluate JavaScript    ${None}    () => window.__rfbCommand(${command})

Toolbar State Should Be
    [Arguments]    ${state}
    Wait For Function
    ...    () => window.__rfbToolbarState && window.__rfbToolbarState.state === '${state}' && !window.__rfbToolbarState.pending

Wait Until Calls
    [Arguments]    ${count}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.calls.length === ${count}

Finish Keyword
    Send Command    {cmd: 'finish'}
    Toolbar State Should Be    idle

Recorded Keyword Replays
    [Arguments]    ${resource}    ${name}    ${url}=${FORM_URL}
    Go To    ${url}
    Import Resource    ${resource}
    Run Keyword    ${name}

Open The Toolbar Shadow Root For Inspection
    Evaluate JavaScript    ${None}
    ...    () => {
    ...    const attach = Element.prototype.attachShadow;
    ...    Element.prototype.attachShadow = function (init) { return attach.call(this, { ...init, mode: 'open' }); };
    ...    }

Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript
    ...    ${None}
    ...    () => {
    ...    const attach = Element.prototype.attachShadow;
    ...    Element.prototype.attachShadow = function (init) { const root = attach.call(this, init); window.toolbarRoot = root; return root; };
    ...    }

Toolbar Element Should Be Shown
    [Arguments]    ${id}
    Wait For Function    () => !window.toolbarRoot.getElementById('${id}').hidden    timeout=2s

Toolbar Element Should Be Hidden
    [Arguments]    ${id}
    Wait For Function    () => window.toolbarRoot.getElementById('${id}').hidden    timeout=2s

Click Inside Toolbar
    [Arguments]    ${finder}
    ${box} =    Evaluate JavaScript    ${None}
    ...    () => { const r = (${finder})().getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }
    Mouse Button    click    ${box}[0]    ${box}[1]

Toolbar Should Touch The Bottom Right Corner
    Wait For Function
    ...    () => { const r = document.querySelector('rfb-recorder-toolbar').shadowRoot.getElementById('panel').getBoundingClientRect(); const d = document.documentElement; return Math.abs(r.right - d.clientWidth) < 1 && Math.abs(r.bottom - d.clientHeight) < 1; }
    ...    timeout=2s

Toolbar Header Point
    ${point} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('title').getBoundingClientRect(); return [r.x + 5, r.y + r.height / 2]; }
    RETURN    ${point}

Toolbar Left
    ${left} =    Evaluate JavaScript    ${None}
    ...    () => window.toolbarRoot.getElementById('panel').getBoundingClientRect().left
    RETURN    ${left}

Toolbar Should Touch The Right Edge
    Wait For Function
    ...    () => Math.abs(window.toolbarRoot.getElementById('panel').getBoundingClientRect().right - document.documentElement.clientWidth) < 1
    ...    timeout=2s

Click Toolbar Collapse Button
    Evaluate JavaScript    rfb-recorder-toolbar >> #collapse    (element) => element.click()
