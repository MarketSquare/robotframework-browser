*** Settings ***
Resource        imports.resource

Test Setup      Open Page And Store ID

*** Variables ***
${PAGE_ID} =    ${EMPTY}

*** Test Cases ***
Coverage
    Start Coverage
    ...    coverage_type=js
    ...    reportAnonymousScripts=True
    ...    resetOnNavigation=True
    ...    config_file=${CURDIR}/coverageConfig.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_file} =    Stop Coverage
    Should Be Equal
    ...    ${coverage_file}
    ...    ${{ pathlib.Path($OUTPUT_DIR) / "browser" / "coverage" / $PAGE_ID / "index.html" }}
    File Should Not Be Empty    ${coverage_file}

Coverage AutoClosing
    Start Coverage
    ...    coverage_type=js
    ...    reportAnonymousScripts=True
    ...    resetOnNavigation=True
    ...    config_file=${CURDIR}/coverageConfig.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request

Check Coverage AutoClosing
    [Setup]    NONE
    File Should Not Be Empty    ${{ pathlib.Path($OUTPUT_DIR) / "browser" / "coverage" / $PAGE_ID / "index.html" }}

Coverage With Options
    ${type} =    Start Coverage    config_file=${CURDIR}/coverageConfig.js    path=SimplePage
    Should Be Equal    ${type}    CoverageType.all
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Go To    ${OWERLAY_URL}
    Click    id=CreateOverlayButton
    Click    id=textHeading
    ${coverage_file} =    Stop Coverage
    File Should Not Be Empty    ${coverage_file}
    Should Be Equal
    ...    ${coverage_file}
    ...    ${{ pathlib.Path($OUTPUT_DIR) / "browser" / "coverage" / "SimplePage" / $PAGE_ID / "index.html" }}
    Close Page
    New Page    ${coverage_file.as_uri()}
    Get Text    .mcr-title    equal    Browser library Coverage Report

Coverage With MarkDown
    Start Coverage    config_file=${CURDIR}/coverageConfigMD.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    Close Context
    ${text} =    Get File
    ...    ${{ pathlib.Path($OUTPUT_DIR) / "browser" / "coverage" / $PAGE_ID / "coverage-summary.md" }}
    Should Contain    ${text}    Browser library Coverage Report MD
    Close Page

Coverage With Raw
    Start Coverage    raw=True
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    ${coverage_file} =    Stop Coverage
    ${coverage_folder} =    Get Parent    ${coverage_file}
    ${files} =    List Files In Directory    ${coverage_folder}/raw
    Should Not Be Empty    ${files}

Coverage With MarkDown And Raw
    Start Coverage    config_file=${CURDIR}/coverageConfigMD.js    raw=True
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    ${coverage_folder} =    Stop Coverage
    ${text} =    Get File    ${coverage_folder}/coverage-summary.md
    Should Contain    ${text}    Browser library Coverage Report MD
    ${files} =    List Files In Directory    ${coverage_folder}/raw
    Should Not Be Empty    ${files}
    Close Page

Run Rfbrowser To Combine Coverage Reports
    ${rel_path} =    Relative To    ${OUTPUT_DIR}    ${EXECDIR}
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${rel_path}/browser/coverage ${rel_path}/combined_coverage_reports_1 --name "New name"
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Contain    ${process.stdout}    page=
    # Test Coverage With Options use argument folder=SimplePage and it must be in srdout at found folders.
    Should Contain    ${process.stdout}    SimplePage${/}page=
    Should Be Equal As Integers    ${process.rc}    0
    Directory Should Not Be Empty    ${OUTPUT_DIR}/combined_coverage_reports_1
    Directory Should Not Be Empty    ${OUTPUT_DIR}/browser/coverage
    ${uri} =    File As Uri    ${OUTPUT_DIR}/combined_coverage_reports_1/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    New name
    Close Page

Run Rfbrowser To Combine Coverage Reports With Different Reports
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/browser/coverage ${OUTPUT_DIR}/combined_coverage_reports_2 --reports html
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Directory Should Not Be Empty    ${OUTPUT_DIR}/combined_coverage_reports_2
    Directory Should Not Be Empty    ${OUTPUT_DIR}/browser/coverage
    ${uri} =    File As Uri    ${OUTPUT_DIR}/combined_coverage_reports_2/index.html
    New Page    ${uri}
    Get Text    h1    equal    All files
    Close Page

Run Rfbrowser To Combine Coverage Reports With Config
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/browser/coverage ${OUTPUT_DIR}/combined_coverage_reports_3 --config ${CURDIR}/coverageConfigCombine.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Directory Should Not Be Empty    ${OUTPUT_DIR}/combined_coverage_reports_3
    Directory Should Not Be Empty    ${OUTPUT_DIR}/browser/coverage
    ${uri} =    File As Uri    ${OUTPUT_DIR}/combined_coverage_reports_3/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Browser library Combined Coverage Report

Run Rfbrowser To Combine Coverage Reports And No Input Dir
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/does_not_exist ${OUTPUT_DIR}/combined_coverage_reports_4 --config ${CURDIR}/coverageConfig.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

Run Rfbrowser To Combine Coverage Reports And No Raw Files
    Create Directory    ${OUTPUT_DIR}/no_raw_files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/no_raw_files ${OUTPUT_DIR}/combined_coverage_reports_5
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

Run Rfbrowser To Combine Coverage Reports And Invalid Config File
    Create Directory    ${OUTPUT_DIR}/no_raw_files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/no_raw_files ${OUTPUT_DIR}/combined_coverage_reports_6 --config ${CURDIR}/not_here.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

*** Keywords ***
Open Page And Store ID
    &{page_info} =    New Page
    Set Suite Variable    ${PAGE_ID}    ${page_info.page_id}
