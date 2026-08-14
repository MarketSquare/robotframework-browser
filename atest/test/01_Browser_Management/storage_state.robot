*** Settings ***
Resource        imports.resource

Suite Setup     New Browser    headless=${HEADLESS}

*** Variables ***
${CUSTOM_STATE_DIR} =       ${OUTPUT_DIR}/custom_state
${SEED_INDEXED_DB} =        async () => { const req = indexedDB.open('rfdb', 1); req.onupgradeneeded = () => req.result.createObjectStore('kv'); const db = await new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); await new Promise((res, rej) => { const tx = db.transaction('kv', 'readwrite'); tx.objectStore('kv').put('token-abc', 'auth'); tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error); }); db.close(); }
${READ_INDEXED_DB} =        async () => { const req = indexedDB.open('rfdb', 1); req.onupgradeneeded = () => req.result.createObjectStore('kv'); const db = await new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); const value = await new Promise((res, rej) => { const tx = db.transaction('kv', 'readonly'); const get = tx.objectStore('kv').get('auth'); get.onsuccess = () => res(get.result); get.onerror = () => rej(get.error); }); db.close(); return value === undefined ? '' : value; }
${DELETE_INDEXED_DB} =      async () => { await new Promise((res, rej) => { const req = indexedDB.deleteDatabase('rfdb'); req.onsuccess = () => res(); req.onerror = () => rej(req.error); req.onblocked = () => rej(new Error('blocked')); }); }

*** Test Cases ***
Save Storage State
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    ${STATE_FILE} =    Save Storage State
    VAR    ${STATE_FILE} =    ${STATE_FILE}    scope=SUITE
    File Should Not Be Empty    ${STATE_FILE}

Restore Storage State
    New Context    storageState=${STATE_FILE}
    ${cookie} =    Get Cookie    Foo
    Should Be Equal    ${cookie.value}    Bar
    ${cookie} =    Get Cookie    Key
    Should Be Equal    ${cookie.value}    Value

Restore Storage State With Invalid Path
    Run Keyword And Expect Error
    ...    ValueError: storageState argument value '/not/here' is not file, but it should be.
    ...    New Context    storageState=/not/here

Restore Storage State With Invalid File
    Append To File    ${OUTPUT_DIR}/invalid_state_file.json    not valid json
    Run Keyword And Expect Error
    ...    SyntaxError*JSON*
    ...    New Context    storageState=${OUTPUT_DIR}/invalid_state_file.json

Save Storage State To Given Path
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    VAR    ${target} =    ${CUSTOM_STATE_DIR}/auth.json
    ${returned} =    Save Storage State    ${target}
    Should Be Equal    ${returned}    ${target}
    File Should Not Be Empty    ${target}

Save Storage State To Given Path Overwrites Existing File
    New Context
    New Page    ${LOGIN_URL}
    VAR    ${target} =    ${CUSTOM_STATE_DIR}/overwritten.json
    Create File    ${target}    not valid json
    Save Storage State    ${target}
    ${content} =    Get File    ${target}
    Should Not Be Equal    ${content}    not valid json
    Should Contain    ${content}    cookies

Set Storage State Restores Cookies And Local Storage
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    ${state} =    Save Storage State
    Delete All Cookies
    Evaluate JavaScript    ${None}    localStorage.clear();
    ${cookies} =    Get Cookies
    Should Be Empty    ${cookies}
    Set Storage State    ${state}
    Reload
    ${cookie} =    Get Cookie    Foo
    Should Be Equal    ${cookie.value}    Bar
    ${color} =    Evaluate JavaScript    ${None}    localStorage.getItem('bgcolor');
    Should Be Equal    ${color}    red

Set Storage State Keeps The Context And Its Pages Open
    New Context
    ${page} =    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    ${state} =    Save Storage State
    Set Storage State    ${state}
    ${current} =    Get Page Ids
    Should Contain    ${current}    ${page}[page_id]

Set Storage State With Invalid Path
    Run Keyword And Expect Error
    ...    ValueError: path argument value '/not/here' is not file, but it should be.
    ...    Set Storage State    /not/here

Save Storage State With IndexedDB Restores IndexedDB
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${SEED_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    New Context
    New Page    ${LOGIN_URL}
    ${value} =    Evaluate JavaScript    ${None}    ${READ_INDEXED_DB}
    Should Be Equal    ${value}    ${EMPTY}
    Set Storage State    ${state}
    Reload
    ${value} =    Evaluate JavaScript    ${None}    ${READ_INDEXED_DB}
    Should Be Equal    ${value}    token-abc

Save Storage State Without IndexedDB Omits IndexedDB
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${SEED_INDEXED_DB}
    ${state} =    Save Storage State
    New Context
    New Page    ${LOGIN_URL}
    Set Storage State    ${state}
    Reload
    ${value} =    Evaluate JavaScript    ${None}    ${READ_INDEXED_DB}
    Should Be Equal    ${value}    ${EMPTY}

Set Storage State Restores IndexedDB Into The Same Context
    [Documentation]    Disabled until https://github.com/microsoft/playwright/issues/42258 is fixed.
    ...    Save Storage State with indexedDB=True leaves an open IndexedDB connection in the
    ...    page, which blocks the restore, so Set Storage State never finishes here. Enable
    ...    this test, and remove the timeout from Set Storage State Times Out On IndexedDB
    ...    Held By An Open Page, once Playwright closes that connection.
    [Tags]    playwright-42258
    Skip    Blocked by https://github.com/microsoft/playwright/issues/42258
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${SEED_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    Evaluate JavaScript    ${None}    ${DELETE_INDEXED_DB}
    Set Storage State    ${state}
    Reload
    ${value} =    Evaluate JavaScript    ${None}    ${READ_INDEXED_DB}
    Should Be Equal    ${value}    token-abc

Set Storage State Times Out On IndexedDB Held By An Open Page
    [Documentation]    Guards the timeout that works around
    ...    https://github.com/microsoft/playwright/issues/42258
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${SEED_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    Run Keyword And Expect Error
    ...    *Set Storage State timed out after 3000 ms*
    ...    Set Storage State    ${state}    timeout=3s

Save Storage State With Credentials Restores WebAuthn Credentials
    New Context
    New Page    ${LOGIN_URL}
    Create Credential    rpId=localhost
    ${credential} =    Get Credential    rpId=localhost
    ${state} =    Save Storage State    credentials=True
    Delete Credential    ${credential}[id]
    Set Storage State    ${state}
    ${restored} =    Get Credential    rpId=localhost
    Should Be Equal    ${restored}[id]    ${credential}[id]

Save Storage State Without Credentials Omits WebAuthn Credentials
    New Context
    New Page    ${LOGIN_URL}
    Create Credential    rpId=localhost
    Get Credential    rpId=localhost
    ${state} =    Save Storage State
    Set Storage State    ${state}
    Run Keyword And Expect Error
    ...    TypeError: Cannot read properties of undefined (reading 'id')
    ...    Get Credential    rpId=localhost

*** Keywords ***
Add Cookies For Storage
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    Add Cookie    Key    Value    url=${url}
    Evaluate JavaScript    ${None}    localStorage.setItem('bgcolor', 'red');
