*** Settings ***
Resource          imports.resource

Suite Setup       Open Suite Context With Init Script
Suite Teardown    Close Browser

*** Test Cases ***
Init Script Runs Before The Page's Own Scripts
    New Context
    Add Init Script    window.seed = 42
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    42

Init Script Is Called With Its Argument
    New Context
    Add Init Script    (value) => { window.seed = value }    arg=${{ {"n": 1, "flags": ["a"]} }}
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    {"n":1,"flags":["a"]}

Init Script Is Read From A File
    New Context
    Add Init Script    path=${CURDIR}/init_seed.js
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    "from file"

Several Init Scripts All Run
    New Context
    Add Init Script    window.seed = 1
    Add Init Script    window.other = 2
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    1
    Get Text    id=other-value    ==    2

Context Init Script Runs In Popups
    New Context
    Add Init Script    window.seed = 42
    New Page    ${INIT_SCRIPT_URL}
    Click    id=popup
    Switch Page    NEW
    Get Text    id=seed-value    ==    42

Page Init Script Runs After Reload But Not In Popups
    New Context
    New Page    ${INIT_SCRIPT_URL}
    Add Init Script    window.seed = 42    on=Page
    Get Text    id=seed-value    ==    unset
    Reload
    Get Text    id=seed-value    ==    42
    Click    id=popup
    Switch Page    NEW
    Get Text    id=seed-value    ==    unset

Context Init Script Lives As Long As Its Context
    Switch Context    ${SUITE_CONTEXT}
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=other-value    ==    "suite"

Init Script Does Not Run In Another Context
    New Context
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=other-value    ==    unset

Broken Init Script Does Not Fail The Keyword
    New Context
    Add Init Script    throw new Error('broken init script')
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    unset
    Get Page Errors    validate    any(e['message'] == 'broken init script' for e in value)

Page Init Script Fails Without A Page
    New Context
    Run Keyword And Expect Error    *no page was open*
    ...    Add Init Script    window.seed = 42    on=Page

Init Script With Argument Must Be A Single Expression
    New Context
    Run Keyword And Expect Error    *must be a single function expression*
    ...    Add Init Script    window.seed = 1; window.other = 2;    arg=${1}

Init Script Needs Exactly One Of Script And Path
    New Context
    Run Keyword And Expect Error    *exactly one of script and path*
    ...    Add Init Script
    Run Keyword And Expect Error    *exactly one of script and path*
    ...    Add Init Script    window.seed = 1    path=${CURDIR}/init_seed.js

*** Keywords ***
Open Suite Context With Init Script
    New Browser    headless=${HEADLESS}
    ${context} =    New Context
    Add Init Script    window.other = 'suite'
    VAR    ${SUITE_CONTEXT} =    ${context}    scope=SUITE
