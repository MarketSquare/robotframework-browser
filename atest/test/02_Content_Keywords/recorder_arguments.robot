*** Settings ***
Resource          recorder.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
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

A Selector Becomes An Argument
    ${promise} =    Promise To    Record Keyword    Fill Field    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Evaluate JavaScript
    ...    ${None}
    ...    () => { const raw = window.__rfbToolbarState.calls[0].values[0].raw; window.__rfbCommand({cmd: 'argument', call: 0, value: 0, start: 0, end: raw.length, name: 'field', raw}); }
    Wait For Function    () => window.__rfbToolbarState.arguments.length === 1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Fill Text${SPACE*4}\${field}${SPACE*4}Alice
    Import Resource    ${RESOURCE}
    Fill Field    input[name="email"]
    Get Property    input[name="email"]    value    ==    Alice

The Replace Offer Marks The Part It Would Replace
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Offer Marks    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    jane
    Fill Text    css=input[name=email]    jane@example.com
    Wait Until Calls    2
    Send Command    {cmd: 'argument', call: 0, value: 1, start: 0, end: 4, name: 'name', raw: 'jane'}
    Wait For Function
    ...    () => [...window.toolbarRoot.querySelectorAll('#offerList mark')].map((m) => m.textContent).join('|') === 'jane'
    ...    timeout=2s
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

The Argument Dialog Shows The Marked Part Without Focus And Survives A Release Outside
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Marked Part    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Click Inside Toolbar    () => [...window.toolbarRoot.querySelectorAll('.cell.pick')].pop()
    Evaluate JavaScript    ${None}    () => window.toolbarRoot.getElementById('argValue').setSelectionRange(1, 3)
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('argName')
    Wait For Function
    ...    () => window.toolbarRoot.activeElement.id === 'argName' && window.toolbarRoot.querySelector('#argMarks mark').textContent === 'li'
    ...    timeout=2s
    ${box} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('argValue').getBoundingClientRect(); return [r.x + 10, r.y + 10]; }
    Mouse Move    ${box}[0]    ${box}[1]
    Mouse Button    down
    Mouse Move    3    300
    Mouse Button    up
    Toolbar Element Should Be Shown    argModal
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
