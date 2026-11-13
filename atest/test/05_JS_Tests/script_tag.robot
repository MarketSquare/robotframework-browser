*** Settings ***
Resource          imports.resource

Suite Setup       New Browser    headless=${HEADLESS}
Suite Teardown    Close Browser
Test Setup        New Page    ${INIT_SCRIPT_URL}

*** Test Cases ***
Script Tag Content Runs In The Page
    Add Script Tag    window.flag = 42;
    ${flag} =    Evaluate JavaScript    ${None}    () => window.flag
    Should Be Equal    ${flag}    ${42}

Script Tag Top-Level Declarations Become Page Globals
    Add Script Tag    const declared = 'global'; function declaredFunction() { return declared; }
    ${value} =    Evaluate JavaScript    ${None}    () => declaredFunction()
    Should Be Equal    ${value}    global

Script Tag Is Loaded From A URL
    Add Script Tag    url=${STATIC_URL}script_tag.js
    ${value} =    Evaluate JavaScript    ${None}    () => window.scriptTagLoaded
    Should Be Equal    ${value}    from url

Script Tag Loads An ES Module From A URL
    Add Script Tag    url=${STATIC_URL}script_tag_module.js    type=module
    ${value} =    Evaluate JavaScript    ${None}    () => window.scriptTagModule
    Should Be True    ${value}

Script Tag Content Runs As An ES Module
    Add Script Tag    window.isModule = typeof import.meta === 'object';    type=module
    ${value} =    Evaluate JavaScript    ${None}    () => window.isModule
    Should Be True    ${value}

Script Tag Is Read From A File
    Add Script Tag    path=${CURDIR}/script_tag_helper.js
    ${value} =    Evaluate JavaScript    ${None}    () => scriptTagHelper
    Should Be Equal    ${value}    from file

Script Tag Is Added To The Frame Of The Frame Selector
    Go To    ${FRAMES_URL}
    Add Script Tag    window.flag = 'left';    frame_selector=id=left >>> body
    ${in_frame} =    Evaluate JavaScript    id=left >>> body    () => window.flag
    Should Be Equal    ${in_frame}    left
    ${in_page} =    Evaluate JavaScript    ${None}    () => window.flag ?? null
    Should Be Equal    ${in_page}    ${None}

Script Tag Is Added To A Nested Frame
    Go To    ${DEEP_FRAMES_URL}
    Add Script Tag    window.flag = 'nested';    frame_selector=id=b >>> id=c >>> body
    ${in_nested} =    Evaluate JavaScript    id=b >>> id=c >>> body    () => window.flag
    Should Be Equal    ${in_nested}    nested

Empty Frame Selector Adds The Script Tag To The Page
    Add Script Tag    window.flag = 42;    frame_selector=${EMPTY}
    ${flag} =    Evaluate JavaScript    ${None}    () => window.flag
    Should Be Equal    ${flag}    ${42}

Script Tag Is Gone After Reload
    Add Script Tag    window.flag = 42;
    Reload
    ${flag} =    Evaluate JavaScript    ${None}    () => window.flag ?? null
    Should Be Equal    ${flag}    ${None}

Script Tag That Fails To Load Fails The Keyword
    Run Keyword And Expect Error    *script_tag_missing.js*
    ...    Add Script Tag    url=${STATIC_URL}script_tag_missing.js

Script Tag That Throws Does Not Fail The Keyword
    Add Script Tag    path=${CURDIR}/script_tag_broken.js
    Get Page Errors    validate
    ...    any(e['message'] == 'broken script tag' and 'script_tag_broken.js' in e['stack'] for e in value)

Script Tag Needs Exactly One Of Content, URL And Path
    Run Keyword And Expect Error    *exactly one of content, url and path*
    ...    Add Script Tag
    Run Keyword And Expect Error    *exactly one of content, url and path*
    ...    Add Script Tag    window.flag = 1;    url=${STATIC_URL}script_tag.js

Script Tag Content Must Not Be Empty
    Run Keyword And Expect Error    *content is empty*
    ...    Add Script Tag    ${EMPTY}

Script Tag Fails Without A Page
    Close Page    ALL
    Run Keyword And Expect Error    *no page was open*
    ...    Add Script Tag    window.flag = 42;
