*** Settings ***
Resource        imports.resource

Suite Setup     New Browser    headless=${HEADLESS}

*** Variables ***
${CUSTOM_STATE_DIR} =       ${OUTPUT_DIR}/custom_state
${OTHER_ORIGIN_URL} =       http://127.0.0.1:${SERVER_PORT}/dist/
${SEED_INDEXED_DB} =        async () => { const req = indexedDB.open('rfdb', 1); req.onupgradeneeded = () => req.result.createObjectStore('kv'); const db = await new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); await new Promise((res, rej) => { const tx = db.transaction('kv', 'readwrite'); tx.objectStore('kv').put('token-abc', 'auth'); tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error); }); db.close(); }
${READ_INDEXED_DB} =        async () => { const req = indexedDB.open('rfdb', 1); req.onupgradeneeded = () => req.result.createObjectStore('kv'); const db = await new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); const value = await new Promise((res, rej) => { const tx = db.transaction('kv', 'readonly'); const get = tx.objectStore('kv').get('auth'); get.onsuccess = () => res(get.result); get.onerror = () => rej(get.error); }); db.close(); return value === undefined ? '' : value; }
${HOLD_INDEXED_DB} =        async () => { const req = indexedDB.open('rfdb', 1); req.onupgradeneeded = () => req.result.createObjectStore('kv'); const db = await new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); await new Promise((res, rej) => { const tx = db.transaction('kv', 'readwrite'); tx.objectStore('kv').put('token-abc', 'auth'); tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error); }); window.__db = db; }
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
    ...    ValueError: storageState argument value '?not?here' is not file, but it should be.
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
    ${expected} =    Normalize Path    ${target}
    Should Be Equal    ${returned}    ${expected}
    File Should Not Be Empty    ${target}

Storage State Keywords Accept A Relative Path
    [Documentation]    The node wrapper runs in its own working directory, so relative paths
    ...    must be resolved before they are sent over grpc. The relative path points into the
    ...    output directory, because the working directory is not writable everywhere, for
    ...    example in the docker image where it is the root directory.
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    VAR    ${target} =    ${OUTPUT_DIR}/relative_auth.json
    VAR    ${relative} =    ${{ os.path.relpath(r"${target}") }}
    Should Not Be Equal    ${relative}    ${target}    The path under test must be relative
    ${returned} =    Save Storage State    ${relative}
    ${expected} =    Normalize Path    ${target}
    Should Be Equal    ${returned}    ${expected}
    File Should Not Be Empty    ${target}
    Delete All Cookies
    Set Storage State    ${relative}
    ${cookie} =    Get Cookie    Foo
    Should Be Equal    ${cookie.value}    Bar
    New Context    storageState=${relative}
    ${cookie} =    Get Cookie    Key
    Should Be Equal    ${cookie.value}    Value

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
    ...    ValueError: path argument value '?not?here' is not file, but it should be.
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
    ...
    ...    SKIP Blocked by https://github.com/microsoft/playwright/issues/42258
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

Set Storage State Times Out On A Service Worker Holding IndexedDB
    [Documentation]    A service worker outlives the pages, so no value of reload_pages frees
    ...    the connection. This is the case which can only end in the timeout, see
    ...    https://github.com/microsoft/playwright/issues/42258
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    New Context
    New Page    ${LOGIN_URL}
    Register IndexedDB Holding Service Worker
    Run Keyword And Expect Error
    ...    *timed out after 3000 ms*service worker*still running*
    ...    Set Storage State    ${state}    timeout=3s    reload_pages=all

Set Storage State Reloads The Affected Pages
    [Documentation]    The page holds an open IndexedDB connection, which blocks the restore
    ...    until the keyword navigates the page away and back again.
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    New Context
    ${page} =    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${DELETE_INDEXED_DB}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    Set Storage State    ${state}
    ${ids} =    Get Page Ids
    Should Contain    ${ids}    ${page}[page_id]
    ${url} =    Get Url
    Should Be Equal    ${url}    ${LOGIN_URL}
    ${value} =    Evaluate JavaScript    ${None}    ${READ_INDEXED_DB}
    Should Be Equal    ${value}    token-abc

Set Storage State Fails Fast With Reload Pages None
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    ${start} =    Get Time    epoch
    Run Keyword And Expect Error
    ...    *holds an open connection to the IndexedDB database(s) rfdb*reload_pages=affected*
    ...    Set Storage State    ${state}    reload_pages=none
    ${end} =    Get Time    epoch
    Should Be True    ${end} - ${start} < 5    Fail fast should not wait for the timeout

Set Storage State Leaves Pages Of Other Origins Alone
    [Documentation]    Only the origins which carry IndexedDB in the state file can block the
    ...    restore, so pages of any other origin must not be touched.
    New Context
    New Page    ${LOGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    ${state} =    Save Storage State    indexedDB=True
    New Context
    New Page    ${LOGIN_URL}
    ${other} =    New Page    ${OTHER_ORIGIN_URL}
    Evaluate JavaScript    ${None}    ${HOLD_INDEXED_DB}
    Set Storage State    ${state}
    Switch Page    ${other}[page_id]
    ${url} =    Get Url
    Should Be Equal    ${url}    ${OTHER_ORIGIN_URL}
    ${still_held} =    Evaluate JavaScript    ${None}    () => !!window.__db
    Should Be True    ${still_held}    The page of the other origin was reloaded

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
Register IndexedDB Holding Service Worker
    Evaluate JavaScript
    ...    ${None}
    ...    async () => { const reg = await navigator.serviceWorker.register('/idb-holder-sw.js'); await navigator.serviceWorker.ready; return reg.scope; }
    Sleep    1s    reason=let the worker open its connection

Add Cookies For Storage
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    Add Cookie    Key    Value    url=${url}
    Evaluate JavaScript    ${None}    localStorage.setItem('bgcolor', 'red');
