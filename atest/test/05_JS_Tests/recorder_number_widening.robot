*** Settings ***
Documentation     The recorder hook of a JS extension, with recorder_number_widening.js:
...               Playwright drops the number at the start of "46 km/h bis 60 km/h"; the
...               extension gives it back, in a recorded click and in a picked selector.

Library           Browser    jsextension=${CURDIR}/recorder_number_widening.js
Resource          imports.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Page With Speed Radios
Test Teardown     Run Keywords    End Any Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder    no-iframe

*** Test Cases ***
A Recorded Click Keeps The Leading Number
    ${promise} =    Promise To    Record Keyword    Choose Speed    ${None}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.state === 'recording'
    Click    id=fast
    Wait For Function    () => window.__rfbToolbarState.calls.length === 1
    ${selector} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.calls[0].values[0].raw
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    Should Contain    ${selector}    46 km/h bis 60 km/h
    Get Attribute    ${selector}    id    ==    fast

A Picked Selector Keeps The Leading Number
    ${promise} =    Promise To    Record Selector
    Wait For Function
    ...    () => window.__rfbToolbarState && window.__rfbToolbarState.phase === 'picking' && document.body.getAttribute('data-pw-cursor') === 'pointer'
    Click    id=fast
    Wait For Function    () => window.__rfbToolbarState.phase === 'picked'
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Contain    ${selector}    46 km/h bis 60 km/h
    Get Attribute    ${selector}    id    ==    fast

*** Keywords ***
Open Page With Speed Radios
    New Page    ${RECORDER_SELECTORS_URL}
    Evaluate JavaScript
    ...    ${None}
    ...    () => { sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000})); sessionStorage.setItem('rfb.toolbar.collapsed', 'true'); }
    VAR    ${radios} =
    ...    <label><input type="radio" name="speed">0 km/h bis 30 km/h</label>
    ...    <label><input type="radio" name="speed">31 km/h bis 45 km/h</label>
    ...    <label><input type="radio" name="speed" id="fast">46 km/h bis 60 km/h</label>
    ...    separator=${EMPTY}
    Evaluate JavaScript    ${None}    (r) => document.body.insertAdjacentHTML('afterbegin', r)    arg=${radios}

Allow Recording Headless
    [Arguments]    ${allow}
    ${lib} =    Get Library Instance    Browser
    Evaluate    setattr($lib, "recorder_allows_headless", $allow)

End Any Session
    Run Keyword And Ignore Error    Send Command    {cmd: 'stop'}

Send Command
    [Arguments]    ${command}
    Evaluate JavaScript    ${None}    () => window.__rfbCommand(${command})
