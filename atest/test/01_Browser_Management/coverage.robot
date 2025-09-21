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
    Should Be Equal As Integers    ${process.rc}    1

Run Rfbrowser To Combine Coverage Reports And Invalid Config File
    Create Directory    ${OUTPUT_DIR}/no_raw_files
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} coverage ${OUTPUT_DIR}/no_raw_files ${OUTPUT_DIR}/combined_coverage_reports_6 --config ${CURDIR}/not_here.js
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    2

No Config File
    Start Coverage
    ...    coverage_type=js
    ...    config_file=not_here.js
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_file} =    Stop Coverage
    Should Be Equal
    ...    ${coverage_file}
    ...    ${{ pathlib.Path($OUTPUT_DIR) / "browser" / "coverage" / $PAGE_ID / "index.html" }}
    File Should Not Be Empty    ${coverage_file}

Merge Coverage Reports With Keyword
    Start Coverage    raw=True
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    ${coverage_folder} =    Stop Coverage
    New Page    ${LOGIN_URL}
    Start Coverage    raw=True
    Click    id=delayed_request
    ${coverage_folder} =    Stop Coverage
    ${combined_folder} =    Merge Coverage Reports
    ...    ${OUTPUT_DIR}/browser/coverage
    ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_0
    Directory Should Not Be Empty    ${combined_folder}
    ${uri} =    File As Uri    ${combined_folder}/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Browser library Merged Coverage Report
    Close Page
    ${combined_folder} =    Merge Coverage Reports
    ...    ${OUTPUT_DIR}/browser/coverage
    ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_1
    ...    name=Custom Merged Name
    Directory Should Not Be Empty    ${combined_folder}
    ${uri} =    File As Uri    ${combined_folder}/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Custom Merged Name
    Close Page
    ${combined_folder} =    Merge Coverage Reports
    ...    ${OUTPUT_DIR}/browser/coverage
    ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_11
    ...    name=Custom Merged Name
    ...    reports=["markdown-summary", "markdown-details"]
    ${files} =    List Files In Directory    ${combined_folder}
    Length Should Be    ${files}    2
    ${data} =    Get File    ${combined_folder}/${files}[1]
    FOR    ${word}    IN    \# Custom Merged Name    Name    Coverage %    Covered    Uncovered    Total
        Should Contain    ${data}    ${word}
    END
    ${data} =    Get File    ${combined_folder}/${files}[0]
    FOR    ${word}    IN    \## Custom Merged Name    Name    Bytes    Statements    Branches    Functions    Lines    Uncovered Lines    overlay.html    Summary
        Should Contain    ${data}    ${word}
    END

Merge Coverage Reports No Raw Reports
    Create Directory    ${OUTPUT_DIR}/no_raw_files_keyword
    TRY
        Merge Coverage Reports
        ...    ${OUTPUT_DIR}/no_raw_files_keyword
        ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_2
    EXCEPT    FileNotFoundError: No raw reports found from *    type=GLOB    AS    ${error}
        Log    Caught expected error ${error}
    END

Merge Coverage Reports No Config File
    Create Directory    ${OUTPUT_DIR}/no_raw_files_keyword
    TRY
        Merge Coverage Reports
        ...    ${OUTPUT_DIR}/browser/coverage
        ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_3
        ...    config=${CURDIR}/not_here.js
    EXCEPT    FileNotFoundError: Configuration file *not_here.js does not exist    type=GLOB    AS    ${error}
        Log    Caught expected error ${error}
    END

Merge Coverage Reports Output Dir Does Exist
    [Documentation]    ...
    ...    LOG 2:3    WARN    Output folder ${OUTPUT_DIR}${/}merge_coverage_reports_keyword_4 already exists, deleting it first
    Create Directory    ${OUTPUT_DIR}/merge_coverage_reports_keyword_4
    Merge Coverage Reports
    ...    ${OUTPUT_DIR}/browser/coverage
    ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_4

Merge Coverage Reports Config File
    ${combined_folder} =    Merge Coverage Reports
    ...    ${OUTPUT_DIR}/browser/coverage
    ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_5
    ...    config_file=${CURDIR}/coverageConfigMD.js
    Directory Should Not Be Empty    ${combined_folder}
    ${uri} =    File As Uri    ${combined_folder}/index.html
    New Page    ${uri}
    Get Text    .mcr-title    equal    Browser library Coverage Report MD
    Close Page

Merge Coverage Reports Invalid Config File
    TRY
        ${combined_folder} =    Merge Coverage Reports
        ...    ${OUTPUT_DIR}/browser/coverage
        ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_6
        ...    config_file=${CURDIR}/coverageConfigInvalid.js
    EXCEPT    SyntaxError: Unexpected token '}'    type=GLOB    AS    ${error}
        Log    Caught expected error ${error}
    END
    TRY
        ${combined_folder} =    Merge Coverage Reports
        ...    ${OUTPUT_DIR}/browser/coverage
        ...    ${OUTPUT_DIR}/merge_coverage_reports_keyword_7
        ...    config_file=${CURDIR}/coverageConfigInvalid.txt
    EXCEPT    SyntaxError: Unexpected identifier 'is'    type=GLOB    AS    ${error}
        Log    Caught expected error ${error}
    END

*** Keywords ***
Open Page And Store ID
    &{page_info} =    New Page
    Set Suite Variable    ${PAGE_ID}    ${page_info.page_id}
