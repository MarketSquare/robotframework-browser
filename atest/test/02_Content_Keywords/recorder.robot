*** Settings ***
Documentation    Scripted recording sessions. The toolbar's closed shadow root cannot be
...              clicked from a test, so commands go through `window.__rfbCommand`, the
...              same channel the toolbar uses, and the page is driven by Browser keywords.

Resource         imports.resource
Library          OperatingSystem

Test Setup       Open Form And Name Resource
Test Teardown    Run Keywords    End Any Recording Session    AND    Wait For All Promises    AND    Close Page    ALL

Test Tags        recorder

*** Test Cases ***
Session Records Two Keywords And Skips Idle Actions
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Fill Text    id=input_name    ignored while idle
    Send Command    {cmd: 'new', name: 'Fill Name'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Finish Keyword
    Send Command    {cmd: 'new', name: 'Check Sms'}
    Toolbar State Should Be    recording
    Check Checkbox    [data-testid="testid-sms"]
    Finish Keyword
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Fill Name
    Should Contain    ${text}    Check Sms
    ${file} =    Get File    ${RESOURCE}
    Should Not Contain    ${file}    ignored while idle
    Should Contain    ${file}    [Tags]    recorded
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
    ${promise} =    Promise To    Record Keyword    Click Then Finish    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    [data-testid="testid-sms"]
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    testid-sms

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
    Should Contain    ${file}    [Arguments]    \${number}=42
    Should Contain    ${file}    id-\${number}
    Import Resource    ${RESOURCE}
    Fill Parametrised    number=7
    Get Property    id=input_name    value    ==    id-7

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
    Should Contain    ${file}    Switch Page    NEW
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

*** Keywords ***
Open Form And Name Resource
    New Page    ${FORM_URL}
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
    [Arguments]    ${resource}    ${name}
    Go To    ${FORM_URL}
    Import Resource    ${resource}
    Run Keyword    ${name}

Open The Toolbar Shadow Root For Inspection
    Evaluate JavaScript    ${None}
    ...    () => {
    ...    const attach = Element.prototype.attachShadow;
    ...    Element.prototype.attachShadow = function (init) { return attach.call(this, { ...init, mode: 'open' }); };
    ...    }
