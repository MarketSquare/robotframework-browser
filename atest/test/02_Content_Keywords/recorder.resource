*** Settings ***
Documentation    Scripted recording sessions. The toolbar's closed shadow root cannot be
...              clicked from a test, so commands go through `window.__rfbCommand`, the
...              same channel the toolbar uses, and the page is driven by Browser keywords.

Resource         imports.resource
Library          OperatingSystem

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

Click Picks On
    [Arguments]    ${page}    ${back}
    Switch Page    ${page}
    Click    id=input_name
    Switch Page    ${back}
    Wait For Function    () => (window.__rfbToolbarState.picker || {}).phase === 'picked'    timeout=1s

Open Second Window
    ${before} =    Get Page Ids
    Evaluate JavaScript    ${None}    () => { window.second = window.open(location.href, '_blank'); }
    Wait Until Keyword Succeeds    5s    0.2s    Page Count Should Be    ${{len($before) + 1}}
    ${after} =    Get Page Ids
    RETURN    ${{(set($after) - set($before)).pop()}}

Page Count Should Be
    [Arguments]    ${count}
    ${ids} =    Get Page Ids
    Length Should Be    ${ids}    ${count}

Add Popup Link
    Evaluate JavaScript
    ...    ${None}
    ...    () => { const a = document.createElement('a'); a.id = 'popup_link'; a.href = location.href; a.target = '_blank'; a.textContent = 'Open popup'; document.body.prepend(a); }

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

Picker Should Be Picking
    Wait For Function
    ...    () => window.__rfbToolbarState.picker && window.__rfbToolbarState.picker.phase === 'picking'
    Playwright Should Be Picking

Playwright Should Be Picking
    [Documentation]    The toolbar shows the pick at once; Playwright takes it up with the
    ...    next poll. Its pick tool turns the pointer into a hand once it listens.
    Wait For Function    () => document.body.getAttribute('data-pw-cursor') === 'pointer'

Wait Until Calls
    [Arguments]    ${count}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.calls.length === ${count}

Finish Keyword
    Send Command    {cmd: 'finish'}
    Toolbar State Should Be    idle

Toolbar Calls Should Be
    [Arguments]    @{keywords}
    ${calls} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.calls.map((call) => call.keyword)
    Should Be Equal    ${calls}    ${keywords}

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

Record An Upload
    [Documentation]    Records choosing this file through the file chooser that clicking ``${opener}`` opens.
    [Arguments]    ${opener}    ${name}
    New Page    ${RECORDER_UPLOAD_URL}
    ${promise} =    Promise To    Record Keyword    ${name}    ${RESOURCE}
    Toolbar State Should Be    recording
    ${upload} =    Promise To Upload File    ${CURDIR}${/}recorder.robot
    Click    ${opener}
    Wait For    ${upload}
    Wait For Function
    ...    () => window.__rfbToolbarState.notice && window.__rfbToolbarState.notice.includes('<define_path_to_file>')
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}

Upload Replays
    [Arguments]    ${recorded}    ${name}
    # Forward slashes: a backslash in the resource would be a Robot escape on Windows.
    VAR    ${folder}    ${CURDIR}
    ${replayable} =    Evaluate
    ...    $recorded.replace('<define_path_to_file>', pathlib.Path($folder).as_posix())
    ...    modules=pathlib
    Create File    ${RESOURCE}    ${replayable}
    Recorded Keyword Replays    ${RESOURCE}    ${name}    ${RECORDER_UPLOAD_URL}
    Get Text    id=upload_result    ==    recorder.robot

Mark Clicked Elements
    [Documentation]    Numbers every clicked element in click order, across the page and its frames.
    [Arguments]    ${selector}
    Evaluate JavaScript
    ...    ${selector}
    ...    (element) => {
    ...    const top = window.top; top.__clickCount = top.__clickCount || 0;
    ...    document.addEventListener('click', (event) => { const target = event.composedPath()[0]; if (target.nodeType === 1) target.__clicked = top.__clickCount++; }, true);
    ...    }

Toolbar Element Point
    [Arguments]    ${id}
    ${point} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('${id}').getBoundingClientRect(); return [r.x + 5, r.y + r.height / 2]; }
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
