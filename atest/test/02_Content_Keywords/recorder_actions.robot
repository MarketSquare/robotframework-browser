*** Settings ***
Resource          recorder.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
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

Switching And Closing Pages Is Recorded
    Add Popup Link
    ${promise} =    Promise To    Record Keyword    Work On Two Pages    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=popup_link
    Wait Until Calls    2
    ${first} =    Switch Page    NEW
    Fill Text    id=input_name    on popup
    Wait Until Calls    3
    ${popup} =    Switch Page    ${first}
    Fill Text    id=input_name    on first
    Wait Until Calls    5
    Close Page    ${popup}
    Wait Until Calls    6
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    \${page}=${SPACE*4}Switch Page${SPACE*4}NEW
    Should Contain    ${file}    \${page_2}=${SPACE*4}Switch Page${SPACE*4}\${page}
    Should Contain    ${file}    Close Page${SPACE*4}\${page_2}
    Go To    ${FORM_URL}
    Add Popup Link
    Import Resource    ${RESOURCE}
    Work On Two Pages
    Get Page Ids    ALL    ==    ${{[$first]}}
    Get Property    id=input_name    value    ==    on first

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

A File Chooser Upload Becomes An Upload Promise Around The Click
    Record An Upload    id=open    Upload Through The Button
    ${file} =    Get File    ${RESOURCE}
    Should Contain
    ...    ${file}
    ...    \${upload}=${SPACE*4}Promise To Upload File${SPACE*4}<define_path_to_file>/recorder.robot\n${SPACE*4}Click${SPACE*4}
    Should Contain    ${file}    Wait For${SPACE*4}\${upload}
    Upload Replays    ${file}    Upload Through The Button

An Upload Into A File Input Becomes Upload File By Selector
    Record An Upload    id=plain-file    Upload Into The Input
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Upload File By Selector
    Should Contain    ${file}    <define_path_to_file>/recorder.robot\n
    Should Not Contain    ${file}    Promise To Upload File
    Upload Replays    ${file}    Upload Into The Input

A Click Two Frames Deep Is Recorded With A Leading Frame Separator
    [Documentation]    Playwright shortens a frame path of two or more frames to
    ...    `internal:control=any-frame`, which Browser writes as a leading `>>>`.
    New Page    ${RECORDER_SELECTORS_URL}
    Evaluate JavaScript
    ...    ${None}
    ...    () => { sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000})); sessionStorage.setItem('rfb.toolbar.collapsed', 'true'); }
    Mark Clicked Elements    id=frame >>> id=inner >>> body
    ${promise} =    Promise To    Record Keyword    Click Deep    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=frame >>> id=inner >>> text=Two frames deep
    Wait Until Calls    1
    ${selector} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.calls[0].values[0].raw
    Should Start With    ${selector}    >>>${SPACE}
    ${notice} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.notice
    Should Be Equal    ${notice}    ${None}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${clicked} =    Evaluate JavaScript    ${selector}    (element) => element.__clicked
    Should Be Equal As Integers    ${clicked}    0
    Recorded Keyword Replays    ${RESOURCE}    Click Deep    ${RECORDER_SELECTORS_URL}
