*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${EMPTY}

*** Test Cases ***
Coverage
    Start Coverage
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_file} =    Stop Coverage
    File Should Not Be Empty    ${coverage_file}
    Close Page

Coverage With Options
    Start Coverage
    Add Locator Handler Click    id=overlay    id=OverlayCloseButton
    Go To    ${OWERLAY_URL}
    Click    id=CreateOverlayButton
    Click    id=CreateOverlayButton
    Click    id=textHeading
    ${coverage_file} =    Stop Coverage    config_file=${CURDIR}/coverageConfig.js    folder_prefix=SimplePage
    File Should Not Be Empty    ${coverage_file}
    ${coverage_file2} =    Convert To String    ${coverage_file}
    Should Contain    ${coverage_file2}    SimplePage
    Close Page
    New Page    ${coverage_file.as_uri()}
    Get Text    .mcr-title    equal    Browser library Coverage Report
