*** Settings ***
Documentation     Scripted Record Selector sessions. The toolbar's closed shadow root cannot be
...               clicked from a test, so commands go through `window.__rfbCommand`, the
...               same channel the toolbar uses, and the page is picked with Browser keywords.

Resource          imports.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open The Selector Page
Test Teardown     End The Picker

Test Tags         recorder

*** Test Cases ***
A Picked Element Gets Playwright's Selector
    ${promise} =    Promise To    Record Selector    Submit button
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Start With    ${selector}    role=button[name
    Get Text    ${selector}    ==    Pressed

The Css Generator Writes A Css Selector
    ${promise} =    Promise To    Record Selector    generator=css
    Picker Should Be Picking
    Click    css=[data-testid="main-content"]
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Not Start With    ${selector}    role=
    Get Element Count    ${selector}    ==    1
    Get Attribute    ${selector}    data-testid    ==    main-content

The Toolbar Switches The Generator For The Same Element
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    ${playwright} =    Picker Selector
    Send Command    {cmd: 'generator', name: 'css'}
    Wait For Function    () => window.__rfbToolbarState.generator === 'css'
    ${css} =    Picker Selector
    Should Not Be Equal    ${css}    ${playwright}
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Be Equal    ${selector}    ${css}
    Get Text    ${selector}    ==    Pressed

An Edited Selector Is Counted And Used
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Wait For Function    () => (window.__rfbToolbarState.count || {}).count === 1
    Send Command    {cmd: 'edit', selector: 'css=button'}
    Wait For Function
    ...    () => { const c = window.__rfbToolbarState.count || {}; return c.selector === 'css=button' && c.count > 1; }
    Send Command    {cmd: 'edit', selector: 'css=h2'}
    Wait For Function
    ...    () => { const c = window.__rfbToolbarState.count || {}; return c.selector === 'css=h2' && c.count === 1; }
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Should Be Equal    ${selector}    css=h2

An Element In A Frame Gets A Frame Piercing Selector From Both Generators
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    id=frame >>> text=In frame
    Picker Should Have Picked
    ${playwright} =    Picker Selector
    Should Contain    ${playwright}    ${SPACE}>>>${SPACE}
    Get Text    ${playwright}    ==    In frame
    Send Command    {cmd: 'generator', name: 'css'}
    Wait For Function    () => window.__rfbToolbarState.generator === 'css'
    Send Command    {cmd: 'use'}
    ${css} =    Wait For    ${promise}
    Should Contain    ${css}    ${SPACE}>>>${SPACE}
    Get Text    ${css}    ==    In frame

An Element In A Shadow Root Gets A Piercing Css Selector
    ${promise} =    Promise To    Record Selector    generator=css
    Picker Should Be Picking
    Click    text=In shadow
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    ${css} =    Wait For    ${promise}
    Should Contain    ${css}    ${SPACE}>>${SPACE}
    Get Text    ${css}    ==    In shadow

The Highlight Can Be Switched Off And On
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Wait For Function    () => window.__rfbToolbarState.highlight === true
    Send Command    {cmd: 'highlight', on: false}
    Wait For Function    () => window.__rfbToolbarState.highlight === false
    Send Command    {cmd: 'highlight', on: true}
    Wait For Function    () => window.__rfbToolbarState.highlight === true && !!window.__rfbToolbarState.count
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Get Text    ${selector}    ==    Pressed

A Minimized Toolbar Offers Reselect And Use
    Evaluate JavaScript    ${None}    () => sessionStorage.setItem('rfb.toolbar.collapsed', 'true')
    Keep The Closed Toolbar Root Reachable
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Click In Toolbar    headReselect
    Picker Should Be Picking
    Click    css=h2
    Picker Should Have Picked
    Click In Toolbar    headUse
    ${selector} =    Wait For    ${promise}
    Get Text    ${selector}    ==    Heading Level Two

Reselect Picks Another Element
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Send Command    {cmd: 'reselect'}
    Picker Should Be Picking
    Click    css=h2
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Get Text    ${selector}    ==    Heading Level Two

A Pick Does Not Reach The Page
    # The page's own handlers listen as most do, bubbling. A capture listener registered
    # before Playwright's pick tool would see the click before Playwright consumes it.
    Evaluate JavaScript
    ...    ${None}
    ...    () => { window.__pageClicks = 0; document.addEventListener('click', () => window.__pageClicks++); }
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Click    text=Pressed
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    Wait For    ${promise}
    ${clicks} =    Evaluate JavaScript    ${None}    () => window.__pageClicks
    Should Be Equal As Integers    ${clicks}    0
    The Page Has Its Own Pointer Again

Cancel Fails The Keyword
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Send Command    {cmd: 'stop'}
    Run Keyword And Expect Error    *Record Selector was cancelled.    Wait For    ${promise}
    The Page Has Its Own Pointer Again
    Wait For Function    () => !window.__rfbToolbarState

Record Keyword Is Refused While Record Selector Runs And Leaves It Running
    ${promise} =    Promise To    Record Selector
    Picker Should Be Picking
    Run Keyword And Expect Error    *already running in this browser context*    Record Keyword    Not Now    ${None}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.mode === 'selector'
    Click    text=Pressed
    Picker Should Have Picked
    Send Command    {cmd: 'use'}
    ${selector} =    Wait For    ${promise}
    Get Text    ${selector}    ==    Pressed

The Idle Timeout Fails The Keyword
    Run Keyword And Expect Error    *timed out*    Record Selector    idle_timeout=1s

Record Selector Fails In A Headless Browser
    [Setup]    Run Keywords    Open The Selector Page    AND    Allow Recording Headless    ${False}
    TRY
        Run Keyword And Expect Error    *needs a visible browser*    Record Selector
    FINALLY
        Allow Recording Headless    ${True}
    END

Record Selector Is Refused While A Recording Session Runs
    ${recording} =    Promise To    Record Keyword    Not Now    ${None}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.state === 'recording'
    Run Keyword And Expect Error
    ...    *Record Keyword(s) session or another Record Selector is running*
    ...    Record Selector
    Send Command    {cmd: 'stop'}
    Wait For    ${recording}

*** Keywords ***
Open The Selector Page
    New Page    ${RECORDER_SELECTORS_URL}
    # The toolbar starts at the top left, over the elements the tests pick.
    Evaluate JavaScript
    ...    ${None}
    ...    () => sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000}))

End The Picker
    Run Keyword And Ignore Error    Send Command    {cmd: 'stop'}
    Run Keyword And Ignore Error    Wait For All Promises
    Close Page    ALL

Allow Recording Headless
    [Arguments]    ${allow}
    ${lib} =    Get Library Instance    Browser
    Evaluate    setattr($lib, "recorder_allows_headless", $allow)

Send Command
    [Arguments]    ${command}
    Evaluate JavaScript    ${None}    () => window.__rfbCommand(${command})

Picker Should Be Picking
    Wait For Function
    ...    () => window.__rfbToolbarState && window.__rfbToolbarState.mode === 'selector' && window.__rfbToolbarState.phase === 'picking'
    Playwright Should Be Picking

Playwright Should Be Picking
    [Documentation]    The toolbar shows the pick at once; Playwright takes it up with the
    ...    next poll. Its pick tool turns the pointer into a hand once it listens.
    Wait For Function    () => document.body.getAttribute('data-pw-cursor') === 'pointer'

Picker Should Have Picked
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.phase === 'picked'

Picker Selector
    ${selector} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.selector
    RETURN    ${selector}

Keep The Closed Toolbar Root Reachable
    Evaluate JavaScript
    ...    ${None}
    ...    () => {
    ...    const attach = Element.prototype.attachShadow;
    ...    Element.prototype.attachShadow = function (init) { const root = attach.call(this, init); if (this.localName === 'rfb-recorder-toolbar') window.toolbarRoot = root; return root; };
    ...    }

Click In Toolbar
    [Arguments]    ${id}
    Wait For Function    () => !window.toolbarRoot.getElementById('${id}').hidden
    ${box} =    Evaluate JavaScript
    ...    ${None}
    ...    () => { const r = window.toolbarRoot.getElementById('${id}').getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }
    Mouse Button    click    ${box}[0]    ${box}[1]

The Page Has Its Own Pointer Again
    [Documentation]    Playwright's pick turns the pointer into a hand on every frame's body.
    Wait For Function    () => !document.body.hasAttribute('data-pw-cursor')    timeout=2s
    Wait For Function    () => !document.querySelector('#frame').contentDocument.body.hasAttribute('data-pw-cursor')
    ...    timeout=2s
