*** Settings ***
Documentation     The recorder hooks of a JS extension, with recorder_title_description.js:
...               a click on an element whose title equals its text and is unique on the
...               page is recorded as role=<role>[description="<title>"s] instead of by
...               its name. Any other click, and a picked selector, are kept as Playwright
...               made them.

Library           Browser    jsextension=${CURDIR}/recorder_title_description.js
Resource          imports.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Recorder Page In New Context
Test Teardown     Run Keywords    End Any Session    AND    Close Context    ALL    AND    Wait For All Promises

Test Tags         recorder    no-iframe

*** Test Cases ***
A Button Whose Unique Title Is Its Text Is Recorded By Its Description
    Add Elements    <button aria-label="Close dialog" title="Close">Close</button>
    ${selector} =    Record Click    css=[aria-label="Close dialog"]
    Should Be Equal    ${selector}    role=button[description="Close"s]
    Get Attribute    ${selector}    aria-label    ==    Close dialog

A Link Whose Unique Title Is Its Text Is Recorded By Its Description
    Add Elements    <a href="#help" aria-label="Open help" title="Help">Help</a>
    ${selector} =    Record Click    css=[aria-label="Open help"]
    Should Be Equal    ${selector}    role=link[description="Help"s]
    Get Attribute    ${selector}    aria-label    ==    Open help

A Button Sharing Its Name With Another Is Recorded By Its Description
    Add Elements
    ...    <button class="titled" aria-label="Remove" title="Remove first">Remove first</button>
    ...    <button class="titled" aria-label="Remove" title="Remove second">Remove second</button>
    ${selector} =    Record Click    css=.titled >> nth=1
    Should Be Equal    ${selector}    role=button[description="Remove second"s]
    Get Text    ${selector}    ==    Remove second

A Button Whose Title Differs From Its Text Keeps Its Name
    Add Elements    <button aria-label="Open menu" title="Menu">=</button>
    ${selector} =    Record Click    css=[aria-label="Open menu"]
    Should Be Equal    ${selector}    role=button[name*="Open menu"i]

A Button Whose Title Is Used Twice Keeps Its Name
    Add Elements
    ...    <button aria-label="Keep draft" title="Save">Save</button>
    ...    <button aria-label="Keep copy" title="Save">Save</button>
    ${selector} =    Record Click    css=[aria-label="Keep draft"]
    Should Be Equal    ${selector}    role=button[name*="Keep draft"i]

A Button Whose Title Is Used Again In A Shadow Root Keeps Its Name
    Add Elements    <button aria-label="Close dialog" title="Close">Close</button><div id="title-host"></div>
    Evaluate JavaScript    id=title-host
    ...    (host) => { host.attachShadow({mode: 'open'}).innerHTML = '<button aria-label="Close panel" title="Close">Close</button>'; }
    ${selector} =    Record Click    css=[aria-label="Close dialog"]
    Should Be Equal    ${selector}    role=button[name*="Close dialog"i]

A Button That Already Has A Description Keeps Its Name
    Add Elements
    ...    <span id="hint">Deletes the file</span>
    ...    <button aria-label="Delete file" title="Delete" aria-describedby="hint">Delete</button>
    ${selector} =    Record Click    css=[aria-label="Delete file"]
    Should Be Equal    ${selector}    role=button[name*="Delete file"i]

Every Click Of A Recording Is Rewritten On Its Own
    Add Elements
    ...    <button aria-label="Close dialog" title="Close">Close</button>
    ...    <button aria-label="Open menu" title="Menu">=</button>
    ...    <button aria-label="Open help" title="Help">Help</button>
    ${promise} =    Promise To    Record Keyword    Click Titled    ${None}
    Toolbar State Should Be    recording
    Click    css=[aria-label="Close dialog"]
    Wait Until Calls    1
    Click    css=[aria-label="Open menu"]
    Wait Until Calls    2
    Click    css=[aria-label="Open help"]
    Wait Until Calls    3
    ${selectors} =    Recorded Selectors
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    Should Be Equal
    ...    ${selectors}
    ...    ${{['role=button[description="Close"s]', 'role=button[name*="Open menu"i]', 'role=button[description="Help"s]']}}

Record Selector Starts The Extension And Keeps The Picked Selector
    Add Elements    <button aria-label="Close dialog" title="Close">Close</button>
    ${promise} =    Promise To    Record Selector
    Wait For Function
    ...    () => window.__rfbToolbarState && window.__rfbToolbarState.phase === 'picking' && document.body.getAttribute('data-pw-cursor') === 'pointer'
    ${binding} =    Evaluate JavaScript    ${None}    () => typeof window.__titledPress
    Should Be Equal    ${binding}    function
    Click    css=[aria-label="Close dialog"]
    Wait For Function    () => window.__rfbToolbarState.phase === 'picked'
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Not Contain    ${selector}    description
    Get Attribute    ${selector}    aria-label    ==    Close dialog

*** Keywords ***
Open Recorder Page In New Context
    New Context
    New Page    ${RECORDER_SELECTORS_URL}
    Evaluate JavaScript
    ...    ${None}
    ...    () => { sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000})); sessionStorage.setItem('rfb.toolbar.collapsed', 'true'); }

Add Elements
    [Arguments]    @{html}
    VAR    ${elements} =    @{html}    separator=${EMPTY}
    Evaluate JavaScript    ${None}    (e) => document.body.insertAdjacentHTML('afterbegin', e)    arg=${elements}

Record Click
    [Arguments]    ${target}
    ${promise} =    Promise To    Record Keyword    Click Titled    ${None}
    Toolbar State Should Be    recording
    Click    ${target}
    Wait Until Calls    1
    ${selectors} =    Recorded Selectors
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    RETURN    ${selectors}[0]

Recorded Selectors
    ${selectors} =    Evaluate JavaScript    ${None}
    ...    () => window.__rfbToolbarState.calls.map((call) => call.values[0].raw)
    RETURN    ${selectors}

Allow Recording Headless
    [Arguments]    ${allow}
    ${lib} =    Get Library Instance    Browser
    Evaluate    setattr($lib, "recorder_allows_headless", $allow)

End Any Session
    Run Keyword And Ignore Error    Send Command    {cmd: 'stop'}

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
