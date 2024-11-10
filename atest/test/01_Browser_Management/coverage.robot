*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${EMPTY}

*** Test Cases ***
Coverage
    Start Coverage
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_dir} =    Stop Coverage
    ${files} =    OperatingSystem.List Files In Directory    ${coverage_dir}
    Should Not Be Empty    ${files}
    Close Page

Coverage With Options
    Start Coverage
    Go To    ${LOGIN_URL}
    Click    id=delayed_request
    ${coverage_dir} =    Stop Coverage    ${CURDIR}/coverageConfig.js
    ${files} =    OperatingSystem.List Files In Directory    ${coverage_dir}
    Should Not Be Empty    ${files}
    Close Page
