*** Settings ***
Documentation     A JS extension changes what Record Keyword and Record Selector record
...               through its ``__recordedAction`` hook. The extension stays loaded in this
...               library instance, so these tests have a suite of their own.

Resource          recorder.resource

Suite Setup       Load The Hook Extension
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
A Hook Records A Select By Its Labels
    ${promise} =    Promise To    Record Keyword    Choose A Make    ${RESOURCE}
    Toolbar State Should Be    recording
    Select Options By    id=ManyOptions    value    13: 6792
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    ${SPACE*4}label${SPACE*4}AMELUNG\n
    Select Options By    id=ManyOptions    value    0: null
    Recorded Keyword Replays    ${RESOURCE}    Choose A Make
    Get Selected Options    id=ManyOptions    value    ==    13: 6792

A Hook Changes The Selector Of A Pick
    New Page    ${RECORDER_SELECTORS_URL}
    Evaluate JavaScript
    ...    ${None}
    ...    () => sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000}))
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
