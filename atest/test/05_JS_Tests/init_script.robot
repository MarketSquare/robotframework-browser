*** Settings ***
Resource          imports.resource

Suite Setup       Open Shared Context With A Suite Init Script
Suite Teardown    Close Browser

*** Test Cases ***
Init Script Runs Before The Page Scripts
    Add Init Script    window.seed = 'early'
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    early

Init Script Function Gets The Arg
    Add Init Script    (value) => { window.seed = value }    arg=${42}
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    42

Init Script From A File
    Add Init Script    path=${CURDIR}/init_seed.js    arg=from file
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    from file

Init Script Reaches Popups
    Add Init Script    window.seed = 'popup'
    New Page    ${CREATE_POPUPS_URL}
    Click    id=first_popup
    Switch Page    NEW
    ${seed} =    Evaluate JavaScript    ${None}    () => window.seed
    Should Be Equal    ${seed}    popup

Several Init Scripts All Run
    Add Init Script    window.seed = 'one'
    Add Init Script    window.other = 'two'
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=seed-value    ==    one
    Get Text    id=other-value    ==    two

Broken Init Script Does Not Fail The Keyword
    Add Init Script    window.seed = ;
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=flag-value    ==    on
    Get Page Errors    validate    any(error["name"] == "SyntaxError" for error in value)

Arg Needs One Function Expression
    Run Keyword And Expect Error    *one expression*
    ...    Add Init Script    window.a = 1; window.b = 2;    arg=${1}

Script Or Path Is Needed
    Run Keyword And Expect Error    *Give either script or path*
    ...    Add Init Script
    Run Keyword And Expect Error    *Give either script or path*
    ...    Add Init Script    window.seed = 1    path=${CURDIR}/init_seed.js

Suite Init Script Reaches Every Test
    New Page    ${INIT_SCRIPT_URL}
    Get Text    id=flag-value    ==    on

*** Keywords ***
Open Shared Context With A Suite Init Script
    New Browser    headless=${HEADLESS}
    New Context
    Run Keyword And Expect Error    *scope=Suite*
    ...    Add Init Script    window.seed = 'suite setup'
    Add Init Script    window.suiteFlag = 'on'    scope=Suite
