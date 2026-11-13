*** Settings ***
Documentation     The recorder hook of a JS extension, with recorder_aria_label.js:
...               Playwright records an element whose role and aria-label are not unique,
...               such as the value help icon of a SAP Fiori input, by its id; the extension
...               records it by its role and aria-label, scoped by the named input beside it,
...               also when the value help dialog the click opens hides the form with aria-hidden.
...               A selector Playwright already made from a role and a name is kept.

Library           Browser    jsextension=${CURDIR}/recorder_aria_label.js
Resource          imports.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Page With Value Help Fields
Test Teardown     Run Keywords    End Any Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder    no-iframe

*** Test Cases ***
A Value Help That Playwright Records By Its Role And Name Is Kept
    Remove Fields Except    APD_::SalesOrderType
    ${selector} =    Record Click    id=APD_::SalesOrderType-inner-vhi
    Should Be Equal    ${selector}    role=button[name*="Wertehilfe einblenden"i]
    Get Attribute    ${selector}    id    ==    APD_::SalesOrderType-inner-vhi

A Recorded Value Help Is Scoped By The Input It Belongs To
    ${selector} =    Record Click    id=APD_::SalesOrganization-inner-vhi
    Should Be Equal
    ...    ${selector}
    ...    role=combobox[name="Verkaufsorganisation"s] >> xpath=.. >> role=button[name="Wertehilfe einblenden"s]
    Get Attribute    ${selector}    id    ==    APD_::SalesOrganization-inner-vhi

A Recorded Value Help Is Scoped By Its Input Although The Opened Dialog Hides The Form
    Evaluate JavaScript    id=form
    ...    (form) => form.addEventListener('click', () => form.setAttribute('aria-hidden', 'true'))
    ${selector} =    Record Click    id=APD_::SalesOrderType-inner-vhi
    Should Be Equal
    ...    ${selector}
    ...    role=combobox[name="Kundenauftragsart"s] >> xpath=.. >> role=button[name="Wertehilfe einblenden"s]
    Evaluate JavaScript    id=form    (form) => form.removeAttribute('aria-hidden')
    Get Attribute    ${selector}    id    ==    APD_::SalesOrderType-inner-vhi

A Recorded Value Help Of An Input Without A Name Is Recorded By Its Role, Aria Label And Index
    ${selector} =    Record Click    id=APD_::Note-inner-vhi
    Should Be Equal    ${selector}    role=button[name="Wertehilfe einblenden"s] >> nth=2
    Get Attribute    ${selector}    id    ==    APD_::Note-inner-vhi

*** Keywords ***
Open Page With Value Help Fields
    New Page    ${RECORDER_SELECTORS_URL}
    Evaluate JavaScript
    ...    ${None}
    ...    () => { sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000})); sessionStorage.setItem('rfb.toolbar.collapsed', 'true'); }
    VAR    ${icon} =    style="display:inline-block;width:1em;height:1em;border:1px solid"
    VAR    ${fields} =
    ...    <section id="form" role="form" aria-label="Kundenauftrag anlegen">
    ...    <div class="field" id="APD_::SalesOrderType"><label id="__label9" for="APD_::SalesOrderType-inner-inner" aria-label="Kundenauftragsart">Kundenauftragsart</label>
    ...    <div><input id="APD_::SalesOrderType-inner-inner" role="combobox" aria-labelledby="__label9">
    ...    <div><span id="APD_::SalesOrderType-inner-vhi" role="button" aria-label="Wertehilfe einblenden" ${icon}></span></div></div></div>
    ...    <div class="field" id="APD_::SalesOrganization"><label id="__label10" for="APD_::SalesOrganization-inner-inner" aria-label="Verkaufsorganisation">Verkaufsorganisation</label>
    ...    <div><input id="APD_::SalesOrganization-inner-inner" role="combobox" aria-labelledby="__label10">
    ...    <div><span id="APD_::SalesOrganization-inner-vhi" role="button" aria-label="Wertehilfe einblenden" ${icon}></span></div></div></div>
    ...    <div class="field" id="APD_::Note">
    ...    <div><input id="APD_::Note-inner-inner" role="combobox">
    ...    <div><span id="APD_::Note-inner-vhi" role="button" aria-label="Wertehilfe einblenden" ${icon}></span></div></div></div>
    ...    </section>
    ...    separator=${EMPTY}
    Evaluate JavaScript    ${None}    (f) => document.body.insertAdjacentHTML('afterbegin', f)    arg=${fields}

Remove Fields Except
    [Arguments]    ${field_id}
    Evaluate JavaScript    ${None}
    ...    (id) => document.querySelectorAll('.field').forEach((field) => field.id !== id && field.remove())
    ...    arg=${field_id}

Record Click
    [Arguments]    ${target}
    ${promise} =    Promise To    Record Keyword    Open Value Help    ${None}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.state === 'recording'
    Click    ${target}
    Wait For Function    () => window.__rfbToolbarState.calls.length === 1
    ${selector} =    Evaluate JavaScript    ${None}    () => window.__rfbToolbarState.calls[0].values[0].raw
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    RETURN    ${selector}

Allow Recording Headless
    [Arguments]    ${allow}
    ${lib} =    Get Library Instance    Browser
    Evaluate    setattr($lib, "recorder_allows_headless", $allow)

End Any Session
    Run Keyword And Ignore Error    Send Command    {cmd: 'stop'}

Send Command
    [Arguments]    ${command}
    Evaluate JavaScript    ${None}    () => window.__rfbCommand(${command})
