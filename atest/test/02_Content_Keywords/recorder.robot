*** Settings ***
Resource          recorder.resource

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

A Second Session In The Same Context Is Refused And Leaves The First Running
    ${promise} =    Promise To    Record Keyword    First Session    ${RESOURCE}
    Toolbar State Should Be    recording
    Run Keyword And Expect Error
    ...    *already running in this browser context*
    ...    Record Keyword
    ...    Second Session
    ...    ${None}
    Fill Text    id=input_name    still recorded
    Wait Until Calls    1
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    still recorded

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

Save Ends A Record Keyword Session
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Save Ends It    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    saved
    Wait Until Calls    1
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('finish')
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    saved
    Recorded Keyword Replays    ${RESOURCE}    Save Ends It

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

Actions While Paused Are Not Recorded
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Keyword    Fill Around A Pause    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    before
    Wait Until Calls    1
    Toolbar Element Should Be Hidden    resume
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('pause')
    Wait For Function    () => window.__rfbToolbarState.paused === true && !window.__rfbToolbarState.pending
    Toolbar Element Should Be Hidden    pause
    Toolbar Element Should Be Shown    resume
    Fill Text    input[name="email"]    while paused
    Sleep    1s
    Click Inside Toolbar    () => window.toolbarRoot.getElementById('resume')
    Wait For Function    () => window.__rfbToolbarState.paused === false && !window.__rfbToolbarState.pending
    Fill Text    input[name="website"]    after
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    before
    Should Contain    ${file}    after
    Should Not Contain    ${file}    while paused

Recording Into A Missing Folder Fails Before It Starts
    Run Keyword And Expect Error    *does not exist*
    ...    Record Keyword    Never Recorded    ${OUTPUT_DIR}${/}no${/}such${/}folder${/}k.resource

Closing The Context Ends The Session And Keeps The Keyword
    ${promise} =    Promise To    Record Keyword    Fill Before Closing    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Wait Until Calls    1
    Close Context
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Fill Text
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Fill Before Closing
