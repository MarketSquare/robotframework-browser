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
    Go To    ${LOGIN_URL}
    Click    id=delayed_request_big
    ${coverage_file} =    Stop Coverage
    File Should Not Be Empty    ${coverage_file}
    Close Page
