*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${EMPTY}

*** Test Cases ***
Coverage
    Start Coverage
    ...    js
    ...    reportAnonymousScripts=True
    ...    resetOnNavigation=True
    ...    config_file=${CURDIR}/coverageConfig.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_file} =    Stop Coverage
    VAR    ${FILE}    ${coverage_file}    scope=suite
    File Should Not Be Empty    ${coverage_file}
    Close Page

Coverage With Options
    ${type} =    Start Coverage    config_file=${CURDIR}/coverageConfig.js    folder_prefix=SimplePage
    Should Be Equal    ${type}    CoverageType.all
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Go To    ${OWERLAY_URL}
    Click    id=CreateOverlayButton
    Click    id=textHeading
    ${coverage_file} =    Stop Coverage
    File Should Not Be Empty    ${coverage_file}
    ${coverage_file2} =    Convert To String    ${coverage_file}
    Should Contain    ${coverage_file2}    SimplePage
    Close Page
    New Page    ${coverage_file.as_uri()}
    Get Text    .mcr-title    equal    Browser library Coverage Report

Coverage With MarkDown
    Start Coverage    config_file=${CURDIR}/coverageConfigMD.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    ${coverage_folder} =    Stop Coverage
    ${text} =    Get File    ${coverage_folder}/coverage-summary.md
    Should Contain    ${text}    Browser library Coverage Report MD
    Close Page

Run Rfbrowser To Combine Coverage Reports
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/coverage_reports ${OUTPUT_DIR}/combined_coverage_reports_1
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Directory Should Not Be Empty    ${OUTPUT_DIR}/combined_coverage_reports_1
    Directory Should Not Be Empty    ${OUTPUT_DIR}/coverage_reports
    ${uri} =    File As Uri    ${OUTPUT_DIR}/combined_coverage_reports_1/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Coverage Report
    Close Page

Run Rfbrowser To Combine Coverage Reports With Config
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/coverage_reports ${OUTPUT_DIR}/combined_coverage_reports_2 --config ${CURDIR}/coverageConfigCombine.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Directory Should Not Be Empty    ${OUTPUT_DIR}/combined_coverage_reports_2
    Directory Should Not Be Empty    ${OUTPUT_DIR}/coverage_reports
    ${uri} =    File As Uri    ${OUTPUT_DIR}/combined_coverage_reports_2/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Browser library Combined Coverage Report

Run Rfbrowser To Combine Coverage Reports And No Input Dir
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/does_not_exist ${OUTPUT_DIR}/combined_coverage_reports_3 --config ${CURDIR}/coverageConfig.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

Run Rfbrowser To Combine Coverage Reports And No Raw Files
    Create Directory    ${OUTPUT_DIR}/no_raw_files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/no_raw_files ${OUTPUT_DIR}/combined_coverage_reports_4
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

Run Rfbrowser To Combine Coverage Reports And Invalid Config File
    Create Directory    ${OUTPUT_DIR}/no_raw_files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/no_raw_files ${OUTPUT_DIR}/combined_coverage_reports_4 --config ${CURDIR}/not_here.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2
